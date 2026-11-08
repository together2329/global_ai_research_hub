import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ontology import load_bundle, publication_window, validate
from query import affiliations, asset_users, experts, person_history, project_people, research_landscape


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

    def vector_measurements(self):
        """Synthetic test fixture, not a literature result or measured benchmark."""
        metrics = ["metric_vector_recall_at_k", "metric_vector_qps", "metric_vector_p99_latency"]
        benchmark = copy.deepcopy(self.entity("benchmark_cxl_regression"))
        benchmark.update(id="benchmark_vector_test", name="Synthetic vector test", workload_refs=["workload_vector_search"])
        experiment = copy.deepcopy(self.entity("experiment_cxl_simulation"))
        experiment.update(id="experiment_vector_test", name="Synthetic vector test", project_ref="research_vector_storage_demo",
                          benchmark_refs=[benchmark["id"]], metric_refs=metrics)
        run = copy.deepcopy(self.entity("run_cxl_simulation"))
        run.update(id="run_vector_test", experiment_ref=experiment["id"], asset_refs=[])
        self.bundle.entities.extend([benchmark, experiment, run])
        profile = {"k": 10, "vector_count": 1000, "dimension": 128, "distance_metric": "cosine",
                   "filter_selectivity": 1.0, "index_version": "test-v1", "query_set_ref": "test-query-v1",
                   "hardware_profile": "synthetic-hardware", "concurrency": 1}
        for metric_ref, value, extra in [
            (metrics[0], 0.96, {"ground_truth_ref": "test-ground-truth"}),
            (metrics[1], 100, {"min_recall": 0.95}),
            (metrics[2], 12, {"sample_count": 100}),
        ]:
            self.bundle.entities.append({"id": "test_" + metric_ref, "type": "Measurement", "access_scope": "public",
                "run_ref": run["id"], "metric_ref": metric_ref, "value": value, "unit": self.entity(metric_ref)["unit"],
                "aggregation": "synthetic-test", "conditions": profile | extra,
                "benchmark_ref": benchmark["id"], "evidence_refs": ["ev_simulation"]})

    def test_public_literature_and_synthetic_internal_records_remain_separate(self):
        records = [e for e in self.bundle.entities if e["type"] == "ExternalResearch"]
        self.assertEqual(14, len(records))
        for record in records:
            self.assertFalse(self.entity(record["source_ref"])["is_synthetic"])
            self.assertEqual("not_reproduced", record["internal_reproduction_status"])
        for source in [e for e in self.bundle.entities if e["type"] == "SourceRecord" and self.bundle.origins[e["id"]] == "synthetic_example"]:
            self.assertTrue(source["is_synthetic"])

    def test_storage_next_is_an_initiative_not_a_generic_research_topic(self):
        initiative = self.entity("initiative_nvidia_storage_next")
        self.assertEqual("TechnologyInitiative", initiative["type"])
        result = research_landscape(self.bundle, "2026-11-08", "direction_storage_next")[0]
        self.assertEqual([initiative["id"]], result["initiative_refs"])
        self.assertIn("under_development", [e["availability_at_publication"] for e in result["external_research"]])

    def test_publication_precision_does_not_invent_a_day(self):
        source = self.entity("source_mooncake")
        self.assertEqual(("2025-02-01", "2025-02-28"), publication_window(source))
        early = research_landscape(self.bundle, "2025-02-01", "direction_context_memory")
        late = research_landscape(self.bundle, "2025-02-28", "direction_context_memory")
        self.assertEqual([], early)
        self.assertEqual("2025-02", late[0]["external_research"][0]["published_on"])
        source["date_precision"] = "day"
        self.has_error("publication date does not match its precision")

    def test_source_cannot_be_published_after_the_snapshot(self):
        self.entity("source_aisaq")["published_on"] = "2026-12-01"
        self.has_error("publication is after the bundle snapshot")

    def test_external_research_cannot_use_a_synthetic_source(self):
        self.entity("external_aisaq")["source_ref"] = "src_ci"
        self.has_error("real HTTPS public-research source")

    def test_perspective_is_not_promoted_to_peer_reviewed_evidence(self):
        self.entity("external_agent_memory_2026")["review_status"] = "peer_reviewed"
        self.has_error("perspective source must retain its research-agenda evidence status")

    def test_synthetic_result_cannot_establish_internal_reproduction(self):
        self.entity("external_aisaq").update(internal_reproduction_status="reproduced", reproduction_evidence_refs=["ev_simulation"])
        self.has_error("internal reproduction requires non-synthetic experiment evidence")

    def test_recall_is_a_ratio_without_test_pass_count_semantics(self):
        self.vector_measurements()
        self.assertEqual([], validate(self.bundle))
        self.entity("test_metric_vector_recall_at_k")["value"] = 1.01
        self.has_error("ratio value must be between zero and one")

    def test_vector_throughput_requires_quality_and_tail_latency(self):
        self.vector_measurements()
        self.bundle.entities.remove(self.entity("test_metric_vector_p99_latency"))
        self.has_error("requires companion metric_vector_p99_latency")

    def test_vector_companions_must_match_filter_and_hardware_profile(self):
        self.vector_measurements()
        self.entity("test_metric_vector_recall_at_k")["conditions"]["filter_selectivity"] = 0.1
        self.has_error("requires companion metric_vector_recall_at_k")
        self.entity("test_metric_vector_recall_at_k")["conditions"]["filter_selectivity"] = 1.0
        self.entity("test_metric_vector_p99_latency")["conditions"]["hardware_profile"] = "other-machine"
        self.has_error("requires companion metric_vector_p99_latency")

    def test_vector_throughput_must_meet_declared_recall_floor(self):
        self.vector_measurements()
        self.entity("test_metric_vector_recall_at_k")["value"] = 0.9
        self.has_error("does not meet its declared recall floor")

    def test_small_io_iops_requires_matching_tail_latency(self):
        experiment = self.entity("experiment_cxl_simulation")
        experiment["metric_refs"].append("metric_small_io_iops")
        m = copy.deepcopy(self.entity("measurement_simulation_pass"))
        m.update(id="test_iops", metric_ref="metric_small_io_iops", value=100, unit="ops/s",
                 conditions={"io_size_bytes":512, "read_write_mix":"read-only", "queue_depth":8,
                             "initiator":"GPU", "io_path":"synthetic-test", "hardware_profile":"test"})
        self.bundle.entities.append(m)
        self.has_error("requires companion metric_storage_p99_latency")

    def test_facets_are_typed_references_not_interchangeable_tags(self):
        self.entity("research_vector_storage_demo")["data_object_refs"] = ["layer_local_flash"]
        self.has_error("data_object_refs reference layer_local_flash has wrong type")

    def test_research_query_exposes_source_status_and_publication_cutoff(self):
        rows = research_landscape(self.bundle, "2026-03-31", "direction_vector_search")[0]["external_research"]
        self.assertNotIn("external_diskann_sql", [r["id"] for r in rows])
        self.assertTrue(all(r["url"].startswith("https://") and r["limitations"] for r in rows))
        with self.assertRaises(ValueError):
            research_landscape(self.bundle, "2026-11-08", "missing_direction")


if __name__ == "__main__":
    unittest.main()
