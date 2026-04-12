---
type: analysis
title: Agent Context Compression Evaluation Checklist
status: active
created: 2026-04-12
updated: 2026-04-12
tags:
  - analysis
  - agents
  - context-management
  - evaluation
sources:
  - "[[sources/context-management-for-deep-agents]]"
---

# Agent Context Compression Evaluation Checklist

## Question

- What implementation and evaluation checks make context compression trustworthy in a long-running agent harness?

## Answer

- Use an external recovery layer, not only lossy summarization. Persist artifacts and prior messages somewhere the agent can search later.
- Offload oversized tool outputs immediately when they would otherwise dominate the context window.
- Evict stale write and edit payloads only after the underlying content is safely available on disk or in another durable store.
- Summarize only after offloading stops creating enough space, and keep the summary structured around intent, artifacts created, and next steps.
- Verify recoverability with targeted tests where key facts disappear from active context and must be fetched back.
- Verify trajectory preservation by forcing summarization mid-task and checking that the agent continues toward the original objective.
- Stress-test candidate implementations with more aggressive thresholds than production so compression events happen often enough to compare variants.
- Watch for post-summary failure modes such as goal drift, premature completion, or unnecessary clarification requests.

## Evidence

- [[sources/context-management-for-deep-agents]] provides a concrete harness pattern: filesystem-backed offloading first, summarization second, and targeted integration tests for recoverability.
- The same source explicitly warns that evaluation thresholds and production thresholds may differ.

## Gaps

- The current evidence is a single harness-specific writeup, not a cross-framework comparison.
- The source does not quantify which threshold settings generalize best across models or workloads.

## Follow-Up

- Compare these checks against other agent harnesses that use memory stores, databases, or tool-call replay instead of a filesystem.
- Determine which of these checks should be considered required for this wiki's own future agent implementations.
