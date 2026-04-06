---
type: concept
title: Agent Skills
status: active
created: 2026-04-06
updated: 2026-04-06
tags:
  - concept
  - agents
  - skills
sources:
  - "[[sources/what-are-skills]]"
  - "[[sources/adding-skills-support-to-an-agent]]"
---

# Agent Skills

## Summary

- Agent skills are portable task modules packaged as folders centered on `SKILL.md`.
- They give agents specialized instructions and optional bundled resources without forcing all of that context into every session.

## Definition

- A skill is a directory containing a `SKILL.md` file with frontmatter metadata and markdown instructions, plus optional supporting folders such as `scripts/`, `references/`, and `assets/`.

## Supporting Evidence

- [[sources/what-are-skills]] defines the core directory structure and required `SKILL.md` frontmatter.
- [[sources/adding-skills-support-to-an-agent]] expands the concept into discovery, activation, permissions, and lifecycle management.
- Both sources treat portability and file-based transparency as core advantages.

## Counterpoints

- A skill system still needs client-side machinery to be genuinely useful; the folder structure alone is not enough.
- Portable file-based skills can introduce trust and collision issues if the host client does not enforce sane loading rules.

## Related Entities

- None yet.

## Related Analyses

- [[analyses/agent-skills-support-checklist]]
