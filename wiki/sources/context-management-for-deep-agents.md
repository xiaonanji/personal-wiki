---
type: source
title: Context Management for Deep Agents
status: active
created: 2026-04-12
updated: 2026-04-12
tags:
  - source
  - agents
  - context-management
  - evaluation
raw_source: raw/inbox/2026-04-12T161756+1000 Context Management for Deep Agents.md
---

# Context Management for Deep Agents

## Source Details

- Type: engineering blog / implementation note
- Topic: harness-level context compression for long-running agents
- Primary subject: [[entities/deep-agents-sdk]]
- Raw path: `raw/inbox/2026-04-12T161756+1000 Context Management for Deep Agents.md`

## Summary

- The source argues that longer-running agents need explicit context-management machinery to avoid context rot and context-window exhaustion.
- It presents the Deep Agents SDK as a filesystem-backed harness that compresses context in three stages: offload large tool results, offload stale large tool inputs, then summarize message history.
- Compression is threshold-driven relative to the model's context window, rather than being triggered at a fixed number of turns.
- The source also gives evaluation guidance: combine real benchmark runs with targeted tests for recoverability and post-summary goal preservation.

## Key Claims

- [[concepts/agent-context-compression]] is a harness responsibility, not just a prompt-writing concern.
- The filesystem can act as external working memory: large artifacts and full pre-summary transcripts are preserved there for later retrieval.
- Large tool results should be offloaded immediately when they exceed a size threshold.
- Old write and edit payloads become eligible for truncation once they are safely persisted elsewhere.
- Summarization should preserve session intent, artifacts created, and next steps, while keeping the full original messages recoverable.
- Evaluation should test not only whether compression reduces token usage, but whether the agent can continue the task and recover summarized-away facts.

## Operational Details Captured In The Source

- Large tool responses above 20,000 tokens are replaced in-context with a file path reference plus a short preview.
- Once context crosses 85% of the model window, older write and edit arguments can be replaced with pointers to filesystem state.
- Summarization is the fallback when offloading no longer creates enough space.
- Summarization has two parts:
  - an in-context structured summary
  - a filesystem copy of the complete original messages
- The source highlights "needle-in-the-haystack" tests and trajectory-preservation tests as targeted eval patterns.

## Source Reliability Notes

- This is a first-party implementation writeup from the authors of the harness, so it is strong evidence for intended design but not a neutral benchmark comparison.
- The examples and traces are useful for understanding mechanism design, while the performance claims should be treated as harness-specific unless compared against external evaluations.

## Connections

- Related entities: [[entities/deep-agents-sdk]]
- Related concepts: [[concepts/agent-context-compression]], [[concepts/skill-support-integration]], [[concepts/progressive-disclosure-for-skills]]
- Related analyses: [[analyses/agent-context-compression-evaluation-checklist]], [[analyses/agent-skills-support-checklist]]

## Contradictions Or Tensions

- The source explicitly says aggressive summarization thresholds can be useful for evaluation while being suboptimal for production performance.
- The design reduces active-token load, but it depends on reliable retrieval from the filesystem; compression without recovery would create goal-drift risk.

## Follow-Up Questions

- How well do these compression patterns transfer to harnesses that do not expose a filesystem abstraction?
- What threshold settings work best across different models and task profiles?
- Which parts of this pattern should be considered baseline requirements for any long-running agent in this wiki's orbit?
