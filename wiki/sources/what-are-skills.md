---
type: source
title: What Are Skills
status: active
created: 2026-04-06
updated: 2026-04-06
tags:
  - source
  - agents
  - skills
  - documentation
raw_source: raw/inbox/2026-04-06T144706+1000 What are skills.md
---

# What Are Skills

## Source Details

- Type: introductory documentation page
- Topic: what an agent skill is and how `SKILL.md` works
- Clip language: English-origin text clipped into markdown
- Raw path: `raw/inbox/2026-04-06T144706+1000 What are skills.md`

## Summary

- The source defines a skill as a folder anchored by a `SKILL.md` file containing metadata and task instructions.
- It presents skills as portable, file-based capability bundles that can optionally include scripts, references, and assets.
- It explains the progressive-disclosure workflow: discover metadata first, load instructions only when relevant, then load referenced resources on demand.
- It emphasizes that the format is intentionally simple and auditable.

## Key Claims

- [[concepts/agent-skills]]: a skill is a directory with `SKILL.md` plus optional bundled resources.
- [[concepts/progressive-disclosure-for-skills]]: skills keep baseline context small by loading more detail only when needed.
- `SKILL.md` needs YAML frontmatter with at least `name` and `description`.
- The format is designed to be self-documenting, extensible, portable, and easy to version.

## Structure

- Defines the file/folder structure of a skill
- Explains discovery, activation, and execution
- Shows the expected shape of `SKILL.md`
- Links out to the specification, client-implementation guide, examples, and authoring practices

## Source Reliability Notes

- This is an explanatory/documentation source, not an empirical report.
- It is useful as a normative description of the intended skill model.

## Connections

- Related concepts: [[concepts/agent-skills]], [[concepts/progressive-disclosure-for-skills]], [[concepts/skill-support-integration]]
- Related analyses: [[analyses/agent-skills-support-checklist]]

## Contradictions Or Tensions

- The source is high-level and does not cover many operational edge cases such as trust boundaries, malformed YAML, or context compaction.

## Follow-Up Questions

- Decide whether this repo should eventually manage its own reusable skills branch under `.agents/skills/`.
- Compare the simple conceptual model here with the more operational guidance in [[sources/adding-skills-support-to-an-agent]].
