"""Load and validate the small YAML ontology without a graph database."""
from __future__ import annotations

import copy
from dataclasses import dataclass
from datetime import date, datetime
import math
from pathlib import Path
import re

import yaml

BASE = Path(__file__).resolve().parents[1]


class StrictLoader(yaml.SafeLoader):
    pass


# Keep dates as strings so validation and JSON output have one representation.
StrictLoader.yaml_implicit_resolvers = copy.deepcopy(yaml.SafeLoader.yaml_implicit_resolvers)
for key, entries in StrictLoader.yaml_implicit_resolvers.items():
    StrictLoader.yaml_implicit_resolvers[key] = [
        entry for entry in entries if entry[0] != "tag:yaml.org,2002:timestamp"
    ]


def _mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"Duplicate YAML mapping key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def read_yaml(path: Path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=StrictLoader)


@dataclass
class Bundle:
    schema: dict
    entities: list[dict]
    as_of: str
    origins: dict[str, str]


def load_bundle(base: Path = BASE) -> Bundle:
    manifest = read_yaml(base / "ontology/manifest.yaml")
    schema = read_yaml(base / manifest["schema_file"])
    entities, origins = [], {}
    as_of = None
    for relative in manifest["data_files"]:
        document = read_yaml(base / relative)
        for entity in document["entities"]:
            entities.append(entity)
            origins[entity["id"]] = document["dataset_kind"]
        if document.get("as_of"):
            as_of = document["as_of"]
    if as_of is None:
        raise ValueError("The example graph must declare an as_of date")
    return Bundle(schema, entities, as_of, origins)


def index_entities(entities: list[dict]) -> dict[str, dict]:
    return {entity["id"]: entity for entity in entities}


def active_on(entity: dict, as_of: str) -> bool:
    return entity.get("valid_from", "0001-01-01") <= as_of < (entity.get("valid_to") or "9999-12-31")


def verified(entity: dict) -> bool:
    return entity.get("assertion_status") == "verified"


def _overlap(a: dict, b: dict) -> bool:
    return max(a["valid_from"], b["valid_from"]) < min(
        a.get("valid_to") or "9999-12-31", b.get("valid_to") or "9999-12-31"
    )


def _contains(outer: dict, inner: dict) -> bool:
    return outer["valid_from"] <= inner["valid_from"] and (
        outer.get("valid_to") or "9999-12-31"
    ) >= (inner.get("valid_to") or "9999-12-31")


def validate(bundle: Bundle) -> list[str]:
    errors, index = [], {}
    classes = bundle.schema["classes"]
    common = bundle.schema["common_fields"]
    rank = {"public": 0, "internal": 1, "restricted_hr": 2}

    def fail(entity, message):
        errors.append(f"{entity.get('id', '<missing-id>')}: {message}")

    for entity in bundle.entities:
        identity = entity.get("id")
        if not isinstance(identity, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", identity):
            fail(entity, "id must be stable snake_case")
        if identity in index:
            fail(entity, "duplicate id")
        else:
            index[identity] = entity

    for entity in bundle.entities:
        kind = entity.get("type")
        if kind not in classes:
            fail(entity, f"unknown type {kind}")
            continue
        fields = {**common, **classes[kind]["fields"]}
        for unknown in set(entity) - set(fields):
            fail(entity, f"unknown field {unknown}")
        for key, spec in fields.items():
            if key not in entity:
                if spec.get("required"):
                    fail(entity, f"missing required field {key}")
                continue
            value = entity[key]
            if value is None and spec.get("nullable"):
                continue
            field_kind = spec["kind"]
            valid = True
            if field_kind in {"string", "ref"}:
                valid = isinstance(value, str) and bool(value.strip())
            elif field_kind in {"refs", "strings"}:
                valid = isinstance(value, list) and all(isinstance(x, str) and x for x in value)
                if valid and (len(value) < spec.get("min_items", 0) or len(value) != len(set(value))):
                    fail(entity, f"{key} has insufficient or duplicate values")
            elif field_kind == "enum":
                valid = value in spec["values"]
            elif field_kind == "boolean":
                valid = isinstance(value, bool)
            elif field_kind == "mapping":
                valid = isinstance(value, dict)
            elif field_kind == "value":
                valid = isinstance(value, (str, int, float, bool, list, dict))
            elif field_kind in {"date", "datetime"}:
                try:
                    if not isinstance(value, str):
                        raise ValueError("not a string")
                    if field_kind == "date":
                        date.fromisoformat(value)
                        valid = len(value) == 10
                    else:
                        valid = datetime.fromisoformat(value).utcoffset() is not None
                except (ValueError, TypeError):
                    valid = False
            else:
                valid = False
            if not valid:
                fail(entity, f"{key} must be {field_kind}")
                continue
            if field_kind in {"ref", "refs"}:
                references = [value] if field_kind == "ref" else value
                for reference in references:
                    target = index.get(reference)
                    if not target:
                        fail(entity, f"{key} unresolved reference {reference}")
                    elif "*" not in spec["target"] and target.get("type") not in spec["target"]:
                        fail(entity, f"{key} reference {reference} has wrong type")
                    elif rank.get(entity.get("access_scope"), -1) < rank.get(target.get("access_scope"), -1):
                        fail(entity, f"{key} references a more restricted object; raise access_scope")

    # Shape failures are returned before semantic rules dereference malformed records.
    if errors:
        return sorted(set(errors))

    def by_type(kind):
        return [e for e in bundle.entities if e["type"] == kind]

    def authority(source_ref, domain, allowed_kinds=None):
        source = index[source_ref]
        return domain in source["authority_domains"] and (
            allowed_kinds is None or source["source_kind"] in allowed_kinds
        )

    def evidence_authorized(entity, kinds, domain=None, source_kinds=None):
        evidence = [index[ref] for ref in entity.get("evidence_refs", [])]
        return bool(evidence) and any(
            e["evidence_kind"] in kinds and (
                domain is None or authority(e["source_ref"], domain, source_kinds)
            ) for e in evidence
        )

    for entity in bundle.entities:
        kind = entity["type"]
        if "valid_from" in entity and entity.get("valid_to") and entity["valid_to"] <= entity["valid_from"]:
            fail(entity, "valid_to must be later than valid_from (exclusive end)")
        if "assertion_status" in entity and verified(entity) and not entity.get("evidence_refs"):
            fail(entity, "verified assertion requires evidence")
        if kind == "SourceRecord" and bundle.origins.get(entity["id"]) == "synthetic_example":
            if not entity["is_synthetic"] or not entity["locator"].startswith("example://"):
                fail(entity, "synthetic examples must not contain real source locators")
        if kind == "Person" and not authority(entity["source_ref"], "employment_affiliation", {"hr"}):
            fail(entity, "Person identity requires an HR-authoritative source")
        if kind == "Organization" and not authority(entity["source_ref"], "organization_structure", {"hr"}):
            fail(entity, "Organization requires an HR-authoritative source")
        if kind == "ResearchTopic":
            parent = index.get(entity.get("parent_topic_ref"))
            if entity["topic_level"] == "topic" and (
                not parent or parent.get("topic_level") != "group" or parent["area_ref"] != entity["area_ref"]
            ):
                fail(entity, "leaf topic requires a group in the same area")
        if kind == "ResearchProject":
            areas = {entity["primary_area_ref"], *entity.get("related_area_refs", [])}
            topics = [index[ref] for ref in entity["topic_refs"]]
            if entity["primary_area_ref"] in entity.get("related_area_refs", []):
                fail(entity, "primary area must not be repeated as a related area")
            if any(t["topic_level"] != "topic" or t["area_ref"] not in areas for t in topics):
                fail(entity, "project topics must be leaves in the primary or explicit related areas")
            if not any(t["area_ref"] == entity["primary_area_ref"] for t in topics):
                fail(entity, "project requires a topic in its primary area")
        rules = {
            "OrganizationRelation": ("organization_structure", {"hr"}, {"hr_record"}),
            "OrganizationMembership": ("employment_affiliation", {"hr"}, {"hr_record"}),
            "ProjectMembership": ("project_membership", {"project_registry"}, {"approved_project_record", "formal_designation"}),
            "RoleAssignment": ("project_role", {"project_registry"}, {"formal_designation", "approved_project_record"}),
            "ExpertiseAssertion": ("expertise_assessment", {"hr", "skills_review"}, {"formal_designation", "reviewed_assessment"}),
            "OrganizationParticipation": ("project_organization", {"project_registry"}, {"approved_project_record", "formal_designation"}),
            "AssetUsage": ("execution", {"execution", "ci"}, {"execution_log", "experiment_result"}),
        }
        if kind in rules and verified(entity):
            domain, source_kinds, evidence_kinds = rules[kind]
            if not authority(entity["source_ref"], domain, source_kinds) or not evidence_authorized(entity, evidence_kinds, domain, source_kinds):
                fail(entity, f"verified {kind} needs authoritative {domain} evidence; Git activity alone is insufficient")
        if kind == "ExpertiseAssertion" and verified(entity):
            if entity["assessment_basis"] not in {"official_profile", "reviewed_demonstration"}:
                fail(entity, "verified expertise cannot come from self-report or activity inference")
            if entity["assessment_basis"] == "reviewed_demonstration" and not entity.get("reviewed_by_ref"):
                fail(entity, "reviewed expertise requires a named reviewer")
        if kind == "RoleAssignment":
            membership = index[entity["membership_ref"]]
            if not _contains(membership, entity):
                fail(entity, "role validity must be inside project membership")
            if verified(entity) and not verified(membership):
                fail(entity, "verified role requires verified project membership")
        if kind in {"OrganizationMembership", "OrganizationRelation"}:
            refs = [entity["organization_ref"]] if kind == "OrganizationMembership" else [entity["child_organization_ref"], entity["parent_organization_ref"]]
            if any(not _contains(index[reference], entity) for reference in refs):
                fail(entity, "affiliation/hierarchy validity must be inside organization lifetime")
        if kind in {"ExperimentRun", "AgentExecution"}:
            if entity.get("ended_at") and datetime.fromisoformat(entity["ended_at"]) < datetime.fromisoformat(entity["started_at"]):
                fail(entity, "run end precedes start")
            if entity["run_status"] == "completed" and (not entity.get("ended_at") or not entity.get("evidence_refs")):
                fail(entity, "completed run requires end time and evidence")
            if entity.get("code_commit_ref") and index[entity["code_commit_ref"]]["artifact_kind"] != "git_commit":
                fail(entity, "code_commit_ref must identify a Git commit artifact")
        if kind == "AgentExecution" and index[entity["agent_asset_ref"]]["asset_kind"] != "agent":
            fail(entity, "agent_asset_ref must be an agent asset")
        if kind == "EvaluationMetric" and entity["contract_status"] == "ready" and (
            not entity.get("unit") or entity["value_kind"] == "family"
        ):
            fail(entity, "ready metric needs a concrete unit and value kind")
        if kind == "AssetUsage" and verified(entity):
            run = index[entity["execution_ref"]]
            project_ref = run.get("project_ref") or index[run["experiment_ref"]]["project_ref"]
            if entity["project_ref"] != project_ref:
                fail(entity, "asset usage project differs from execution project")
            if run["run_status"] != "completed":
                fail(entity, "verified asset usage requires a completed execution")
            if not set(entity.get("evidence_refs", [])) & set(run.get("evidence_refs", [])):
                fail(entity, "asset usage must share evidence with the linked execution")
            if run.get("ended_at"):
                when = datetime.fromisoformat(entity["used_at"])
                if not (datetime.fromisoformat(run["started_at"]) <= when <= datetime.fromisoformat(run["ended_at"])):
                    fail(entity, "asset usage time lies outside the execution")
            else:
                fail(entity, "verified asset usage requires execution end time")
            if run["type"] == "AgentExecution" and (
                entity["asset_ref"] != run["agent_asset_ref"] or entity["person_ref"] != run["initiated_by_ref"]
            ):
                fail(entity, "asset usage person/asset differs from execution")
            if run["type"] == "ExperimentRun" and entity["asset_ref"] not in run.get("asset_refs", []):
                fail(entity, "used asset is absent from the experiment execution")
        if kind == "Measurement":
            metric = index[entity["metric_ref"]]
            run = index[entity["run_ref"]]
            if run["type"] == "ExperimentRun":
                experiment = index[run["experiment_ref"]]
                if entity["metric_ref"] not in experiment["metric_refs"]:
                    fail(entity, "measured metric is absent from the experiment design")
                if entity.get("benchmark_ref") and entity["benchmark_ref"] not in experiment.get("benchmark_refs", []):
                    fail(entity, "measurement benchmark differs from the experiment design")
            if metric["contract_status"] != "ready" or metric["value_kind"] == "family":
                fail(entity, "measurement requires a concrete ready metric; PPA is a family")
            if entity["unit"] != metric.get("unit"):
                fail(entity, "measurement unit differs from metric contract")
            if set(metric.get("required_conditions", [])) - set(entity["conditions"]):
                fail(entity, "measurement is missing required conditions")
            if metric["value_kind"] == "number" and (
                isinstance(entity["value"], bool) or not isinstance(entity["value"], (int, float)) or not math.isfinite(entity["value"])
            ):
                fail(entity, "measurement value must be a finite number")
            if entity["unit"] == "ratio":
                p, n = entity["conditions"].get("passed_count"), entity["conditions"].get("total_count")
                if isinstance(p, bool) or isinstance(n, bool) or not isinstance(p, int) or not isinstance(n, int) or n <= 0 or not 0 <= p <= n:
                    fail(entity, "ratio requires valid passed_count and total_count")
                elif not isinstance(entity["value"], (int, float)) or not math.isclose(entity["value"], p / n):
                    fail(entity, "ratio value differs from numerator/denominator")
        if kind == "RelationAssertion":
            signature = bundle.schema["relation_predicates"].get(entity["predicate"])
            if not signature or index[entity["subject_ref"]]["type"] not in signature["from"] or index[entity["object_ref"]]["type"] not in signature["to"]:
                fail(entity, "relation predicate has an invalid type signature")
            if verified(entity) and entity["predicate"] == "COMPATIBLE_WITH" and not evidence_authorized(entity, {"experiment_result"}):
                fail(entity, "compatibility requires experiment evidence")
            if verified(entity) and entity["predicate"] == "SUPERSEDES" and not evidence_authorized(entity, {"hr_record"}, "organization_structure", {"hr"}):
                fail(entity, "organizational succession requires HR evidence")

    # Check overlapping primary affiliations and duplicated participation intervals.
    for kind, keys in [
        ("OrganizationMembership", ["person_ref"]),
        ("ProjectMembership", ["person_ref", "project_ref"]),
        ("OrganizationRelation", ["child_organization_ref"]),
    ]:
        records = [e for e in by_type(kind) if verified(e) and (kind != "OrganizationMembership" or e["membership_kind"] == "primary")]
        for i, a in enumerate(records):
            for b in records[i + 1:]:
                if all(a[k] == b[k] for k in keys) and _overlap(a, b):
                    fail(a, f"overlapping verified {kind} interval with {b['id']}")

    hierarchy = [e for e in by_type("OrganizationRelation") if verified(e)]
    boundaries = {e["valid_from"] for e in hierarchy} | {e["valid_to"] for e in hierarchy if e.get("valid_to")}
    for boundary in boundaries:
        parent_map = {e["child_organization_ref"]: e["parent_organization_ref"] for e in hierarchy if active_on(e, boundary)}
        for child in parent_map:
            seen, current = set(), child
            while current in parent_map:
                if current in seen:
                    errors.append(f"organization hierarchy: cycle at {boundary}")
                    break
                seen.add(current)
                current = parent_map[current]

    memberships = {e["id"]: e for e in by_type("ProjectMembership") if verified(e) and active_on(e, bundle.as_of)}
    owner_projects = {memberships[e["membership_ref"]]["project_ref"] for e in by_type("RoleAssignment") if verified(e) and e["role_ref"] == "role_project_owner" and active_on(e, bundle.as_of) and e["membership_ref"] in memberships}
    for project in by_type("ResearchProject"):
        if project["lifecycle_status"] == "active" and project["id"] not in owner_projects:
            fail(project, f"active project requires a verified current Project Owner at {bundle.as_of}")
    return sorted(set(errors))
