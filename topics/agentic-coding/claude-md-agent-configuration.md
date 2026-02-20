---
id: kb-2025-016
title: "CLAUDE.md: The Layered Instruction Model for Agent Configuration"
created: 2026-02-19
updated: 2026-02-19

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: secondary
    title: "Using CLAUDE.MD Files: Customizing Claude Code for Your Codebase"
    url: "https://claude.com/blog/using-claude-md-files"
    accessed: 2026-02-19
    quotes:
      - text: "Think of it as a configuration file that Claude automatically incorporates into every conversation."
        location: "Introduction"
      - text: "Your CLAUDE.md file becomes part of Claude's system prompt. Every conversation starts with this context already loaded."
        location: "How CLAUDE.md works"
      - text: "A well-maintained CLAUDE.md evolves with your codebase, continuously reducing the friction of working with AI assistance."
        location: "Best practices"
  - id: src-002
    type: primary
    title: "Claude Code Documentation"
    url: "https://code.claude.com/docs"
    accessed: 2026-02-19
    quotes:
      - text: "CLAUDE.md is a markdown file you add to your project root that Claude Code reads at the start of every session. Use it to set coding standards, architecture decisions, preferred libraries, and review checklists."
        location: "Overview - Customize section"
      - text: "Create custom slash commands to package repeatable workflows your team can share."
        location: "Overview - Customize section"
  - id: src-003
    type: primary
    title: "Building Effective Agents"
    authors: ["Anthropic"]
    url: "https://www.anthropic.com/engineering/building-effective-agents"
    accessed: 2026-02-19
    quotes:
      - text: "Prioritize transparency by explicitly showing the agent's planning steps."
        location: "Summary"

topics:
  - agent-configuration
  - agentic-coding
  - prompt-engineering
  - context-management

confidence: high
verified: false
verified_by: unverified
verification_notes: "AI-assisted draft; quotes sourced from official documentation but need human verification"

ai_metadata:
  model: claude-opus-4-6
  generation_date: 2026-02-19
  reviewed_by: pending
---

# CLAUDE.md: The Layered Instruction Model for Agent Configuration

## Overview

General-purpose LLMs know a lot about programming but nothing about your project. They do not know your directory layout, your team's naming conventions, which testing framework you use, or why that one module has a non-obvious architecture. Every conversation starts from scratch, and the developer wastes tokens re-explaining the same context.

CLAUDE.md solves this by providing a persistent configuration layer between the model's general training and the specific task at hand. "Think of it as a configuration file that Claude automatically incorporates into every conversation" [src-001]. Rather than relying on the model to infer project conventions from code alone, you declare them explicitly, and the agent reads those declarations before it does anything else.

This article covers the layered instruction model that CLAUDE.md implements, how the layers compose, what belongs in each layer, and how the system compares to alternatives in other agentic coding tools.

## The Layered Instruction Model

CLAUDE.md is not a single file. It is a set of files at different scopes that merge together to form the agent's working instructions. This layered design addresses a fundamental tension: some instructions are personal, some are shared with the team, and some apply only to a specific part of a monorepo.

### Layer 1: Global Personal Preferences (~/.claude/CLAUDE.md)

The global file lives in your home directory and applies to every project you open with Claude Code. This is the place for preferences that follow you regardless of what codebase you are working in.

Typical contents:
- Autonomy preferences (when to ask vs. proceed)
- Communication style (verbosity, emoji usage, language)
- Environment setup notes (package managers, shell, OS quirks)
- Workflow conventions (branching strategy, commit style)
- Tool preferences (editor integrations, terminal conventions)

Because this file is outside any repository, it is never committed to version control. It is purely personal.

### Layer 2: Project Root CLAUDE.md (./CLAUDE.md)

The project-level file lives at the root of your repository and is checked into version control. This is the team-shared configuration: "CLAUDE.md is a markdown file you add to your project root that Claude Code reads at the start of every session. Use it to set coding standards, architecture decisions, preferred libraries, and review checklists" [src-002].

Typical contents:
- Architecture overview and directory structure
- Coding standards and style rules
- Common commands (build, test, lint, deploy)
- Preferred libraries and frameworks
- Review checklists and PR conventions
- Domain-specific warnings and gotchas

Because this file is in the repo, every team member (and every CI agent) gets the same baseline instructions. When conventions change, the CLAUDE.md changes with them in the same pull request.

### Layer 3: User-Private Project Overrides (~/.claude/projects/<path>/CLAUDE.md)

The private project override lives in your home directory but is scoped to a specific project path. This is for instructions that apply to one project but should not be shared with the team.

Typical contents:
- Personal workflow notes ("I always run tests with -v")
- Credentials or token reminders (not the secrets themselves)
- Task-specific memory ("Last time I worked on the auth module, I discovered...")
- Overrides for team conventions you handle differently locally

The path-based scoping means you can have different private overrides for different repositories without any collision.

### Layer 4: Parent Directory CLAUDE.md (../ and above)

In monorepo setups, CLAUDE.md files can exist at parent directory levels above the project root. Claude Code walks up the directory tree and includes any CLAUDE.md files it finds. This lets a monorepo define shared conventions at the top level while individual packages define their own specifics.

For example:
```
monorepo/
  CLAUDE.md              # Shared: "Use pnpm, not npm. All packages use vitest."
  packages/
    frontend/
      CLAUDE.md          # Package-specific: "This is a Next.js app. Use App Router."
    backend/
      CLAUDE.md          # Package-specific: "This is a FastAPI service. Use pytest."
```

### Layer 5: Subdirectory CLAUDE.md Files

CLAUDE.md files can also appear in subdirectories below the project root. When the agent is working in a particular area of the codebase, it picks up any CLAUDE.md files in directories between the project root and the current working context. This enables fine-grained, localized instructions for specific modules or subsystems.

## How Layers Compose

"Your CLAUDE.md file becomes part of Claude's system prompt. Every conversation starts with this context already loaded" [src-001]. When a session starts, Claude Code discovers all applicable CLAUDE.md files and merges their contents into the system prompt. The composition follows a straightforward model:

1. Global personal preferences load first (broadest scope)
2. Parent directory files load next (monorepo level)
3. Project root file loads (team conventions)
4. Subdirectory files load as the agent works in specific areas
5. Private project overrides load last (narrowest scope, highest priority)

All layers are additive. Later layers do not replace earlier ones; they augment them. If a private override contradicts a team convention, the agent sees both and must reconcile them. In practice, this means you should write overrides as explicit amendments ("For this project, I prefer X instead of the team default Y") rather than restating everything from scratch.

The total cost of CLAUDE.md is context window space. Every line across all layers consumes tokens that could otherwise be used for code, tool results, or conversation history. This creates a practical ceiling on how verbose your instructions can be.

## What to Put in CLAUDE.md

The most effective CLAUDE.md files are concise, actionable, and specific. They tell the agent what it needs to know to start working, not everything about the project.

### Coding Standards

Declare the non-obvious rules that the agent cannot infer from code alone:

```markdown
## Code Style
- Use absolute imports, never relative
- Error handling: always use custom exception classes from src/errors.py
- No print statements in production code; use the logger from src/logging.py
- SQL: use parameterized queries, never string interpolation
```

### Architecture Decisions

Explain the "why" behind structural choices so the agent does not accidentally violate them:

```markdown
## Architecture
- src/core/ contains business logic with zero external dependencies
- src/adapters/ wraps all third-party services (database, APIs, file system)
- Never import from adapters into core (dependency inversion)
- The event bus in src/events.py is the only way modules communicate
```

### Common Commands

Give the agent the exact commands it needs, so it does not guess:

```markdown
## Commands
- Test: `pytest tests/ -x --tb=short`
- Lint: `ruff check . --fix`
- Type check: `mypy src/ --strict`
- Build: `docker compose build`
```

### Domain Warnings

Flag the things that are easy to get wrong:

```markdown
## Gotchas
- The `users` table has soft deletes; always filter by `deleted_at IS NULL`
- Timezone: all datetimes are stored as UTC; convert on display only
- The legacy API (v1) is read-only; never add write endpoints to it
```

## The /init Command

For new projects, Claude Code provides an `/init` command that automatically generates a starter CLAUDE.md by analyzing the repository. It inspects the directory structure, package files, configuration, and existing documentation to produce an initial draft.

The generated file is a starting point, not a finished product. "A well-maintained CLAUDE.md evolves with your codebase, continuously reducing the friction of working with AI assistance" [src-001]. The initial generation captures the obvious (language, framework, directory layout), but the most valuable content --- architecture rationale, domain gotchas, team conventions --- requires human input.

A practical workflow: run `/init` to get the skeleton, then iterate on it over several sessions, adding the instructions you find yourself repeating.

## Skills and Slash Commands

Beyond static configuration, Claude Code supports **skills** --- packaged workflows that can be invoked as slash commands. "Create custom slash commands to package repeatable workflows your team can share" [src-002].

Skills live as markdown files in a `.claude/commands/` directory:

```
.claude/
  commands/
    commit.md        # /commit - guided commit workflow
    review-pr.md     # /review-pr - PR review checklist
    add-test.md      # /add-test - test generation workflow
```

Each skill file contains instructions that Claude follows when the command is invoked. This is essentially procedure programming for the agent: instead of hoping it remembers how you like commits done, you write the procedure once and invoke it by name.

Skills complement CLAUDE.md nicely. CLAUDE.md provides the persistent context (what the project is, how it works), while skills provide the repeatable procedures (how to do specific tasks). Together they capture both declarative knowledge and procedural knowledge.

### Personal vs. Team Skills

Like CLAUDE.md itself, skills can live at different scopes:
- **Project skills** (`.claude/commands/` in the repo) are shared with the team
- **Personal skills** (`~/.claude/commands/`) apply to all your projects

## Project Memory

Claude Code maintains an auto-memory directory at `~/.claude/projects/<path>/` where it can store persistent learnings across sessions. This is distinct from the CLAUDE.md override in the same directory. While CLAUDE.md contains your explicit instructions, the memory directory contains things the agent has learned through interaction.

For example, after discovering that a particular test suite is flaky, the agent might store a note so it does not re-investigate the same issue in future sessions. This creates a feedback loop: the agent gets better at working in your project over time without requiring you to manually update configuration files.

## Comparison with Alternatives

CLAUDE.md is not the only approach to agent configuration. Other agentic coding tools have their own mechanisms, and comparing them highlights the design tradeoffs.

### Cursor Rules (.cursor/rules/)

Cursor uses a rules directory where each file defines a rule with optional glob-pattern matching for when it applies. Rules can be set to "always apply," "auto-detect," or "agent-requested." This provides more granular conditional activation than CLAUDE.md's directory-based approach, at the cost of a more complex configuration surface.

### GitHub Copilot Instructions (.github/copilot-instructions.md)

GitHub Copilot supports a single instructions file at `.github/copilot-instructions.md`. This is closest to CLAUDE.md's Layer 2 (project root, team-shared), but without the layering. There is no personal override, no monorepo hierarchy, and no skills system. It is simpler but less expressive.

### Windsurf Rules (.windsurfrules)

Windsurf uses a `.windsurfrules` file at the project root, similar in spirit to a single-layer CLAUDE.md. Like Copilot instructions, it lacks the multi-layer composition model.

### Key Differences

| Feature | CLAUDE.md | Cursor Rules | Copilot Instructions | Windsurf Rules |
|---------|-----------|-------------|---------------------|----------------|
| Multi-layer composition | Yes | Partial (glob-based) | No | No |
| Personal overrides | Yes | Yes | No | No |
| Team-shared (in repo) | Yes | Yes | Yes | Yes |
| Monorepo support | Yes (directory walk) | Yes (glob patterns) | No | No |
| Skills/commands | Yes | No | No | No |
| Auto-generation | Yes (/init) | No | No | No |
| Conditional activation | By directory | By glob + mode | Always | Always |

The fundamental distinction is that CLAUDE.md treats agent configuration as a layered, composable system rather than a flat file. This mirrors how software configuration generally works (environment variables override config files, which override defaults) and scales better to complex projects and diverse teams.

## Anti-Patterns

### Overly Long Files

Every line of CLAUDE.md consumes context window tokens. A 500-line CLAUDE.md leaves less room for actual code and conversation. The agent must also parse all of it at the start of every session, even if most of it is irrelevant to the current task. Keep files focused and concise. If you find your CLAUDE.md growing large, consider whether some content belongs in skills, subdirectory files, or project documentation.

### Sensitive Data

CLAUDE.md files (especially the project root one) are checked into version control. Never put API keys, passwords, database connection strings, or other secrets in them. Use environment variable references instead ("The API key is in $ACME_API_KEY") and document where secrets are stored, not what they contain.

### Conflicting Instructions Across Layers

Because all layers merge additively, contradictions between layers create ambiguity. If the project CLAUDE.md says "use tabs" and your personal override says "use spaces," the agent sees both and must choose. Write overrides as explicit amendments that acknowledge and supersede the base instruction, rather than silently contradicting it.

### Stale Configuration

CLAUDE.md should evolve with the codebase. A configuration file that references deleted directories, deprecated tools, or outdated conventions actively misleads the agent. Treat CLAUDE.md updates as part of the same pull requests that change the conventions they describe.

### Duplicating Documentation

CLAUDE.md is not a replacement for project documentation. It should reference docs, not reproduce them. If you find yourself copying architecture diagrams or API specifications into CLAUDE.md, link to them instead and let the agent read the source when it needs details.

## Transparency and Trust

The layered instruction model aligns with broader principles for building effective agents. Anthropic recommends to "prioritize transparency by explicitly showing the agent's planning steps" [src-003]. CLAUDE.md extends this principle to the configuration itself: because the instructions are plain markdown files in known locations, both the developer and the agent can see exactly what context is being loaded. There is no hidden configuration, no opaque fine-tuning, no magic --- just text files that compose in a predictable way.

This transparency also supports debugging. When the agent does something unexpected, you can inspect the loaded CLAUDE.md files to see if a stale instruction, a layer conflict, or a missing convention is the cause. The configuration is auditable in the same way that code is auditable.

## Practical Considerations

### Starting Small

You do not need a comprehensive CLAUDE.md on day one. Start with the commands section (build, test, lint) and one or two architecture notes. Add content as you notice the agent making the same mistakes or asking the same questions.

### Review as Code

Treat CLAUDE.md changes with the same rigor as code changes. Review them in pull requests. When a team member adds a new convention, make sure it does not conflict with existing instructions. Over time, the CLAUDE.md becomes a living style guide that is enforced by the agent rather than by memory alone.

### Measuring Effectiveness

The best signal that your CLAUDE.md is working is a reduction in corrections. If you find yourself repeatedly telling the agent "no, we do it this way," that correction belongs in CLAUDE.md. If you find yourself rarely needing to override the agent's choices, your configuration is doing its job.

## Further Reading

- [Using CLAUDE.MD Files](https://claude.com/blog/using-claude-md-files) - Detailed guide on crafting effective CLAUDE.md files [src-001]
- [Claude Code Documentation](https://code.claude.com/docs) - Official reference for Claude Code features [src-002]
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) - Anthropic's principles for agent design [src-003]
- [Claude Code Architecture](claude-code-architecture.md) - How Claude Code works as an agentic system
- [Context Window Management](context-window-management.md) - Managing the token budget that CLAUDE.md consumes
- [Human-in-the-Loop Patterns](../agents/human-in-the-loop.md) - How agent configuration relates to oversight
