"""Query public research sources and synthetic organization examples."""
import argparse
from datetime import date, datetime
import json
from zoneinfo import ZoneInfo

from ontology import active_on, index_entities, load_bundle, publication_window, validate, verified


def local_day(timestamp):
    return datetime.fromisoformat(timestamp).astimezone(ZoneInfo("Asia/Seoul")).date().isoformat()


def affiliations(bundle, person_ref, as_of):
    index = index_entities(bundle.entities)
    return [
        {"organization_ref": e["organization_ref"], "name": index[e["organization_ref"]]["name"],
         "valid_from": e["valid_from"], "valid_to": e.get("valid_to"), "evidence_refs": e["evidence_refs"]}
        for e in bundle.entities
        if e["type"] == "OrganizationMembership" and e["person_ref"] == person_ref
        and verified(e) and active_on(e, as_of)
    ]


def experts(bundle, expertise_refs, as_of):
    index, matches = index_entities(bundle.entities), {}
    wanted = set(expertise_refs)
    for e in bundle.entities:
        if e["type"] == "ExpertiseAssertion" and verified(e) and active_on(e, as_of) and e["expertise_ref"] in wanted:
            matches.setdefault(e["person_ref"], []).append(e)
    return [
        {"person_ref": person_ref, "name": index[person_ref]["name"],
         "verified_expertise_refs": sorted({e["expertise_ref"] for e in assertions}),
         "assertion_refs": [e["id"] for e in assertions],
         "affiliations_as_of": affiliations(bundle, person_ref, as_of)}
        for person_ref, assertions in sorted(matches.items())
        if wanted <= {e["expertise_ref"] for e in assertions}
    ]


def project_people(bundle, project_ref, as_of):
    index = index_entities(bundle.entities)
    people = []
    for membership in bundle.entities:
        if membership["type"] != "ProjectMembership" or membership["project_ref"] != project_ref or not verified(membership) or not active_on(membership, as_of):
            continue
        assignments = [e for e in bundle.entities if e["type"] == "RoleAssignment" and
                       e["membership_ref"] == membership["id"] and verified(e) and active_on(e, as_of)]
        people.append({"person_ref": membership["person_ref"], "name": index[membership["person_ref"]]["name"],
                       "membership_ref": membership["id"], "role_refs": [e["role_ref"] for e in assignments],
                       "affiliations_as_of": affiliations(bundle, membership["person_ref"], as_of)})
    organizations = [
        {"organization_ref": e["organization_ref"], "name": index[e["organization_ref"]]["name"],
         "participation_kind": e["participation_kind"], "evidence_refs": e["evidence_refs"]}
        for e in bundle.entities if e["type"] == "OrganizationParticipation" and
        e["project_ref"] == project_ref and verified(e) and active_on(e, as_of)
    ]
    return {"project_ref": project_ref, "participants": people, "explicit_organization_participation": organizations}


def asset_users(bundle, asset_ref, as_of):
    index = index_entities(bundle.entities)
    return [
        {"person_ref": e["person_ref"], "name": index[e["person_ref"]]["name"],
         "project_ref": e["project_ref"], "execution_ref": e["execution_ref"], "used_at": e["used_at"],
         "affiliations_at_use": affiliations(bundle, e["person_ref"], local_day(e["used_at"])),
         "evidence_refs": e["evidence_refs"]}
        for e in bundle.entities if e["type"] == "AssetUsage" and e["asset_ref"] == asset_ref and verified(e)
        and local_day(e["used_at"]) <= as_of
    ]


def person_history(bundle, person_ref, as_of):
    memberships = [e for e in bundle.entities if e["type"] == "ProjectMembership" and e["person_ref"] == person_ref and verified(e) and e["valid_from"] <= as_of]
    membership_refs = {e["id"] for e in memberships}
    return {
        "person_ref": person_ref,
        "organization_memberships": [e for e in bundle.entities if e["type"] == "OrganizationMembership" and e["person_ref"] == person_ref and verified(e) and e["valid_from"] <= as_of],
        "project_memberships": memberships,
        "role_assignments": [e for e in bundle.entities if e["type"] == "RoleAssignment" and e["membership_ref"] in membership_refs and verified(e) and e["valid_from"] <= as_of],
        "actual_asset_usage": [e for e in bundle.entities if e["type"] == "AssetUsage" and e["person_ref"] == person_ref and verified(e) and local_day(e["used_at"]) <= as_of],
    }


def research_landscape(bundle, as_of, direction_ref=None):
    index = index_entities(bundle.entities)
    if direction_ref and (direction_ref not in index or index[direction_ref]["type"] != "ResearchDirection"):
        raise ValueError("Unknown research direction: " + direction_ref)
    result = []
    for direction in bundle.entities:
        if direction["type"] != "ResearchDirection" or (direction_ref and direction["id"] != direction_ref):
            continue
        literature = []
        for reference in direction["external_research_refs"]:
            record = index[reference]
            source = index[record["source_ref"]]
            window = publication_window(source)
            # A month-only date is not treated as a known publication on day one.
            if window is None or window[1] > as_of:
                continue
            literature.append({
                "id": reference, "name": record["name"], "url": source["locator"],
                "publisher": source["publisher"], "published_on": source.get("published_on"),
                "date_precision": source["date_precision"], "checked_on": record["checked_on"],
                "inspection_scope": record["inspection_scope"],
                "retrieved_at": source["retrieved_at"], "review_status": record["review_status"],
                "evidence_basis": record["evidence_basis"],
                "validation_stage_ref": record["validation_stage_ref"],
                "availability_at_publication": record["availability_at_publication"],
                "internal_reproduction_status": record["internal_reproduction_status"],
                "key_findings": record["key_findings"], "limitations": record["limitations"],
                "event_started_on": record.get("event_started_on"),
                "event_ended_on": record.get("event_ended_on"),
                "explicitly_linked_project_refs": [p["id"] for p in bundle.entities
                    if p["type"] == "ResearchProject" and reference in p.get("external_research_refs", [])],
            })
        if literature:
            result.append({key: direction[key] for key in (
                "id", "name", "topic_refs", "data_object_refs", "system_layer_refs",
                "bottleneck_refs", "metric_refs", "as_of", "coverage_notes"
            )} | {"initiative_refs": direction.get("initiative_refs", []), "external_research": literature})
    return result


def answers(bundle, as_of):
    return {
        "cxl-experts": experts(bundle, ["expertise_cxl"], as_of),
        "project-people": project_people(bundle, "research_cxl_controller", as_of),
        "asset-users": asset_users(bundle, "asset_rtl_agent_v1", as_of),
        "dual-expertise": experts(bundle, ["expertise_hbf", "expertise_kv_cache"], as_of),
        "person-history": person_history(bundle, "person_engineer_a", as_of),
        "research-landscape": research_landscape(bundle, as_of),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", help="YYYY-MM-DD; validity date or literature publication cutoff, not a known-at history")
    parser.add_argument("--query", default="all", choices=["all", "cxl-experts", "project-people", "asset-users", "dual-expertise", "person-history", "research-landscape"])
    parser.add_argument("--direction", help="Research direction ID or suffix, e.g. vector_search or storage_next")
    args = parser.parse_args()
    bundle = load_bundle()
    problems = validate(bundle)
    if problems:
        parser.error("Ontology validation failed: " + "; ".join(problems))
    # This CLI is an example reader, not an HR authorization service.
    if any(e["access_scope"] != "public" for e in bundle.entities):
        parser.error("Demo query accepts public records only")
    as_of = args.as_of or bundle.as_of
    try:
        date.fromisoformat(as_of)
        if len(as_of) != 10:
            raise ValueError("non-ISO date")
    except ValueError:
        parser.error("--as-of must be YYYY-MM-DD")
    result = answers(bundle, as_of)
    if args.direction:
        if args.query not in {"all", "research-landscape"}:
            parser.error("--direction applies to research-landscape")
        reference = args.direction if args.direction.startswith("direction_") else "direction_" + args.direction
        try:
            result["research-landscape"] = research_landscape(bundle, as_of, reference)
        except ValueError as error:
            parser.error(str(error))
    if args.query != "all":
        result = {args.query: result[args.query]}
    print(json.dumps({"notice": "Public literature is real; organization, people and internal execution examples are synthetic. Source claims are not internal reproductions.", "as_of": as_of, "curation_snapshot": bundle.as_of, "results": result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
