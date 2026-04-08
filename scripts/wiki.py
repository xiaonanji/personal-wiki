#!/usr/bin/env python3
"""
Minimal local tooling for a markdown-first LLM wiki.

Commands:
  python scripts/wiki.py search "query text"
  python scripts/wiki.py qsearch "query text"
  python scripts/wiki.py qquery "query text"
  python scripts/wiki.py qstatus
  python scripts/wiki.py recent
  python scripts/wiki.py lint
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT / "wiki"
INDEX_FILE = WIKI_DIR / "index.md"
LOG_FILE = WIKI_DIR / "log.md"
QMD_SCRIPT = ROOT / "scripts" / "qmd_store.mjs"

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def markdown_files() -> list[Path]:
    return sorted(path for path in WIKI_DIR.rglob("*.md") if path.is_file())


def page_key(path: Path) -> str:
    relative = path.relative_to(WIKI_DIR).with_suffix("")
    return relative.as_posix()


def load_pages() -> dict[str, dict[str, object]]:
    pages: dict[str, dict[str, object]] = {}
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        key = page_key(path)
        title = extract_title(text) or path.stem
        links = extract_links(text)
        pages[key] = {
            "path": path,
            "text": text,
            "title": title,
            "links": links,
        }
    return pages


def extract_title(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def extract_links(text: str) -> list[str]:
    return [normalize_link(match.group(1).strip()) for match in WIKILINK_RE.finditer(text)]


def normalize_link(link: str) -> str:
    cleaned = link.strip().strip("/")
    return cleaned.removesuffix(".md")


def search(query: str) -> int:
    pages = load_pages()
    terms = [term.lower() for term in re.findall(r"\w+", query) if term.strip()]
    if not terms:
        print("No search terms provided.", file=sys.stderr)
        return 1

    scored: list[tuple[int, str, dict[str, object]]] = []
    for key, page in pages.items():
        haystack = f"{page['title']}\n{page['text']}".lower()
        counts = Counter(haystack.count(term) for term in terms)
        score = sum(haystack.count(term) for term in terms)
        if score:
            scored.append((score + max(counts, default=0), key, page))

    scored.sort(key=lambda item: (-item[0], item[1]))

    for score, key, page in scored[:10]:
        path = Path(page["path"])
        print(f"{score:>3}  {key}  ({path.relative_to(ROOT).as_posix()})")
        excerpt = first_matching_line(str(page["text"]), terms)
        if excerpt:
            print(f"     {excerpt}")
    if not scored:
        print("No matches found.")
    return 0


def first_matching_line(text: str, terms: list[str]) -> str:
    for line in text.splitlines():
        lower = line.lower()
        if any(term in lower for term in terms):
            stripped = line.strip()
            return stripped[:140]
    return ""


def recent() -> int:
    if not LOG_FILE.exists():
        print("wiki/log.md not found.", file=sys.stderr)
        return 1
    entries = [line for line in LOG_FILE.read_text(encoding="utf-8").splitlines() if line.startswith("## [")]
    for line in entries[-10:]:
        print(line)
    return 0


def qmd_available() -> bool:
    return QMD_SCRIPT.exists()


def run_qmd(command: str, query: str | None = None) -> int:
    if not qmd_available():
        print("QMD wrapper not found.", file=sys.stderr)
        return 1

    # Try to find node executable
    node_paths = [
        "C:/Users/sean.ji/node-v24.14.0-win-x64/node.exe",  # User-specific path
        "node",  # Fallback to system PATH
    ]

    node_exe = None
    for path in node_paths:
        if Path(path).exists() if "/" in path or "\\" in path else True:
            node_exe = path
            break

    if not node_exe:
        print("Node executable not found.", file=sys.stderr)
        return 1

    args = [node_exe, str(QMD_SCRIPT), command]
    if query:
        args.append(query)

    result = subprocess.run(args, cwd=ROOT)
    return result.returncode


def qsearch(query: str) -> int:
    result = run_qmd("search", query)
    if result == 0:
        return 0

    print("Falling back to basic local search.", file=sys.stderr)
    return search(query)


def qquery(query: str) -> int:
    result = run_qmd("query", query)
    if result == 0:
        return 0

    print("QMD semantic query unavailable; falling back to basic local search.", file=sys.stderr)
    return search(query)


def qstatus() -> int:
    return run_qmd("status")


def lint() -> int:
    pages = load_pages()
    keys = set(pages)
    inbound: dict[str, set[str]] = defaultdict(set)
    broken: list[tuple[str, str]] = []

    for source_key, page in pages.items():
        for target in page["links"]:
            if target in keys:
                inbound[target].add(source_key)
            else:
                broken.append((source_key, target))

    index_text = INDEX_FILE.read_text(encoding="utf-8") if INDEX_FILE.exists() else ""
    indexed = set(extract_links(index_text))

    exempt_orphans = {
        "home",
        "index",
        "log",
        "entities/README",
        "concepts/README",
        "sources/README",
        "analyses/README",
        "meta/open-questions",
        "meta/contradictions",
    }
    missing_from_index = sorted(key for key in keys if key not in indexed and key not in {"index"})
    orphans = sorted(key for key in keys if key not in inbound and key not in exempt_orphans)

    problems = 0

    if broken:
        problems += len(broken)
        print("Broken links:")
        for source, target in broken:
            print(f"  - {source} -> {target}")

    if missing_from_index:
        problems += len(missing_from_index)
        print("Missing from index:")
        for key in missing_from_index:
            print(f"  - {key}")

    if orphans:
        problems += len(orphans)
        print("Orphan pages:")
        for key in orphans:
            print(f"  - {key}")

    if problems == 0:
        print("Lint passed: no broken links, missing index entries, or unexpected orphans.")
        return 0

    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local helper tools for the LLM wiki.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search wiki pages.")
    search_parser.add_argument("query", help="Search query.")

    qsearch_parser = subparsers.add_parser("qsearch", help="Search wiki pages with qmd, falling back to basic search.")
    qsearch_parser.add_argument("query", help="Search query.")

    qquery_parser = subparsers.add_parser("qquery", help="Run qmd hybrid search, falling back to basic search if needed.")
    qquery_parser.add_argument("query", help="Search query.")

    subparsers.add_parser("recent", help="Show recent log headings.")
    subparsers.add_parser("lint", help="Run simple wiki structure checks.")
    subparsers.add_parser("qstatus", help="Show qmd index status.")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "search":
        return search(args.query)
    if args.command == "qsearch":
        return qsearch(args.query)
    if args.command == "qquery":
        return qquery(args.query)
    if args.command == "recent":
        return recent()
    if args.command == "lint":
        return lint()
    if args.command == "qstatus":
        return qstatus()

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
