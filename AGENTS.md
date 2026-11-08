# Global AI Research Hub instructions

- Start with `ai_research_ontology/README.md` and `ontology/manifest.yaml` inside that module.
- Treat the schema and vocabulary as a proposed model. Do not mark organizational adoption or real research outcomes as verified without evidence.
- Keep ResearchArea separate from Organization. ResearchProject connects the technical and organizational axes.
- Keep the five ResearchArea portfolio categories separate from TechnologyDomain. Leaf topics have one primary technical domain and may reference related domains; ResearchConcern supplies cross-cutting evaluation perspectives.
- Treat the executive brief as a proposed reporting view. Topic/source counts and validator success do not establish organizational coverage, investment priority, actual productivity or the leader's internal intent.
- Keep Person, OrganizationMembership, ProjectMembership, RoleAssignment, and ExpertiseAssertion distinct. Preserve their validity intervals and source provenance.
- HR is authoritative for organization structure and employment affiliation. Git activity does not establish a project role or expertise.
- Use stable IDs, `*_ref` / `*_refs`, ISO dates, and timezone-aware timestamps. Intervals use an exclusive end date.
- Keep original source references, assertion status, and evidence. Candidate relationships must remain distinguishable from verified facts.
- Keep all bundled examples synthetic. Real HR exports and private research records belong in authorized, access-controlled source systems.
- Public literature in `research/public_research_registry.yaml` is real source metadata, separate from `examples/graph.yaml`. Preserve publication precision, inspection scope, availability at publication, limitations and internal reproduction status.
- Keep vendor initiatives such as NVIDIA Storage-Next distinct from generic technical topics, implemented assets and adopted standards. A source review does not establish interoperability or internal reproduction.
- Research directions are dated, curated coverage. Do not imply exhaustive global coverage or automatic ongoing collection. Extend the evidence registry alongside the taxonomy when adding trends.
- Access-scope metadata and the static validator are not a production authorization service.
- Keep this repository lightweight. Introduce an application, database, or service only for an explicit task.
- Validate changes with the module validator and relevant unit tests. Add focused regression cases for material modeling rules.
- Commit coherent changes and keep unrelated work out of each commit.
