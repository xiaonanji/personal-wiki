---
type: entity
title: Deep Agents SDK
status: active
created: 2026-04-12
updated: 2026-04-12
tags:
  - entity
  - product
  - agents
  - context-management
sources:
  - "[[sources/context-management-for-deep-agents]]"
---

# Deep Agents SDK

## Summary

- Open-source agent harness from LangChain for long-running tasks that may require planning, filesystem access, and subagents.
- In the current wiki, it is the main concrete example of [[concepts/agent-context-compression]] implemented at the harness level.

## Key Facts

- Provides an agent harness rather than only a prompt or tool wrapper.
- Exposes a filesystem abstraction so agents can list, read, write, search, and execute against persisted artifacts.
- Uses three compression mechanisms to manage context growth:
  - offload large tool results
  - offload stale large tool inputs
  - summarize conversation history when offloading is no longer enough
- Uses model-profile metadata to tune compression thresholds relative to the model's context window.

## Relationships

- Built by LangChain.
- Implements [[concepts/agent-context-compression]] as a concrete harness feature set.
- Extends the broader context-maintenance concerns also visible in [[concepts/skill-support-integration]].

## Timeline

- 2026-04-12: first captured in this wiki via [[sources/context-management-for-deep-agents]]

## Open Questions

- How opinionated is the SDK relative to other agent harnesses on summarization prompt structure and retrieval behavior?
- Which of its context-management features are portable patterns versus Deep-Agents-specific implementation details?

## Related Pages

- [[sources/context-management-for-deep-agents]]
- [[concepts/agent-context-compression]]
- [[analyses/agent-context-compression-evaluation-checklist]]
