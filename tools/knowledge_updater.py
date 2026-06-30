# -*- coding: utf-8 -*-
"""
knowledge_updater.py — self-improving knowledge pipeline for Skill #143
(Financial Market Trend Analysis & Portfolio Allocation, cluster: finance-insurance).

Pipeline
========
1. Fetch  — ArXiv API (Atom XML) for q-fin.PM / q-fin.RM; optional crawl4ai for
            authoritative web sources. Pure-stdlib by default (urllib + xml).
2. Parse  — title, authors, year, venue, DOI/URL, abstract/summary.
3. Score  — recency * domain-keyword relevance; higher is better.
4. Dedup  — skip entries whose URL/DOI SHA-256 hash (first 16 hex) already
            exists in SECOND-KNOWLEDGE-BRAIN.md (hidden <!--hash:...--> markers).
5. Append — date-stamped, ranked, well-formed Markdown entries.
6. Exit   — graceful degradation: network unavailable -> log + exit 0 so the
            skill keeps working off the existing knowledge base.

Usage
=====
    python tools/knowledge_updater.py                 # live run
    python tools/knowledge_updater.py --dry-run       # parse + score + print, no write
    python tools/knowledge_updater.py --limit 20      # cap fetched entries per category
    python tools/knowledge_updater.py --no-arxiv --no-web   # no-op graceful exit
    python tools/knowledge_updater.py --verbose

Schedule: weekly cron, e.g.  `0 3 * * 1  python tools/knowledge_updater.py`
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import html
import logging
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Iterable

# --------------------------------------------------------------------------- #
# Constants & defaults
# --------------------------------------------------------------------------- #

DEFAULT_ARXIV_CATEGORIES = ("q-fin.PM", "q-fin.RM")
DEFAULT_WEB_SOURCES = (
    "https://www.cfainstitute.org",
    "https://www.morningstar.com",
    "https://www.imf.org",
    "https://www.bis.org",
)
DEFAULT_SEARCH_QUERIES = (
    "factor investing performance update",
    "risk parity portfolio research",
    "macro regime asset allocation",
    "rebalancing strategy tax efficiency",
)
ARXIV_API = "http://export.arxiv.org/api/query"
USER_AGENT = "skill-143-knowledge-updater/1.0 (+educational research)"
HTTP_TIMEOUT = 20  # seconds

BRAIN_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "SECOND-KNOWLEDGE-BRAIN.md")
)

# Atom namespaces used by the ArXiv API.
_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
}

_HASH_RE = re.compile(r"<!--hash:([0-9a-f]{16})-->")

logger = logging.getLogger("knowledge_updater")


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass
class Entry:
    """A single knowledge-base entry."""

    title: str
    authors: str
    year: str
    venue: str
    url: str
    abstract: str = ""
    doi: str = ""
    published: str = ""  # ISO date if known

    @property
    def dedup_key(self) -> str:
        """Stable hash used for deduplication (URL preferred, else DOI)."""
        seed = self.doi or self.url
        return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]

    def relevance_score(self, keywords: Iterable[str]) -> float:
        blob = (self.title + " " + self.abstract).lower()
        kws = [k.lower() for k in keywords]
        if not kws:
            return 0.0
        hits = sum(1 for k in kws if k in blob)
        return hits / len(kws)

    def recency_score(self, today: _dt.date | None = None) -> float:
        """1.0 for current year, decaying by 0.1 per prior year, floored at 0.1."""
        today = today or _dt.date.today()
        try:
            year = int(str(self.year)[:4])
        except (TypeError, ValueError):
            return 0.1
        delta = max(0, today.year - year)
        return max(0.1, 1.0 - 0.1 * delta)


@dataclass
class Config:
    brain_path: str = BRAIN_PATH
    arxiv_categories: tuple[str, ...] = DEFAULT_ARXIV_CATEGORIES
    web_sources: tuple[str, ...] = DEFAULT_WEB_SOURCES
    search_queries: tuple[str, ...] = DEFAULT_SEARCH_QUERIES
    limit: int = 50
    arxiv: bool = True
    web: bool = True
    crawl4ai: bool = True
    dry_run: bool = False
    verbose: bool = False

    @property
    def relevance_keywords(self) -> list[str]:
        return [w for q in self.search_queries for w in q.split()]


# --------------------------------------------------------------------------- #
# Networking helpers (stdlib only; isolated so tests can mock)
# --------------------------------------------------------------------------- #

def _http_get(url: str, timeout: int = HTTP_TIMEOUT) -> str:
    """Perform a GET request and return decoded text. Raises on HTTP error."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (trusted URLs)
        raw = resp.read()
    charset = resp.headers.get_content_charset() or "utf-8"
    return raw.decode(charset, errors="replace")


# --------------------------------------------------------------------------- #
# ArXiv fetcher
# --------------------------------------------------------------------------- #

def _arxiv_url(category: str, limit: int) -> str:
    # ArXiv API expects the category with a dot, e.g. q-fin.PM.
    params = {
        "search_query": f"cat:{category}",
        "start": "0",
        "max_results": str(limit),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    return ARXIV_API + "?" + urllib.parse.urlencode(params)


def _parse_year(published: str) -> str:
    if not published:
        return ""
    m = re.match(r"(\d{4})", published)
    return m.group(1) if m else ""


def parse_arxiv_atom(xml_text: str) -> list[Entry]:
    """Parse an ArXiv API Atom feed into Entry objects. Namespace-aware."""
    entries: list[Entry] = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        logger.warning("arxiv: failed to parse Atom feed: %s", exc)
        return entries

    for el in root.findall("atom:entry", _NS):
        title_el = el.find("atom:title", _NS)
        summary_el = el.find("atom:summary", _NS)
        published_el = el.find("atom:published", _NS)
        id_el = el.find("atom:id", _NS)
        doi_el = el.find("arxiv:doi", _NS)

        title = html.unescape((title_el.text or "").strip()) if title_el is not None else ""
        summary = html.unescape((summary_el.text or "").strip()) if summary_el is not None else ""
        published = (published_el.text or "").strip() if published_el is not None else ""
        arxiv_id = (id_el.text or "").strip().rsplit("/", 1)[-1] if id_el is not None else ""

        authors = []
        for a in el.findall("atom:author", _NS):
            name = a.find("atom:name", _NS)
            if name is not None and name.text:
                authors.append(name.text.strip())
        authors_str = ", ".join(authors) if authors else "-"

        doi = (doi_el.text or "").strip() if doi_el is not None else ""
        url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else (doi and f"https://doi.org/{doi}")
        if not url:
            continue

        entries.append(
            Entry(
                title=title or f"arXiv {arxiv_id}",
                authors=authors_str,
                year=_parse_year(published),
                venue="arXiv",
                url=url,
                abstract=summary,
                doi=doi,
                published=published[:10],
            )
        )
    return entries


def fetch_arxiv(cfg: Config) -> list[Entry]:
    """Fetch recent entries from each configured ArXiv category."""
    out: list[Entry] = []
    for cat in cfg.arxiv_categories:
        url = _arxiv_url(cat, cfg.limit)
        try:
            text = _http_get(url)
            parsed = parse_arxiv_atom(text)
            logger.info("arxiv %s: parsed %d entries", cat, len(parsed))
            out.extend(parsed)
        except Exception as exc:  # network/DNS/HTTP/parse -> graceful degradation
            logger.warning("arxiv %s: fetch failed (%s); skipping", cat, exc)
    return out


# --------------------------------------------------------------------------- #
# Web source fetcher (optional, crawl4ai if installed)
# --------------------------------------------------------------------------- #

def fetch_web(cfg: Config) -> list[Entry]:
    """Fetch authoritative web sources via crawl4ai when available.

    crawl4ai is optional and heavyweight; if it is not installed the function
    logs once and returns [] (graceful degradation). The skill keeps working
    off ArXiv results and the existing knowledge base.
    """
    if not cfg.web:
        return []
    try:
        from crawl4ai import WebCrawler  # type: ignore
    except Exception as exc:
        logger.info("crawl4ai unavailable (%s); skipping web sources", exc)
        return []

    out: list[Entry] = []
    try:
        crawler = WebCrawler()
        crawler.warmup()
        for src in cfg.web_sources:
            try:
                res = crawler.run(url=src)
                md = getattr(res, "markdown", "") or ""
                if md.strip():
                    out.append(
                        Entry(
                            title=f"Update scan: {src}",
                            authors="-",
                            year=str(_dt.date.today().year),
                            venue=src,
                            url=src,
                            abstract=md[:600],
                        )
                    )
            except Exception as exc:
                logger.warning("web source %s: crawl failed (%s); skipping", src, exc)
    except Exception as exc:
        logger.warning("crawl4ai init failed (%s); skipping all web sources", exc)
    return out


# --------------------------------------------------------------------------- #
# Brain file I/O + dedup + append
# --------------------------------------------------------------------------- #

def existing_hashes(text: str) -> set[str]:
    """Return the set of dedup hashes already present in the brain text."""
    return set(_HASH_RE.findall(text))


def rank_entries(entries: list[Entry], keywords: list[str]) -> list[Entry]:
    """Rank by relevance * recency (descending). Stable on title as tiebreak."""
    today = _dt.date.today()
    return sorted(
        entries,
        key=lambda e: (e.relevance_score(keywords) * e.recency_score(today), e.title.lower()),
        reverse=True,
    )


def format_entry(e: Entry, relevance: float) -> str:
    auth = e.authors or "-"
    year = e.year or "-"
    venue = e.venue or "-"
    finding = (e.abstract or "").strip().replace("\n", " ")
    if len(finding) > 240:
        finding = finding[:237].rstrip() + "..."
    return (
        f"- **{e.title}** — {auth} ({venue}, {year}). "
        f"URL: {e.url}. "
        f"Key finding: {finding or 'n/a'}. "
        f"Relevance: {relevance:.2f}. "
        f"<!--hash:{e.dedup_key}-->"
    )


def append_entries(entries: list[Entry], cfg: Config) -> int:
    """Append deduplicated, ranked entries to the brain file. Returns count added."""
    if not entries:
        logger.info("no entries to append")
        return 0
    if not os.path.exists(cfg.brain_path):
        logger.error("knowledge brain not found: %s", cfg.brain_path)
        return 0

    with open(cfg.brain_path, "r", encoding="utf-8") as fh:
        text = fh.read()
    seen = existing_hashes(text)

    ranked = rank_entries(entries, cfg.relevance_keywords)
    today = _dt.date.today().isoformat()
    lines: list[str] = []
    added = 0
    for e in ranked:
        if not e.url:
            continue
        h = e.dedup_key
        if h in seen:
            continue
        rel = e.relevance_score(cfg.relevance_keywords) * e.recency_score()
        if rel <= 0:
            continue
        lines.append(format_entry(e, rel))
        seen.add(h)
        added += 1

    if added and not cfg.dry_run:
        block = f"\n### Auto-crawl {today}\n" + "\n".join(lines) + "\n"
        with open(cfg.brain_path, "a", encoding="utf-8") as fh:
            fh.write(block)
    logger.info("%s %d new entries to %s",
                "would append" if cfg.dry_run else "appended", added, cfg.brain_path)
    return added


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="knowledge_updater",
        description="Self-improving knowledge pipeline for Skill #143 "
                    "(market-trend-portfolio-allocation).",
    )
    p.add_argument("--brain", default=BRAIN_PATH,
                   help="Path to SECOND-KNOWLEDGE-BRAIN.md (default: repo default).")
    p.add_argument("--limit", type=int, default=50,
                   help="Max entries to fetch per ArXiv category (default: 50).")
    p.add_argument("--dry-run", action="store_true",
                   help="Fetch, parse, score, and print — but do not write to the brain.")
    p.add_argument("--no-arxiv", action="store_true", help="Skip ArXiv fetch.")
    p.add_argument("--no-web", action="store_true", help="Skip web-source fetch.")
    p.add_argument("--no-crawl4ai", action="store_true",
                   help="Disable optional crawl4ai web fetcher (ArXiv still used).")
    p.add_argument("--verbose", "-v", action="store_true", help="Debug logging.")
    return p


def config_from_args(argv: list[str] | None = None) -> Config:
    args = build_arg_parser().parse_args(argv)
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )
    return Config(
        brain_path=os.path.abspath(args.brain),
        limit=max(1, args.limit),
        arxiv=not args.no_arxiv,
        web=not args.no_web,
        crawl4ai=not args.no_crawl4ai,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )


def run(cfg: Config) -> int:
    logger.info("knowledge_updater for skill #143 (market-trend-portfolio-allocation)")
    logger.info("brain=%s dry_run=%s arxiv=%s web=%s",
                cfg.brain_path, cfg.dry_run, cfg.arxiv, cfg.web)
    entries: list[Entry] = []
    if cfg.arxiv:
        entries.extend(fetch_arxiv(cfg))
    if cfg.web and cfg.crawl4ai:
        entries.extend(fetch_web(cfg))

    if cfg.dry_run and entries:
        ranked = rank_entries(entries, cfg.relevance_keywords)
        print(f"--- dry-run: {len(ranked)} ranked entries (top 10 shown) ---")
        for e in ranked[:10]:
            rel = e.relevance_score(cfg.relevance_keywords) * e.recency_score()
            print(f"  [{rel:.2f}] {e.title} ({e.venue}, {e.year}) {e.url}")

    added = append_entries(entries, cfg)
    if added == 0:
        logger.info("no new entries this run (network/dedup/relevance).")
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        cfg = config_from_args(argv)
    except SystemExit as exc:  # argparse --help / error
        return int(exc.code or 0)
    return run(cfg)


if __name__ == "__main__":
    sys.exit(main())
