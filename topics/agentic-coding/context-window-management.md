---
id: kb-2025-015
title: "Context Window Management for Coding Agents"
created: 2026-02-19
updated: 2026-02-19

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "Lost in the Middle: How Language Models Use Long Contexts"
    authors: ["Liu et al."]
    url: "https://arxiv.org/abs/2307.03172"
    accessed: 2026-02-19
    published: 2023-07-06
    arxiv: "2307.03172"
    quotes:
      - text: "Performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts."
        location: "Abstract"
  - id: src-002
    type: primary
    title: "Claude Code Documentation"
    url: "https://code.claude.com/docs"
    accessed: 2026-02-19
    quotes:
      - text: "The system will automatically compress prior messages in your conversation as it approaches context limits."
        location: "System prompt"
  - id: src-003
    type: primary
    title: "Claude Models Overview"
    url: "https://docs.anthropic.com/en/docs/about-claude/models"
    accessed: 2026-02-19
    quotes:
      - text: "Claude Opus 4.6 and Sonnet 4.6 support a 1M token context window when using the context-1m-2025-08-07 beta header."
        location: "Latest models comparison footnote"
  - id: src-004
    type: primary
    title: "Building Effective Agents"
    authors: ["Anthropic"]
    url: "https://www.anthropic.com/engineering/building-effective-agents"
    accessed: 2026-02-19
    quotes:
      - text: "Give the model enough tokens to think before it writes itself into a corner."
        location: "Appendix 2: Prompt engineering your tools"

topics:
  - context-management
  - agentic-coding
  - agents
  - optimization

confidence: high
verified: false
verified_by: unverified
verification_notes: "AI-assisted draft; quotes sourced from papers and docs but need human verification against originals"

ai_metadata:
  model: claude-opus-4-6
  generation_date: 2026-02-19
  reviewed_by: pending
---

# Context Window Management for Coding Agents

## Overview

Context window management is one of the most consequential and least visible challenges in agentic coding. An LLM-based coding agent lives and dies by what fits in its context window -- the finite buffer of tokens the model can attend to at any given time. Every file read, every tool result, every reasoning step consumes tokens from this budget. Run out, and the agent loses the thread of what it was doing. Waste tokens on irrelevant information, and the agent drowns in noise.

For coding agents like Claude Code, effective context management means the difference between an agent that completes a complex multi-file refactoring and one that forgets what it was doing halfway through. This article covers the mechanics of context windows, the research on their limitations, and the practical strategies that make agentic coding sessions productive.

## Context Window Fundamentals

### What Tokens Are

A token is the fundamental unit of text that an LLM processes. Tokens are not characters and not words -- they are subword units produced by a tokenizer (typically BPE or SentencePiece). In English, a rough heuristic is 1 token per 4 characters, or about 0.75 words per token. Code tends to tokenize less efficiently than prose because of special characters, indentation, and naming conventions.

The context window is measured in tokens. Every piece of information the model works with -- the system prompt, conversation history, tool definitions, file contents, tool results, and the model's own output -- must fit within this window.

### Current Context Window Sizes

Claude models currently support a 200K token standard context window. For applications that need more, "Claude Opus 4.6 and Sonnet 4.6 support a 1M token context window when using the context-1m-2025-08-07 beta header" [src-003]. Claude Code uses the extended context to accommodate longer coding sessions.

To put 200K tokens in perspective: that is roughly 150,000 words, or about 500 pages of text. A 1M token context is approximately 750,000 words. That sounds like a lot, but a moderately complex codebase can easily have hundreds of files, each consuming thousands of tokens. A single large file read can use 5,000-10,000 tokens, and tool results accumulate fast in an agentic loop.

### Input vs. Output Tokens

Context windows have two components:

- **Input tokens**: Everything the model reads -- system prompt, conversation history, tool definitions, and tool results. These are the "given" context.
- **Output tokens**: Everything the model generates -- reasoning, tool calls, and responses. These are produced by the model and also consume context space.

In an agentic coding session, input tokens dominate early (reading files, absorbing context), while output tokens accumulate as the agent generates plans, code, and tool calls. Both count against the same window limit.

## The "Lost in the Middle" Problem

Liu et al. demonstrated a significant limitation of how LLMs process long contexts: "Performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts" [src-001].

This has direct implications for coding agents:

- **System prompts and recent messages get the most attention**. Instructions at the top and the latest tool results are best retained.
- **Mid-conversation context is most vulnerable**. A file read from 50 turns ago may be poorly recalled even if it is still technically in the window.
- **Recency bias is real**. The model attends more strongly to recent context, which means early decisions and observations can be effectively "forgotten" even before compaction occurs.

### What This Means in Practice

Consider a coding agent that reads 15 files to understand a codebase, then starts making changes. By the time it is editing the 8th file, the contents of the first few files may be in the "lost middle" zone -- present in the context but poorly attended to. This can lead to:

- Inconsistent changes across files (forgetting conventions seen earlier)
- Re-reading files the agent already read (wasting tokens to compensate)
- Losing track of the overall plan in favor of the immediate task

The practical remedy is to structure sessions so that the most critical information is either at the beginning (system prompt, CLAUDE.md) or refreshed near the end (re-reading a key file before editing it).

## Compaction Strategies

### Automatic Compaction in Claude Code

When a conversation approaches the context limit, Claude Code does not simply truncate. Instead, "the system will automatically compress prior messages in your conversation as it approaches context limits" [src-002]. This compression (called "compaction") summarizes earlier parts of the conversation to free up token space while preserving the essential information.

Compaction is lossy by design. The model produces a summary of what happened, what was decided, and what the current state is, then discards the original verbose history. This means:

- Exact file contents from earlier reads are lost (only summaries remain)
- Specific error messages or stack traces may be paraphrased
- The overall trajectory and key decisions are preserved
- Tool results are summarized rather than retained verbatim

### Manual Compaction

Users can trigger compaction explicitly with the `/compact` command in Claude Code, optionally providing a focus prompt (e.g., `/compact focus on the database migration work`). This is useful when:

- You know you are about to start a new phase of work and want a clean slate
- The conversation has accumulated irrelevant context (exploration, dead ends)
- You want to bias the summary toward specific aspects of the work

### Surviving Compaction

Compaction can disrupt work in progress if the agent was relying on details that get summarized away. Strategies to mitigate this:

1. **Persistent memory files**: Store critical context in CLAUDE.md or project memory files so it survives compaction (see Memory Systems below).
2. **Re-read before editing**: If the agent needs exact file contents, re-read the file rather than relying on a compacted summary.
3. **Checkpoint progress**: For multi-step tasks, commit intermediate work so the agent can recover context from the actual codebase state rather than from memory.

## Token Efficiency

Efficient token usage extends how far a session can go before compaction is needed. Every wasted token is a tax on the agent's working memory.

### Structuring Sessions for Efficiency

- **Be specific in requests**. "Fix the authentication bug in `src/auth.py`" is more token-efficient than "there's a bug somewhere in the auth system, can you find and fix it?" The latter requires exploratory reads that consume context.
- **Provide file paths when you know them**. Letting the agent search for files (glob, grep) costs tokens for the search results. Pointing directly to the relevant file skips that overhead.
- **Break large tasks into focused sessions**. A single session that refactors 30 files will hit context limits. Three sessions that each handle 10 files will each have more working room.

### Avoiding Re-reads

One of the most common sources of token waste is reading the same file multiple times. This happens when:

- The agent reads a file, does other work, then needs the file again but has lost the details to the "lost in the middle" effect
- Compaction summarized a file's contents and the agent needs exact content again
- The agent reads an entire file when only a specific function was needed

Targeted tool calls help: reading specific line ranges or grepping for specific patterns uses fewer tokens than reading entire files.

### Tool Call Efficiency

Anthropic advises to "give the model enough tokens to think before it writes itself into a corner" [src-004]. This applies symmetrically: give the agent enough context to act, but not so much that it drowns.

- **Prefer grep over cat**. Searching for a pattern returns only relevant lines, not entire files.
- **Use glob patterns to narrow searches**. `**/*.py` is better than searching everything.
- **Read specific line ranges** when you know approximately where the relevant code is.
- **Avoid redundant tool calls**. If the agent just read a file, it should not need to read it again immediately.

## Memory Systems

Context windows are ephemeral -- they exist only for the duration of a conversation. Memory systems provide persistence across sessions.

### CLAUDE.md as Persistent Memory

The `CLAUDE.md` file (at the project root, in `~/.claude/CLAUDE.md`, or in subdirectories) serves as persistent memory that is loaded into every conversation's system prompt. This is the single most important tool for surviving context limits because:

- It is always at the **beginning** of the context (best attention position per [src-001])
- It survives compaction (it is re-injected, not summarized)
- It persists across sessions (it is a file, not conversation state)

Effective CLAUDE.md content includes:

- Project conventions and architecture decisions
- Common commands (test, build, lint)
- File organization and naming patterns
- Known gotchas and workarounds

### Project Memory Files

Claude Code supports project-specific memory in `~/.claude/projects/<project>/memory/`. These files are also injected into the system prompt but are private to the user (not checked into the repository). They are useful for personal workflow notes, learned preferences, and session-specific context that should not be in the shared CLAUDE.md.

### Auto-Memory

Claude Code can automatically update memory files when it learns something important during a session. For example, if the agent discovers that a project uses a non-standard test runner, it can store that fact in memory so future sessions do not need to rediscover it. This creates a feedback loop where the agent's context management improves over time.

### The Memory Hierarchy

Information flows through several layers, each with different persistence and token cost:

```
System prompt (CLAUDE.md, memory files)   -- persistent, always loaded
   |
Conversation context                      -- session-scoped, compactable
   |
Tool results                              -- ephemeral, most verbose
   |
Compaction summaries                      -- lossy, replaces conversation
```

The goal is to push important information upward in this hierarchy. If something matters across sessions, it belongs in CLAUDE.md. If it only matters within a session, it can stay in conversation context. If it is only needed momentarily, a tool result suffices.

## Prompt Caching

Prompt caching is an API-level optimization that reduces the cost of repeated context. When the same prefix of tokens appears across multiple API calls (which happens constantly in agentic loops, since the system prompt and early conversation are stable), the provider can cache the KV computations for those tokens.

### How Cache Breakpoints Work

Cache breakpoints mark positions in the prompt where caching should apply. Everything before the breakpoint is cached on the first call and reused on subsequent calls. This dramatically reduces latency and cost for the stable portions of the context (system prompt, tool definitions, CLAUDE.md).

### When Caching Invalidates

The cache is prefix-based: if any token before the breakpoint changes, the entire cache invalidates. This means:

- Editing CLAUDE.md invalidates the cache (the system prompt prefix changes)
- Adding new tool definitions can invalidate if they appear before the breakpoint
- Conversation messages after the breakpoint do not affect caching

In practice, Claude Code manages cache breakpoints automatically. The user does not need to configure them, but understanding the mechanism explains why the first message in a session is slower (cache cold) and subsequent messages are faster (cache warm).

## Extended Thinking and Context

### Thinking Tokens vs. Context Tokens

Extended thinking (also called "reasoning tokens") gives the model a scratchpad for internal reasoning before producing a response. These thinking tokens are generated by the model and visible to the user but, in most models, are **not** carried forward into subsequent turns (Opus 4.5+ preserves them by default; see [Extended Thinking and Reasoning](../ai-fundamentals/extended-thinking-reasoning.md)).

This distinction matters for context management:

- **Thinking tokens are billed** as output tokens, even though Claude 4+ returns only summaries. You pay for the full reasoning.
- **In most models, thinking tokens do not accumulate** across turns -- each turn's thinking starts fresh. This means they do not fill up the context window over time (Opus 4.5+ is the exception, where thinking blocks persist).
- **Context tokens** (conversation history, tool results) always accumulate and consume the context window.
- Heavy use of extended thinking increases per-turn cost and latency but (in most models) does not fill the context window. Heavy use of verbose tool results does.

### Thinking Budget Management

The thinking budget controls how many tokens the model can use for internal reasoning on each turn. A higher budget allows deeper analysis but increases latency and cost per turn. The budget does not affect context window consumption across turns.

For complex coding tasks (understanding a new codebase, planning a large refactoring), a generous thinking budget helps the model reason through the problem before acting. For simple tasks (renaming a variable, fixing a typo), a lower budget or no extended thinking is sufficient.

## Practical Session Structuring

### The Single-Focus Session

The most context-efficient pattern: one session, one task, one clear goal.

```
1. Agent reads CLAUDE.md (automatic)
2. Agent reads the 2-3 files relevant to the task
3. Agent makes changes
4. Agent runs tests
5. Agent commits (if asked)
```

This fits comfortably in a 200K window for most tasks and rarely triggers compaction.

### The Multi-Phase Session

For larger work, break the session into phases with natural compaction points:

```
Phase 1: Exploration
  - Read files, understand the codebase
  - Compact with focus: "summarize the architecture and the plan"

Phase 2: Implementation
  - Work from the compacted summary + re-reading files as needed
  - Compact when context fills up

Phase 3: Testing and Cleanup
  - Run tests, fix issues
  - Final commit
```

Each phase starts with a relatively clean context that includes the essential summary from the previous phase.

### Using Worktrees for Isolation

Git worktrees provide a complementary form of isolation. By working in a separate worktree, the agent's changes are isolated from the main branch. This means:

- The agent can commit intermediate work without polluting the main branch
- If a session goes wrong, the worktree can be discarded
- Multiple sessions can work on different tasks in parallel without context interference

Worktrees do not directly affect context management, but they reduce the cognitive overhead of managing branch state within a session.

### When to Start a New Session

Start a new session when:

- The task is complete and you are moving to unrelated work
- Multiple compactions have occurred and the summary has drifted
- The agent is re-reading files it has already read multiple times
- The agent seems confused about what it was doing (a sign of context degradation)

## Practical Considerations

### Monitoring Context Usage

Claude Code displays a context usage indicator showing how full the context window is. Watching this helps you anticipate compaction and decide when to break work into a new session. A session at 80% context is likely to compact soon, which may disrupt complex in-progress work.

### The Cost Dimension

Context window usage directly affects cost. Larger contexts mean more input tokens processed per API call, and in agentic loops, this compounds -- each turn includes the entire conversation history. Efficient context management is not just about capability; it is about economics.

A session with 100K tokens of context costs roughly twice as much per turn as a session with 50K tokens. Over a 30-turn agentic session, the cumulative difference is substantial.

### Common Anti-Patterns

- **The kitchen sink session**: Trying to do everything in one session until context overflows
- **Excessive exploration**: Reading every file in a directory "just in case" instead of targeted searches
- **Ignoring compaction signals**: Continuing complex work after compaction without verifying the summary captured the essential context
- **Not using CLAUDE.md**: Repeating the same instructions every session instead of storing them persistently

## Further Reading

- [Lost in the Middle (Liu et al.)](https://arxiv.org/abs/2307.03172) - Context position effects on LLM performance [src-001]
- [Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents) - Agent design principles [src-004]
- [Claude Code Architecture](claude-code-architecture.md) - How Claude Code structures its agent loop
- [CLAUDE.md and Agent Configuration](claude-md-agent-configuration.md) - Persistent memory through instruction files
- [Claude Model Family](../ai-fundamentals/claude-model-family.md) - Context window sizes across models
- [Extended Thinking and Reasoning](../ai-fundamentals/extended-thinking-reasoning.md) - Thinking tokens and budget management
