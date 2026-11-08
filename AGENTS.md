# Global AI Research Hub instructions

- Start with `ai_research_ontology/README.md` and `ontology/manifest.yaml` inside that module.
- Treat the schema and vocabulary as a proposed model. Do not mark organizational adoption or real research outcomes as verified without evidence.
- Keep ResearchArea separate from Organization. ResearchProject connects the technical and organizational axes.
- Keep Person, OrganizationMembership, ProjectMembership, RoleAssignment, and ExpertiseAssertion distinct. Preserve their validity intervals and source provenance.
- HR is authoritative for organization structure and employment affiliation. Git activity does not establish a project role or expertise.
- Use stable IDs, `*_ref` / `*_refs`, ISO dates, and timezone-aware timestamps. Intervals use an exclusive end date.
- Keep original source references, assertion status, and evidence. Candidate relationships must remain distinguishable from verified facts.
- Keep all bundled examples synthetic. Real HR exports and private research records belong in authorized, access-controlled source systems.
- Access-scope metadata and the static validator are not a production authorization service.
- Keep this repository lightweight. Introduce an application, database, or service only for an explicit task.
- Validate changes with the module validator and relevant unit tests. Add focused regression cases for material modeling rules.
- Commit coherent changes and keep unrelated work out of each commit.
