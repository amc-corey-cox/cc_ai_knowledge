---
id: kb-2025-013
title: "Claude Code Architecture: How an Agentic Coding Tool Works"
created: 2026-02-19
updated: 2026-02-19

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "Claude Code Documentation"
    url: "https://code.claude.com/docs"
    accessed: 2026-02-19
    quotes:
      - text: "Claude Code is an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools."
        location: "Overview page"
      - text: "Each surface connects to the same underlying Claude Code engine, so your CLAUDE.md files, settings, and MCP servers work across all of them."
        location: "Overview page"

  - id: src-002
    type: primary
    title: "Building Effective Agents"
    authors: ["Anthropic"]
    url: "https://www.anthropic.com/engineering/building-effective-agents"
    accessed: 2026-02-19
    quotes:
      - text: "Agents are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."
        location: "What are agents?"
      - text: "Maintain simplicity in your agent's design."
        location: "Summary"

  - id: src-003
    type: secondary
    title: "Using CLAUDE.MD Files: Customizing Claude Code for Your Codebase"
    url: "https://claude.com/blog/using-claude-md-files"
    accessed: 2026-02-19
    quotes:
      - text: "Think of it as a configuration file that Claude automatically incorporates into every conversation."
        location: "Introduction"
      - text: "Your CLAUDE.md file becomes part of Claude's system prompt. Every conversation starts with this context already loaded."
        location: "How CLAUDE.md works"

topics:
  - agentic-coding
  - coding-agents
  - agents
  - tool-use
  - context-management

confidence: high
verified: false
verified_by: unverified
verification_notes: "AI-assisted draft; quotes sourced from documentation but need human verification"

ai_metadata:
  model: claude-opus-4-6
  generation_date: 2026-02-19
  reviewed_by: pending
---

# Claude Code Architecture: How an Agentic Coding Tool Works

## Overview

Claude Code is "an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools" [src-001]. It is a concrete, production implementation of the agent architectures described in [LLM Agent Architectures and Patterns](../agents/agent-architectures.md) -- specifically, it runs a ReAct-style loop where a language model repeatedly reasons about a coding task, takes actions through tools, observes the results, and decides what to do next.

What makes Claude Code architecturally interesting is not that it invented a new agent paradigm but that it applies a well-understood one (the agentic loop) to the specific domain of software engineering, with careful attention to safety, context management, and developer ergonomics. Anthropic's own guidance is to "maintain simplicity in your agent's design" [src-002], and Claude Code follows this principle: a single model in a single loop, with a rich but straightforward set of tools.

This article examines the key architectural components: the agentic loop, the tool system, the permission model, hooks, context management, and the CLAUDE.md instruction layer.

## The Agentic Loop

### From Theory to Practice

"Agents are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks" [src-002]. In [LLM Agent Architectures](../agents/agent-architectures.md), the core agent loop is described as:

```
while not done:
    observation = perceive(environment)
    thought = reason(observation, memory, goal)
    action = decide(thought)
    result = execute(action)
    memory = update(memory, result)
```

Claude Code implements exactly this pattern. When you give it a task -- "refactor this function to use async/await" or "find and fix the bug in the auth module" -- the model enters a loop:

1. **Read/perceive**: Examine relevant files, search the codebase, check error output
2. **Reason**: Analyze the code, form a plan, identify what needs to change
3. **Act**: Edit files, run commands, create new files
4. **Observe**: Check the results -- did the edit parse? did the tests pass?
5. **Continue or finish**: Decide whether more work is needed or the task is complete

The model controls the loop. There is no external orchestrator deciding the next step -- Claude itself determines which tool to call, what arguments to pass, and when the task is done. This is what distinguishes an agent from a pipeline: the LLM is in the driver's seat.

### Single Loop, Not Multi-Agent

Unlike some coding systems that use multiple specialized agents (a planner, a coder, a reviewer), Claude Code uses a single model in a single loop. This keeps the architecture simple and avoids the coordination overhead of multi-agent systems (see [Multi-Agent Systems](../agents/multi-agent-systems.md)). The same Claude model that plans the change also writes the code and verifies the result.

This design choice reflects a practical tradeoff. Multi-agent architectures can offer specialization and parallelism, but they introduce message-passing complexity, potential for conflicting actions, and harder debugging. For an interactive developer tool where a human is watching and can intervene, a single coherent loop is easier to understand and steer.

## The Tool System

### Built-In Tools

The tool system is how Claude Code interacts with the development environment. Following the general tool use protocol described in [Tool Use and Function Calling](../agents/tool-use-function-calling.md), Claude Code provides the model with a set of tool definitions -- names, descriptions, and parameter schemas -- and the model generates structured tool calls during its reasoning loop.

Claude Code ships with a focused set of built-in tools:

| Tool | Purpose |
|------|---------|
| **Read** | Read file contents, with optional line range |
| **Write** | Create or overwrite files |
| **Edit** | Make targeted string replacements in existing files |
| **Bash** | Execute shell commands |
| **Glob** | Find files by name pattern |
| **Grep** | Search file contents with regex |
| **WebFetch** | Retrieve and process web content |
| **WebSearch** | Search the web for information |
| **NotebookEdit** | Edit Jupyter notebook cells |

These tools are deliberately atomic -- each does one thing well. The `Edit` tool performs exact string replacement rather than rewriting entire files, which reduces the risk of unintended changes. The `Bash` tool provides general-purpose command execution for anything the specialized tools do not cover: running tests, installing dependencies, using git, invoking language-specific toolchains.

### Tool Design Philosophy

The tool set reflects Anthropic's "maintain simplicity" principle [src-002]. Rather than providing hundreds of specialized tools (one for each git operation, one for each file system operation), Claude Code provides a small number of general tools and trusts the model to compose them. Need to run tests? Use Bash with `pytest`. Need to check git status? Use Bash with `git status`. Need to find a function definition? Use Grep with a regex pattern.

This composability is a strength. The model does not need to learn a large custom API -- it can leverage its broad knowledge of command-line tools and programming languages to accomplish virtually any development task through Bash alone, with the specialized tools (Read, Edit, Glob, Grep) offering optimized paths for the most common operations.

### MCP: Extending the Tool System

Beyond built-in tools, Claude Code supports the **Model Context Protocol** (MCP) for connecting to external tool servers. MCP is an open standard that lets developers expose custom tools, resources, and prompts through a client-server architecture (see [Model Context Protocol](../protocols/model-context-protocol.md)).

"Each surface connects to the same underlying Claude Code engine, so your CLAUDE.md files, settings, and MCP servers work across all of them" [src-001]. This means MCP servers configured for Claude Code work regardless of whether you are using the CLI, an IDE extension, or another integration surface. The tool system is the same engine underneath.

MCP servers can provide tools for anything: querying databases, interacting with project management systems, accessing internal documentation, or connecting to specialized development infrastructure. This extensibility means Claude Code's tool set is open-ended without the core tool system needing to grow.

## The Permission Model

### Safety-First Design

A coding agent that can read any file, edit any file, and run any shell command is powerful but dangerous. Claude Code addresses this with a tiered permission model that balances autonomy with safety.

The model has three operating tiers for tool execution:

**Tier 1: Always Allowed (Read-Only)**
Tools that only observe the environment -- reading files, searching code, listing directories -- run without any confirmation. These operations cannot modify state and are safe to execute automatically.

**Tier 2: Auto-Edit (Confirm on Write)**
File modifications (Write, Edit) can be configured to run with or without confirmation. In the default mode, Claude Code asks for permission before making edits. In more permissive modes, edits proceed automatically while still requiring confirmation for shell commands.

**Tier 3: Full Autonomy (YOLO Mode)**
In fully autonomous mode, all operations -- including shell commands -- proceed without confirmation. This is useful for trusted, well-scoped tasks but removes the human-in-the-loop safety net.

### Why Tiers Matter

The permission model is not just a UX convenience -- it is a safety architecture. Shell commands are the most dangerous tool because they have unbounded side effects: a `rm -rf` can delete your project, a `curl | bash` can execute arbitrary code, a `git push --force` can destroy shared history.

By defaulting to confirmation for destructive operations and letting users opt into more autonomy as they build trust, Claude Code follows the principle of least privilege. The human remains in the loop for high-stakes actions unless they explicitly choose otherwise.

This mirrors the "tool use with confirmation" pattern described in [Tool Use and Function Calling](../agents/tool-use-function-calling.md): the agent proposes actions, the human approves or rejects, and execution proceeds accordingly.

## Hooks: Programmatic Control Points

### Pre- and Post-Action Hooks

Hooks provide a programmatic extension point in the agentic loop. They are user-defined scripts or commands that run at specific points during Claude Code's execution:

- **Pre-tool hooks**: Run before a tool executes, with the ability to block the action
- **Post-tool hooks**: Run after a tool completes, with access to the result

Hooks receive structured JSON input describing the tool call (tool name, parameters, and for post-hooks, the result) and can:
- Allow the action to proceed
- Block the action with an error message
- Log or audit the action
- Transform inputs or outputs

### Use Cases

Hooks serve several practical purposes:

**Custom Validation**: Enforce project-specific rules. For example, a pre-hook on the Bash tool could block any command that modifies the production database, or a pre-hook on Edit could reject changes to files in a protected directory.

**Audit Logging**: Record every tool invocation for compliance or debugging. Post-hooks can log what Claude Code did, enabling replay and review of agent sessions.

**Automated Formatting**: A post-hook on Write or Edit could automatically run a code formatter (like `black` or `prettier`) on any file Claude Code modifies, ensuring all changes conform to project style.

**Notification**: Post-hooks can send notifications when the agent completes certain actions, integrating Claude Code into broader development workflows.

### Hooks vs. Permissions

Hooks and the permission model are complementary. The permission model provides coarse-grained safety tiers (allow, confirm, auto-allow). Hooks provide fine-grained, programmable control. A team might run in a permissive mode for speed while using hooks to enforce specific safety boundaries -- blocking certain shell commands, preventing edits to certain files, or requiring that all database migrations include a rollback step.

## Context Management

### The 200K Token Window

Claude Code operates within a 200K token context window. For a coding agent, this window must hold:
- The system prompt (including CLAUDE.md instructions)
- The conversation history (user messages and agent responses)
- Tool call inputs and outputs (file contents, command output, search results)
- The model's own reasoning

For small tasks, 200K tokens is more than sufficient. But for complex, multi-file tasks -- refactoring a large module, debugging an issue that spans many files, or implementing a feature that touches dozens of files -- the context window can fill up.

### Compaction

When the context window fills, Claude Code performs **compaction**: summarizing the conversation history to free up space while retaining the most important information. This is analogous to the "summarized/compressed memory" pattern described in [LLM Agent Architectures](../agents/agent-architectures.md).

Compaction is lossy by design. The summary captures what was done, what was learned, and what the current state of the task is, but it discards the detailed content of individual tool calls and reasoning steps. This means the agent may need to re-read files it previously examined, and subtle context from earlier in the conversation may be lost.

For more on context window strategies and their tradeoffs, see [Context Window Management](context-window-management.md).

### Memory Files

To persist information across compaction boundaries and even across separate conversations, Claude Code uses **memory files**. These are Markdown files (typically named `MEMORY.md`) stored in the project's `.claude/` directory or the user's home `~/.claude/` directory.

Memory files serve as external long-term memory. The agent can write important facts, decisions, and project-specific knowledge to memory files, and this information will be available in future sessions. This pattern -- using external storage to extend beyond the context window -- is a practical implementation of the episodic memory concept described in the agent architectures literature.

Common uses for memory files include:
- Recording project conventions discovered during work
- Noting which approaches were tried and failed
- Storing key architectural decisions and their rationale
- Tracking the state of multi-session tasks

## CLAUDE.md: The Instruction Layer

### What CLAUDE.md Does

CLAUDE.md is the mechanism by which developers configure Claude Code's behavior for their project. "Think of it as a configuration file that Claude automatically incorporates into every conversation" [src-003]. It is not a tool, a plugin, or a separate system -- it is simply a Markdown file whose contents become part of the model's context.

"Your CLAUDE.md file becomes part of Claude's system prompt. Every conversation starts with this context already loaded" [src-003]. This means the instructions in CLAUDE.md have the same weight as any other system prompt content: they shape the model's behavior, priorities, and constraints from the first turn of the conversation.

### The Layered Hierarchy

CLAUDE.md files can exist at multiple levels, and they stack:

1. **Project root** (`/project/CLAUDE.md`): Project-wide instructions, coding standards, architectural guidelines. Checked into version control and shared with the team.

2. **User global** (`~/.claude/CLAUDE.md`): Personal preferences that apply across all projects -- editor settings, communication style, workflow preferences.

3. **Project-specific user** (`~/.claude/projects/<project>/MEMORY.md`): Per-project personal notes and memory, not shared with the team.

4. **Parent directories**: CLAUDE.md files in parent directories are also loaded, allowing organization-wide or monorepo-wide instructions to be set once and inherited by all sub-projects.

When multiple CLAUDE.md files exist, they are concatenated into the system prompt. This layering means a team can set project-wide rules (in the repo root), individuals can customize their experience (in their home directory), and both coexist without conflict.

### What Goes in CLAUDE.md

Effective CLAUDE.md files typically include:

**Project context**: What the project is, what it does, key architectural decisions. This saves the agent from having to discover this information by reading code.

**Coding standards**: Preferred languages, frameworks, formatting rules, naming conventions. "Use functional components, not class components." "All Python code uses type hints." "Tests go in `__tests__/` directories."

**Workflow rules**: How to run tests, how to format commits, which branches to target, what CI checks must pass. These encode team practices that a new contributor (human or AI) would otherwise need to learn by asking.

**Safety boundaries**: Files or directories that should not be modified, commands that should not be run, architectural constraints that must be preserved.

**Tool guidance**: How to use project-specific tools, scripts, or build systems that the model might not know about.

### CLAUDE.md as Agent Configuration

From an architectural perspective, CLAUDE.md is a form of **prompt engineering that persists across sessions**. Unlike one-off instructions in a chat message, CLAUDE.md content is always present. This makes it the primary mechanism for shaping long-term agent behavior without modifying the model itself.

This is a deliberate design choice. Rather than building a complex configuration system with specialized DSLs or GUIs, Claude Code uses plain Markdown files that are human-readable, version-controllable, and editable with any text editor. The "configuration language" is natural language, which means the full expressiveness of human instruction is available.

## How the Pieces Fit Together

To understand Claude Code as a system, consider how the components interact during a typical task:

1. **Session starts**: CLAUDE.md files are loaded into the system prompt. Memory files provide context from prior sessions. The permission tier is set.

2. **User gives a task**: "Fix the failing tests in the auth module."

3. **Agentic loop begins**:
   - Claude reads the test output (Bash: `pytest tests/auth/`)
   - Observes which tests fail and why
   - Reads the relevant source files (Read tool)
   - Reasons about the cause of failure
   - Edits the source code (Edit tool)
   - Re-runs the tests to verify (Bash)
   - If tests still fail, iterates

4. **Permission checks**: Each tool call is checked against the permission tier. In default mode, edits proceed after confirmation; bash commands require approval.

5. **Hooks fire**: Pre-hooks validate proposed actions (e.g., blocking edits to protected files). Post-hooks run after actions complete (e.g., auto-formatting modified files).

6. **Context management**: If the conversation grows long, compaction summarizes earlier turns. Critical information is preserved in memory files.

7. **Task completes**: Claude reports what it did and what the result was.

The simplicity of this architecture -- one model, one loop, a handful of tools, layered configuration -- is what makes it work. There is no complex orchestration, no message-passing between agents, no separate planning and execution phases. The model handles all of it in a single coherent stream of reasoning and action.

## Practical Considerations

### Strengths of the Architecture

**Transparency**: Because there is one loop and the model's reasoning is visible, developers can follow what the agent is doing and why. This builds trust and makes debugging agent behavior straightforward.

**Composability**: The small, general tool set means Claude Code can handle tasks its designers did not specifically anticipate. Any command-line tool is available through Bash; any external service is accessible through MCP.

**Configurability without complexity**: CLAUDE.md provides powerful customization through natural language, avoiding the need for specialized configuration formats or APIs.

**Progressive trust**: The tiered permission model lets developers start cautious and increase autonomy as they gain confidence in the agent's behavior.

### Limitations

**Context window ceiling**: Even with compaction, 200K tokens limits the amount of codebase context the agent can hold simultaneously. Very large refactoring tasks may require the developer to break work into smaller pieces.

**Single-threaded reasoning**: The single-loop architecture means Claude Code works on one train of thought at a time. It cannot, for example, simultaneously explore two alternative approaches and compare them (as a Tree of Thoughts architecture might).

**Compaction is lossy**: After compaction, the agent may forget details from earlier in the conversation. Tasks that depend on precise recall of earlier context may need to be re-grounded.

**Latency**: Each step in the loop is an LLM inference call. Long agentic trajectories (20+ steps) take time, and the developer is waiting.

### When to Use an Agentic Coding Tool

Agentic coding tools like Claude Code are most valuable for tasks that require:
- Exploration across multiple files before making changes
- Iterative refinement (edit, test, fix, test again)
- Knowledge of the surrounding codebase to make correct changes
- Routine but tedious multi-file modifications

They are less suited for:
- Pure greenfield design (where the human should be driving architectural decisions)
- Tasks requiring understanding that spans more code than fits in the context window
- Situations where every action must be audited in real time (though hooks help here)

## Further Reading

- [Claude Code Documentation](https://code.claude.com/docs) - Official reference [src-001]
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) - Anthropic's agent design philosophy [src-002]
- [Using CLAUDE.md Files](https://claude.com/blog/using-claude-md-files) - Guide to configuration [src-003]
- [LLM Agent Architectures and Patterns](../agents/agent-architectures.md) - The theoretical foundations
- [Tool Use and Function Calling](../agents/tool-use-function-calling.md) - How tool use works in general
- [Model Context Protocol](../protocols/model-context-protocol.md) - The MCP extension system
- [Context Window Management](context-window-management.md) - Strategies for working within token limits
- [CLAUDE.md and Agent Configuration](claude-md-agent-configuration.md) - Deep dive into the instruction layer
