# CC AI Knowledge

A curated knowledge base for understanding the AI/ML landscape. Educational content for humans, not operational documentation.

## Purpose

This knowledge base distills the firehose of AI information into curated, understandable content that builds mental models. It's designed to help an expert programmer learn about AI.

## What Belongs Here

- **Conceptual explanations**: What is quantization? How do transformers work?
- **Landscape orientation**: How do different approaches compare? What are the tradeoffs?
- **Curated insights**: Distilled understanding from papers, blogs, community experience
- **Verified sources**: Every claim traceable to primary or secondary sources

## What Does NOT Belong Here

- **Operational docs**: Setup guides, deployment commands
- **System-specific info**: Hardware specs, local paths
- **Raw data**: Model parameters, context lengths (see [cc_ai_model_ontology](https://github.com/youruser/cc_ai_model_ontology))

## Structure

```
cc_ai_knowledge/
├── PROVENANCE.md           # Attribution and trust design
├── topics/                 # Knowledge by topic
│   ├── ai-fundamentals/    # Core AI concepts
│   ├── agents/             # AI agent patterns
│   ├── local-inference/    # Running models locally
│   └── transformers/       # Transformer architecture
├── pending/                # Unverified content
├── sources/                # Cached source material
└── curriculum/             # Learning paths
```

## Knowledge Entry Format

Each entry includes YAML frontmatter with:
- Source citations with exact quotes
- Curation type (human_curated, ai_assisted, ai_generated)
- Verification status
- Confidence level

See [PROVENANCE.md](PROVENANCE.md) for full attribution design.

## Related Projects

- [cc_forge](https://github.com/youruser/cc_forge) - Local-first AI coding assistant
- [cc_ai_model_ontology](https://github.com/youruser/cc_ai_model_ontology) - Structured model catalog

## License

Apache-2.0
