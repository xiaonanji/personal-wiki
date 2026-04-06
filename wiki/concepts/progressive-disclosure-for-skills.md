---
type: concept
title: Progressive Disclosure for Skills
status: active
created: 2026-04-06
updated: 2026-04-06
tags:
  - concept
  - agents
  - context-management
  - skills
sources:
  - "[[sources/what-are-skills]]"
  - "[[sources/adding-skills-support-to-an-agent]]"
---

# Progressive Disclosure for Skills

## Summary

- Progressive disclosure is the context-loading strategy behind skills.
- The agent reveals only lightweight catalog data at session start, then loads full instructions only for relevant skills, and loads referenced resources only when needed.

## Definition

- Three-tier loading strategy:
- Tier 1: catalog metadata such as skill name and description
- Tier 2: full `SKILL.md` instructions when activated
- Tier 3: referenced scripts, assets, and supporting materials on demand

## Supporting Evidence

- [[sources/what-are-skills]] presents discovery, activation, and execution as the operational path.
- [[sources/adding-skills-support-to-an-agent]] makes the three-tier model explicit and frames it as the shared strategy across compatible clients.
- The main benefit is token control: agents do not pay the cost of every installed skill upfront.

## Counterpoints

- Progressive disclosure only works if the agent can reliably discover relevant skills and preserve loaded instructions in context.
- Poor catalog descriptions or bad activation logic can hide useful skills from the model.

## Related Entities

- None yet.

## Related Analyses

- [[analyses/agent-skills-support-checklist]]
