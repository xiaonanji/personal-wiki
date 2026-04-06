# LLM Wiki

A starter repository for a personal knowledge base maintained by an LLM agent.

This repo separates knowledge into three layers:

1. `raw/`: immutable source material.
2. `wiki/`: LLM-maintained markdown pages.
3. `AGENTS.md`: the operating schema that tells the agent how to maintain the wiki.

## Layout

```text
.
|-- AGENTS.md
|-- README.md
|-- raw/
|   |-- assets/
|   `-- inbox/
|-- scripts/
|   `-- wiki.py
|-- templates/
|   |-- analysis-page.md
|   |-- concept-page.md
|   |-- entity-page.md
|   `-- source-page.md
`-- wiki/
    |-- analyses/
    |-- concepts/
    |-- entities/
    |-- home.md
    |-- index.md
    |-- log.md
    |-- meta/
    `-- sources/
```

## Basic workflow

1. Put new source material in `raw/inbox/`.
2. Ask your agent to ingest a specific source.
3. The agent reads `AGENTS.md`, updates relevant pages in `wiki/`, and appends to `wiki/log.md`.
4. Ask questions against the wiki, then file durable outputs back into `wiki/analyses/` when useful.
5. Run periodic lint passes with `python scripts/wiki.py lint`.

## New Machine Setup

After cloning this repo onto a new machine, run:

```bash
npm install
npm run qmd:init
```

What this does:

- installs the repo-local `qmd` dependency into `node_modules/`
- creates the repo-local `qmd` index under `.cache/qmd/`
- downloads the local models needed for hybrid `qmd` search
- generates embeddings for the current `wiki/` contents
- warms the hybrid query path

After that, the repo is ready to use with:

```bash
python scripts/wiki.py qsearch "your query"
python scripts/wiki.py qquery "your query"
```

## Refresh After Wiki Updates

Whenever the wiki content changes and you want `qmd` search to reflect the new state, run:

```bash
npm run qmd:refresh
```

This is the normal maintenance command after ingests or manual edits. It:

- updates the `qmd` index
- generates embeddings for new or changed wiki pages

Use `npm run qmd:init` only for first-time setup on a machine or if the local `qmd` state needs to be rebuilt from scratch.

## Optional local tools

Search wiki pages:

```bash
python scripts/wiki.py search "your query"
```

Search wiki pages with repo-local `qmd` and fall back to basic search if needed:

```bash
python scripts/wiki.py qsearch "your query"
```

Run hybrid `qmd` search with semantic retrieval + reranking:

```bash
python scripts/wiki.py qquery "your query"
```

Show recent log entries:

```bash
python scripts/wiki.py recent
```

Run simple structural checks:

```bash
python scripts/wiki.py lint
```

## QMD Setup

This repo includes a repo-local installation of `@tobilu/qmd` through `package.json`. The dependency metadata is committed, but the actual installed packages, index database, and downloaded local models are machine-local and are not committed.

Useful commands:

```bash
npm run qmd:refresh
npm run qmd:status
npm run qmd:update
npm run qmd:search -- "ghost GDP"
npm run qmd:query -- "how do the main AI crisis concepts differ?"
```

Notes:

- `qmd` state is isolated to this repo via `.cache/`.
- `python scripts/wiki.py search` remains the lightweight fallback.
- `python scripts/wiki.py qsearch` uses `qmd` BM25 search.
- `python scripts/wiki.py qquery` uses `qmd` hybrid search and falls back if the semantic index is not ready.
- `npm run qmd:refresh` is the normal post-ingest maintenance command.
- `npm run qmd:init` is the heavy step: it downloads local models and builds embeddings.
- Do not run multiple `qmd` commands against this repo-local index at the same time; the SQLite index is not meant for concurrent writers.
- A new machine still needs the one-time bootstrap above; that part cannot be eliminated without committing `node_modules`, the SQLite index, and the downloaded GGUF models.

## Notes

- This repo is intentionally markdown-first and local-first.
- `raw/` files are source-of-truth inputs and should not be edited by the agent.
- `wiki/` is expected to evolve continuously as new sources and questions arrive.
