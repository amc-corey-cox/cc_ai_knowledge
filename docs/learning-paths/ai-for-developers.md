# AI for Developers

A structured path through the knowledge base for experienced developers who use AI daily but want to build stronger fundamentals. Each module builds on the previous one — start at the top and work through in order.

Articles marked *(optional)* can be skipped without losing the thread, but they deepen understanding if you have time.

---

## Module 1: How LLMs Actually Work

Before you can effectively use AI tools, it helps to have intuition about what's happening inside them. You don't need to implement a transformer from scratch, but understanding the architecture explains a lot of behaviors you see in practice — why models are good at some tasks and bad at others, why context length matters, and why "just make it bigger" isn't always the answer.

### Articles

1. **[Transformer Architecture Overview](../topics/transformers/transformer-architecture.md)** — The encoder-decoder structure, how tokens flow through the model, and why this architecture displaced everything that came before it.

2. **[The Attention Mechanism](../topics/transformers/attention-mechanism.md)** — The core innovation. How attention lets models weigh the relevance of every token against every other token, and why this matters for understanding model capabilities and limitations.

3. **[Modern Transformer Variants](../topics/transformers/modern-variants.md)** *(optional)* — How the original architecture has evolved: decoder-only models (GPT), encoder-only (BERT), mixture of experts, and efficiency improvements. Useful context for understanding why different models have different strengths.

### What to take away

After this module you should understand why transformers process entire sequences in parallel (not word-by-word like RNNs), what the attention mechanism actually computes, and why context window size is a fundamental constraint — not just a product limitation.

---

## Module 2: The Models You Use

Now that you understand the architecture, let's look at the specific models you interact with daily. This module covers the Claude model family and how reasoning capabilities work across different models.

### Articles

1. **[The Claude Model Family](../topics/ai-fundamentals/claude-model-family.md)** — Opus, Sonnet, Haiku: what each model is optimized for, capability tradeoffs, and how to choose the right model for a task.

2. **[Extended Thinking, Chain-of-Thought, and Reasoning](../topics/ai-fundamentals/extended-thinking-reasoning.md)** — How models "think step by step," what extended thinking actually does under the hood, and when reasoning capabilities make a practical difference.

### What to take away

You should be able to make informed decisions about which model to use for a given task, and understand when extended thinking will help versus when it's overhead.

---

## Module 3: Talking to Models Effectively

With a mental model of how transformers work and what the Claude models can do, you're ready to be more intentional about prompting. This isn't a tips-and-tricks collection — it connects prompting strategies back to the architecture you learned about.

### Articles

1. **[Prompt Engineering for Code Generation](../topics/ai-fundamentals/prompt-engineering-code.md)** — Structured techniques for getting better code output: context management, few-shot examples, constraint specification, and why certain prompting patterns work given what you now know about attention and context.

### What to take away

You should understand why providing relevant context in your prompts matters (attention over the context window), how to structure prompts for code generation specifically, and how to debug prompt failures.

---

## Module 4: How AI Agents Work

The jump from "model that responds to prompts" to "agent that takes actions" is one of the most important developments in practical AI. This module covers the architecture patterns that make tools like Claude Code possible.

### Articles

1. **[LLM Agent Architectures and Patterns](../topics/agents/agent-architectures.md)** — The fundamental patterns: ReAct, plan-and-execute, and how agents combine LLM reasoning with tool execution in a loop. This is the conceptual foundation for everything in the agentic coding module.

2. **[Tool Use and Function Calling](../topics/agents/tool-use-function-calling.md)** — How models learn to call functions, the structured formats involved, and what happens at the API level when an agent uses a tool. Critical for understanding both MCP and agentic coding.

3. **[Human-in-the-Loop Patterns](../topics/agents/human-in-the-loop.md)** *(optional)* — How and when to keep humans in the decision loop. Relevant if you're thinking about trust, safety, and approval workflows in automated systems.

4. **[Multi-Agent Systems](../topics/agents/multi-agent-systems.md)** *(optional)* — When a single agent isn't enough: orchestration patterns, communication protocols, and the tradeoffs of multi-agent architectures.

5. **[Sub-Agent Delegation](../topics/agents/sub-agent-delegation.md)** *(optional)* — A specific pattern within multi-agent systems where a primary agent spawns specialized sub-agents. Directly relevant to how Claude Code uses sub-agents for parallel tasks.

### What to take away

You should understand the agent loop (observe → think → act → observe), how tool calling works at a technical level, and how these patterns compose into more sophisticated architectures. The optional articles provide depth on patterns you'll see in practice with Claude Code.

---

## Module 5: Agentic Coding in Practice

This is where theory meets your daily workflow. You've learned how transformers work, what the models can do, how agents use tools, and now you'll see how all of that comes together in agentic coding tools.

### Articles

1. **[Claude Code Architecture](../topics/agentic-coding/claude-code-architecture.md)** — How Claude Code is built: the agent loop, tool system, permission model, and how it orchestrates file edits, shell commands, and search. This article ties together concepts from Modules 1 and 4.

2. **[Agentic Coding Patterns](../topics/agentic-coding/agentic-coding-patterns.md)** — Practical workflows for AI-assisted development: when to use agents vs. chat, how to decompose tasks, iteration patterns, and quality gates.

3. **[CLAUDE.md: Agent Configuration](../topics/agentic-coding/claude-md-agent-configuration.md)** — The layered instruction model that lets you configure agent behavior per-project, per-user, and per-directory. How to write effective CLAUDE.md files that improve agent performance.

4. **[Context Window Management](../topics/agentic-coding/context-window-management.md)** — Why context management is the central challenge of agentic coding. Strategies for keeping agents effective across long sessions, and how tools like compaction and sub-agents help.

5. **[Autonomous Coding Agents](../topics/agentic-coding/autonomous-coding-agents.md)** *(optional)* — The broader landscape of autonomous coding tools beyond Claude Code: Cursor, Copilot, Devin, and others. Useful for understanding where the field is heading.

### What to take away

You should understand how to work effectively with Claude Code (or similar tools), how to configure agent behavior for your projects, and how to manage the context window constraint that underlies most agentic coding challenges.

---

## Module 6: Extending Capabilities with MCP

The Model Context Protocol lets you give agents access to your own tools and data sources. This module covers the protocol itself and how to build servers for it.

### Articles

1. **[Model Context Protocol (MCP)](../topics/protocols/model-context-protocol.md)** — What MCP is, how it works (the client-server architecture, transport mechanisms, capability negotiation), and why it matters for the agent ecosystem.

2. **[Building MCP Servers](../topics/protocols/mcp-server-development.md)** — Practical guide to implementing MCP servers: the SDK, tool definition, resource exposure, and deployment patterns.

### What to take away

You should understand how to extend agent capabilities beyond built-in tools by building MCP servers that expose your own APIs, databases, and services.

---

## Module 7: Running Models Locally *(optional module)*

Everything above uses cloud-hosted models. This module covers running models on your own hardware — useful for privacy, cost control, offline use, or just understanding what's involved.

### Articles

1. **[Quantization Methods](../topics/local-inference/quantization-methods.md)** — How to shrink models to fit on consumer hardware: GPTQ, GGUF, AWQ, and the quality tradeoffs at different bit widths.

2. **[Local Inference Engines](../topics/local-inference/inference-engines.md)** — The software that runs quantized models: llama.cpp, Ollama, vLLM, and others. Capabilities, performance characteristics, and when to use each.

3. **[Hardware Requirements and Optimization](../topics/local-inference/hardware-and-optimization.md)** — GPU memory math, CPU fallback strategies, Apple Silicon considerations, and how to estimate what hardware you need for a given model.

### What to take away

You should be able to evaluate whether running a model locally makes sense for your use case, choose appropriate quantization and engine, and estimate hardware requirements.
