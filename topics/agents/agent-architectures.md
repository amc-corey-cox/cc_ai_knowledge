---
id: kb-2025-007
title: "LLM Agent Architectures and Patterns"
created: 2025-02-10
updated: 2025-02-10

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "ReAct: Synergizing Reasoning and Acting in Language Models"
    authors: ["Yao et al."]
    url: "https://arxiv.org/abs/2210.03629"
    accessed: 2025-02-10
    published: 2022-10-06
    quotes:
      - text: "We explore the use of LLMs to generate both reasoning traces and task-specific actions in an interleaved manner, allowing for greater synergy between the two."
        location: "Abstract"
      - text: "ReAct prompts LLMs to generate both verbal reasoning traces and actions pertaining to a task in an interleaved manner, which allows the model to perform dynamic reasoning to create, maintain, and adjust high-level plans for acting."
        location: "Section 1 - Introduction"

  - id: src-002
    type: primary
    title: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
    authors: ["Wei et al."]
    url: "https://arxiv.org/abs/2201.11903"
    accessed: 2025-02-10
    published: 2022-01-28
    quotes:
      - text: "We explore how generating a chain of thought — a series of intermediate reasoning steps — significantly improves the ability of large language models to perform complex reasoning."
        location: "Abstract"

  - id: src-003
    type: primary
    title: "A Survey on Large Language Model based Autonomous Agents"
    authors: ["Wang et al."]
    url: "https://arxiv.org/abs/2308.11432"
    accessed: 2025-02-10
    published: 2023-08-22
    quotes:
      - text: "The key characteristics of agents can be summarized as: autonomy, reactivity, pro-activeness, and social ability."
        location: "Section 2.1 - Origin of AI Agents"

  - id: src-004
    type: primary
    title: "Reflexion: Language Agents with Verbal Reinforcement Learning"
    authors: ["Shinn et al."]
    url: "https://arxiv.org/abs/2303.11366"
    accessed: 2025-02-10
    published: 2023-03-20
    quotes:
      - text: "Reflexion agents verbally reflect on task feedback signals, then maintain their own reflective text in an episodic memory buffer to induce better decision-making in subsequent trials."
        location: "Abstract"

  - id: src-005
    type: primary
    title: "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
    authors: ["Yao et al."]
    url: "https://arxiv.org/abs/2305.10601"
    accessed: 2025-02-10
    published: 2023-05-17
    quotes:
      - text: "We introduce a new framework for language model inference, Tree of Thoughts (ToT), which generalizes over the popular Chain of Thought approach to prompting language models, and enables exploration over coherent units of text (thoughts) that serve as intermediate steps toward problem solving."
        location: "Abstract"

topics:
  - agents
  - architectures
  - reasoning
  - ai-fundamentals

confidence: high
verified: false
verified_by: unverified
verification_notes: "AI-assisted draft; quotes sourced from papers but need human verification against originals"

ai_metadata:
  model: claude-opus-4-6
  generation_date: 2025-02-10
  reviewed_by: pending
---

# LLM Agent Architectures and Patterns

## Overview

An LLM agent is a system where a language model operates in a loop, taking actions, observing results, and deciding what to do next. The key characteristics of agents are "autonomy, reactivity, pro-activeness, and social ability" [src-003]. This distinguishes agents from single-shot LLM calls: an agent persists, plans, acts, and adapts.

## The Core Agent Loop

At its simplest, every LLM agent follows the same pattern:

```
while not done:
    observation = perceive(environment)
    thought = reason(observation, memory, goal)
    action = decide(thought)
    result = execute(action)
    memory = update(memory, result)
```

The variations between agent architectures are really about how they implement `reason`, `decide`, and `memory`. Everything else is plumbing.

## Reasoning Patterns

### Chain-of-Thought (CoT)

Wei et al. showed that "generating a chain of thought — a series of intermediate reasoning steps — significantly improves the ability of large language models to perform complex reasoning" [src-002].

CoT is the simplest reasoning pattern: instead of jumping to an answer, the model writes out its reasoning step by step. This works because:
- It decomposes complex problems into manageable sub-steps
- Each step is more likely to be correct than a single large leap
- The written reasoning becomes context for subsequent steps

CoT is a **prompting technique**, not an architecture, but it's foundational to every agent pattern that follows.

### ReAct (Reason + Act)

ReAct interleaves reasoning and action in a single stream. Yao et al. "explore the use of LLMs to generate both reasoning traces and task-specific actions in an interleaved manner" [src-001].

A ReAct trace looks like:

```
Thought: I need to find who directed Inception.
Action: search("Inception director")
Observation: Christopher Nolan directed Inception (2010).
Thought: The answer is Christopher Nolan.
Action: finish("Christopher Nolan")
```

The key insight is that "ReAct prompts LLMs to generate both verbal reasoning traces and actions pertaining to a task in an interleaved manner, which allows the model to perform dynamic reasoning to create, maintain, and adjust high-level plans for acting" [src-001].

**Why it works**: Reasoning without acting (pure CoT) can hallucinate facts. Acting without reasoning (direct tool use) can be unfocused. ReAct combines the grounding of real observations with the planning of explicit reasoning.

**Limitation**: ReAct is fundamentally linear — it follows one chain of thought. If it goes down a wrong path, it may not recover.

### Tree of Thoughts (ToT)

ToT generalizes CoT from a single chain to a tree: "exploration over coherent units of text (thoughts) that serve as intermediate steps toward problem solving" [src-005].

Instead of committing to one reasoning path, ToT:
1. Generates multiple candidate next-steps
2. Evaluates each candidate
3. Explores the most promising paths (via BFS or DFS)
4. Can backtrack from dead ends

This is more powerful but significantly more expensive — each branch requires LLM calls. Best suited for problems with clear evaluation criteria (math, puzzles, constrained planning).

### Reflexion

Reflexion adds self-critique and memory across attempts. Agents "verbally reflect on task feedback signals, then maintain their own reflective text in an episodic memory buffer to induce better decision-making in subsequent trials" [src-004].

The pattern:
1. Attempt a task
2. Observe failure (or suboptimal result)
3. Reflect: "What went wrong? What should I do differently?"
4. Store the reflection in memory
5. Re-attempt with the reflection as additional context

This is essentially verbal reinforcement learning — the agent learns from its mistakes within a session without any weight updates.

## Planning Patterns

### Plan-then-Execute

The simplest planning approach: generate a full plan upfront, then execute each step. Works well for straightforward tasks but is brittle — if the plan is wrong, the agent follows it off a cliff.

```
Plan:
1. Read the configuration file
2. Find the database connection string
3. Update the port number
4. Write the file back

Execute steps 1-4 sequentially.
```

### Iterative Refinement

Generate an initial plan, start executing, and revise the plan as new information emerges. More robust than plan-then-execute because the agent adapts, but requires the model to manage the cognitive overhead of tracking plan state.

### Hierarchical Planning

Decompose a high-level goal into sub-goals, and sub-goals into concrete actions. Common in complex coding agents where a feature request decomposes into: understand requirements → identify files → plan changes → implement → test.

## Memory Architectures

Agents need memory beyond the current context window. Common approaches:

### Context Window as Working Memory

The simplest approach: everything the agent has seen is in the prompt. Works until you hit context limits. Most production agents start here.

### Summarized/Compressed Memory

Periodically summarize older context to fit more history into the window. Lossy but practical. The agent maintains a "running summary" of what it's done.

### External Memory (RAG-style)

Store observations, reflections, and results in a vector store or structured database. Retrieve relevant memories when needed. Scales beyond context limits but adds latency and retrieval noise.

### Episodic Memory

Store specific experiences (like Reflexion's reflections) as discrete episodes that can be recalled. This is closer to how humans learn from specific past events.

## Practical Considerations

### When to Use an Agent vs. a Single Call

Not everything needs an agent. Use a single LLM call when:
- The task is self-contained (no external information needed)
- The output format is well-defined
- No iteration or correction is needed

Use an agent when:
- The task requires multiple steps with real-world interaction
- The model needs to gather information before answering
- The task may require course correction based on intermediate results
- Tool use is required (see [Tool Use and Function Calling](tool-use-function-calling.md))

### The Cost of Agency

Each agent step is an LLM call. A 10-step agent trajectory costs 10x a single call. More sophisticated patterns (ToT, Reflexion) multiply this further. The tradeoff is always: autonomy and robustness vs. cost and latency.

### Failure Modes

- **Looping**: The agent repeats the same action without progress
- **Goal drift**: The agent loses track of the original objective over long trajectories
- **Over-planning**: Spending more tokens planning than executing
- **Hallucinated actions**: Attempting to call tools that don't exist or with wrong parameters

## Further Reading

- [ReAct Paper](https://arxiv.org/abs/2210.03629) - Reasoning + Acting [src-001]
- [Chain-of-Thought Paper](https://arxiv.org/abs/2201.11903) - Foundation for agent reasoning [src-002]
- [Agent Survey](https://arxiv.org/abs/2308.11432) - Comprehensive overview [src-003]
- [Tool Use and Function Calling](tool-use-function-calling.md) - How agents interact with the world
- [Multi-Agent Systems](multi-agent-systems.md) - When one agent isn't enough
- [Sub-Agent Delegation](sub-agent-delegation.md) - Context isolation and task decomposition
- [Human-in-the-Loop Patterns](human-in-the-loop.md) - Permission models and oversight
- [Claude Code Architecture](../agentic-coding/claude-code-architecture.md) - A production agentic coding system
- [Agentic Coding Patterns](../agentic-coding/agentic-coding-patterns.md) - Agent patterns applied to software development
