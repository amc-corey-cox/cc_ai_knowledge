---
id: kb-2025-018
title: "Model Context Protocol (MCP)"
created: 2026-02-19
updated: 2026-02-19

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "Model Context Protocol Specification"
    url: "https://spec.modelcontextprotocol.io/specification/2025-03-26/"
    accessed: 2026-02-19
    quotes:
      - text: "MCP follows a client-server architecture where an MCP host establishes connections to one or more MCP servers."
        location: "Architecture - Participants"

  - id: src-002
    type: primary
    title: "Model Context Protocol - Introduction"
    url: "https://modelcontextprotocol.io/introduction"
    accessed: 2026-02-19
    quotes:
      - text: "MCP (Model Context Protocol) is an open-source standard for connecting AI applications to external systems."
        location: "Introduction"
      - text: "Think of MCP like a USB-C port for AI applications. Just as USB-C provides a standardized way to connect electronic devices, MCP provides a standardized way to connect AI applications to external systems."
        location: "Introduction"

  - id: src-003
    type: primary
    title: "MCP Architecture Overview"
    url: "https://modelcontextprotocol.io/docs/learn/architecture"
    accessed: 2026-02-19
    quotes:
      - text: "MCP focuses solely on the protocol for context exchange—it does not dictate how AI applications use LLMs or manage the provided context."
        location: "Scope"
      - text: "MCP defines three core primitives that servers can expose: Tools, Resources, and Prompts."
        location: "Architecture Overview"

topics:
  - mcp
  - protocols
  - tool-use
  - agents

confidence: high
verified: false
verified_by: unverified
verification_notes: "AI-assisted draft; quotes sourced from official MCP documentation but need human verification"

ai_metadata:
  model: claude-opus-4-6
  generation_date: 2026-02-19
  reviewed_by: pending
---

# Model Context Protocol (MCP)

## Overview

The Model Context Protocol (MCP) is "an open-source standard for connecting AI applications to external systems" [src-002]. It defines a uniform way for AI-powered applications to discover and interact with tools, data sources, and prompt templates without requiring bespoke integration code for each combination of client and server.

The simplest way to understand MCP is through analogy: "Think of MCP like a USB-C port for AI applications. Just as USB-C provides a standardized way to connect electronic devices, MCP provides a standardized way to connect AI applications to external systems" [src-002]. Before USB-C, every device had its own proprietary connector. Before MCP, every AI application implemented its own tool integration layer. MCP replaces that N-times-M integration problem with a single protocol that any client and any server can speak.

### Why MCP Matters

Without a standard protocol, tool integration is fragile and duplicative. Every AI application that wants to read files, query databases, or interact with APIs must build its own connectors. Every tool provider must build separate integrations for each application. MCP breaks this coupling:

- **Tool authors** write one MCP server and it works with any MCP-compatible client
- **Application developers** add MCP client support once and gain access to the entire ecosystem of MCP servers
- **End users** can mix and match tools and applications without waiting for specific integrations

This is the same dynamic that made HTTP transformative: a standard protocol enables an ecosystem far larger than any single organization could build.

### What MCP Is Not

It is important to understand the boundaries of the protocol. "MCP focuses solely on the protocol for context exchange -- it does not dictate how AI applications use LLMs or manage the provided context" [src-003]. MCP does not:

- Define how models reason about or select tools
- Specify how context should be injected into prompts
- Mandate any particular LLM or inference strategy
- Replace existing tool-use APIs (it complements them)

MCP is purely about the plumbing between applications and external capabilities. What the application does with those capabilities is entirely up to the application.

## Architecture

### The Three Participants

"MCP follows a client-server architecture where an MCP host establishes connections to one or more MCP servers" [src-001]. There are three distinct roles in the architecture:

**Host** -- The user-facing application that wants to leverage external tools and data. Examples include Claude Desktop, an IDE with AI features, or a custom AI workflow tool. The host is responsible for:
- Managing the lifecycle of MCP client instances
- Controlling which servers are connected and what permissions they have
- Mediating between the LLM and the MCP clients
- Enforcing security policies and user consent

**Client** -- A protocol-level component that maintains a 1:1 connection with a single MCP server. Each client instance handles the JSON-RPC communication, capability negotiation, and message routing for its server. Hosts typically create one client per connected server. The client is usually invisible to end users -- it is infrastructure that the host manages internally.

**Server** -- A lightweight process or service that exposes specific capabilities through the MCP protocol. A server might provide access to a filesystem, a database, a web API, a code interpreter, or any other external system. Servers are designed to be focused and composable -- one server per concern, rather than monolithic servers that do everything.

### How They Fit Together

A typical deployment looks like this:

```
                    +-----------+
                    |   Host    |  (e.g., Claude Desktop, an IDE)
                    |           |
                    | +-------+ |      +------------------+
                    | |Client1|-------->| Server: filesystem|
                    | +-------+ |      +------------------+
                    |           |
                    | +-------+ |      +------------------+
                    | |Client2|-------->| Server: database  |
                    | +-------+ |      +------------------+
                    |           |
                    | +-------+ |      +------------------+
                    | |Client3|-------->| Server: web-search |
                    | +-------+ |      +------------------+
                    +-----------+
```

The host creates a client for each server it connects to. When the LLM needs to use a tool, the host routes the request through the appropriate client to the right server. The host aggregates capabilities from all connected servers and presents them to the LLM as a unified set of available tools, resources, and prompts.

## Protocol Layers

MCP is structured into two layers: the **data layer** and the **transport layer**. This separation mirrors how HTTP separates the application protocol from the underlying TCP transport.

### Data Layer (JSON-RPC 2.0)

The data layer uses JSON-RPC 2.0 as its message format. Every interaction between client and server is a JSON-RPC message -- either a request (expecting a response), a notification (fire-and-forget), or a response. This gives MCP a well-understood, language-agnostic wire format with built-in support for request/response correlation, error handling, and asynchronous notifications.

A typical tool call over MCP looks like:

```json
// Client -> Server (request)
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": {
      "path": "/home/user/config.yaml"
    }
  }
}

// Server -> Client (response)
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "database:\n  host: localhost\n  port: 5432"
      }
    ]
  }
}
```

### Transport Layer

The transport layer defines how JSON-RPC messages are physically transmitted between client and server. MCP supports two primary transport mechanisms:

**stdio** -- For local servers running as child processes. The host spawns the server process and communicates over stdin/stdout. This is the simplest and most common transport for local tool servers. There is no network overhead, no authentication complexity, and the server lifecycle is tied to the host. Most MCP servers used with desktop applications (like Claude Desktop or Claude Code) use stdio transport.

**Streamable HTTP** -- For remote servers accessible over the network. The client connects to an HTTP endpoint. The server can use Server-Sent Events (SSE) to stream responses back to the client. This transport supports remote deployment, multi-tenant servers, and integration with existing HTTP infrastructure (load balancers, API gateways, authentication proxies). As of the current specification (2025-03-26), Streamable HTTP is the standard network transport, replacing an earlier SSE-only transport from prior revisions.

The choice of transport is transparent to the higher protocol layers. A tool call works the same way regardless of whether the server is a local process or a remote service -- only the connection setup differs.

## Core Primitives

"MCP defines three core primitives that servers can expose: Tools, Resources, and Prompts" [src-003]. These primitives represent the three fundamental types of capability a server can offer.

### Tools

Tools are executable functions that the LLM can invoke to perform actions or retrieve computed results. They are the most commonly used primitive and the closest analog to traditional function calling.

Each tool has a name, a description (used by the LLM to understand when and how to use it), and a JSON Schema defining its input parameters. The server executes the tool and returns structured results.

Examples of tools:
- `read_file` -- Read the contents of a file from disk
- `execute_sql` -- Run a SQL query against a database
- `create_issue` -- Create an issue in a project tracker
- `search_web` -- Search the internet for information

Tools are **model-controlled**: the LLM decides when to call them based on the user's request and the tool descriptions. The host may require human confirmation before executing certain tools, but the selection logic is driven by the model.

### Resources

Resources represent data that can be read by the client. Unlike tools, resources are identified by URIs and are meant for data retrieval rather than computation or side effects. Think of resources as the "nouns" of MCP, while tools are the "verbs."

Resources use URI schemes to identify what they provide:
- `file:///home/user/document.txt` -- A local file
- `postgres://localhost/mydb/users` -- A database table
- `github://repo/owner/issues` -- GitHub issues

Resources can be static (their content is known ahead of time) or dynamic (generated on request). They support subscription, so clients can be notified when resource content changes.

Resources are **application-controlled**: the host application decides which resources to include in the LLM's context, often based on user actions like selecting a file or opening a project.

### Prompts

Prompts are reusable templates that define structured interactions. A server can expose prompt templates that clients can present to users or inject into conversations. Prompts can include parameters that are filled in at invocation time.

For example, a code review server might expose a prompt template:

```
name: "review-code"
description: "Review code for bugs and style issues"
arguments:
  - name: "code"
    description: "The code to review"
    required: true
  - name: "language"
    description: "Programming language"
    required: false
```

Prompts are **user-controlled**: the user explicitly selects which prompt to use, often through a UI affordance like a slash command or menu.

### Control Model Summary

The three primitives differ in who controls their invocation:

| Primitive | Controlled by | Analogy |
|-----------|--------------|---------|
| Tools     | LLM (model)  | Functions the AI can call |
| Resources | Application   | Data the app provides to the AI |
| Prompts   | User          | Templates the user selects |

This separation of control is deliberate -- it ensures that high-agency actions (tools) go through the model's reasoning, data selection (resources) is managed by the application, and interaction patterns (prompts) are chosen by the human.

## Client Primitives

In addition to the server-side primitives, MCP defines capabilities that clients can expose back to servers.

### Sampling

Sampling allows a server to request that the client perform an LLM inference. This enables sophisticated agentic patterns where a tool server can ask the host's LLM to reason about intermediate results without the server needing its own LLM access. The host always mediates sampling requests and can enforce policies (rate limits, content filtering, user approval) before forwarding them to the model.

### Elicitation

Elicitation allows a server to request structured input from the user through the host application. When a server needs information it cannot determine programmatically -- such as a confirmation, a choice between options, or a missing credential -- it can send an elicitation request. The host renders an appropriate UI element and returns the user's response. This keeps the user in the loop for decisions that require human judgment.

### Logging

Servers can emit structured log messages back to the client for debugging and observability. Log messages include severity levels and can carry arbitrary data. The host decides how to surface these -- in a debug console, a log file, or not at all.

## Connection Lifecycle

An MCP connection follows a well-defined lifecycle with four phases.

### 1. Initialization

When a client connects to a server, they exchange initialization messages. The client sends its protocol version and declared capabilities. The server responds with its own protocol version and capabilities. This handshake ensures both sides agree on what features are available before any real work begins.

### 2. Capability Negotiation

During initialization, both client and server declare which optional features they support. A server might declare that it supports tools and resources but not prompts. A client might declare that it supports sampling but not elicitation. This negotiation allows both minimal and full-featured implementations to interoperate -- a simple server does not need to implement every primitive.

### 3. Operation

After initialization, the connection is in the operation phase. The client can discover available tools, resources, and prompts, then invoke them as needed. The server can send notifications (such as resource-change events or log messages). This phase lasts as long as the connection is active.

### 4. Shutdown

Either side can terminate the connection. For stdio transport, this typically means the host terminates the server process. For HTTP transport, the client closes the connection. Clean shutdown allows both sides to release resources gracefully.

## Security Considerations

MCP introduces a significant attack surface because it connects LLMs to external systems with real-world effects. The specification and ecosystem address this through several mechanisms.

### Permission Models

Hosts are expected to implement permission controls that govern what servers can do. Common patterns include:

- **Per-tool approval**: The host prompts the user before executing each tool call (or each new type of tool call)
- **Allowlists**: Only pre-approved tools can be invoked without confirmation
- **Scoped access**: Servers are limited to specific directories, databases, or API endpoints

The key principle is that the host is the trust boundary. Servers should not be trusted implicitly -- the host mediates all interactions and enforces the user's security preferences.

### OAuth for Remote Servers

When using Streamable HTTP transport with remote servers, MCP supports OAuth 2.1 for authentication. This allows servers to verify the identity of connecting clients and enforce access controls. The OAuth flow is handled at the transport layer, so the MCP data layer does not need to be aware of authentication details.

### Prompt Injection and Trust

Because MCP servers provide content that enters the LLM's context, they are a potential vector for prompt injection attacks. A malicious or compromised server could return tool results that attempt to manipulate the model's behavior. Hosts should treat server output with the same caution as any untrusted input -- sandboxing, content validation, and clear provenance tracking all help mitigate this risk.

### Principle of Least Privilege

MCP servers should request only the minimum capabilities they need. A file-reading server should not also request write access. A search server should not request filesystem access. The protocol's capability negotiation supports this by allowing fine-grained declaration of what each server offers and requires.

## MCP in Practice

### The Ecosystem Today

MCP has seen rapid adoption since its release. Major AI applications including Claude Desktop, Claude Code, Cursor, Windsurf, and various IDE extensions support MCP clients. The server ecosystem spans hundreds of community-built servers covering databases, cloud platforms, developer tools, productivity apps, and more.

### Building an MCP Server

Building an MCP server is straightforward with the official SDKs (available for TypeScript, Python, Java, Kotlin, C#, and other languages). A minimal server:

1. Declares its capabilities (which primitives it supports)
2. Registers tool/resource/prompt handlers
3. Implements the transport layer (stdio or HTTP)

The SDKs handle the JSON-RPC plumbing, capability negotiation, and lifecycle management, so server authors can focus on the domain logic.

### Composability

One of MCP's strengths is composability. A host can connect to many servers simultaneously, and the LLM sees a unified set of capabilities. This enables workflows like:

- A coding agent using filesystem + git + code search + documentation servers
- A data analysis agent using database + visualization + notebook servers
- A DevOps agent using cloud provider + monitoring + incident management servers

Each server is a focused, reusable building block. The LLM orchestrates them based on the task at hand.

## Practical Considerations

### When to Use MCP

MCP is a good fit when:
- You want to expose capabilities to multiple AI applications without building separate integrations
- You need a standard interface for tool discovery and invocation
- You are building an AI application that should be extensible by third parties
- You want to separate tool implementation from the AI application that uses it

MCP may be unnecessary when:
- You have a single application with a fixed, small set of tools (direct function calling is simpler)
- The tool integration is purely internal and will never be reused
- You need extremely low-latency tool calls where the JSON-RPC overhead matters

### Relationship to Function Calling

MCP and function calling (see [Tool Use and Function Calling](../agents/tool-use-function-calling.md)) are complementary, not competing. Function calling is the mechanism by which an LLM generates structured tool invocations. MCP is the protocol for discovering, connecting to, and communicating with the actual tool implementations. In a typical MCP-enabled application:

1. The host discovers available tools from connected MCP servers
2. Tool descriptions are passed to the LLM as function definitions
3. The LLM uses function calling to select and parameterize a tool
4. The host routes the call through the appropriate MCP client to the server
5. The server executes the tool and returns results via MCP
6. Results are fed back to the LLM

### Debugging and Development

The MCP ecosystem includes an Inspector tool that allows developers to connect to a server, browse its capabilities, and invoke tools interactively. This is invaluable for development and debugging. The structured logging primitive also helps -- servers can emit detailed logs that the Inspector or host application can surface.

## Further Reading

- [MCP Specification](https://spec.modelcontextprotocol.io/specification/2025-03-26/) - Full protocol specification [src-001]
- [MCP Introduction](https://modelcontextprotocol.io/introduction) - Official overview and motivation [src-002]
- [MCP Architecture](https://modelcontextprotocol.io/docs/learn/architecture) - Detailed architecture documentation [src-003]
- [Tool Use and Function Calling](../agents/tool-use-function-calling.md) - How LLMs invoke tools
- [Claude Code Architecture](../agentic-coding/claude-code-architecture.md) - An MCP-enabled agentic coding tool
- [MCP Server Development](mcp-server-development.md) - Building your own MCP servers
