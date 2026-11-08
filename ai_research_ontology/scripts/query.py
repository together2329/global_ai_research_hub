"""Executable competency questions over public, synthetic example records."""
import argparse
from datetime import date, datetime
import json
from zoneinfo import ZoneInfo

from ontology import active_on, index_entities, load_bundle, validate, verified


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


def answers(bundle, as_of):
    return {
        "cxl-experts": experts(bundle, ["expertise_cxl"], as_of),
        "project-people": project_people(bundle, "research_cxl_controller", as_of),
        "asset-users": asset_users(bundle, "asset_rtl_agent_v1", as_of),
        "dual-expertise": experts(bundle, ["expertise_hbf", "expertise_kv_cache"], as_of),
        "person-history": person_history(bundle, "person_engineer_a", as_of),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", help="YYYY-MM-DD; defaults to the example snapshot date")
    parser.add_argument("--query", default="all", choices=["all", "cxl-experts", "project-people", "asset-users", "dual-expertise", "person-history"])
    args = parser.parse_args()
    bundle = load_bundle()
    problems = validate(bundle)
    if problems:
        parser.error("Ontology validation failed: " + "; ".join(problems))
    # This CLI is an example reader, not an HR authorization service.
    if any(e["access_scope"] != "public" for e in bundle.entities):
        parser.error("Demo query accepts public synthetic data only")
    as_of = args.as_of or bundle.as_of
    try:
        date.fromisoformat(as_of)
        if len(as_of) != 10:
            raise ValueError("non-ISO date")
    except ValueError:
        parser.error("--as-of must be YYYY-MM-DD")
    result = answers(bundle, as_of)
    if args.query != "all":
        result = {args.query: result[args.query]}
    print(json.dumps({"notice": "Synthetic examples only; no real HR or research results", "as_of": as_of, "results": result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
