import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ontology import load_bundle, validate
from query import affiliations, asset_users, experts, person_history, project_people


class OntologyContractTests(unittest.TestCase):
    def setUp(self):
        self.bundle = copy.deepcopy(load_bundle())

    def entity(self, identity):
        return next(e for e in self.bundle.entities if e["id"] == identity)

    def has_error(self, text):
        self.assertTrue(any(text in e for e in validate(self.bundle)), text)

    def test_example_bundle_satisfies_contracts(self):
        self.assertEqual([], validate(self.bundle))

    def test_move_preserves_project_membership_and_historical_affiliation(self):
        old = affiliations(self.bundle, "person_engineer_a", "2026-10-31")
        new = affiliations(self.bundle, "person_engineer_a", "2026-11-01")
        self.assertEqual(["org_interface_team"], [e["organization_ref"] for e in old])
        self.assertEqual(["org_ax_team"], [e["organization_ref"] for e in new])
        for day in ["2026-10-31", "2026-11-01"]:
            result = project_people(self.bundle, "research_cxl_controller", day)
            self.assertEqual("membership_a_cxl", result["participants"][0]["membership_ref"])

    def test_git_activity_does_not_verify_expertise(self):
        e = self.entity("skill_a_cxl")
        e.update(source_ref="src_git", evidence_refs=["ev_git"], assessment_basis="inferred_from_activity")
        self.has_error("expertise_assessment")
        self.has_error("cannot come from self-report or activity inference")

    def test_git_activity_does_not_assign_project_owner(self):
        self.entity("roleassign_a_cxl_owner").update(source_ref="src_git", evidence_refs=["ev_git"])
        self.has_error("project_role")

    def test_candidate_expertise_is_excluded_from_verified_results(self):
        self.assertEqual(["person_engineer_b"], [e["person_ref"] for e in experts(self.bundle, ["expertise_hbf", "expertise_kv_cache"], "2026-11-08")])

    def test_primary_affiliation_periods_must_not_overlap(self):
        self.entity("affiliation_a_old")["valid_to"] = "2026-11-02"
        self.has_error("overlapping verified OrganizationMembership")

    def test_role_period_is_contained_in_participation(self):
        self.entity("roleassign_a_cxl_owner")["valid_from"] = "2026-07-01"
        self.has_error("role validity must be inside project membership")

    def test_dangling_reference_and_wrong_type_are_rejected(self):
        self.entity("membership_a_cxl")["project_ref"] = "missing_project"
        self.has_error("unresolved reference")
        self.entity("membership_a_cxl")["project_ref"] = "person_engineer_b"
        self.has_error("wrong type")

    def test_duplicate_ids_are_rejected(self):
        self.bundle.entities.append(copy.deepcopy(self.entity("research_cxl_controller")))
        self.has_error("duplicate id")

    def test_asset_use_requires_matching_observed_execution(self):
        self.entity("usage_a_rtl_agent")["person_ref"] = "person_engineer_b"
        self.has_error("person/asset differs from execution")

    def test_asset_users_are_based_on_execution_not_project_membership(self):
        result = asset_users(self.bundle, "asset_rtl_agent_v1", "2026-11-08")
        self.assertEqual(["person_engineer_a"], [e["person_ref"] for e in result])
        self.assertEqual([], asset_users(self.bundle, "asset_rtl_agent_v1", "2026-10-31"))

    def test_incomplete_execution_returns_errors_without_crashing(self):
        self.entity("agent_run_a_rtl")["ended_at"] = None
        self.has_error("requires end time and evidence")
        self.has_error("requires execution end time")

    def test_history_excludes_future_affiliation_and_usage(self):
        result = person_history(self.bundle, "person_engineer_a", "2026-10-31")
        self.assertEqual(["affiliation_a_old"], [e["id"] for e in result["organization_memberships"]])
        self.assertEqual([], result["actual_asset_usage"])

    def test_asset_use_as_of_date_is_in_seoul_timezone(self):
        self.entity("usage_a_rtl_agent")["used_at"] = "2026-11-05T16:01:00+00:00"
        self.entity("agent_run_a_rtl")["started_at"] = "2026-11-05T16:00:00+00:00"
        self.entity("agent_run_a_rtl")["ended_at"] = "2026-11-05T16:20:00+00:00"
        self.assertEqual([], validate(self.bundle))
        self.assertEqual([], asset_users(self.bundle, "asset_rtl_agent_v1", "2026-11-05"))
        self.assertEqual(1, len(asset_users(self.bundle, "asset_rtl_agent_v1", "2026-11-06")))

    def test_metric_contract_preserves_units_and_denominator(self):
        self.entity("measurement_simulation_pass")["unit"] = "percent"
        self.has_error("unit differs from metric contract")
        self.entity("measurement_simulation_pass")["unit"] = "ratio"
        self.entity("measurement_simulation_pass")["conditions"].pop("total_count")
        self.has_error("missing required conditions")

    def test_public_reference_cannot_expose_restricted_person(self):
        self.entity("person_engineer_a")["access_scope"] = "restricted_hr"
        self.has_error("more restricted object")

    def test_organization_hierarchy_cannot_cycle(self):
        edge = copy.deepcopy(self.entity("orgrel_systems"))
        edge.update(id="orgrel_cycle", child_organization_ref="org_memory_solutions", parent_organization_ref="org_interface_team")
        self.bundle.entities.append(edge)
        self.has_error("hierarchy: cycle")

    def test_cmx_hbf_compatibility_is_not_implied_by_shared_workload(self):
        edge = copy.deepcopy(self.entity("link_kv_studies"))
        edge.update(id="link_unproven_compatibility", subject_ref="asset_cmx", predicate="COMPATIBLE_WITH", object_ref="asset_hbf_prototype")
        self.bundle.entities.append(edge)
        self.has_error("compatibility requires experiment evidence")


if __name__ == "__main__":
    unittest.main()
