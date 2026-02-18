---
id: kb-2025-008
title: "Tool Use and Function Calling"
created: 2025-02-10
updated: 2025-02-10

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "Toolformer: Language Models Can Teach Themselves to Use Tools"
    authors: ["Schick et al."]
    url: "https://arxiv.org/abs/2302.04761"
    accessed: 2025-02-10
    published: 2023-02-09
    quotes:
      - text: "We introduce Toolformer, a model trained to decide which APIs to call, when to call them, what arguments to pass, and how to best incorporate the results into future token prediction."
        location: "Abstract"
      - text: "Each API call is represented as a tuple (a_c, i_c) where a_c is the name of the API and i_c is the corresponding input."
        location: "Section 2 - Approach"

  - id: src-002
    type: primary
    title: "Gorilla: Large Language Model Connected with Massive APIs"
    authors: ["Patil et al."]
    url: "https://arxiv.org/abs/2305.15334"
    accessed: 2025-02-10
    published: 2023-05-24
    quotes:
      - text: "Gorilla enables LLMs to use tools by invoking APIs. Given a natural language query, Gorilla can write semantically- and syntactically-correct API calls."
        location: "Abstract"

  - id: src-003
    type: primary
    title: "Anthropic Tool Use Documentation"
    url: "https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview"
    accessed: 2025-02-10
    quotes:
      - text: "Tools are defined by providing Claude with the tool name, a description of what it does, and a JSON Schema for the tool's parameters."
        location: "How tool use works"

  - id: src-004
    type: primary
    title: "OpenAI Function Calling Documentation"
    url: "https://platform.openai.com/docs/guides/function-calling"
    accessed: 2025-02-10

  - id: src-005
    type: primary
    title: "Berkeley Function-Calling Leaderboard"
    authors: ["Yan et al."]
    url: "https://gorilla.cs.berkeley.edu/leaderboard.html"
    accessed: 2025-02-10

topics:
  - agents
  - tool-use
  - function-calling
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

# Tool Use and Function Calling

## Overview

Tool use is the mechanism by which LLMs interact with the external world — searching the web, reading files, executing code, calling APIs. It transforms a language model from a text generator into an agent that can take real actions.

The core idea is simple: instead of only generating text, the model can also generate structured requests to external tools, receive results, and incorporate those results into its reasoning.

## How Tool Use Works

### The Basic Protocol

Most tool use implementations follow the same pattern:

1. **Define tools**: Tell the model what tools are available, with names, descriptions, and parameter schemas
2. **Model decides**: Given a user request and available tools, the model either responds directly or generates a tool call
3. **Execute**: The system (not the model) executes the tool call
4. **Return results**: Tool output is sent back to the model as a new message
5. **Continue**: The model reasons about the results and either makes another tool call or produces a final response

This is a **cooperative protocol** — the model proposes actions, the system executes them. The model never directly runs code or accesses external systems.

### Tool Definitions

Tools are specified as structured schemas. In the Anthropic API, "tools are defined by providing Claude with the tool name, a description of what it does, and a JSON Schema for the tool's parameters" [src-003]. For example:

```json
{
  "name": "search",
  "description": "Search the web for current information",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The search query"
      }
    },
    "required": ["query"]
  }
}
```

The quality of tool descriptions matters enormously — the model uses them to decide when and how to call each tool. Vague descriptions lead to misuse; overly restrictive descriptions lead to underuse.

### Function Calling vs. Tool Use

These terms are used almost interchangeably. "Function calling" (OpenAI's original terminology) and "tool use" (Anthropic's terminology) describe the same capability. The model generates a structured JSON object representing a function/tool invocation, and the caller executes it.

Some providers also support "parallel tool use" (multiple tool calls in a single turn) and "forced tool use" (requiring the model to use a specific tool).

## Approaches to Teaching Tool Use

### Fine-Tuning (Toolformer)

Schick et al. "introduce Toolformer, a model trained to decide which APIs to call, when to call them, what arguments to pass, and how to best incorporate the results into future token prediction" [src-001].

Toolformer's approach was self-supervised:
1. Sample potential API call positions in training text
2. Execute the calls and check if including the results reduces perplexity
3. Fine-tune the model on examples where tools helped

"Each API call is represented as a tuple (a_c, i_c) where a_c is the name of the API and i_c is the corresponding input" [src-001]. The model learns to emit special tokens that trigger tool execution inline with text generation.

### In-Context Learning (Prompting)

Most production systems don't fine-tune for tool use. Instead, tool definitions are injected into the system prompt, and the model learns the calling convention from examples and instructions. This is more flexible (tools can change per request) but depends on the model's instruction-following ability.

### Specialized Training (Gorilla)

Gorilla was trained specifically on API documentation to generate correct API calls. "Given a natural language query, Gorilla can write semantically- and syntactionally-correct API calls" [src-002]. This approach fine-tunes on a curated dataset of API docs and usage examples.

## Tool Use Patterns

### Single-Shot Tool Use

The simplest pattern: user asks a question, model makes one tool call, returns the answer. Good for lookup tasks.

```
User: What's the weather in Portland?
Model: [calls weather_api(location="Portland, OR")]
System: {"temp": 45, "conditions": "rainy"}
Model: It's 45°F and rainy in Portland.
```

### Chained Tool Use

Multiple sequential tool calls where each informs the next. The model reasons about intermediate results to decide the next action.

```
User: Find the bug in my test failures.
Model: [calls read_file("tests/test_auth.py")]
Model: [calls read_file("src/auth.py")]  # informed by test file contents
Model: [calls search_code("validate_token")]  # investigating a function
Model: The bug is on line 42...
```

### Parallel Tool Use

When the model needs multiple pieces of independent information, it can issue several tool calls simultaneously. This reduces latency significantly for tasks like "check the status of these three services."

### Tool Use with Confirmation

For high-stakes actions (deleting files, sending emails, modifying databases), the system can require human confirmation before executing. The model proposes the action, the human approves or rejects, and execution proceeds accordingly.

## Practical Considerations

### Tool Design Principles

- **Clear names**: `search_web` over `sw` — the model reads these
- **Descriptive parameters**: Include `description` fields in the schema, not just type constraints
- **Atomic operations**: Each tool should do one thing well
- **Informative errors**: Return structured error messages the model can reason about
- **Minimal side effects**: Prefer read operations; make writes explicit and confirmable

### Common Failure Modes

- **Hallucinated tools**: The model calls a tool that doesn't exist
- **Wrong parameters**: Correct tool, incorrect arguments (especially types)
- **Over-use**: Using a tool when the model already knows the answer
- **Under-use**: Answering from training data when it should verify with a tool
- **Infinite loops**: Repeatedly calling the same tool with the same arguments

### Evaluation

The [Berkeley Function-Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) [src-005] tracks model accuracy on tool use across categories:
- **AST accuracy**: Does the generated call parse correctly?
- **Exec accuracy**: Does it produce the right result when executed?
- **Relevance detection**: Does the model correctly identify when no tool is needed?

## The MCP Protocol

The **Model Context Protocol** (MCP) is an open standard for connecting LLMs to external tools and data sources. Rather than each application implementing its own tool integration, MCP provides a unified protocol so tools can be written once and used by any MCP-compatible client.

MCP uses a client-server architecture:
- **MCP servers** expose tools, resources, and prompts
- **MCP clients** (like Claude Code, IDEs, or custom apps) connect to servers and make tools available to the model

This standardizes the "plumbing" of tool use so developers can focus on building useful tools rather than integration code.

## Further Reading

- [Toolformer Paper](https://arxiv.org/abs/2302.04761) - Self-supervised tool learning [src-001]
- [Gorilla Paper](https://arxiv.org/abs/2305.15334) - API-focused tool use [src-002]
- [Anthropic Tool Use Docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) [src-003]
- [Berkeley Function-Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) [src-005]
- [LLM Agent Architectures](agent-architectures.md) - How tool use fits into agent patterns
- [Multi-Agent Systems](multi-agent-systems.md) - Tools shared across agents
