---
id: kb-2025-014
title: "Agentic Coding Patterns and AI-Assisted Development Workflows"
created: 2026-02-19
updated: 2026-02-19

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "Building Effective Agents"
    authors: ["Anthropic"]
    url: "https://www.anthropic.com/engineering/building-effective-agents"
    accessed: 2026-02-19
    quotes:
      - text: "Workflows are systems where LLMs and tools are orchestrated through predefined code paths."
        location: "What are agents?"
      - text: "Agents are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."
        location: "What are agents?"
      - text: "Agentic systems often trade latency and cost for better task performance, and you should consider when this tradeoff makes sense."
        location: "When (and when not) to use agents"
      - text: "Carefully craft your agent-computer interface (ACI) through thorough tool documentation and testing."
        location: "Summary"

  - id: src-002
    type: primary
    title: "Claude Code Documentation"
    url: "https://code.claude.com/docs"
    accessed: 2026-02-19
    quotes:
      - text: "Describe what you want in plain language. Claude Code plans the approach, writes the code across multiple files, and verifies it works."
        location: "Build features and fix bugs"

  - id: src-003
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

topics:
  - agentic-coding
  - coding-agents
  - agents
  - prompt-engineering

confidence: high
verified: false
verified_by: unverified
verification_notes: "AI-assisted draft; quotes sourced from official docs and papers but need human verification against originals"

ai_metadata:
  model: claude-opus-4-6
  generation_date: 2026-02-19
  reviewed_by: pending
---

# Agentic Coding Patterns and AI-Assisted Development Workflows

## Overview

Agentic coding refers to software development workflows where an AI model operates with significant autonomy -- reading codebases, planning changes, writing code across multiple files, running tests, and iterating on failures. This is a step change from earlier AI coding tools that offered autocomplete suggestions or answered questions in a chat window. In an agentic workflow, the model drives the process: it decides which files to read, what changes to make, and how to verify its work.

The distinction matters because it shifts the developer's role from writing code to directing an agent. Instead of typing out a function, you describe the behavior you want. "Describe what you want in plain language. Claude Code plans the approach, writes the code across multiple files, and verifies it works" [src-002]. The developer becomes a reviewer, architect, and decision-maker rather than a typist.

This article covers the spectrum of AI coding assistance, the workflow patterns that make agentic coding effective, and the practical tradeoffs involved.

## The Spectrum of AI Coding Assistance

AI-assisted development is not a single thing. It spans a wide range, from passive suggestions to fully autonomous operation. Understanding where different tools fall on this spectrum helps you choose the right approach for a given task.

### Level 1: Autocomplete

The simplest form of AI coding assistance. The model predicts the next few tokens as you type and offers inline completions. Examples include GitHub Copilot's inline suggestions and similar editor plugins.

**Strengths**: Low latency, minimal disruption to flow, works well for boilerplate and repetitive patterns.

**Limitations**: No understanding of intent beyond the immediate cursor position. Cannot reason about the broader codebase or project structure.

### Level 2: Chat-Based Assistance

The developer asks questions or pastes code into a chat interface and receives explanations, suggestions, or code snippets. The model responds to explicit prompts but takes no actions on its own.

**Strengths**: Good for learning, debugging, and exploring approaches. The developer maintains full control.

**Limitations**: The developer must manually copy code, switch between chat and editor, and decide what context to provide. The model sees only what you show it.

### Level 3: Agentic Workflows

This is where the model begins to take actions. In Anthropic's terminology, "workflows are systems where LLMs and tools are orchestrated through predefined code paths" [src-001]. The model can read files, search codebases, write changes, and execute commands, but it follows a structured process with human checkpoints.

**Strengths**: Can handle multi-file changes, understands project context, iterates on its own work.

**Limitations**: Still requires human oversight at key decision points. Performance depends heavily on prompt quality and tool design.

### Level 4: Autonomous Agents

At the far end of the spectrum, "agents are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks" [src-001]. The model decides not just what to do, but how to do it and when to stop.

**Strengths**: Can handle complex, multi-step tasks with minimal human intervention.

**Limitations**: Harder to predict behavior, more expensive (each decision is an LLM call), and riskier when the agent makes wrong assumptions early.

Most practical coding tools today operate at Level 3, with elements of Level 4 for well-defined tasks. The sweet spot is giving the model enough autonomy to be productive while keeping the developer in the loop for decisions that matter.

## Workflow Patterns from Anthropic

Anthropic's "Building Effective Agents" guide identifies several patterns for orchestrating LLMs with tools [src-001]. These patterns apply broadly to agent design, but they are particularly relevant to coding agents because software development naturally involves multi-step reasoning, tool use, and iterative refinement.

### Prompt Chaining

Break a task into sequential steps, where each step's output feeds into the next. In a coding context, this might look like:

1. Analyze the issue description and identify affected files
2. Read those files and understand the current implementation
3. Generate a plan for the changes
4. Implement the changes
5. Write or update tests

Each step is a separate LLM call with focused instructions. The advantage is that each call is simpler and more reliable than trying to do everything at once. The disadvantage is rigidity -- if step 2 reveals that the wrong files were identified in step 1, the chain must restart.

### Routing

Direct different types of requests to different handling paths. A coding agent might route a request to fix a typo through a simple edit path, while routing a request to add a new feature through a more elaborate planning path.

Routing reduces cost and latency for simple tasks while preserving thoroughness for complex ones. The router itself can be an LLM call that classifies the request, or a simpler heuristic based on keywords or patterns.

### Parallelization

Run independent subtasks concurrently. For example, when investigating a bug, the agent might simultaneously read the failing test, search for related issues, and check recent commits to the affected file. The results are gathered and synthesized in a subsequent step.

This is especially valuable in coding workflows because codebases are large and reading files is I/O-bound. Parallel file reads and searches significantly reduce the time to gather context.

### Orchestrator-Workers

A central orchestrator LLM breaks a task into subtasks and delegates them to specialized worker LLMs. Each worker handles one piece -- perhaps one worker writes the implementation while another writes the tests, or different workers handle different files.

This pattern scales to large changes but introduces coordination overhead. The orchestrator must clearly define each worker's scope and then integrate their outputs coherently.

### Evaluator-Optimizer

One LLM generates a solution, and another evaluates it. The generator revises based on the evaluation. This continues until the evaluator is satisfied or a maximum number of iterations is reached.

In coding, the "evaluator" is often not a second LLM but the test suite itself. The agent writes code, runs tests, reads the failures, and revises. This tight feedback loop is one of the most powerful patterns in agentic coding.

### Autonomous Agents

The most open-ended pattern: the model has a goal and a set of tools, and it decides its own approach at each step. There is no predefined sequence. The model reasons about what to do next based on what it has observed so far.

This is the pattern used by tools like Claude Code for complex tasks. The agent might start by exploring the codebase, form a hypothesis, try an implementation, discover it does not work, backtrack, and try a different approach -- all without human intervention between steps.

## The Plan-Then-Execute Pattern

One of the most effective patterns in agentic coding is explicit planning before implementation. Rather than jumping straight to writing code, the agent first produces a structured plan that the developer can review and approve.

### How It Works

1. **Understand**: The agent reads relevant files, searches for patterns, and builds a mental model of the codebase
2. **Plan**: The agent produces a concrete plan: which files to modify, what changes to make, what tests to add
3. **Review**: The developer reviews the plan and provides feedback or approval
4. **Execute**: The agent implements the plan, making the specified changes
5. **Verify**: The agent runs tests and checks that the implementation matches the plan

### Why It Matters

Planning serves several functions:

- **Alignment check**: The developer can catch misunderstandings before code is written
- **Scope control**: The plan makes the extent of changes visible before they happen
- **Reduced waste**: Revising a plan is cheaper than revising an implementation
- **Transparency**: The developer understands what the agent intends to do and why

The plan-then-execute pattern is not unique to AI coding -- human developers do the same thing when they discuss an approach before writing code. The difference is that an AI agent can produce detailed, file-level plans much faster than a human, making the planning step nearly free relative to the implementation.

## Iterative Refinement: The Write-Test-Fix Cycle

Perhaps the most practically important pattern in agentic coding is the ability to iterate: write code, run tests, read failures, and fix issues. This mimics the human development cycle but runs much faster.

### The Core Loop

```
while tests_failing:
    analyze_failures()
    identify_root_cause()
    apply_fix()
    run_tests()
```

The agent treats test output as structured feedback. A failing test is not a dead end -- it is information about what needs to change. The agent reads the error message, traces it back to the code, and makes a targeted fix.

### What Makes This Work

- **Concrete feedback**: Test failures provide specific, actionable signals (line numbers, assertion failures, stack traces)
- **Bounded scope**: Each iteration focuses on the current failure, preventing drift
- **Convergence**: Each successful fix reduces the remaining failures, creating visible progress
- **Self-verification**: The tests serve as an objective measure of correctness, not just the model's opinion

### Where It Breaks Down

- **Flaky tests**: If tests pass or fail nondeterministically, the agent chases ghosts
- **Missing tests**: If there are no tests for the changed behavior, the agent has no feedback signal
- **Deep bugs**: Some failures require understanding that spans the entire system, not just the immediate error message
- **Oscillation**: The agent may fix one test and break another, entering a cycle without converging

## The Agent-Computer Interface (ACI)

Anthropic emphasizes a concept they call the Agent-Computer Interface: "Carefully craft your agent-computer interface (ACI) through thorough tool documentation and testing" [src-001]. This is the idea that the tools an agent uses need to be designed with the same care as user-facing APIs.

### Why ACI Matters

When a human developer uses a command-line tool, they can read the man page, try different flags, and use their judgment about unexpected output. An LLM agent relies entirely on the tool's description and schema to decide how to use it. If the tool documentation is vague, the agent will misuse the tool. If error messages are unhelpful, the agent cannot recover.

Good ACI design means:

- **Clear tool descriptions**: Explain what the tool does, when to use it, and what the output means
- **Well-defined parameters**: Use descriptive names and include constraints in the schema
- **Informative output**: Return structured results that the model can parse and reason about
- **Predictable behavior**: The same inputs should produce the same outputs
- **Graceful errors**: When something goes wrong, explain what happened and suggest alternatives

### ACI vs. API vs. UI

| Aspect | UI (Human) | API (Developer) | ACI (Agent) |
|--------|-----------|-----------------|-------------|
| Consumer | Human user | Human developer | LLM model |
| Discovery | Visual exploration | Documentation | Tool descriptions in prompt |
| Error handling | Visual feedback | Error codes + messages | Structured errors the model can parse |
| Tolerance for ambiguity | High | Medium | Low |
| Cost of misuse | Low (undo) | Medium (debugging) | High (wasted tokens, cascading errors) |

The key insight is that agents are less tolerant of ambiguity than humans. A human developer can figure out that `-v` means "verbose" from context. An agent needs the description to say so explicitly.

## Benchmarking Coding Agents

### SWE-Bench

"SWE-bench is a benchmark that tests systems' ability to solve GitHub issues drawn from real Python repositories" [src-003]. It has become the standard evaluation for coding agents because it uses real-world tasks with real codebases, not synthetic toy problems.

Each SWE-Bench task provides:
- A GitHub issue description
- The repository at the relevant commit
- A test patch that validates the correct fix

The agent must read the issue, understand the codebase, produce a patch, and pass the tests. This evaluates the full pipeline: understanding natural language requirements, navigating code, reasoning about the fix, and implementing it correctly.

### Why Benchmarks Matter

Benchmarks like SWE-Bench provide an objective way to compare different agent architectures, prompting strategies, and tool designs. Without them, claims about agent performance are anecdotal. With them, we can measure whether a new approach actually improves the ability to solve real problems.

### Limitations of Current Benchmarks

- **Task distribution**: SWE-Bench draws from popular Python repositories, which may not represent the diversity of real-world development
- **Isolated tasks**: Each task is independent, while real development involves ongoing context and accumulated knowledge
- **Binary evaluation**: A patch either passes the tests or it doesn't, with no credit for partial solutions
- **Missing dimensions**: Code quality, maintainability, and documentation are not evaluated

## When Agents Help vs. When They Hurt

"Agentic systems often trade latency and cost for better task performance, and you should consider when this tradeoff makes sense" [src-001]. Not every coding task benefits from an agentic approach.

### Agents Excel At

- **Well-scoped tasks**: Fix this bug, add this field, refactor this function. Clear inputs, clear outputs.
- **Multi-file changes**: Adding a new API endpoint that touches routes, handlers, models, tests, and documentation.
- **Boilerplate-heavy work**: Generating CRUD operations, writing test scaffolding, adding error handling.
- **Code exploration**: Understanding an unfamiliar codebase by systematically reading and summarizing files.
- **Iterative debugging**: When a failing test provides clear signal, agents can converge on a fix faster than manual debugging.

### Agents Struggle With

- **Ambiguous requirements**: "Make the UX better" gives the agent no actionable direction.
- **Novel architecture decisions**: Choosing between a microservices vs. monolith approach requires judgment that agents lack.
- **Cross-system reasoning**: Changes that depend on understanding deployment infrastructure, runtime behavior, or production data patterns.
- **Taste and style**: Code that is correct but poorly structured, or that violates unstated project conventions.
- **Long-running sessions**: As context accumulates, agents lose track of earlier decisions and may contradict themselves.

### The Right Granularity

The most productive use of agentic coding is at the task level: one issue, one feature, one bug fix. Trying to use an agent for an entire project or an open-ended refactor usually fails because the scope is too large and the feedback signals are too sparse.

## Practical Considerations

### Cost and Latency

Every agent step is an LLM call. A typical coding task might involve 10-50 steps (reading files, planning, writing code, running tests, fixing issues). At current API pricing, this can cost dollars per task rather than fractions of a cent per completion. The tradeoff is worthwhile when the agent saves significant developer time, but it is wasteful for tasks the developer could do faster manually.

### Prompt Engineering for Coding Agents

The quality of instructions given to a coding agent matters enormously. Effective prompts for agentic coding:

- **Specify the outcome**, not the steps: "Add input validation that rejects negative numbers" rather than "Open the file, find the function, add an if statement"
- **Provide context**: Mention relevant files, conventions, or constraints the agent should know about
- **Set boundaries**: "Only modify files in the `src/auth/` directory" prevents scope creep
- **Define done**: "The existing tests should still pass, and add a new test for the edge case" gives the agent a concrete verification criterion

### Safety and Oversight

Coding agents can execute arbitrary commands, modify files, and interact with external services. Safety measures include:

- **Permission models**: Requiring explicit approval for destructive operations (file deletion, git force-push, production deployments)
- **Sandboxing**: Running the agent in a restricted environment where it cannot access sensitive resources
- **Audit trails**: Logging every action the agent takes for later review
- **Scope limits**: Restricting which files and directories the agent can modify

## Further Reading

- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) - Anthropic's guide to agent workflow patterns [src-001]
- [Claude Code Documentation](https://code.claude.com/docs) - Reference for Claude Code's agentic capabilities [src-002]
- [SWE-bench Paper](https://arxiv.org/abs/2310.06770) - Benchmark for evaluating coding agents [src-003]
- [Claude Code Architecture](claude-code-architecture.md) - How Claude Code implements these patterns
- [Agent Architectures and Patterns](../agents/agent-architectures.md) - General agent design patterns
- [Context Window Management](context-window-management.md) - Managing context in long agentic sessions
- [Autonomous Coding Agents](autonomous-coding-agents.md) - Fully autonomous development workflows
