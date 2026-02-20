---
id: kb-2025-020
title: "The Claude Model Family"
created: 2026-02-19
updated: 2026-02-19

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "Claude Models Overview"
    url: "https://docs.anthropic.com/en/docs/about-claude/models"
    accessed: 2026-02-19
    quotes:
      - text: "Claude is a family of state-of-the-art large language models developed by Anthropic."
        location: "Introduction"
      - text: "The most intelligent model for building agents and coding"
        location: "Latest models comparison - Claude Opus 4.6 description"
      - text: "The best combination of speed and intelligence"
        location: "Latest models comparison - Claude Sonnet 4.6 description"
      - text: "The fastest model with near-frontier intelligence"
        location: "Latest models comparison - Claude Haiku 4.5 description"
  - id: src-002
    type: primary
    title: "Anthropic Extended Thinking Documentation"
    url: "https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking"
    accessed: 2026-02-19
    quotes:
      - text: "Extended thinking gives Claude enhanced reasoning capabilities for complex tasks, while providing varying levels of transparency into its step-by-step thought process before it delivers its final answer."
        location: "Introduction"

topics:
  - model-families
  - ai-fundamentals
  - agents

confidence: high
verified: false
verified_by: unverified
verification_notes: "AI-assisted draft; quotes sourced from Anthropic documentation but need human verification"

ai_metadata:
  model: claude-opus-4-6
  generation_date: 2026-02-19
  reviewed_by: pending
---

# The Claude Model Family

## Overview

"Claude is a family of state-of-the-art large language models developed by Anthropic" [src-001]. Rather than a single model, Claude is a tiered product line where each tier makes a different tradeoff between capability, speed, and cost. Understanding these tiers and their characteristics is essential for selecting the right model for a given task -- whether that task is a quick classification, a complex multi-step coding workflow, or a long-running agentic process.

The Claude family follows a naming convention: the **name** indicates the capability tier (Opus, Sonnet, Haiku), and the **version number** indicates the generation. As of early 2026, the current generation spans Claude 4.6 (Opus and Sonnet) and Claude 4.5 (Haiku), reflecting Anthropic's rapid iteration cadence.

## The Three Tiers

### Opus: Maximum Capability

Claude Opus is the most powerful tier in the family. Anthropic describes Opus 4.6 as "the most intelligent model for building agents and coding" [src-001]. It is the model you reach for when accuracy, nuance, and deep reasoning matter more than speed or cost.

Opus excels at:
- Complex, multi-step agentic workflows that require sustained reasoning over long trajectories
- Difficult coding tasks: architectural decisions, large refactors, subtle bug diagnosis
- Tasks requiring careful analysis of lengthy documents or codebases
- Problems where getting the answer right on the first try saves more than the extra cost

The tradeoff is straightforward: Opus is slower and more expensive than the other tiers. For tasks where a simpler model would suffice, using Opus wastes time and money.

### Sonnet: The Balanced Choice

Claude Sonnet occupies the middle ground. Anthropic positions Sonnet 4.6 as "the best combination of speed and intelligence" [src-001]. In practice, Sonnet is the default choice for most production workloads because it provides strong reasoning at a fraction of Opus's cost and latency.

Sonnet handles well:
- Day-to-day coding assistance: writing functions, explaining code, generating tests
- Content generation and editing
- Data analysis and summarization
- Multi-step tasks that don't require Opus-level reasoning depth
- High-throughput applications where latency matters

For many tasks, the quality difference between Sonnet and Opus is negligible. The skill is knowing when you actually need Opus.

### Haiku: Speed and Efficiency

Claude Haiku is the fastest and cheapest tier. Anthropic describes Haiku 4.5 as "the fastest model with near-frontier intelligence" [src-001]. Haiku is designed for high-volume, latency-sensitive applications where cost efficiency is paramount.

Haiku is the right choice for:
- Real-time classification and routing (e.g., deciding which tier should handle a request)
- Simple extraction and formatting tasks
- High-volume processing where per-call cost dominates
- Interactive applications requiring sub-second responses
- Lightweight summarization and labeling

Haiku is not a toy model. "Near-frontier intelligence" means it handles a surprisingly wide range of tasks well. The key constraint is that it has less headroom for complex reasoning chains compared to Sonnet and Opus.

## Current Generation Specifications

### Context Windows

All current Claude models support a 200K token context window as the standard offering. For Opus 4.6 and Sonnet 4.6, a 1M token context window is available in beta, which enables processing of very large codebases, lengthy documents, or extended conversation histories in a single call.

The 200K standard window is already substantial -- roughly equivalent to a medium-sized novel or a significant portion of a codebase. The 1M beta extends this to scenarios like analyzing entire repositories or processing book-length documents without chunking.

### Maximum Output Tokens

Output limits vary by tier:

| Model | Max Output Tokens |
|-------|-------------------|
| Opus 4.6 | 128K |
| Sonnet 4.6 | 64K |
| Haiku 4.5 | 64K |

Opus 4.6's 128K output limit is particularly relevant for agentic coding workflows where the model may need to produce large code files, detailed architectural plans, or extended multi-step responses.

### Pricing

Pricing follows the tiered structure (per million tokens):

| Model | Input | Output |
|-------|-------|--------|
| Opus 4.6 | $5 | $25 |
| Sonnet 4.6 | $3 | $15 |
| Haiku 4.5 | $1 | $5 |

These per-million-token rates apply regardless of context window size -- the 1M beta context does not change per-token pricing, only the maximum tokens per request.

The 5x difference between Haiku and Opus output pricing makes tier selection economically significant at scale. A workflow that processes thousands of requests per day will see meaningful cost differences. Prompt caching and batching can further reduce effective costs across all tiers.

## Key Capabilities

### Extended Thinking

"Extended thinking gives Claude enhanced reasoning capabilities for complex tasks, while providing varying levels of transparency into its step-by-step thought process before it delivers its final answer" [src-002]. This is one of the most important capabilities in the current Claude generation.

Extended thinking works differently across tiers:

- **Opus 4.6**: Supports **adaptive thinking**, where the model automatically determines how much reasoning to apply based on task complexity. For simple questions, it may think briefly or not at all. For complex problems, it may engage in extended internal deliberation. This makes Opus particularly effective as a general-purpose agent -- it allocates reasoning effort proportionally.

- **Sonnet 4.6**: Supports extended thinking with **manual budget control**. Developers set a thinking budget (minimum and maximum tokens), and the model reasons within those bounds. This gives precise control over the cost/quality tradeoff but requires the developer to estimate appropriate reasoning depth.

- **Haiku 4.5**: Does not support extended thinking. Haiku is optimized for speed, and the overhead of extended reasoning would undermine its primary value proposition.

The practical impact of extended thinking is substantial. Tasks that benefit from "thinking before answering" -- math problems, code debugging, complex analysis -- see significant quality improvements when extended thinking is enabled. For more detail, see [Extended Thinking and Reasoning](extended-thinking-reasoning.md).

### Vision (Multimodal Input)

All current Claude models accept image inputs alongside text. This enables:
- Analyzing screenshots, diagrams, and charts
- Reading text from images (OCR-like capability)
- Understanding UI mockups and wireframes
- Processing photographs for description or analysis

Vision is available across all three tiers, though Opus and Sonnet provide more nuanced image understanding for complex visual reasoning tasks.

### Multilingual Support

Claude models support a broad range of languages for both input and output. While English is the strongest language across all tiers, the models handle major world languages competently for translation, content generation, and analysis tasks.

### Tool Use and Function Calling

All Claude tiers support tool use (function calling), which is the foundation for agentic behavior. The model can be given descriptions of available tools and will generate structured calls to those tools, process the results, and continue reasoning. This capability is what enables Claude to power coding assistants, research agents, and other autonomous systems.

Opus 4.6 is particularly strong at complex tool-use patterns: knowing when to use which tool, chaining multiple tool calls effectively, and recovering from tool-call errors. See [Tool Use and Function Calling](../agents/tool-use-function-calling.md) for a detailed treatment.

## Model Selection Guidance

Choosing the right tier is one of the most consequential decisions when building with Claude. Here is a practical framework:

### Use Opus 4.6 When:
- Building agentic systems that run autonomously for many steps
- The task involves complex reasoning that directly impacts outcomes (e.g., code that must be correct)
- You need the highest accuracy on first attempt (retry cost exceeds tier cost difference)
- Working with very long contexts where maintaining coherence over 100K+ tokens matters
- The task requires sophisticated judgment (e.g., architectural decisions, nuanced analysis)

### Use Sonnet 4.6 When:
- Building production applications with moderate complexity
- You need a good balance of quality and throughput
- The task is well-defined and doesn't require frontier-level reasoning
- Cost matters but quality can't be sacrificed entirely
- You're building interactive features where response time affects user experience

### Use Haiku 4.5 When:
- Processing high volumes of relatively simple tasks
- Latency is critical (real-time applications, interactive UIs)
- The task is classification, extraction, or formatting
- You're building a routing layer that decides which tier to use for subsequent calls
- Cost is the primary constraint and task complexity is low

### The Cascade Pattern

A common production architecture uses multiple tiers in a cascade:
1. **Haiku** classifies incoming requests by complexity
2. **Sonnet** handles the majority of requests
3. **Opus** handles only the requests that Haiku identified as complex

This pattern optimizes cost while maintaining quality where it matters. The routing step (Haiku) adds minimal latency and cost, but prevents expensive Opus calls on tasks that Sonnet handles equally well.

## Evolution of the Claude Family

### From Claude 3 to Claude 4.6

The Claude family has evolved rapidly:

- **Claude 3** (early 2024): Introduced the three-tier naming (Opus, Sonnet, Haiku) and established the capability hierarchy. Claude 3 Opus was the first model widely recognized as competitive with GPT-4.

- **Claude 3.5** (mid-late 2024): Significant capability jump. Claude 3.5 Sonnet became a standout model, often matching or exceeding Claude 3 Opus performance at much lower cost. This generation demonstrated that the middle tier could advance faster than the top tier.

- **Claude 4** (2025): Continued the performance trajectory with improvements in coding, instruction following, and agentic reliability. Introduced extended thinking capabilities.

- **Claude 4.5** (late 2025): Brought Haiku up to near-frontier capability, making the cheapest tier viable for a much broader range of tasks.

- **Claude 4.6** (early 2026): The current generation for Opus and Sonnet. Opus 4.6 introduced adaptive thinking and pushed the frontier for agentic coding. Sonnet 4.6 further closed the gap with Opus for most practical tasks.

### The Trend

Two patterns stand out across generations:

1. **The middle tier improves fastest**: Each Sonnet generation has leapfrogged the previous Opus. Today's Sonnet is better than yesterday's Opus at a fraction of the cost. This means the "default choice" keeps getting more capable.

2. **The capability floor rises**: Each Haiku generation is roughly comparable to the previous generation's Sonnet. This steady upward pressure means that even cost-optimized deployments get significantly more capable over time.

## Practical Considerations

### Latency Profiles

Latency varies significantly across tiers and configurations:
- **Haiku**: Fastest time-to-first-token and tokens-per-second. Suitable for real-time applications.
- **Sonnet**: Moderate latency. Acceptable for interactive use, noticeable for real-time streaming.
- **Opus**: Highest latency, especially with extended thinking enabled. Best for background/batch tasks or situations where quality justifies the wait.

When extended thinking is active, Opus may take significantly longer on complex prompts as it reasons through the problem. Thinking tokens are billed as output tokens (for Claude 4+, you pay for the full thinking even though only a summary is returned), so extended thinking increases both cost and wall-clock time.

### Rate Limits and Throughput

Higher tiers typically have lower rate limits. At scale, this means Haiku can handle higher request volumes. Production architectures should account for this when designing their tier routing logic.

### API Compatibility

All three tiers share the same API interface. Switching between tiers requires only changing the model identifier -- no code changes to tool definitions, system prompts, or response parsing. This makes it straightforward to experiment with different tiers during development and to implement dynamic tier selection in production.

### Prompt Caching

All current Claude models support prompt caching, which reduces cost and latency for repeated prefixes (e.g., system prompts, tool definitions, or shared context). This is particularly impactful for agentic workflows where the system prompt and tool definitions are identical across many calls.

## Further Reading

- [Anthropic Models Documentation](https://docs.anthropic.com/en/docs/about-claude/models) - Official model specifications [src-001]
- [Extended Thinking Documentation](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking) - Detailed guide to extended thinking [src-002]
- [Extended Thinking and Reasoning](extended-thinking-reasoning.md) - Deep dive into reasoning capabilities
- [Claude Code Architecture](../agentic-coding/claude-code-architecture.md) - How Claude powers agentic coding tools
- [Tool Use and Function Calling](../agents/tool-use-function-calling.md) - Foundation for agent capabilities
- [LLM Agent Architectures](../agents/agent-architectures.md) - Patterns for building with Claude agents
