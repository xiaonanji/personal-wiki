---
type: analysis
title: Agent Skills Support Checklist
status: active
created: 2026-04-06
updated: 2026-04-06
tags:
  - analysis
  - agents
  - skills
sources:
  - "[[sources/what-are-skills]]"
  - "[[sources/adding-skills-support-to-an-agent]]"
---

# Agent Skills Support Checklist

## Question

- What are the durable implementation steps for adding skills support to an agent or development tool?

## Answer

- Support discovery of skill directories and find subdirectories containing `SKILL.md`.
- Parse `SKILL.md` into metadata plus body and tolerate common cross-client formatting mistakes where practical.
- Disclose only a catalog at session start: skill name, description, and activation path.
- Activate skills on demand by file read or by a dedicated activation tool.
- Preserve activated skill content during context compaction and avoid injecting the same skill repeatedly.
- Resolve relative paths against the skill directory and load supporting resources only when referenced.
- Apply trust and precedence rules so project-level skills can be useful without silently overriding the user in unsafe ways.

## Evidence

- [[sources/what-are-skills]] defines the core skill object and the discovery-activation-execution model.
- [[sources/adding-skills-support-to-an-agent]] provides the full lifecycle and operational guardrails.

## Gaps

- These sources describe the architecture, but they do not settle which local policy choices are best for any specific agent.
- They also do not benchmark how much skill support improves agent performance in practice.

## Follow-Up

- Decide which directories and trust rules matter for the target agent.
- Decide whether activation should be driven by raw file reads or a dedicated activation tool.
- Compare these recommendations with the actual conventions already used by local agent clients.
