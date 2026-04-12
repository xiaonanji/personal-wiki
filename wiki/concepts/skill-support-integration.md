---
type: concept
title: Skill Support Integration
status: active
created: 2026-04-06
updated: 2026-04-12
tags:
  - concept
  - agents
  - implementation
  - skills
sources:
  - "[[sources/adding-skills-support-to-an-agent]]"
  - "[[sources/what-are-skills]]"
  - "[[sources/context-management-for-deep-agents]]"
---

# Skill Support Integration

## Summary

- Skill support integration is the client-side architecture needed to make skills usable in practice.
- The guide breaks this into discovery, parsing, disclosure, activation, and context maintenance.
- Newer context-management material in the wiki makes that last step more concrete: long-running agents may need filesystem-backed offloading and summarization rather than only "keep the skill in context."

## Definitions

- Discovery: find skill directories and extract metadata
- Parsing: read `SKILL.md` frontmatter and body robustly
- Disclosure: tell the model which skills exist without loading full instructions
- Activation: inject or return the full skill when it is relevant
- Context maintenance: preserve skill content across context compaction and avoid duplicate activation

## Supporting Evidence

- [[sources/adding-skills-support-to-an-agent]] is effectively a full checklist for implementing the lifecycle.
- It highlights trust checks, project-vs-user precedence, lenient YAML handling, permissions, and deduplication.
- [[sources/what-are-skills]] supplies the simpler conceptual basis that this lifecycle operates on.
- [[sources/context-management-for-deep-agents]] provides a concrete harness example for the context-maintenance slice of the lifecycle, especially when sessions become long enough that compaction is unavoidable.

## Counterpoints

- Not every agent needs the full lifecycle from day one.
- Some environments may deliberately choose a narrower implementation, for example only built-in skills or only file-read activation.

## Related Entities

- None yet.

## Related Analyses

- [[analyses/agent-skills-support-checklist]]
- [[analyses/agent-context-compression-evaluation-checklist]]
