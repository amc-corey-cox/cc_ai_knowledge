# Agent Instructions for CC AI Knowledge

This document provides guidance for AI agents working in this repository.

## Purpose

This repository is a **curated knowledge base** for understanding AI/ML concepts. It serves as an educational resource for humans and (eventually) a RAG source for AI agents.

## What This Repo Contains

- `topics/` - Knowledge articles organized by topic
- `PROVENANCE.md` - Design document for attribution and trust
- `pending/` - Unverified content awaiting review
- `sources/` - Cached source material
- `curriculum/` - Learning paths (future)

## Core Principle: Provenance

Every claim must be traceable to a source. See `PROVENANCE.md` for full details.

### Required Frontmatter

All knowledge entries must include YAML frontmatter:

```yaml
---
id: kb-2025-xxx
title: "Article Title"
created: 2025-01-27
updated: 2025-01-27

author: human  # or agent:<agent-id>
curation_type: human_curated  # human_curated | ai_assisted | ai_generated | ai_unverified

sources:
  - id: src-001
    type: primary  # primary | secondary | tertiary
    title: "Source Title"
    url: "https://..."
    accessed: 2025-01-27
    quotes:
      - text: "Exact quote from source"
        location: "Section/page"

topics: [topic1, topic2]
confidence: high  # high | medium | low | uncertain

verified: true
verified_by: human
verification_date: 2025-01-27
---
```

## What You Should Do

### When Adding Content
- Place in appropriate `topics/` subdirectory
- Include full frontmatter with sources
- Use exact quotes when citing
- Mark AI-generated content as `ai_unverified` until human reviews

### When Updating Content
- Update the `updated` date
- Add any new sources consulted
- Note changes in verification status if applicable

### Content Guidelines
- **Explain concepts**, don't just list facts
- **Compare approaches**, highlight tradeoffs
- **Cite sources**, especially for claims
- **Keep it digestible**, this is for learning

## What Does NOT Belong Here

- Operational documentation (setup guides) → use cc_forge/docs/
- Raw data/specs → use cc_ai_model_ontology
- System-specific configuration → use environment variables

## Related Repositories

| Repository | Purpose |
|------------|---------|
| `cc_forge` | Local-first AI coding assistant (main project) |
| `cc_ai_model_ontology` | Structured model catalog (LinkML) |

## Topic Structure

```
topics/
├── ai-fundamentals/     # Core AI concepts
├── agents/              # AI agent patterns
├── local-inference/     # Running models locally
└── transformers/        # Transformer architecture
```

Add new subdirectories as topics expand.
