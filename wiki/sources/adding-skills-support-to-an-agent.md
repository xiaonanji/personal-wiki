---
type: source
title: Adding Skills Support to an Agent
status: active
created: 2026-04-06
updated: 2026-04-06
tags:
  - source
  - agents
  - skills
  - implementation
raw_source: raw/inbox/2026-04-06T144635+1000 How to add skills support to your agent.md
---

# Adding Skills Support to an Agent

## Source Details

- Type: implementation guide
- Topic: how an agent or tool should discover, disclose, activate, and maintain skills
- Clip language: English-origin text clipped into markdown
- Raw path: `raw/inbox/2026-04-06T144635+1000 How to add skills support to your agent.md`

## Summary

- The source gives an end-to-end design for skill-enabled agents: discover skills, parse `SKILL.md`, disclose the catalog, activate relevant skills, and preserve their instructions in context over time.
- It frames the core integration around two variables: where skills live and how the model can access their contents.
- It recommends progressive disclosure as the token-management strategy and emphasizes trust boundaries, deterministic collision handling, and context preservation.
- It treats skill support as a client/harness responsibility rather than something that emerges automatically from the model.

## Key Claims

- [[concepts/skill-support-integration]]: a skills-capable agent needs explicit support for discovery, parsing, disclosure, activation, and context management.
- [[concepts/progressive-disclosure-for-skills]]: three tiers should be loaded progressively: catalog, instructions, then referenced resources.
- Project-level skills should typically override user-level skills when names collide.
- Project-level skill loading may need trust gating because repository instructions can be untrusted.
- Dedicated activation tools are useful even when file reads are possible because they allow stronger control over wrapping, permissions, and analytics.

## Operational Guidance Captured In The Source

- Discovery paths may include project-level and user-level client-specific skill directories plus `.agents/skills/` for interoperability.
- Discovery should scan for subdirectories containing `SKILL.md` and set practical limits on depth and total directories.
- Parsing should be lenient enough to recover from common malformed YAML patterns.
- Disclosure should expose only name and description at session start.
- Activation can be model-driven by file reads or by a dedicated activation tool.
- Skill content should be protected from context-pruning and not injected repeatedly when already loaded.

## Source Reliability Notes

- This is a normative implementation guide.
- It is especially useful for client/harness design decisions, not for end-user task content.

## Connections

- Related concepts: [[concepts/agent-skills]], [[concepts/progressive-disclosure-for-skills]], [[concepts/skill-support-integration]]
- Related analyses: [[analyses/agent-skills-support-checklist]]

## Contradictions Or Tensions

- The guide is broad and architecture-agnostic, so many decisions remain local policy choices rather than fixed rules.
- Some recommendations trade simplicity for robustness; a minimal agent may intentionally implement a narrower subset.

## Follow-Up Questions

- Which skill scopes and trust rules are appropriate for this repo's intended agent workflow?
- Should this wiki eventually track concrete design decisions for a specific skill-enabled agent implementation?
