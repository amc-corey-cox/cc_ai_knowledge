# About CC AI Knowledge

## Why This Exists

This repository is a personal knowledge base built by an experienced developer who jumped into AI without a formal ML background. After a year of using AI tools daily, the articles here capture what's actually useful to understand — organized for someone who wants to build effective AI-assisted workflows, not publish papers.

## Design Principles

**Provenance over volume.** Every claim traces to a source. Articles include exact quotes, access dates, and confidence levels. AI-generated content is explicitly labeled and must pass automated verification before promotion. See [Provenance Design](reference/provenance.md).

**Practical over theoretical.** The focus is on concepts that change how you work — how attention mechanisms affect what models can do, why context windows matter for coding agents, how MCP extends tool capabilities. Theory appears only where it builds useful intuition.

**Structured for machines and humans.** Articles use YAML frontmatter validated against a [LinkML](https://linkml.io/) schema. Topics are drawn from the [Artificial Intelligence Ontology](https://github.com/berkeleybop/artificial-intelligence-ontology). This structure enables RAG retrieval by [cc_forge](https://github.com/amc-corey-cox/cc_forge) while remaining readable as documentation.

## Verification Model

Content follows an automated-first verification pipeline:

1. **Schema validation** — frontmatter conforms to LinkML schema
2. **Term validation** — topic CURIEs resolve against AIO ontology
3. **Quote verification** — quoted text found in source content (planned)
4. **Claims cross-check** — no contradictions with existing articles (planned)

Content passing all automated checks is promoted from `ai_unverified` to `ai_generated`. Human review is only required when automated checks flag failures.

## Related Projects

| Repository | Relationship |
|------------|-------------|
| [cc_forge](https://github.com/amc-corey-cox/cc_forge) | RAG consumer — retrieves articles for agent context |
| [cc_ai_model_ontology](https://github.com/amc-corey-cox/cc_ai_model_ontology) | Structured model metadata referenced by articles |
