# LLM Wiki Operating Schema

This repository is a persistent knowledge base maintained by an LLM agent.

The goal is not to answer questions from raw documents from scratch every time. The goal is to continuously compile sources into an interlinked wiki that improves over time.

## Mission

- Treat `raw/` as immutable source material.
- Treat `wiki/` as the maintained knowledge layer.
- Keep the wiki structured, cross-linked, and current.
- Prefer incremental synthesis over one-off answers.
- File durable outputs back into the wiki whenever they would be useful later.

## Repository Contract

### `raw/`

- Contains source documents, notes, transcripts, clippings, exported chats, images, and datasets.
- Do not modify files in `raw/`.
- New sources usually arrive in `raw/inbox/`.
- Images referenced by sources may live in `raw/assets/`.

### `wiki/`

- Contains markdown pages written and maintained by the agent.
- The agent may create, rename, split, merge, and update pages here when doing so improves the knowledge base.
- Main page groups:
  - `wiki/sources/`: one page per source or source bundle.
  - `wiki/entities/`: people, organizations, places, products, characters, projects.
  - `wiki/concepts/`: themes, ideas, mechanisms, frameworks.
  - `wiki/analyses/`: durable answers, comparisons, syntheses, timelines.
  - `wiki/meta/`: maintenance pages such as open questions and contradictions.

### `AGENTS.md`

- This file is the operating manual.
- Follow it before taking wiki actions.
- If a workflow here becomes inadequate, improve this file as part of the work.

## Core Rules

1. Never edit raw source files.
2. Prefer updating existing relevant pages over creating duplicate pages.
3. Every substantive new wiki page should be linked from `wiki/index.md`.
4. Every ingest, durable query result, or lint pass should be appended to `wiki/log.md`.
5. When claims conflict, record the conflict explicitly instead of silently overwriting old synthesis.
6. Preserve uncertainty. Distinguish source claims, inferred synthesis, and open questions.
7. Use concise markdown. Optimize for future retrieval and maintenance, not literary prose.
8. Use Obsidian-style wiki links where practical, for example `[[concepts/attention]]`.

## Page Conventions

Use YAML frontmatter for most pages when it adds structure. Prefer this shape:

```yaml
---
type: source | entity | concept | analysis | meta
title: Page title
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - ...
sources:
  - "[[sources/example-source]]"
---
```

Guidelines:

- `title` should match the page topic.
- `updated` should change whenever a page is materially revised.
- `sources` should point to source pages in `wiki/sources/`, not raw files directly.
- If a page has no evidence yet, omit `sources` and state the gap in the body.

## Required Anchor Files

### `wiki/home.md`

- Human-readable top-level overview of the wiki.
- Summarize major domains, current focus areas, and how to navigate the knowledge base.

### `wiki/index.md`

- Content-oriented catalog of wiki pages.
- Organize by section.
- Each entry should include:
  - page link
  - one-line description
  - optional source count or last-updated note
- Update it every time pages are added, removed, renamed, or materially reframed.

### `wiki/log.md`

- Append-only chronological record.
- Use headings in this exact format:

```md
## [YYYY-MM-DD] ingest | Source Title
## [YYYY-MM-DD] query | Question or analysis title
## [YYYY-MM-DD] lint | Short summary
```

- Under each heading, include a short bullet list:
  - what changed
  - pages touched
  - unresolved follow-ups

## Source Ingest Workflow

When asked to ingest a source:

1. Identify the raw file and read it fully.
2. If the source references important local images, inspect the relevant images in `raw/assets/`.
3. If the source contains code examples, SQL queries, configuration snippets, or other technical implementation details, preserve them in the source page using appropriate markdown code blocks. Do not summarize or omit code examples.
4. Discuss key takeaways with the user when interpretation or prioritization matters.
5. Create or update a page in `wiki/sources/` for the source.
6. Update any impacted entity, concept, and analysis pages.
7. Add newly warranted pages if the source introduces a durable subject that does not yet have a home.
8. Add contradictions or unresolved tensions to `wiki/meta/contradictions.md`.
9. Add unanswered but important leads to `wiki/meta/open-questions.md`.
10. Update `wiki/index.md`.
11. Append an ingest entry to `wiki/log.md`.
12. If repo-local `qmd` is available, run `npm run qmd:refresh` after the wiki updates so search stays current.

Default expectation: a single source ingest may touch many pages.

## Query Workflow

When asked a substantive question:

1. Read `wiki/index.md` first.
2. Prefer `python scripts/wiki.py qsearch "..."` or `python scripts/wiki.py qquery "..."` when the wiki grows large enough that direct file selection is unclear.
3. If `qmd` is unavailable or not initialized, fall back to direct page reads or `python scripts/wiki.py search "..."`.
4. Select and read the most relevant pages from `wiki/`.
5. Synthesize an answer grounded in the wiki.
6. Cite the relevant wiki pages in the answer.
7. If the result is likely to be useful again, create or update a page in `wiki/analyses/`.
8. Update `wiki/index.md` if a durable page was added.
9. Append a query entry to `wiki/log.md` if the result was filed into the wiki.

## QMD Search Backend

- This repo may use a repo-local `qmd` install managed through `package.json`.
- `qmd` state lives under `.cache/qmd/` and is not committed.
- On a fresh machine, bootstrap with:
  - `npm install`
  - `npm run qmd:init`
- After the wiki changes, prefer:
  - `npm run qmd:refresh`
- Useful commands:
  - `npm run qmd:refresh`
  - `npm run qmd:status`
  - `npm run qmd:search -- "your query"`
  - `npm run qmd:query -- "your query"`
- The Python helper exposes:
  - `python scripts/wiki.py qsearch "your query"`
  - `python scripts/wiki.py qquery "your query"`
- Keep `python scripts/wiki.py search` as the fallback path.
- After ingests or material wiki edits, run `npm run qmd:refresh` when the local `qmd` setup is available.
- If `qmd` has not been bootstrapped on the current machine yet, do not block the ingest on it; complete the wiki updates and note that `qmd` refresh is pending.
- Do not run multiple repo-local `qmd` commands concurrently against the same `.cache/qmd/index.sqlite` database.

## Lint Workflow

When asked to lint or health-check the wiki:

- Look for broken links.
- Look for orphan pages with no inbound links.
- Look for stale claims that newer sources challenge.
- Look for important concepts repeatedly mentioned without dedicated pages.
- Look for duplicate or near-duplicate pages.
- Look for gaps in `wiki/index.md`.
- Look for entries that should be added to `wiki/meta/open-questions.md` or `wiki/meta/contradictions.md`.

After a lint pass:

- Fix straightforward structural issues immediately.
- Summarize higher-judgment issues for the user.
- Append a lint entry to `wiki/log.md`.

## Writing Standards

- Prefer explicit section headings.
- Prefer bullet lists over long paragraphs for source extraction.
- Distinguish clearly between:
  - direct source claims
  - synthesized conclusions
  - speculation or inference
- If an inference is important, label it as inference.
- If evidence is weak or disputed, say so.
- Preserve code examples, SQL queries, configuration snippets, and technical implementation details from sources using properly-formatted markdown code blocks with language identifiers (e.g., ```sql, ```python, ```yaml).

## Naming Guidance

- Use stable, descriptive page names.
- Prefer lowercase kebab-case filenames.
- Keep human-readable titles in frontmatter and headings.
- When in doubt:
  - entities go in `wiki/entities/`
  - abstract topics go in `wiki/concepts/`
  - single-source summaries go in `wiki/sources/`
  - reusable answers and comparisons go in `wiki/analyses/`

## Maintenance Bias

Bias toward maintaining a coherent knowledge base, not merely producing a helpful chat reply.

If a question reveals a missing page, missing cross-reference, or missing synthesis, fix the wiki as part of answering.
