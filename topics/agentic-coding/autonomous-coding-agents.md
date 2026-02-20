---
id: kb-2025-017
title: "The Landscape of Autonomous Coding Agents"
created: 2026-02-19
updated: 2026-02-19

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?"
    authors: ["Jimenez et al."]
    url: "https://arxiv.org/abs/2310.06770"
    accessed: 2026-02-19
    published: 2023-10-10
    arxiv: "2310.06770"
    quotes:
      - text: "SWE-bench is a benchmark that tests systems' ability to solve GitHub issues drawn from real Python repositories."
        location: "Abstract"
  - id: src-002
    type: primary
    title: "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering"
    authors: ["Yang et al."]
    url: "https://arxiv.org/abs/2405.15793"
    accessed: 2026-02-19
    published: 2024-05-06
    arxiv: "2405.15793"
    quotes:
      - text: "We introduce SWE-agent, which sets the state-of-the-art on the full SWE-bench test set, with a 12.47% resolve rate."
        location: "Abstract"
  - id: src-003
    type: primary
    title: "Claude Code Documentation"
    url: "https://code.claude.com/docs"
    accessed: 2026-02-19
    quotes:
      - text: "Claude Code is an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools."
        location: "Overview"
  - id: src-004
    type: primary
    title: "Building Effective Agents"
    authors: ["Anthropic"]
    url: "https://www.anthropic.com/engineering/building-effective-agents"
    accessed: 2026-02-19
    quotes:
      - text: "Agents are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."
        location: "What are agents?"

topics:
  - coding-agents
  - agentic-coding
  - agents
  - tool-use

confidence: medium
verified: false
verified_by: unverified
verification_notes: "AI-assisted draft; product details evolve rapidly and may be outdated by the time of review"

ai_metadata:
  model: claude-opus-4-6
  generation_date: 2026-02-19
  reviewed_by: pending
---

# The Landscape of Autonomous Coding Agents

## Overview

As of early 2026, the market for AI-powered coding tools has exploded into a crowded, fast-moving space. What began with autocomplete suggestions (GitHub Copilot, 2021) has evolved into a new category: autonomous coding agents that can read entire codebases, plan multi-file changes, execute shell commands, run tests, and iterate on failures. "Agents are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks" [src-004], and that definition now describes a growing number of developer-facing products.

This article surveys the major autonomous coding agents, examines how they differ along key dimensions (autonomy, context management, tool access, permission models), discusses the SWE-bench benchmark ecosystem that has emerged to evaluate them, and identifies the convergence trends shaping this space.

For the underlying agent architectures these tools build on, see [LLM Agent Architectures and Patterns](../agents/agent-architectures.md). For the workflow patterns they enable, see [Agentic Coding Patterns](agentic-coding-patterns.md).

## A Taxonomy of Coding Agents

Not all coding agents are built the same way. They differ in where they run, how much autonomy they assume, and how they integrate into a developer's existing workflow. A useful taxonomy organizes them by their primary interface:

**IDE-integrated agents** live inside a code editor (VS Code, JetBrains, etc.) and blend autocomplete, chat, and agentic features into the editing experience. Examples: Cursor, Windsurf, GitHub Copilot.

**Terminal-based agents** operate in the command line alongside the developer's existing tools. They treat the shell as the primary interface and the file system as the workspace. Example: Claude Code.

**Cloud-based agents** run on remote infrastructure, often with their own browser-based IDE, and can work autonomously for extended periods without the developer present. Examples: Devin, GitHub Copilot Workspace, Claude Code (web/headless mode).

These categories are not rigid -- most tools are expanding across boundaries. Claude Code, for instance, started as a terminal tool but now runs in VS Code and as a headless cloud agent. Cursor started as an IDE but added terminal-like agentic capabilities. The convergence is real, but the starting point shapes the design philosophy.

## Claude Code

### Architecture and Philosophy

Claude Code is "an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools" [src-003]. It is built on a single-loop ReAct architecture: one model (Claude) in one loop, with a small set of general-purpose tools (Read, Write, Edit, Bash, Grep, Glob, and others). For a deep dive into its architecture, see [Claude Code Architecture](claude-code-architecture.md).

The design philosophy follows Anthropic's own guidance that agent architectures should stay simple [src-004]. Rather than a multi-agent system with specialized planner, coder, and reviewer components, Claude Code trusts a single capable model to handle the full cycle: understand the task, explore the codebase, make changes, verify the results.

### Key Features

**Terminal-first interface**: Claude Code runs in the terminal, which means it works wherever the developer works. It has access to the same file system, the same shell, and the same tools the developer uses. There is no separate sandbox or remote environment -- the agent operates directly on the local codebase.

**CLAUDE.md configuration**: Developers configure Claude Code's behavior through CLAUDE.md files -- plain Markdown documents that describe project conventions, coding standards, and workflow rules. These files are loaded into the model's context at the start of every session, providing persistent instruction without a specialized configuration format. See [CLAUDE.md and Agent Configuration](claude-md-agent-configuration.md) for details.

**Tiered permission model**: Claude Code enforces a safety model where read-only operations (searching, reading files) proceed automatically, file modifications may require confirmation, and shell commands can be gated behind approval. This lets developers calibrate the level of autonomy to their comfort and the risk of the task.

**Sub-agents**: For complex tasks, Claude Code can spawn sub-agents -- separate Claude instances that handle sub-tasks with their own context windows. This provides a form of parallelism and context isolation within the single-loop architecture.

**Hooks**: Programmatic extension points (pre-tool and post-tool scripts) allow developers to inject custom validation, logging, or transformation at each step of the agentic loop.

**MCP integration**: Through the Model Context Protocol, Claude Code can connect to external tool servers, giving it access to databases, project management systems, internal documentation, and any other service exposed through MCP. See [Model Context Protocol](../protocols/model-context-protocol.md).

### Strengths and Tradeoffs

Claude Code's strength is transparency and composability. The developer can watch every step, intervene at any point, and extend the tool through familiar mechanisms (shell scripts, MCP servers, Markdown configuration). The single-loop design is easy to reason about.

The tradeoff is that terminal-first can feel lower-level than an IDE-integrated experience. There is no inline diff preview, no visual file tree, no built-in GUI for reviewing changes (though IDE extensions address some of this). The tool also inherits the strengths and limitations of its underlying model -- the quality of Claude Code is fundamentally the quality of Claude applied to coding tasks.

## Cursor

### IDE-First Approach

Cursor is a fork of VS Code that reimagines the editor around AI assistance. Rather than adding AI as a sidebar or plugin, Cursor makes AI interaction a first-class part of the editing experience. The core insight is that developers spend most of their time in an IDE, and the AI should meet them there.

### Key Features

**Tab completion**: Cursor's autocomplete goes beyond single-line suggestions. It can predict multi-line edits, function completions, and even cross-file changes based on the current editing context. The model anticipates what the developer is about to type based on recent edits and surrounding code.

**Composer mode**: Cursor's agentic mode, where the model can plan and execute multi-file changes. The developer describes a task in natural language, and Cursor generates a plan, makes edits across files, and presents a diff for review. This is the closest analog to Claude Code's agentic loop, but rendered within the IDE's diff viewer.

**Cursor Rules**: Analogous to CLAUDE.md, Cursor Rules (stored in `.cursor/rules/`) let developers specify project conventions, coding patterns, and behavioral guidelines. These rules shape the model's output across all interactions.

**Context awareness**: Cursor indexes the codebase to provide relevant context to the model. It uses a combination of embeddings and heuristic retrieval to identify which files and symbols are relevant to the current task, managing the context window more aggressively than a terminal-based tool that relies on explicit file reads.

### Strengths and Tradeoffs

Cursor excels at the tight edit-review loop. Because it operates inside the editor, changes are presented as familiar diffs, and the developer can accept, reject, or modify individual hunks. The visual feedback is immediate and rich.

The tradeoff is coupling to the IDE. Cursor's agentic features are tied to VS Code's UI paradigm. Tasks that are more naturally expressed in the terminal (running test suites, managing git workflows, interacting with infrastructure) require switching contexts. Cursor also uses its own proprietary model routing, which means the developer has less control over which model handles which task compared to tools that let you choose directly.

## GitHub Copilot

### From Autocomplete to Agent

GitHub Copilot launched in 2021 as the first widely-adopted AI coding assistant, focused on inline autocomplete powered by OpenAI's Codex model. It changed what developers expected from their editor: suddenly, the AI could write boilerplate, suggest function implementations, and generate test cases as you typed.

### Evolution

Copilot has evolved through several phases:

**Copilot (original)**: Single-line and multi-line autocomplete. Fast, unobtrusive, and surprisingly useful for routine code. Still the most-used feature.

**Copilot Chat**: A conversational interface within the IDE for asking questions, explaining code, and requesting changes. More interactive but not agentic -- the model suggests code but does not execute changes.

**Copilot Workspace**: GitHub's entry into the agentic space. Copilot Workspace takes a GitHub issue as input and generates a multi-step plan: identify relevant files, propose changes, create a pull request. It operates in a cloud environment and can handle the full cycle from issue to PR.

**Copilot Coding Agent**: The latest evolution, where Copilot can be assigned issues directly and work on them autonomously in a cloud sandbox, similar to Devin's model. This represents GitHub's shift from augmenting developers to automating some development tasks entirely.

### Strengths and Tradeoffs

Copilot's advantage is distribution and integration. It is embedded in GitHub, the platform where most open-source and much enterprise development already happens. The path from issue to PR to merge is seamless when the tool lives in the same ecosystem.

The tradeoff is that Copilot's agentic features are newer and less mature than its autocomplete. The cloud-based agent workflow is a different paradigm from the inline suggestions that made Copilot popular, and it is still finding its footing. Copilot also operates within GitHub's infrastructure, which means less flexibility for developers who want to run against local environments or use custom toolchains.

## Devin

### The Fully Autonomous Vision

Devin, created by Cognition Labs, was announced in early 2024 as "the first AI software engineer." It is a cloud-based agent that operates in a full virtual environment -- a browser, a terminal, a code editor -- and can work on tasks for extended periods without human intervention.

### Architecture

Devin runs in a sandboxed cloud environment with its own VS Code instance, terminal, and web browser. The agent can:

- Read and write code across a full repository
- Browse the web to look up documentation or Stack Overflow answers
- Run tests, build projects, and debug failures
- Create pull requests and deploy changes

The key architectural difference from tools like Claude Code or Cursor is the level of isolation and autonomy. Devin is designed to be handed a task and left to work on it, reporting back when finished. The developer interacts with Devin asynchronously rather than watching each step in real time.

### Controversy and Reality

Devin's launch was accompanied by bold claims about its capabilities, including cherry-picked benchmark results that generated significant skepticism in the developer community. Independent evaluations showed performance well below the marketing claims, and the "first AI software engineer" framing struck many as premature.

That said, the product has matured since launch. The core idea -- a cloud-based autonomous agent that can handle well-specified tasks end-to-end -- has proven viable for certain categories of work (dependency upgrades, boilerplate generation, well-scoped bug fixes). The gap between the vision and the reality has narrowed, even if the marketing got ahead of the technology.

### Strengths and Tradeoffs

Devin's strength is autonomy. For tasks that do not require real-time human judgment, offloading work to an agent that runs in the background is genuinely productive. The cloud environment also means the agent cannot accidentally damage the developer's local setup.

The tradeoffs are significant: latency (the agent may take 20-60 minutes for tasks a human could scope in 5), cost (cloud compute for each session), lack of transparency (the developer cannot easily observe the agent's reasoning in real time), and the fundamental challenge that most real development work requires judgment calls that benefit from human involvement.

## Windsurf (Codeium)

### Cascade and Flow-Based Editing

Windsurf, built by Codeium, is another IDE-based coding agent. Its signature feature is "Cascade" -- a flow-based editing system where the AI maintains awareness of the developer's recent actions and proactively suggests next steps. The idea is that coding is a flow, and the AI should anticipate the natural continuation rather than waiting for explicit instructions.

### Key Features

**Cascade flows**: Windsurf tracks the developer's editing context -- which files have been opened, what changes have been made, what the developer seems to be working on -- and uses this context to generate increasingly relevant suggestions. The model is not just responding to the current cursor position but to the trajectory of recent work.

**Deep context awareness**: Windsurf indexes the full repository and maintains a semantic understanding of the codebase. When the developer is editing a function, Windsurf knows about the callers of that function, the tests that cover it, and the related types and interfaces.

**Multi-file agentic mode**: Like Cursor's Composer, Windsurf can operate in an agentic mode where it plans and executes changes across multiple files. The developer describes the intent, and Windsurf generates a coordinated set of edits.

### Strengths and Tradeoffs

Windsurf's strength is the flow concept -- the idea that the AI should be proactive rather than purely reactive. When it works well, it feels like pair programming with someone who is already up to speed on what you are doing.

The tradeoff is that proactive suggestions can be distracting when they miss the mark. Context awareness is powerful when accurate but annoying when it guesses wrong about what the developer is trying to do. The balance between helpful anticipation and unwanted interruption is a UX challenge that all proactive AI tools face.

## SWE-Bench: Evaluating Coding Agents

### What It Measures

"SWE-bench is a benchmark that tests systems' ability to solve GitHub issues drawn from real Python repositories" [src-001]. Unlike coding benchmarks that test isolated function generation (like HumanEval or MBPP), SWE-bench evaluates whether an agent can resolve real-world issues in real codebases. Each task is a GitHub issue from a popular open-source Python project (Django, scikit-learn, sympy, etc.) paired with a test patch that verifies the fix.

This makes SWE-bench a meaningful signal about practical coding ability. The tasks require the agent to:

1. Understand the issue description (often ambiguous or underspecified)
2. Navigate a large, unfamiliar codebase
3. Identify the relevant files and functions
4. Make correct changes (sometimes across multiple files)
5. Produce a patch that passes the test suite

### SWE-bench Variants

The original SWE-bench contains 2,294 tasks, but evaluating against the full set is expensive. Several variants have emerged:

**SWE-bench Lite**: A curated subset of 300 tasks, designed to be more tractable while remaining representative. Most published results report on this subset.

**SWE-bench Verified**: A human-verified subset where annotators have confirmed that the task descriptions are clear and the test patches are correct. This addresses concerns about noisy or ambiguous tasks in the original set.

### State of the Art

When SWE-agent was introduced, it "sets the state-of-the-art on the full SWE-bench test set, with a 12.47% resolve rate" [src-002]. That number has since been surpassed dramatically. As of early 2026, top systems resolve over 50% of SWE-bench Verified tasks, with the best results coming from agentic systems built on frontier models like Claude 3.5 Sonnet, GPT-4o, and their successors.

The rapid improvement curve tells a story: the bottleneck for coding agents is increasingly the agent scaffolding (context management, tool design, error recovery) rather than the raw capability of the underlying model. Better models help, but better agent architectures help at least as much.

### Limitations of SWE-Bench

SWE-bench has limitations that are important to understand:

**Python only**: All tasks are from Python repositories. Performance on Python issues may not transfer to other languages, especially languages with different tooling ecosystems.

**Issue resolution only**: SWE-bench tests bug fixing and feature implementation from an issue description. It does not test code review, architecture design, documentation writing, or the many other tasks developers do.

**Test-based evaluation**: Success is defined as passing the test patch. A solution that passes the tests but introduces technical debt, poor naming, or subtle bugs is scored the same as an elegant fix. Code quality is not measured.

**Limited scope per task**: Most SWE-bench tasks involve changes to a handful of files. Real development often involves larger-scale coordination that the benchmark does not capture.

**Benchmark gaming**: As SWE-bench has become the primary leaderboard for coding agents, there is pressure to optimize for it. Some techniques that boost SWE-bench scores (like ensembling multiple attempts and picking the best one) do not represent realistic development workflows.

Despite these limitations, SWE-bench remains the most credible benchmark for coding agents because it uses real code, real issues, and real tests. It is imperfect but meaningfully grounded.

## SWE-agent and the ACI Concept

### Agent-Computer Interface

SWE-agent introduced a concept that has influenced the entire field: the **Agent-Computer Interface (ACI)** [src-002]. Just as UI design shapes human productivity with software, the interface between an agent and its computing environment shapes agent productivity.

SWE-agent's key insight is that existing command-line tools were designed for humans, not for LLMs. An LLM parsing the output of `git diff` or `find . -name "*.py"` is working with an interface optimized for human eyes. SWE-agent created custom commands designed specifically for how LLMs process text:

**Custom file navigation**: Instead of `cat` or `less`, SWE-agent provides a `open` command that shows a window of the file with line numbers, and `scroll_up`/`scroll_down` commands to navigate. This gives the model a consistent, bounded view of file contents.

**Targeted editing**: Instead of full-file rewrites, SWE-agent provides an `edit` command that takes a line range and replacement text. This reduces the risk of the model corrupting parts of the file it was not intending to change.

**Search tools**: Custom `search_file` and `search_dir` commands that return results in a format optimized for LLM consumption -- with context lines, file paths, and clear delimiters.

### Influence on the Field

The ACI concept has been adopted, explicitly or implicitly, by most coding agents that followed. Claude Code's tool set (Read with line ranges, Edit with exact string matching, Grep with structured output) reflects the same principle: give the model tools that are designed for how it works, not for how a human would use the terminal.

Anthropic's guidance to "carefully craft your agent-computer interface (ACI) through thorough tool documentation and testing" [src-004] echoes this directly. The quality of the tools -- their documentation, their error messages, their output format -- is a first-order determinant of agent performance.

## Key Differentiators Across the Landscape

### Autonomy Level

The coding agents differ significantly in how much autonomy they assume:

| Tool | Default Autonomy | Maximum Autonomy |
|------|------------------|------------------|
| GitHub Copilot (autocomplete) | Suggestions only | Suggestions only |
| Cursor | Edit-on-approval | Agentic with Composer |
| Windsurf | Proactive suggestions | Agentic with Cascade |
| Claude Code | Confirm on write | Full autonomy (YOLO mode) |
| Devin | High autonomy | Fully autonomous |
| Copilot Coding Agent | High autonomy | Fully autonomous |

The spectrum runs from purely assistive (Copilot autocomplete) to fully autonomous (Devin). Most developers find a sweet spot in the middle: enough autonomy to avoid confirming every file read, but enough oversight to catch mistakes before they propagate. See [Human-in-the-Loop Patterns](../agents/human-in-the-loop.md) for a deeper discussion of this tradeoff.

### Context Management

How each tool handles codebase context is a critical differentiator:

**Explicit context (Claude Code)**: The developer (or the agent itself) explicitly reads files and searches the codebase. The model's context contains exactly what has been fetched. This is transparent but requires the model to know what to look for.

**Indexed context (Cursor, Windsurf)**: The tool pre-indexes the codebase using embeddings or syntax analysis and automatically retrieves relevant context. This can surface information the model would not have known to search for, but the retrieval may be noisy or miss relevant files.

**Full environment (Devin)**: The agent has access to the entire repository and can navigate it freely, but within a cloud sandbox. Context management is the agent's responsibility, similar to Claude Code but in an isolated environment.

### Tool Access

The scope of what each agent can do varies:

- **Copilot autocomplete**: Read-only access to the current file and open files
- **Cursor/Windsurf**: File read/write, terminal commands (within the IDE)
- **Claude Code**: Full file system access, arbitrary shell commands, MCP extensions, web access
- **Devin**: Full virtual environment including a web browser, terminal, and editor

Broader tool access enables more autonomy but increases the risk surface. Claude Code's permission model and hooks are a response to this tension -- give the agent broad capabilities but let the developer control when and how they are used.

### Permission Models

Only some coding agents have explicit permission models:

- **Claude Code**: Tiered permissions (read-only auto, write confirm, bash confirm) with configurable autonomy levels and hooks for fine-grained control
- **Cursor**: Accept/reject diffs in the IDE, with settings for auto-apply
- **Devin**: Operates in a sandbox, so permissions are implicit (it cannot affect local files)
- **Copilot Workspace**: Generates PRs that require human review before merge

The permission model is particularly important as agents gain more capability. An agent that can run arbitrary shell commands needs stronger guardrails than one that can only suggest code edits.

## Convergence Trends

### Everyone Is Becoming Agentic

The most striking trend in early 2026 is convergence. Tools that started as autocomplete are adding agentic capabilities. Tools that started as terminal agents are adding IDE integrations. Tools that started in the cloud are adding local modes. The end state appears to be that every coding tool will offer the full spectrum: autocomplete, chat, agentic editing, and autonomous task execution.

This convergence is driven by user expectations. Developers who have experienced agentic coding do not want to go back to pure autocomplete. But they also do not want to give up the speed and low-friction of inline suggestions. The winning tools will offer both, with smooth transitions between modes.

### The Model Matters Less (and More)

Paradoxically, the underlying model is both less and more important than it was a year ago. Less important because the scaffolding -- context management, tool design, permission models, IDE integration -- has become a major differentiator. A well-designed agent with a good model can outperform a poorly designed agent with a great model.

More important because as scaffolding converges, the model becomes the differentiator again. If every tool offers similar IDE integration and tool sets, the quality of reasoning, code generation, and instruction following determines which tool produces better results. This is why the model providers (Anthropic, OpenAI, Google) are increasingly building their own coding agents rather than relying solely on third-party wrappers.

### From Tool to Teammate

The framing is shifting from "AI tool" to "AI teammate." Early coding assistants were clearly tools: they suggested, you decided. The current generation occupies an ambiguous space -- capable enough to handle significant tasks independently, but not reliable enough to be trusted without oversight.

This shift has implications for how developers work. The skills that matter are changing: specifying tasks clearly, reviewing AI-generated code effectively, and knowing when to intervene become more important than typing speed or memorizing API surfaces. The best developers are not those who can write code fastest but those who can direct an AI agent most effectively.

## Practical Considerations

### Choosing a Coding Agent

The right tool depends on the developer's workflow and priorities:

**Choose an IDE-integrated agent (Cursor, Windsurf)** if you want the tightest possible edit-review loop, prefer visual diffs, and work primarily within a single editor. These tools minimize context switching.

**Choose a terminal-based agent (Claude Code)** if you value transparency, composability, and control. Terminal agents work well for developers who are comfortable with the command line and want to integrate AI into their existing tool chain rather than replacing it.

**Choose a cloud-based agent (Devin, Copilot Coding Agent)** if you have well-specified, self-contained tasks that can be delegated without real-time oversight. These tools are best for "background work" -- tasks you would hand to a junior developer and check on later.

**Use multiple tools** if different tasks call for different approaches. Many developers use autocomplete for routine coding, an agentic tool for multi-file changes, and a cloud agent for repetitive tasks like dependency upgrades.

### What Benchmarks Do and Do Not Tell You

SWE-bench scores are a useful signal but not the whole picture. A tool that resolves 55% of SWE-bench Verified tasks may not be the best choice for your workflow if its context management is poor, its permission model is too permissive, or its IDE integration is clunky.

When evaluating coding agents, consider:
- **Task fit**: Does the tool handle your typical tasks well? (Not all development is bug fixing.)
- **Integration**: Does it fit into your existing workflow or require you to change it?
- **Transparency**: Can you understand what the agent is doing and why?
- **Safety**: What happens when the agent makes a mistake? How quickly can you catch and correct it?
- **Cost**: Both monetary (API calls, subscriptions) and cognitive (context switching, review overhead)

### The Human Remains Essential

Even the most capable coding agents benefit from human direction. Clear task descriptions, good CLAUDE.md files (or Cursor Rules), and well-structured codebases all improve agent performance. The developer's role is shifting, but it is not disappearing.

The most effective pattern, as of early 2026, is collaborative: the human handles architecture, design decisions, and quality judgment while the agent handles exploration, implementation, and iteration. This is not a temporary compromise -- it reflects the genuine comparative advantages of humans (judgment, taste, domain knowledge) and AI (speed, breadth, tirelessness).

## Further Reading

- [SWE-bench Paper](https://arxiv.org/abs/2310.06770) - The benchmark that defined coding agent evaluation [src-001]
- [SWE-agent Paper](https://arxiv.org/abs/2405.15793) - The ACI concept and agent-computer interface design [src-002]
- [Claude Code Documentation](https://code.claude.com/docs) - Official reference for Claude Code [src-003]
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) - Anthropic's agent design philosophy [src-004]
- [Claude Code Architecture](claude-code-architecture.md) - Deep dive into Claude Code's agentic loop and tool system
- [Agentic Coding Patterns](agentic-coding-patterns.md) - Workflow patterns for AI-assisted development
- [LLM Agent Architectures and Patterns](../agents/agent-architectures.md) - The theoretical foundations of agent design
- [Human-in-the-Loop Patterns](../agents/human-in-the-loop.md) - Balancing autonomy and oversight
