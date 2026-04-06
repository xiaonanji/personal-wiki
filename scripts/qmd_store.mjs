#!/usr/bin/env node

import { mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(SCRIPT_DIR, "..");
const CACHE_ROOT = join(ROOT, ".cache");
const QMD_DIR = join(CACHE_ROOT, "qmd");
const DB_PATH = join(QMD_DIR, "index.sqlite");
const WIKI_PATH = join(ROOT, "wiki");

process.env.XDG_CACHE_HOME ??= CACHE_ROOT;

mkdirSync(QMD_DIR, { recursive: true });

const { createStore, extractSnippet } = await import("@tobilu/qmd");

function usage() {
  console.error(`Usage:
  node scripts/qmd_store.mjs status
  node scripts/qmd_store.mjs update
  node scripts/qmd_store.mjs embed [--force]
  node scripts/qmd_store.mjs search <query> [-n N]
  node scripts/qmd_store.mjs query <query> [-n N] [--min-score N]
  node scripts/qmd_store.mjs warmup [<query>]`);
}

function parseArgs(argv) {
  const command = argv[0];
  const options = {
    limit: 10,
    minScore: 0,
    force: false,
    json: false,
  };
  const parts = [];

  for (let i = 1; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === "-n" || token === "--limit") {
      options.limit = Number(argv[i + 1]);
      i += 1;
      continue;
    }
    if (token === "--min-score") {
      options.minScore = Number(argv[i + 1]);
      i += 1;
      continue;
    }
    if (token === "--force" || token === "-f") {
      options.force = true;
      continue;
    }
    if (token === "--json") {
      options.json = true;
      continue;
    }
    parts.push(token);
  }

  return { command, options, query: parts.join(" ").trim() };
}

async function openStore() {
  const store = await createStore({
    dbPath: DB_PATH,
    config: {
      collections: {
        wiki: {
          path: WIKI_PATH,
          pattern: "**/*.md",
        },
      },
    },
  });

  await store.setGlobalContext(
    "LLM-maintained markdown wiki for this repository. Search this before reading raw source material."
  );

  return store;
}

function formatPercent(score) {
  return `${Math.round(score * 100)}%`;
}

function resultPath(result) {
  return result.displayPath || result.filepath || result.file;
}

async function formatResults(store, results, query, asJson) {
  if (asJson) {
    console.log(JSON.stringify(results, null, 2));
    return;
  }

  if (!results.length) {
    console.log("No matches found.");
    return;
  }

  for (const result of results) {
    const path = resultPath(result);
    console.log(`${formatPercent(result.score)}  ${path}`);
    if (result.title) {
      console.log(`     Title: ${result.title}`);
    }
    if (result.context) {
      console.log(`     Context: ${result.context}`);
    }

    let snippet = "";
    if (result.bestChunk) {
      snippet = result.bestChunk.trim().replace(/\s+/g, " ").slice(0, 220);
    } else {
      const body = await store.getDocumentBody(result.filepath || result.file);
      if (body) {
        snippet = extractSnippet(body, query, 220).snippet.replace(/\s+/g, " ");
      }
    }
    if (snippet) {
      console.log(`     ${snippet}`);
    }
  }
}

async function main() {
  const { command, options, query } = parseArgs(process.argv.slice(2));
  if (!command) {
    usage();
    process.exit(1);
  }

  const store = await openStore();
  try {
    if (command === "status") {
      const status = await store.getStatus();
      console.log(JSON.stringify(status, null, 2));
      return;
    }

    if (command === "update") {
      const result = await store.update();
      console.log(JSON.stringify(result, null, 2));
      return;
    }

    if (command === "embed") {
      await store.update();
      const result = await store.embed({ force: options.force });
      console.log(JSON.stringify(result, null, 2));
      return;
    }

    if (command === "warmup") {
      await store.update();
      const status = await store.getStatus();
      if (!status.hasVectorIndex || status.needsEmbedding > 0) {
        console.error("Embeddings are missing. Run `npm run qmd:embed` first.");
        process.exit(2);
      }
      const warmupQuery = query || "wiki";
      const results = await store.search({ query: warmupQuery, limit: 1 });
      console.log(`Warmed query models with "${warmupQuery}". ${results.length} result(s).`);
      return;
    }

    if (command === "search") {
      if (!query) {
        usage();
        process.exit(1);
      }
      await store.update();
      const results = await store.searchLex(query, { limit: options.limit, collection: "wiki" });
      await formatResults(store, results, query, options.json);
      return;
    }

    if (command === "query") {
      if (!query) {
        usage();
        process.exit(1);
      }
      await store.update();
      const status = await store.getStatus();
      if (!status.hasVectorIndex || status.needsEmbedding > 0) {
        console.error("QMD semantic search is not initialized. Run `npm run qmd:init` first.");
        process.exit(2);
      }
      const results = await store.search({
        query,
        limit: options.limit,
        minScore: options.minScore,
        collection: "wiki",
      });
      await formatResults(store, results, query, options.json);
      return;
    }

    usage();
    process.exit(1);
  } finally {
    await store.close();
  }
}

await main();
