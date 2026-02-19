---
id: kb-2025-022
title: "Extended Thinking, Chain-of-Thought, and Reasoning Models"
created: 2026-02-19
updated: 2026-02-19

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "Anthropic Extended Thinking Documentation"
    url: "https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking"
    accessed: 2026-02-19
    quotes:
      - text: "Extended thinking gives Claude enhanced reasoning capabilities for complex tasks, while providing varying levels of transparency into its step-by-step thought process before it delivers its final answer."
        location: "Introduction"
      - text: "When extended thinking is turned on, Claude creates thinking content blocks where it outputs its internal reasoning. Claude incorporates insights from this reasoning before crafting a final response."
        location: "How extended thinking works"
  - id: src-002
    type: primary
    title: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
    authors: ["Wei et al."]
    url: "https://arxiv.org/abs/2201.11903"
    accessed: 2026-02-19
    published: 2022-01-28
    arxiv: "2201.11903"
    quotes:
      - text: "We explore how generating a chain of thought — a series of intermediate reasoning steps — significantly improves the ability of large language models to perform complex reasoning."
        location: "Abstract"
  - id: src-003
    type: primary
    title: "Let's Verify Step by Step"
    authors: ["Lightman et al."]
    url: "https://arxiv.org/abs/2305.20050"
    accessed: 2026-02-19
    published: 2023-05-31
    arxiv: "2305.20050"
    quotes:
      - text: "We find that process supervision significantly outperforms outcome supervision for training models to solve problems from the MATH dataset."
        location: "Abstract"
  - id: src-004
    type: primary
    title: "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
    authors: ["Yao et al."]
    url: "https://arxiv.org/abs/2305.10601"
    accessed: 2026-02-19
    published: 2023-05-17
    arxiv: "2305.10601"
    quotes:
      - text: "We introduce a new framework for language model inference, Tree of Thoughts (ToT), which generalizes over the popular Chain of Thought approach."
        location: "Abstract"

topics:
  - extended-thinking
  - reasoning
  - ai-fundamentals
  - agents

confidence: high
verified: false
verified_by: unverified
verification_notes: "AI-assisted draft; quotes sourced from Anthropic documentation and papers but need human verification"

ai_metadata:
  model: claude-opus-4-6
  generation_date: 2026-02-19
  reviewed_by: pending
---

# Extended Thinking, Chain-of-Thought, and Reasoning Models

## Overview

The history of improving LLM reasoning is a story of making models "think before they speak." Early language models produced answers in a single forward pass -- fast, but limited to the patterns they could compute in one shot. The breakthrough insight, formalized by Wei et al., was that "generating a chain of thought -- a series of intermediate reasoning steps -- significantly improves the ability of large language models to perform complex reasoning" [src-002]. From that foundation, the field has evolved through several stages: prompt-based chain-of-thought, process supervision during training, structured search over reasoning paths, and finally dedicated reasoning modes built into the models themselves.

This article traces that evolution, from the "think step by step" prompting trick to Anthropic's extended thinking in Claude, covering the concepts, tradeoffs, and practical implications along the way.

## Chain-of-Thought Prompting

### The Foundational Technique

Chain-of-thought (CoT) prompting is deceptively simple: instead of asking a model for a direct answer, you prompt it to show its work. The canonical approach is to add "Let's think step by step" to a prompt, or to provide few-shot examples that include intermediate reasoning steps. Wei et al. demonstrated that this technique "significantly improves the ability of large language models to perform complex reasoning" across arithmetic, commonsense, and symbolic reasoning tasks [src-002].

Why does writing out intermediate steps help? Several factors contribute:

- **Decomposition**: A hard problem becomes a sequence of easier sub-problems. Each individual step is more likely to be correct than a single leap to the final answer.
- **Working memory**: The generated text acts as an external scratchpad. The model can reference its own earlier reasoning as context for later steps, effectively extending its working memory beyond what fits in a single forward pass.
- **Error visibility**: When reasoning is explicit, mistakes become observable -- both to the model (which may self-correct) and to humans reviewing the output.

### Limitations of Prompt-Based CoT

CoT prompting is a technique applied at inference time. It does not change the model's weights or training. This means:

- The model may produce plausible-sounding but incorrect reasoning steps (faithful-looking but unfaithful reasoning).
- The quality of reasoning depends heavily on model scale -- small models do not benefit much from CoT prompting.
- The model has no mechanism to verify its own steps unless explicitly prompted to do so.
- CoT uses output tokens, increasing cost and latency proportional to the length of reasoning.

These limitations motivated two parallel lines of research: better training signals for reasoning (process supervision) and more structured search over reasoning paths (Tree of Thoughts).

## Process Supervision vs. Outcome Supervision

### The Core Distinction

When training a model to solve multi-step problems, there are two fundamentally different approaches to providing feedback:

- **Outcome supervision**: Check only whether the final answer is correct. The model gets a reward signal based on the end result, regardless of how it got there.
- **Process supervision**: Check each intermediate step for correctness. The model gets feedback on whether its reasoning process is sound, not just whether it arrived at the right answer.

Lightman et al. investigated this distinction rigorously and found that "process supervision significantly outperforms outcome supervision for training models to solve problems from the MATH dataset" [src-003].

### Why Process Supervision Works Better

The intuition is straightforward. Outcome supervision has a credit assignment problem: if a model gets the final answer wrong, which step was the mistake? With many intermediate steps, the training signal is diluted. A model might learn to arrive at correct answers via flawed reasoning, which fails to generalize to harder problems.

Process supervision provides a denser training signal. Every step gets feedback, so the model learns not just what to conclude but how to reason correctly. This produces more reliable reasoning chains and better generalization.

### Implications for Reasoning Models

Process supervision is conceptually related to how modern reasoning models are trained. While the exact training details of models like OpenAI's o1 or Anthropic's extended thinking are not public, the general direction is clear: the field has moved toward rewarding correct reasoning processes, not just correct final answers. This shift is one of the key enablers of the "reasoning model" paradigm.

## Tree of Thoughts

### Beyond Linear Reasoning

Standard CoT produces a single chain of reasoning -- one path from question to answer. Yao et al. proposed Tree of Thoughts (ToT), which "generalizes over the popular Chain of Thought approach" by exploring multiple reasoning paths simultaneously [src-004].

The ToT framework works as follows:

1. **Generate** multiple candidate "thoughts" (intermediate reasoning steps) at each point.
2. **Evaluate** each candidate using the model itself or an external heuristic.
3. **Search** over the tree of possibilities using breadth-first search, depth-first search, or beam search.
4. **Backtrack** from dead ends when a path is evaluated as unpromising.

### When ToT Helps

ToT is most valuable for problems where:

- The solution space has many possible paths, some of which are dead ends.
- There is a clear way to evaluate intermediate progress (e.g., mathematical constraints, puzzle validity).
- The cost of exploring multiple paths is justified by the difficulty of the problem.

Examples include mathematical proofs, constraint satisfaction problems, and creative planning tasks where the first idea is often not the best.

### The Cost Tradeoff

ToT is significantly more expensive than linear CoT. Each branch of the tree requires LLM calls for both generation and evaluation. A tree with branching factor 3 and depth 4 might require dozens of LLM calls for a single problem. This makes ToT impractical for routine tasks but valuable for high-stakes problems where correctness matters more than cost.

## Extended Thinking in Claude

### How It Works

Anthropic's extended thinking is a reasoning capability built directly into Claude models. "Extended thinking gives Claude enhanced reasoning capabilities for complex tasks, while providing varying levels of transparency into its step-by-step thought process before it delivers its final answer" [src-001].

When extended thinking is enabled, "Claude creates thinking content blocks where it outputs its internal reasoning. Claude incorporates insights from this reasoning before crafting a final response" [src-001]. The API response contains two types of content blocks:

1. **Thinking blocks**: The model's internal reasoning, returned before the final answer.
2. **Text blocks**: The final response that incorporates insights from the reasoning.

Each thinking block includes a cryptographic `signature` field that verifies the block was genuinely produced by Claude. This signature is required when passing thinking blocks back to the API in multi-turn conversations -- particularly during tool-use loops where reasoning continuity matters.

### Summarized vs. Full Thinking

An important distinction across model generations:

- **Claude Sonnet 3.7**: Returns full, unabridged thinking output. You see exactly what the model reasoned through.
- **Claude 4 models and later**: Return summarized thinking. The model still performs full reasoning internally, but the API returns a condensed version. You are billed for the full thinking tokens, not the summary. The summarization is performed by a separate model and preserves the key ideas with minimal added latency.

This means the visible token count in the response will not match the billed output token count for Claude 4+ models. The full reasoning happens, and you pay for it, but what you see is a summary.

### Thinking Block Preservation Across Turns

How thinking blocks persist across conversation turns also varies by model:

| Behavior | Models |
|----------|--------|
| Thinking blocks removed from prior turns | Claude Sonnet 3.7, Claude 4 through Opus 4.1, Sonnet 4.5 |
| Thinking blocks preserved by default | Claude Opus 4.5, Claude Sonnet 4.6, Claude Opus 4.6 |

Preservation in Opus 4.5+ means thinking blocks from earlier assistant turns stay in context, which enables better cache hits during tool-use loops and maintains richer conversational context. The tradeoff is that long conversations consume more context space since thinking blocks are retained.

## Controlling Reasoning Depth

### Budget Tokens (Manual Mode)

For models that support manual extended thinking (primarily Claude Sonnet 4.6 and earlier Claude 4 models), you control reasoning depth with the `budget_tokens` parameter:

```json
{
  "thinking": {
    "type": "enabled",
    "budget_tokens": 10000
  }
}
```

The `budget_tokens` value sets the maximum number of tokens Claude can use for internal reasoning. Key details:

- **Minimum**: 1,024 tokens.
- **Practical range**: Start at 10K-16K for moderate tasks; use 32K+ for genuinely hard problems.
- **Diminishing returns**: Claude often does not use the entire budget, especially above 32K. Increasing the budget beyond what the task requires adds latency without improving quality.
- **Must be less than `max_tokens`**: The budget is part of your overall output token allocation.

### Adaptive Thinking (Opus 4.6)

Claude Opus 4.6 introduces adaptive thinking, which replaces manual budget management:

```json
{
  "thinking": {
    "type": "adaptive"
  }
}
```

With adaptive thinking, the model automatically determines how much reasoning to apply based on the complexity of the task. For simple questions, it may think briefly or not at all. For complex problems, it engages in extensive deliberation. This eliminates the guesswork of choosing a budget and makes Opus 4.6 particularly effective as a general-purpose model -- it allocates effort proportionally.

Manual mode (`type: "enabled"` with `budget_tokens`) is deprecated on Opus 4.6 and will be removed in a future release.

### The Effort Parameter

Adaptive thinking can be further tuned using the `effort` parameter, which provides a high-level control over how much reasoning the model applies without requiring you to specify exact token counts. This gives developers a middle ground between fully automatic allocation and manual token budgeting.

## Interleaved Thinking

### Reasoning Between Tool Calls

Standard extended thinking produces a single thinking block at the start of the model's response. Interleaved thinking extends this: Claude can reason after receiving each tool result, producing additional thinking blocks between tool calls.

Without interleaved thinking:

```
[thinking] -> [tool_use] -> tool_result -> [tool_use] -> tool_result -> [text]
                                           ^ no reasoning here
```

With interleaved thinking:

```
[thinking] -> [tool_use] -> tool_result -> [thinking] -> [tool_use] -> tool_result -> [thinking] -> [text]
                                           ^ reasons about result    ^ reasons again
```

This is critical for agentic workflows. Without interleaved thinking, the model must decide its entire plan upfront. With it, the model can adapt its approach based on what each tool call returns -- closer to how a human developer works.

### Model Support for Interleaved Thinking

- **Opus 4.6**: Automatic with adaptive thinking. No beta header needed.
- **Sonnet 4.6**: Supported via the `interleaved-thinking-2025-05-14` beta header, or automatic with adaptive thinking.
- **Other Claude 4 models** (Opus 4.5, Opus 4.1, Opus 4, Sonnet 4.5, Sonnet 4): Requires the `interleaved-thinking-2025-05-14` beta header.

With interleaved thinking enabled, the `budget_tokens` parameter represents the total budget across all thinking blocks within one assistant turn, not per-block. The budget can also exceed `max_tokens` in this mode, since the effective limit becomes the full context window.

## When to Use Extended Thinking

### Tasks That Benefit Most

Extended thinking shows the largest improvements on tasks that require deliberate, multi-step reasoning:

- **Complex mathematics**: Multi-step proofs, optimization problems, competition-style math.
- **Difficult coding**: Architectural decisions, subtle bug diagnosis, complex refactoring where understanding the full codebase context matters.
- **Multi-step analysis**: Tasks that require synthesizing information from many sources, weighing tradeoffs, or following a complex logical chain.
- **Constrained generation**: Producing output that must satisfy multiple simultaneous constraints (e.g., writing code that matches a spec while maintaining backward compatibility).
- **Ambiguous or nuanced tasks**: Problems where the right approach is not obvious and the model benefits from exploring different angles before committing.

### Tasks Where It Adds Little Value

Extended thinking adds latency and cost. For the following task types, it provides little or no benefit:

- **Simple classification**: Sentiment analysis, intent detection, basic categorization.
- **Straightforward extraction**: Pulling structured data from unstructured text.
- **Formatting and transformation**: Converting between formats, simple text editing.
- **Short factual questions**: Questions with direct, well-known answers.
- **High-volume, low-complexity tasks**: Anything where latency or cost per call dominates.

For these tasks, a model without extended thinking (or Haiku) is the right choice.

## Comparing Reasoning Approaches

### CoT Prompting vs. Extended Thinking vs. Reasoning Models

These three approaches represent different points on a spectrum:

| Dimension | CoT Prompting | Extended Thinking (Claude) | Reasoning Models (o1-style) |
|-----------|---------------|---------------------------|----------------------------|
| **Mechanism** | Prompt technique ("think step by step") | Built-in reasoning mode with thinking blocks | End-to-end trained for reasoning |
| **Training** | No special training required | Model trained to leverage thinking blocks | Specifically trained with reasoning objectives |
| **Visibility** | Full -- reasoning is in the output | Summarized (Claude 4+) or full (3.7) | Varies; often hidden |
| **Control** | Prompt-level only | Budget tokens, adaptive, effort parameter | Limited (model decides) |
| **Cost** | Output tokens for reasoning text | Billed for full thinking tokens | Typically higher per-token |
| **Quality ceiling** | Limited by model's base capability | Higher -- model is optimized for this mode | Highest for pure reasoning tasks |
| **Flexibility** | Works with any LLM | Claude-specific | Provider-specific |

The key tradeoff: CoT prompting is universal and free (beyond token cost), extended thinking is more powerful but Claude-specific, and dedicated reasoning models may excel at narrow reasoning benchmarks but offer less control and transparency.

### When to Use Which

- **CoT prompting**: When you need reasoning from a model that does not support dedicated reasoning modes, or when the task is simple enough that a prompting trick suffices.
- **Extended thinking**: When you are using Claude and need higher-quality reasoning with control over depth. The default choice for complex tasks in Claude.
- **Reasoning models**: When pure reasoning performance is the primary metric and you are willing to accept less control over the process.

In practice, extended thinking with Claude often matches or exceeds reasoning model performance on practical tasks (coding, analysis, planning) while offering more transparency and control.

## Context Window Implications

### How Thinking Tokens Interact with Context

Thinking tokens have a specific relationship with the context window that is important to understand:

- **Current turn**: Thinking tokens count against your `max_tokens` limit for that turn. If you set `max_tokens: 16000` and `budget_tokens: 10000`, you have at most 6,000 tokens for the actual text response (in practice, Claude manages this allocation intelligently).
- **Previous turns**: In models prior to Opus 4.5, thinking blocks from previous turns are stripped and do not count toward your context window. In Opus 4.5+, they are preserved by default.
- **Strict enforcement**: Unlike older Claude models that silently adjusted limits, Claude 3.7+ enforces `max_tokens` strictly. If `prompt_tokens + max_tokens` exceeds the context window, the API returns an error rather than silently truncating.

The effective context window calculation with thinking enabled:

```
context_window = (input_tokens - previous_thinking_tokens) + max_tokens
```

With tool use, thinking tokens from the current tool-use loop remain in context:

```
context_window = (input_tokens + current_turn_thinking_tokens + tool_tokens) + max_tokens
```

### Practical Impact

For long conversations or agentic workflows with many tool calls:

- Monitor token usage actively, especially when thinking blocks are preserved (Opus 4.5+).
- Use the token counting API to get accurate counts before making requests.
- Consider that interleaved thinking accumulates thinking tokens across all tool calls in a single turn.
- For thinking budgets above 32K, use batch processing to avoid HTTP timeout issues.

## Practical Considerations

### Prompt Engineering for Extended Thinking

Extended thinking works best when:

- The prompt clearly defines the problem and what constitutes a good answer.
- You avoid over-constraining the reasoning process (let the model think naturally).
- You provide all necessary context upfront rather than requiring the model to ask for clarification.
- For complex tasks, you describe the desired output structure so the model can plan toward it.

### Feature Constraints

Extended thinking has several compatibility constraints:

- **Temperature**: Cannot be modified when thinking is enabled. The model uses a fixed sampling strategy.
- **top_k**: Not compatible with thinking.
- **top_p**: Can be set between 0.95 and 1.0 only.
- **Response prefilling**: Cannot pre-fill responses when thinking is enabled.
- **Forced tool use**: Incompatible -- only `tool_choice: "auto"` or `tool_choice: "none"` work with thinking.

### Cost and Latency Considerations

- You are billed for full thinking tokens, even though you only see summaries (Claude 4+).
- Extended thinking adds wall-clock time, sometimes significantly for complex problems.
- For latency-sensitive applications, consider whether the quality improvement justifies the wait.
- Prompt caching helps reduce costs for repeated system prompts and tool definitions, but cache breakpoints for messages are invalidated when thinking parameters change.

### Thinking Redaction

Occasionally, Claude's internal reasoning triggers safety system flags. When this happens, some or all of a thinking block is returned encrypted as a `redacted_thinking` block. The encrypted content is not human-readable but can be passed back to the API, where it is decrypted to maintain reasoning continuity. Applications should handle this gracefully rather than treating it as an error.

## Further Reading

- [Anthropic Extended Thinking Documentation](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking) - Official guide [src-001]
- [Chain-of-Thought Paper (Wei et al., 2022)](https://arxiv.org/abs/2201.11903) - The foundational CoT paper [src-002]
- [Let's Verify Step by Step (Lightman et al., 2023)](https://arxiv.org/abs/2305.20050) - Process vs. outcome supervision [src-003]
- [Tree of Thoughts (Yao et al., 2023)](https://arxiv.org/abs/2305.10601) - Structured reasoning search [src-004]
- [The Claude Model Family](claude-model-family.md) - Model tiers and extended thinking support per tier
- [LLM Agent Architectures](../agents/agent-architectures.md) - How reasoning patterns fit into agent design
- [Claude Code Architecture](../agentic-coding/claude-code-architecture.md) - Extended thinking in agentic coding workflows
