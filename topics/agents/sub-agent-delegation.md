---
id: kb-2025-023
title: "Sub-Agent Delegation Patterns"
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
      - text: "Maintain simplicity in your agent's design."
        location: "Summary"
  - id: src-002
    type: primary
    title: "Claude Code Documentation"
    url: "https://code.claude.com/docs"
    accessed: 2026-02-19
    quotes:
      - text: "Spawn multiple Claude Code agents that work on different parts of a task simultaneously. A lead agent coordinates the work, assigns subtasks, and merges results."
        location: "Overview - Run agent teams"
  - id: src-003
    type: primary
    title: "A Survey on Large Language Model based Autonomous Agents"
    authors: ["Wang et al."]
    url: "https://arxiv.org/abs/2308.11432"
    accessed: 2026-02-19
    published: 2023-08-22
    quotes:
      - text: "The key characteristics of agents can be summarized as: autonomy, reactivity, pro-activeness, and social ability."
        location: "Section 2.1 - Origin of AI Agents"

topics:
  - delegation
  - agents
  - multi-agent
  - agentic-coding

confidence: high
verified: false
verified_by: unverified
verification_notes: "AI-assisted draft; quotes sourced from official docs and papers but need human verification"

ai_metadata:
  model: claude-opus-4-6
  generation_date: 2026-02-19
  reviewed_by: pending
---

# Sub-Agent Delegation Patterns

## Overview

Sub-agent delegation is the practice of having a lead agent spawn subordinate agents to handle portions of a larger task. Rather than a single agent trying to do everything within one context window, work is decomposed and distributed to specialized sub-agents that operate independently and return their results.

Three motivations drive this pattern:

1. **Context isolation** -- sub-agents get fresh context windows, protecting the lead agent from context overflow and keeping each sub-task focused.
2. **Parallelism** -- independent sub-tasks can run concurrently, reducing wall-clock time.
3. **Specialization** -- different sub-agents can carry different tool sets, system prompts, and constraints optimized for their specific role.

This article examines the mechanics of sub-agent delegation, with particular attention to how Claude Code implements it in practice.

## Context Isolation

The most fundamental reason to delegate is context management. An LLM agent's context window is finite, and as a conversation grows, several problems compound:

- **Attention dilution**: With more tokens in context, the model's attention spreads thinner across the conversation history, degrading performance on the current task.
- **Irrelevant context**: Details from earlier sub-tasks pollute the reasoning for the current one. A sub-agent that just finished researching database schemas does not need 10,000 tokens of prior CSS debugging history.
- **Context window exhaustion**: Long-running agents eventually fill their context windows entirely, forcing lossy summarization or truncation.

Sub-agent delegation solves this by giving each sub-agent a clean slate. The lead agent sends a focused prompt describing the sub-task, and the sub-agent operates within its own fresh context. When the sub-agent returns its result, only the relevant output -- not the full trajectory of the sub-agent's reasoning -- flows back to the lead agent.

This is conceptually similar to function calls in programming: the caller does not need to see the callee's local variables, only the return value. The sub-agent's internal reasoning is an implementation detail.

## The Orchestrator-Worker Pattern

The most common delegation architecture is orchestrator-worker, where a single lead agent acts as coordinator:

```
Lead Agent (Orchestrator)
│
├── 1. Receive task
├── 2. Decompose into sub-tasks
├── 3. Spawn sub-agents (workers)
│     ├── Worker A: research
│     ├── Worker B: implementation
│     └── Worker C: testing
├── 4. Collect results
├── 5. Aggregate and synthesize
└── 6. Produce final output
```

The orchestrator's responsibilities are:
- **Task decomposition**: Breaking the problem into independent, well-scoped pieces
- **Delegation**: Formulating clear instructions for each worker
- **Aggregation**: Combining worker outputs into a coherent whole
- **Error handling**: Detecting and recovering from worker failures

The workers' responsibilities are narrower: execute the assigned sub-task and return the result. Workers typically do not communicate with each other -- all coordination flows through the orchestrator.

Anthropic's guidance on agent design emphasizes that "workflows are systems where LLMs and tools are orchestrated through predefined code paths" [src-001]. The orchestrator-worker pattern embodies this: the orchestrator defines the workflow structure, and workers execute within it.

## Claude Code's Task Tool

Claude Code provides a concrete implementation of sub-agent delegation through its Task tool. The lead agent can "spawn multiple Claude Code agents that work on different parts of a task simultaneously. A lead agent coordinates the work, assigns subtasks, and merges results" [src-002].

### How It Works

When the lead agent invokes the Task tool, it provides:
- A **description** of the sub-task (the prompt the sub-agent will receive)
- A **type** hint that constrains the sub-agent's available tools

The sub-agent runs in its own context, executes its task, and returns output to the lead agent. The lead agent never sees the sub-agent's intermediate steps -- only the final result.

### Sub-Agent Types

Different task types give sub-agents different capabilities:

- **General-purpose**: Full access to tools (file reading, writing, search, bash). Used for tasks that require autonomous problem-solving.
- **Bash**: Constrained to shell commands. Useful for running tests, checking build output, or gathering system information.
- **Plan**: Focused on analysis and planning without side effects. The sub-agent can read and search but not write files.

This type system enforces the principle of least privilege: a sub-agent that only needs to read files should not have write access. This reduces the blast radius of errors and keeps each sub-agent's scope tight.

### Background Execution

Claude Code supports running sub-agents in the background with `run_in_background`. This enables true parallelism -- the lead agent can spawn multiple workers and continue its own work while they execute. The lead agent checks for completed results when it needs them.

This is particularly valuable for tasks with independent sub-components:

```
Lead Agent:
  1. Spawn background worker: "Run the test suite"
  2. Spawn background worker: "Check lint and formatting"
  3. Continue working on code changes
  4. Check worker results before committing
```

## Specialization Through Delegation

Beyond context management, delegation enables specialization. Different sub-tasks often benefit from different approaches:

### Research vs. Implementation

A research sub-agent might be prompted to:
- Search broadly across the codebase
- Read documentation and configuration files
- Summarize findings without making changes

An implementation sub-agent receives the research output and:
- Makes targeted code changes
- Follows specific patterns identified by the researcher
- Stays focused on a narrow set of files

### Writing vs. Review

Code generation and code review are fundamentally different cognitive tasks. A writing sub-agent generates code to fulfill a requirement, while a review sub-agent evaluates that code with fresh eyes. The reviewer brings an unbiased perspective because it was not involved in the generation decisions.

### Exploratory vs. Focused

Some sub-tasks require open-ended exploration (understanding a new codebase, finding relevant files), while others require focused execution (applying a specific change to a known file). Tuning the sub-agent's prompt and tool access for each mode improves results.

## Task Decomposition

Effective delegation depends on effective decomposition. The orchestrator must break the problem into pieces that are:

### Independent

Sub-tasks should have minimal dependencies on each other. If Worker B needs the output of Worker A, they cannot run in parallel. The orchestrator should identify the dependency graph and schedule accordingly -- parallel where possible, sequential where necessary.

### Well-Scoped

Each sub-task should be completable within a single sub-agent context without requiring back-and-forth clarification. The orchestrator's instructions must be specific enough that the worker can execute without ambiguity.

Bad decomposition:
```
Worker A: "Fix the bugs in the authentication module"
```

Better decomposition:
```
Worker A: "In src/auth/token.py, the refresh_token() function does not
handle expired tokens correctly. When the token has expired, it should
raise TokenExpiredError instead of returning None. Update the function
and its unit tests in tests/auth/test_token.py."
```

### Appropriately Sized

Too-large sub-tasks reintroduce the context problems delegation was meant to solve. Too-small sub-tasks create excessive coordination overhead -- the orchestrator spends more time managing workers than it saves.

A good heuristic: each sub-task should be something a developer could complete in a single focused work session, with a clear definition of done.

## Results Aggregation

Once workers complete their sub-tasks, the orchestrator must combine their outputs. This is more than simple concatenation -- it requires synthesis:

### Merge Strategies

- **Sequential assembly**: Workers produce ordered components (e.g., sections of a document). The orchestrator assembles them in sequence.
- **Conflict resolution**: Multiple workers modify the same codebase. The orchestrator must detect and resolve conflicts, similar to a git merge.
- **Quality filtering**: The orchestrator evaluates worker outputs and may reject or request re-work for subpar results.
- **Synthesis**: Worker outputs are raw material that the orchestrator transforms into a final product (e.g., combining research findings into a coherent summary).

### The Return Value Problem

A key design decision is how much of the worker's output flows back to the orchestrator. Options range from:
- **Full output**: Everything the worker produced. Maximizes information but can overwhelm the orchestrator's context.
- **Summarized output**: The worker (or the framework) summarizes key findings. Compact but potentially lossy.
- **Structured output**: The worker returns data in a predefined format (JSON, specific sections). Balances detail with parsability.

In practice, Claude Code sub-agents return their full textual output, and the lead agent is responsible for extracting the relevant pieces. This works because the sub-agent's output is typically much smaller than its full internal context trajectory.

## When to Delegate vs. Do Directly

Delegation has overhead. Every sub-agent invocation involves:
- The orchestrator formulating the sub-task prompt
- The sub-agent's startup and context initialization
- The sub-agent's execution
- Result transfer back to the orchestrator
- The orchestrator parsing and integrating the result

For simple tasks, this overhead exceeds the benefit. Anthropic advises: "Maintain simplicity in your agent's design" [src-001].

### Delegate When

- The task involves multiple independent sub-problems
- Context window pressure is a concern (long-running conversations)
- Different sub-tasks need different tool sets
- Parallel execution would meaningfully reduce total time
- The sub-task benefits from a fresh perspective (e.g., code review)

### Do Directly When

- The task is straightforward and fits in current context
- The task requires tight integration with the current conversation state
- The communication cost of describing the sub-task exceeds the cost of doing it
- The task has heavy dependencies on the orchestrator's accumulated context
- Speed matters more than isolation (sub-agent spawning adds latency)

### The Communication Cost Test

A useful rule of thumb: if explaining the sub-task to a worker would take as many tokens as doing the task yourself, skip the delegation. The value of delegation scales with the ratio of (sub-task complexity) to (description complexity).

## Failure Handling

Sub-agents can fail. Robust orchestrators plan for this.

### Failure Modes

- **Task misunderstanding**: The sub-agent interprets the task differently than intended and produces incorrect output. Often caused by ambiguous instructions.
- **Tool errors**: The sub-agent encounters errors from its tools (file not found, command failed, permission denied).
- **Context exhaustion**: The sub-task is larger than expected and the sub-agent runs out of context.
- **Hallucination**: The sub-agent confabulates results rather than admitting it cannot complete the task.
- **Timeout**: The sub-agent takes too long, consuming excessive resources.

### Recovery Strategies

- **Retry with clarification**: If the sub-agent misunderstood, re-delegate with more specific instructions. Include context about what went wrong.
- **Retry with decomposition**: If the sub-task was too large, break it into smaller pieces.
- **Fallback to direct execution**: If delegation keeps failing, the orchestrator can attempt the task itself.
- **Graceful degradation**: If a non-critical sub-task fails, proceed without it and note the gap.
- **Validation before integration**: Always validate sub-agent output before incorporating it. Run tests, check for consistency, verify against requirements.

### The Idempotency Principle

Where possible, design sub-tasks to be idempotent -- safe to retry without side effects. A sub-agent that reads and analyzes code is inherently idempotent. A sub-agent that writes files is not, unless it writes deterministically (same input always produces same output).

## Relationship to Agent Characteristics

Wang et al. identify the key characteristics of agents as "autonomy, reactivity, pro-activeness, and social ability" [src-003]. Sub-agent delegation engages all four:

- **Autonomy**: Each sub-agent operates independently within its scope
- **Reactivity**: Sub-agents respond to their environment (tool outputs, file contents)
- **Pro-activeness**: The orchestrator proactively decomposes tasks and delegates before problems arise
- **Social ability**: The orchestrator and workers communicate through structured delegation and result passing

The delegation pattern trades individual agent autonomy for system-level coordination. Each worker has less autonomy than a fully independent agent, but the system as a whole is more capable than any single agent.

## Practical Considerations

### Prompt Engineering for Delegation

The quality of delegation depends heavily on how the orchestrator formulates sub-task prompts. Effective delegation prompts include:

- **Clear objective**: What the sub-agent should accomplish
- **Relevant context**: Background information needed for the task (but no more)
- **Constraints**: What the sub-agent should not do
- **Expected output format**: What the orchestrator needs back
- **Scope boundaries**: Explicit limits on what the sub-agent should attempt

### Cost and Latency

Each sub-agent is an independent LLM session. In a system like Claude Code, spawning three sub-agents means three separate inference sessions. The cost scales linearly with the number of sub-agents and the size of their contexts. Parallel execution helps with latency but not with total compute cost.

### Observability

Debugging multi-agent systems is inherently harder than debugging single-agent systems. When something goes wrong, you need to trace which sub-agent produced the problematic output, what instructions it received, and what its internal reasoning was. Logging sub-agent inputs and outputs is essential for post-hoc analysis.

### Context Window Budget

The orchestrator must manage its own context budget. If it spawns many sub-agents and ingests all their outputs, it can exhaust its own context window. The orchestrator should summarize or selectively retain sub-agent outputs rather than accumulating everything verbatim.

## Further Reading

- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) - Anthropic's guide to agent design [src-001]
- [Claude Code Documentation](https://code.claude.com/docs) - Sub-agent capabilities in Claude Code [src-002]
- [Agent Survey](https://arxiv.org/abs/2308.11432) - Comprehensive overview of agent characteristics [src-003]
- [Multi-Agent Systems](multi-agent-systems.md) - Broader multi-agent coordination patterns
- [LLM Agent Architectures](agent-architectures.md) - Single-agent patterns and reasoning strategies
- [Claude Code Architecture](../agentic-coding/claude-code-architecture.md) - How Claude Code implements the agent loop
- [Human-in-the-Loop](human-in-the-loop.md) - Keeping humans involved in agent decisions
