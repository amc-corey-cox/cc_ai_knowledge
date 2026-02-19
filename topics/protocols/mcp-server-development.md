---
id: kb-2025-019
title: "Building MCP Servers"
created: 2026-02-19
updated: 2026-02-19

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "MCP Python SDK"
    url: "https://github.com/modelcontextprotocol/python-sdk"
    accessed: 2026-02-19
    quotes:
      - text: "The Model Context Protocol Python SDK provides a complete implementation of the MCP protocol, making it easy to build MCP servers and clients in Python."
        location: "README"
  - id: src-002
    type: primary
    title: "MCP TypeScript SDK"
    url: "https://github.com/modelcontextprotocol/typescript-sdk"
    accessed: 2026-02-19
    quotes:
      - text: "Official TypeScript SDK for the Model Context Protocol, providing server and client implementations with full protocol support."
        location: "README"
  - id: src-003
    type: primary
    title: "MCP Server Development Guide"
    url: "https://modelcontextprotocol.io/docs/develop/build-server"
    accessed: 2026-02-19
    quotes:
      - text: "Create MCP servers to expose your data and tools."
        location: "Introduction"
  - id: src-004
    type: primary
    title: "MCP Architecture Overview"
    url: "https://modelcontextprotocol.io/docs/learn/architecture"
    accessed: 2026-02-19
    quotes:
      - text: "MCP defines three core primitives that servers can expose: Tools, Resources, and Prompts."
        location: "Data Layer Protocol - Primitives"

topics:
  - mcp
  - protocols
  - tool-use
  - coding-agents

confidence: medium
verified: false
verified_by: unverified
verification_notes: "AI-assisted draft; quotes sourced from official docs and SDKs but need human verification"

ai_metadata:
  model: claude-opus-4-6
  generation_date: 2026-02-19
  reviewed_by: pending
---

# Building MCP Servers

## Overview

The Model Context Protocol (MCP) is an open standard that defines how AI applications connect to external tools and data sources. Instead of each AI client implementing bespoke integrations, MCP provides a uniform protocol so that a tool written once can be used by any compatible client -- Claude Code, IDE extensions, custom agent systems, and more.

Building an MCP server is the primary way developers extend AI capabilities with custom integrations. An MCP server is a program that exposes tools, resources, and prompts over a well-defined protocol. Clients discover what the server offers, invoke its capabilities, and incorporate results into the model's reasoning loop.

This article covers the practical side: how to structure a server, implement the three primitives, choose a transport, test it, and deploy it. For the protocol specification itself, see [Model Context Protocol](model-context-protocol.md).

## The Three Primitives

"MCP defines three core primitives that servers can expose: Tools, Resources, and Prompts" [src-004].

**Tools** are actions the model can invoke -- querying a database, calling an API, running a calculation, manipulating files. Each tool has a name, a description, and an input schema (JSON Schema). The description is critical: the model reads it to decide whether and how to use the tool.

**Resources** are data the model can read -- file contents, database records, configuration values. Unlike tools, resources are read-only and are used to provide context rather than trigger actions. Resources are identified by URIs and can be listed, read individually, or subscribed to for change notifications.

**Prompts** are reusable templates -- pre-built system prompts, conversation starters, or domain-specific instruction sets. They are the least commonly implemented primitive but valuable for servers that encapsulate domain expertise.

## SDK Options

### Python SDK

"The Model Context Protocol Python SDK provides a complete implementation of the MCP protocol, making it easy to build MCP servers and clients in Python" [src-001]. The package is available as `mcp` on PyPI.

The Python SDK offers two API levels:

- **FastMCP** (high-level): A decorator-based API that minimizes boilerplate. You define tools as plain Python functions with type hints, and the SDK handles schema generation, serialization, and protocol plumbing.
- **Low-level server API**: Direct access to the protocol for advanced use cases -- custom transports, fine-grained control over message handling, or integration with existing async frameworks.

### TypeScript SDK

The TypeScript SDK (`@modelcontextprotocol/sdk`) is the "official TypeScript SDK for the Model Context Protocol, providing server and client implementations with full protocol support" [src-002]. It provides a `McpServer` class with methods for registering tool, resource, and prompt handlers. TypeScript is a natural fit for servers that wrap web APIs or need to run in serverless environments.

## Building a Server in Python

The fastest path to a working server uses FastMCP [src-001]:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
async def lookup_user(user_id: str) -> str:
    """Look up a user by their ID and return their profile information.

    Args:
        user_id: The unique identifier for the user to look up.
    """
    return f"User {user_id}: name=Alice, role=admin"

if __name__ == "__main__":
    mcp.run()
```

Several things are happening here:

1. **`FastMCP("my-server")`** creates a server instance with a human-readable name. Clients see this name when they connect.
2. **`@mcp.tool()`** registers the function as an MCP tool. The SDK inspects the function signature and docstring to generate the tool's name, description, and input schema automatically.
3. **Type hints drive schema generation.** The `user_id: str` annotation becomes a `{"type": "string"}` property in the JSON Schema. Complex types (Pydantic models, dataclasses) are supported for richer schemas.
4. **`mcp.run()`** starts the server, defaulting to stdio transport.

### Adding Resources and Prompts

```python
@mcp.resource("config://app/settings")
async def get_settings() -> str:
    """Return the current application settings."""
    return json.dumps({"debug": False, "log_level": "INFO"})

@mcp.prompt()
async def review_code(language: str) -> str:
    """A prompt template for code review focused on a specific language."""
    return f"You are a senior {language} developer performing a code review..."
```

The string argument to `@mcp.resource()` is the URI clients use to request the resource. URIs can use any scheme meaningful to your domain (`file://`, `db://`, `config://`).

## Building a Server in TypeScript

The TypeScript SDK uses a class-based approach with Zod schemas for input validation [src-002]:

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({ name: "my-server", version: "1.0.0" });

server.tool(
  "lookup_user",
  "Look up a user by their ID and return their profile information.",
  { user_id: z.string().describe("The unique identifier for the user") },
  async ({ user_id }) => ({
    content: [{ type: "text", text: `User ${user_id}: name=Alice, role=admin` }],
  })
);

server.resource("app-settings", "config://app/settings", async (uri) => ({
  contents: [{ uri: uri.href, mimeType: "application/json", text: "{}" }],
}));
```

Zod provides runtime type checking and clear error messages when the model sends malformed arguments. The SDK also supports returning multiple content types (text, images, embedded resources) in a single tool response, which is useful for tools that produce rich output.

## Transport Configuration

MCP supports multiple transport mechanisms [src-003].

**stdio (Standard I/O)** is the default for local development. The client launches the server as a subprocess and communicates over stdin/stdout. It is simple (no network config), secure (runs locally with the user's permissions), and ephemeral (starts and stops with the client session). This is how most MCP servers are used with Claude Code and other desktop clients.

**Streamable HTTP** is for production and remote deployments. The server runs as an HTTP service that clients connect to over the network, enabling remote access, shared server instances, and standard HTTP infrastructure (load balancers, containers):

```python
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8080)
```

## Testing and Debugging

**MCP Inspector** is an interactive debugging tool for connecting to a server, listing its capabilities, calling tools with custom arguments, and watching protocol messages. Use it before testing with a real AI client to catch schema errors, missing descriptions, and incorrect return types.

**Testing with Claude Code**: add your server to `.mcp.json`, start a conversation, and observe whether the model discovers and uses tools correctly. This reveals problems the Inspector cannot catch -- ambiguous descriptions, missing context, or schema mismatches.

**Unit testing**: both SDKs support programmatic testing. You can call tool handler functions directly, or use the in-memory client/server pairs to test the full protocol round-trip without real I/O:

```python
import pytest
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("test-server")

@mcp.tool()
async def add(a: int, b: int) -> str:
    """Add two numbers."""
    return str(a + b)

@pytest.mark.anyio
async def test_add_tool():
    result = await add(2, 3)
    assert result == "5"
```

## Common Server Patterns

**Database query servers** expose a read-only interface to a database. Tools accept SQL queries or structured filters; resources expose table schemas. Key: restrict to SELECT statements, set query timeouts, and expose schema as resources so the model knows what is available.

**API gateway servers** wrap external REST or GraphQL APIs. Each endpoint becomes an MCP tool. Handle authentication centrally (never expose credentials to the model), implement rate limiting, and transform responses into concise, model-friendly formats.

**File system servers** provide controlled access to a project directory. Restrict access to a specific directory tree, make write operations explicit and confirmable, and support standard operations (read, write, search, list).

**Composite servers** combine multiple patterns. A development productivity server might expose both file system tools and Git operations, or a data analysis server might combine database queries with charting tools. The key is keeping the tool count manageable -- a server with 5-10 well-described tools is more effective than one with 50 vague ones.

## Error Handling and Validation

Return errors as structured content rather than raising exceptions. The model cannot catch exceptions, but it can read and reason about error messages:

```python
@mcp.tool()
async def query_database(sql: str) -> str:
    """Execute a read-only SQL query against the application database."""
    if not sql.strip().upper().startswith("SELECT"):
        return "Error: Only SELECT queries are allowed."
    try:
        results = await db.execute(sql)
        return json.dumps(results, default=str)
    except Exception as e:
        return json.dumps({
            "error": "query_failed",
            "message": str(e),
            "suggestion": "Check table names and column types"
        })
```

Including a `suggestion` field helps the model recover gracefully. The SDKs validate inputs against the schema before calling your handler, but always validate semantic constraints (like "SELECT only") in your code.

## Deployment and Security

For production Streamable HTTP servers, containerization is standard:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install .
COPY . .
EXPOSE 8080
CMD ["python", "-m", "my_server", "--transport", "streamable-http", "--port", "8080"]
```

Security considerations are paramount because MCP servers give the model the ability to take real actions:

- **Least privilege**: only expose capabilities the model actually needs
- **Input sanitization**: treat tool inputs like user input in a web app -- they can be adversarial via prompt injection
- **OAuth authentication**: MCP supports OAuth 2.0 for remote servers, with standard discovery, authorization, and token flows
- **Audit logging**: log all tool invocations with arguments and results

## Practical Considerations

**Start with one tool.** Resist the temptation to build a comprehensive server with dozens of tools. Start with the single most useful tool, test it with a real client, and iterate. Debugging a model's behavior across 20 poorly-described tools is hard.

**Descriptions are documentation for the model.** Write tool descriptions as if explaining the tool to a colleague who has never seen your codebase. Include what it does, when to use it, what it returns, and any constraints.

**Schema design matters.** Use descriptive parameter names (`user_email` not `e`), include `description` fields on every property, mark required fields, and use enums for fixed-set values. The model reads every piece of schema information.

**Consider the context window.** Tool results consume tokens. If a tool can return very large results, truncate, summarize, or paginate. A tool that returns 50,000 characters is not useful.

**Test with adversarial inputs.** The model will sometimes pass unexpected values -- empty strings, very long inputs, injection attempts. Handle them gracefully.

## Further Reading

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) - Official Python implementation [src-001]
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) - Official TypeScript implementation [src-002]
- [MCP Server Development Guide](https://modelcontextprotocol.io/docs/develop/build-server) - Official build guide [src-003]
- [MCP Architecture Overview](https://modelcontextprotocol.io/docs/learn/architecture) - Protocol architecture [src-004]
- [Model Context Protocol](model-context-protocol.md) - Protocol specification and concepts
- [Claude Code Architecture](../agentic-coding/claude-code-architecture.md) - How Claude Code uses MCP servers
- [Tool Use and Function Calling](../agents/tool-use-function-calling.md) - Broader context of tool use in AI systems
