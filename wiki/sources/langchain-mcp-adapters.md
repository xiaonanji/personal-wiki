---
type: source
title: LangChain MCP Adapters
status: active
created: 2026-04-12
updated: 2026-04-12
tags:
  - source
  - agents
  - mcp
  - langchain
  - interoperability
raw_source: raw/inbox/2026-04-12T173021+1000 langchain_mcp_adapters.md
---

# LangChain MCP Adapters

## Source Details

- Type: library documentation / README
- Topic: adapting Anthropic Model Context Protocol (MCP) tools, prompts, and resources for LangChain and LangGraph
- Primary subject: [[entities/langchain-mcp-adapters]]
- Raw path: `raw/inbox/2026-04-12T173021+1000 langchain_mcp_adapters.md`

## Summary

- The source describes a lightweight adapter library that makes MCP servers usable from LangChain and LangGraph applications.
- It frames the library around two core capabilities:
  - convert MCP tools into LangChain tools
  - manage connections to one or more MCP servers through a reusable client layer
- Beyond tools, the documented API surface also covers MCP prompts, resources, callbacks, sessions, and call interceptors.
- The examples show three integration styles:
  - direct agent construction with `create_agent`
  - explicit LangGraph `StateGraph` wiring
  - deployment inside a LangGraph API server

## Key Claims

- [[concepts/mcp-to-langchain-adaptation]]: MCP tool definitions can be converted into LangChain-compatible tools rather than rewritten manually.
- A multi-server client can unify tools from heterogeneous MCP transports behind one LangChain-facing interface.
- The adapter surface extends beyond tools to prompts and resources, which implies MCP can carry more than just callable actions into LangChain systems.
- HTTP-based transports can accept runtime headers for authentication and tracing.
- `stdio` transport deserves caution in web-server contexts and may be the wrong abstraction if a plain `@tool` would suffice.

## Features Called Out In The Source

- Convert MCP tools into LangChain tools for LangGraph agents.
- Connect to multiple MCP servers and load tools from them.
- Support multiple transport styles, including `stdio`, HTTP-based transports, SSE, WebSocket, and streamable HTTP in the documented API surface.
- Convert MCP prompts to LangChain messages.
- Convert MCP resources to LangChain `Blob` objects.
- Support callbacks, tool-call interceptors, and session-management helpers.

## Installation

```bash
pip install langchain-mcp-adapters
```

### Quickstart Dependencies

```bash
pip install langchain-mcp-adapters langgraph "langchain[openai]"

export OPENAI_API_KEY=<your_api_key>
```

## Code Examples Preserved From The Source

### Example MCP Server

```python
# math_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Quickstart Client

```python
# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent

server_params = StdioServerParameters(
    command="python",
    # Make sure to update to the full absolute path to your math_server.py file
    args=["/path/to/math_server.py"],
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Initialize the connection
        await session.initialize()

        # Get tools
        tools = await load_mcp_tools(session)

        # Create and run the agent
        agent = create_agent("openai:gpt-4.1", tools)
        agent_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
```

### Multiple MCP Servers

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["/path/to/math_server.py"],
            "transport": "stdio",
        },
        "weather": {
            # Make sure you start your weather server on port 8000
            "url": "http://localhost:8000/mcp",
            "transport": "http",
        }
    }
)
tools = await client.get_tools()
agent = create_agent("openai:gpt-4.1", tools)
math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
weather_response = await agent.ainvoke({"messages": "what is the weather in nyc?"})
```

### Explicit Session For A Named Server

```python
from langchain_mcp_adapters.tools import load_mcp_tools

client = MultiServerMCPClient({...})
async with client.session("math") as session:
    tools = await load_mcp_tools(session)
```

### Streamable HTTP Via Python MCP SDK

```python
# Use server from examples/servers/streamable-http-stateless/

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from langchain.agents import create_agent
from langchain_mcp_adapters.tools import load_mcp_tools

async with streamablehttp_client("http://localhost:3000/mcp") as (read, write, _):
    async with ClientSession(read, write) as session:
        # Initialize the connection
        await session.initialize()

        # Get tools
        tools = await load_mcp_tools(session)
        agent = create_agent("openai:gpt-4.1", tools)
        math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
```

### Streamable HTTP Via `MultiServerMCPClient`

```python
# Use server from examples/servers/streamable-http-stateless/
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

client = MultiServerMCPClient(
    {
        "math": {
            "transport": "http",
            "url": "http://localhost:3000/mcp"
        },
    }
)
tools = await client.get_tools()
agent = create_agent("openai:gpt-4.1", tools)
math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
```

### Passing Runtime Headers

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

client = MultiServerMCPClient(
    {
        "weather": {
            "transport": "http",
            "url": "http://localhost:8000/mcp",
            "headers": {
                "Authorization": "Bearer YOUR_TOKEN",
                "X-Custom-Header": "custom-value"
            },
        }
    }
)
tools = await client.get_tools()
agent = create_agent("openai:gpt-4.1", tools)
response = await agent.ainvoke({"messages": "what is the weather in nyc?"})
```

### LangGraph `StateGraph` Integration

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition

from langchain.chat_models import init_chat_model
model = init_chat_model("openai:gpt-4.1")

client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["./examples/math_server.py"],
            "transport": "stdio",
        },
        "weather": {
            # make sure you start your weather server on port 8000
            "url": "http://localhost:8000/mcp",
            "transport": "http",
        }
    }
)
tools = await client.get_tools()

def call_model(state: MessagesState):
    response = model.bind_tools(tools).invoke(state["messages"])
    return {"messages": response}

builder = StateGraph(MessagesState)
builder.add_node(call_model)
builder.add_node(ToolNode(tools))
builder.add_edge(START, "call_model")
builder.add_conditional_edges(
    "call_model",
    tools_condition,
)
builder.add_edge("tools", "call_model")
graph = builder.compile()
math_response = await graph.ainvoke({"messages": "what's (3 + 5) x 12?"})
weather_response = await graph.ainvoke({"messages": "what is the weather in nyc?"})
```

### LangGraph API Server Integration

```python
# graph.py
from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

async def make_graph():
    client = MultiServerMCPClient(
        {
            "weather": {
                # make sure you start your weather server on port 8000
                "url": "http://localhost:8000/mcp",
                "transport": "http",
            },
            # ATTENTION: MCP's stdio transport was designed primarily to support applications running on a user's machine.
            # Before using stdio in a web server context, evaluate whether there's a more appropriate solution.
            # For example, do you actually need MCP? or can you get away with a simple `@tool`?
            "math": {
                "command": "python",
                # Make sure to update to the full absolute path to your math_server.py file
                "args": ["/path/to/math_server.py"],
                "transport": "stdio",
            },
        }
    )
    tools = await client.get_tools()
    agent = create_agent("openai:gpt-4.1", tools)
    return agent
```

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./graph.py:make_graph"
  }
}
```

## Notable API Surface Mentioned In The Source

### Classes

- `MultiServerMCPClient`
- `McpHttpClientFactory`
- `StdioConnection`
- `SSEConnection`
- `StreamableHttpConnection`
- `WebsocketConnection`
- `CallbackContext`
- `LoggingMessageCallback`
- `ProgressCallback`
- `ElicitationCallback`
- `Callbacks`
- `MCPToolArtifact`
- `MCPToolCallRequest`
- `ToolCallInterceptor`

### Functions

- `convert_mcp_prompt_message_to_langchain_message`
- `load_mcp_prompt`
- `convert_mcp_resource_to_langchain_blob`
- `get_mcp_resource`
- `load_mcp_resources`
- `create_session`
- `convert_mcp_tool_to_langchain_tool`
- `load_mcp_tools`
- `to_fastmcp`

### Modules

- `prompts`
- `resources`
- `client`
- `sessions`
- `callbacks`
- `tools`
- `interceptors`

## Source Reliability Notes

- This is a first-party library documentation page, so it is strong evidence for intended usage and supported API surface.
- It is not a neutral comparison against other MCP integration libraries and does not quantify runtime costs, failure modes, or production tradeoffs.

## Connections

- Related entities: [[entities/langchain-mcp-adapters]]
- Related concepts: [[concepts/mcp-to-langchain-adaptation]], [[concepts/skill-support-integration]]
- Related analyses: [[analyses/langchain-mcp-adapters-integration-checklist]]

## Contradictions Or Tensions

- The source positions MCP as a flexible interoperability layer, but it also explicitly warns that `stdio` can be a poor fit inside server contexts.
- The examples emphasize convenience, but they leave open operational questions around session reuse, transport choice, and auth/security policy.

## Follow-Up Questions

- When should a team use an MCP adapter instead of defining plain native LangChain `@tool` functions?
- Which session lifecycle is best for multi-server agent deployments: per-call sessions or longer-lived sessions?
- How should prompts, resources, and tool interception be used together in a production LangGraph system?
