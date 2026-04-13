---
type: concept
title: Agent Context Compression
status: active
created: 2026-04-12
updated: 2026-04-12
tags:
  - concept
  - agents
  - context-management
  - summarization
sources:
  - "[[sources/context-management-for-deep-agents]]"
---

# Agent Context Compression

## Summary

- Agent context compression is the harness strategy for shrinking active model context while preserving enough state to continue the task.
- It combines lossy and non-lossy techniques: offloading recoverable artifacts out of context, trimming redundant payloads, and summarizing conversation state when needed.

## Definitions

- Large-result offloading: move oversized tool outputs out of the active transcript and replace them with a pointer plus a short preview.
- Stale-input eviction: remove older write or edit payloads from context once the underlying artifact already exists on disk.
- Structured summarization: replace long message history with a compact representation of intent, progress, artifacts, and next steps.
- Recovery path: preserve enough external state that the agent can later retrieve facts or artifacts that were compressed away.

## Supporting Evidence

- [[sources/context-management-for-deep-agents]] describes a threshold-based implementation that escalates from offloading to summarization.
- The source treats the filesystem as the recovery layer that makes compression usable rather than purely lossy.
- It also highlights evaluation patterns that test whether compression preserves trajectory and recoverability.

## Counterpoints

- Compression settings that are useful for evaluation can be worse for production task performance if they trigger too aggressively.
- Summarization is dangerous without a strong recovery path; otherwise agents may drift from the original goal or falsely conclude a task is complete.

## Related Entities

- [[entities/deep-agents-sdk]]

## Related Concepts

- [[concepts/progressive-disclosure-for-skills]] - narrower context-loading pattern for skills rather than full-session compression
- [[concepts/skill-support-integration]] - broader client lifecycle that also needs durable context maintenance

## Related Analyses

- [[analyses/agent-context-compression-evaluation-checklist]]
