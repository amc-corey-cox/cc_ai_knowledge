---
id: kb-2025-009
title: "Multi-Agent Systems"
created: 2025-02-10
updated: 2025-02-10

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation"
    authors: ["Wu et al."]
    url: "https://arxiv.org/abs/2308.08155"
    accessed: 2025-02-10
    published: 2023-08-16
    quotes:
      - text: "AutoGen is an open-source framework that allows developers to build LLM applications via multiple agents that can converse with each other to accomplish tasks."
        location: "Abstract"
      - text: "AutoGen agents are customizable, conversable, and can operate in various modes that employ combinations of LLMs, human inputs, and tools."
        location: "Abstract"

  - id: src-002
    type: primary
    title: "Communicative Agents for Software Development"
    authors: ["Qian et al."]
    url: "https://arxiv.org/abs/2307.07924"
    accessed: 2025-02-10
    published: 2023-07-16
    quotes:
      - text: "We present ChatDev, a virtual chat-powered software development company that mirrors the classic waterfall model, segmenting the development process into four chronological stages: designing, coding, testing, and documenting."
        location: "Abstract"

  - id: src-003
    type: primary
    title: "CrewAI Documentation"
    url: "https://docs.crewai.com/"
    accessed: 2025-02-10
    quotes:
      - text: "CrewAI is a framework for orchestrating role-playing autonomous AI agents."
        location: "Introduction"

  - id: src-004
    type: primary
    title: "Scaling LLM-Based Multi-Agent Systems"
    authors: ["Chen et al."]
    url: "https://arxiv.org/abs/2309.02427"
    accessed: 2025-02-10
    published: 2023-09-05

  - id: src-005
    type: primary
    title: "More Agents Is All You Need"
    authors: ["Li et al."]
    url: "https://arxiv.org/abs/2402.05120"
    accessed: 2025-02-10
    published: 2024-02-07
    quotes:
      - text: "We find that, simply scaling the number of instantiated LLM agents and having them vote on their generated outputs can consistently improve performance across diverse tasks."
        location: "Abstract"

topics:
  - agents
  - multi-agent
  - coordination
  - ai-fundamentals

confidence: high
verified: false
verified_by: unverified
verification_notes: "AI-assisted draft; quotes sourced from papers and docs but need human verification"

ai_metadata:
  model: claude-opus-4-6
  generation_date: 2025-02-10
  reviewed_by: pending
---

# Multi-Agent Systems

## Overview

Multi-agent systems use multiple LLM-powered agents that communicate and collaborate to accomplish tasks. Instead of a single model doing everything, work is distributed across specialized agents with different roles, tools, and perspectives.

The question is always: when does the added complexity of multiple agents actually help, versus when is a single capable agent sufficient?

## Why Multiple Agents?

### Specialization

Different agents can have different system prompts, tools, and context. A "researcher" agent has web search tools; a "coder" agent has file editing tools; a "reviewer" agent has testing tools. Each agent is optimized for its role rather than trying to be good at everything.

### Separation of Concerns

Long, complex tasks can overwhelm a single agent's context window and coherence. Splitting into sub-tasks with separate agents keeps each context focused. The "planner" agent doesn't need to carry the full codebase in context — it just needs the high-level structure.

### Debate and Verification

Multiple agents can check each other's work. An agent that generates code and a separate agent that reviews it will catch errors that a single self-reviewing agent might miss, because each brings a fresh perspective to the problem.

### Ensemble / Voting

Li et al. found that "simply scaling the number of instantiated LLM agents and having them vote on their generated outputs can consistently improve performance across diverse tasks" [src-005]. Multiple independent attempts with majority voting is a brute-force but effective quality improvement.

## Coordination Patterns

### Conversation-Based (AutoGen)

AutoGen models multi-agent interaction as conversations. "AutoGen agents are customizable, conversable, and can operate in various modes that employ combinations of LLMs, human inputs, and tools" [src-001].

Agents communicate through messages, and conversation flow can be:
- **Two-agent chat**: Back-and-forth between two agents (e.g., coder and reviewer)
- **Group chat**: Multiple agents in a shared conversation with a manager agent directing who speaks next
- **Nested chat**: An agent can internally spawn a sub-conversation with other agents

### Role-Based Pipeline (ChatDev)

ChatDev mirrors real software development by "segmenting the development process into four chronological stages: designing, coding, testing, and documenting" [src-002]. Different agent pairs handle each stage:

- CEO + CTO: requirements → design
- CTO + Programmer: design → code
- Programmer + Tester: code → tested code
- CEO + Reviewer: tested code → documented release

This is essentially a **pipeline** — each stage's output becomes the next stage's input. Simple, predictable, but rigid.

### Orchestrator Pattern

A central "orchestrator" agent receives the task, plans sub-tasks, delegates to specialist agents, aggregates results, and produces the final output. The orchestrator is the only agent that sees the full picture; workers have narrow, focused contexts.

```
Orchestrator
├── delegates to → Research Agent
├── delegates to → Coding Agent
├── delegates to → Testing Agent
└── aggregates results → Final output
```

### Hierarchical

Generalization of the orchestrator pattern with multiple levels. A top-level planner delegates to mid-level coordinators, who delegate to worker agents. Useful for very complex tasks but hard to debug.

### Peer-to-Peer

Agents communicate directly with each other without a central coordinator. More flexible but harder to control. Can lead to circular conversations or agents talking past each other.

## Frameworks

### AutoGen (Microsoft)

"An open-source framework that allows developers to build LLM applications via multiple agents that can converse with each other to accomplish tasks" [src-001]. Conversation-first design, supports human-in-the-loop, flexible agent definitions. Now evolved into AutoGen 0.4+ with an event-driven architecture.

### CrewAI

"A framework for orchestrating role-playing autonomous AI agents" [src-003]. Emphasizes role definitions, goals, and backstories for each agent. Simpler API than AutoGen, more opinionated about the role-based pattern. Popular for its ease of use.

### LangGraph

Part of the LangChain ecosystem. Models agent workflows as graphs (state machines) with nodes as actions and edges as transitions. More explicit control flow than conversation-based approaches. Good for workflows that need deterministic structure with LLM-powered nodes.

### Claude Code Sub-Agents

Claude Code uses a practical multi-agent pattern internally: the main agent can spawn specialized sub-agents (Explore, Plan, Bash, etc.) for specific tasks. Each sub-agent has a constrained tool set and focused context. Results flow back to the main agent, which maintains the overall conversation.

## When Multi-Agent Helps (and When It Doesn't)

### Good fits

- **Code generation + review**: Separate writing and reviewing catches more bugs
- **Research + synthesis**: One agent gathers information, another synthesizes it
- **Long, multi-phase tasks**: Where context window limits would degrade single-agent performance
- **Tasks requiring diverse tools**: Where no single agent prompt can effectively manage all tools

### Poor fits

- **Simple tasks**: A single well-prompted agent is faster and cheaper
- **Tightly coupled tasks**: If agents constantly need each other's context, the communication overhead negates the benefits
- **Latency-sensitive tasks**: Each agent handoff adds latency
- **Small context needs**: If everything fits in one context window, splitting it adds complexity without benefit

### The Complexity Tax

Every additional agent adds:
- Communication overhead (serializing/deserializing between agents)
- Potential for misunderstanding (information lost in translation)
- Debugging difficulty (which agent went wrong?)
- Cost multiplication (more LLM calls)
- Coordination logic that itself can fail

The bar for adding agents should be: "Does the task decompose into genuinely independent sub-problems that benefit from separate contexts?"

## Open Challenges

- **Evaluation**: How do you benchmark multi-agent systems? Individual agent performance doesn't capture coordination quality.
- **Error propagation**: One bad agent output cascades through the pipeline.
- **Context sharing**: How much context should agents share? Too much defeats the purpose; too little causes misalignment.
- **Cost control**: Multi-agent runs can be expensive. How do you set budgets and termination conditions?

## Further Reading

- [AutoGen Paper](https://arxiv.org/abs/2308.08155) - Conversation-based multi-agent framework [src-001]
- [ChatDev Paper](https://arxiv.org/abs/2307.07924) - Role-based software development [src-002]
- [CrewAI Docs](https://docs.crewai.com/) - Role-playing agent framework [src-003]
- [More Agents Is All You Need](https://arxiv.org/abs/2402.05120) - Scaling via ensemble [src-005]
- [LLM Agent Architectures](agent-architectures.md) - Single-agent patterns
- [Tool Use and Function Calling](tool-use-function-calling.md) - How agents interact with tools
- [Sub-Agent Delegation](sub-agent-delegation.md) - Context isolation and orchestration patterns
- [Human-in-the-Loop Patterns](human-in-the-loop.md) - Oversight in multi-agent workflows
- [Autonomous Coding Agents](../agentic-coding/autonomous-coding-agents.md) - Multi-agent approaches in coding tools
