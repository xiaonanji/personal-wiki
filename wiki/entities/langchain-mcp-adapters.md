---
type: entity
title: LangChain MCP Adapters
status: active
created: 2026-04-12
updated: 2026-04-12
tags:
  - entity
  - library
  - agents
  - mcp
  - langchain
sources:
  - "[[sources/langchain-mcp-adapters]]"
---

# LangChain MCP Adapters

## Summary

- Python library that adapts MCP servers to LangChain and LangGraph interfaces.
- In the current wiki, it is the main concrete example of MCP interoperability for LangChain-based agent systems.

## Key Facts

- Converts MCP tools into LangChain tools.
- Includes a `MultiServerMCPClient` for connecting to multiple MCP servers.
- Supports adapting not only tools but also prompts and resources.
- Documents multiple connection styles and transports, including `stdio` and HTTP-based transports.
- Exposes callback and interceptor surfaces around tool execution and session behavior.

## Relationships

- Bridges Anthropic's Model Context Protocol into LangChain and LangGraph runtimes.
- Implements [[concepts/mcp-to-langchain-adaptation]] as a library rather than requiring hand-written wrappers.
- Sits adjacent to, but distinct from, [[concepts/skill-support-integration]] because it focuses on tool/server interoperability rather than `SKILL.md` lifecycle management.

## Timeline

- 2026-04-12: first captured in this wiki via [[sources/langchain-mcp-adapters]]

## Open Questions

- How stable is the adapter surface across Python and JavaScript implementations?
- Which parts of the library are essential in production versus mostly convenience wrappers?

## Related Pages

- [[sources/langchain-mcp-adapters]]
- [[concepts/mcp-to-langchain-adaptation]]
- [[analyses/langchain-mcp-adapters-integration-checklist]]
