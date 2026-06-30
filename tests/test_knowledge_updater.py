# -*- coding: utf-8 -*-
"""Tests for tools/knowledge_updater.py - fully offline (no network).

Run with:  pytest tests/test_knowledge_updater.py -q
"""
import datetime as _dt
import os
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import knowledge_updater as ku  # noqa: E402


# --------------------------------------------------------------------------- #
# Entry / scoring
# --------------------------------------------------------------------------- #

def test_dedup_key_stable_and_16hex():
    e = ku.Entry(title="t", authors="a", year="2024", venue="arXiv",
                 url="https://arxiv.org/abs/2401.00001")
    h = e.dedup_key
    assert len(h) == 16
    assert all(c in "0123456789abcdef" for c in h)
    assert ku.Entry(title="t2", authors="a2", year="2025", venue="x",
                    url="https://arxiv.org/abs/2401.00001").dedup_key == h


def test_dedup_key_uses_doi_when_url_empty():
    e = ku.Entry(title="t", authors="a", year="2024", venue="v",
                 url="", doi="10.2307/2975974")
    assert e.dedup_key and len(e.dedup_key) == 16


def test_relevance_score_counts_keywords():
    e = ku.Entry(title="Risk parity portfolio research", authors="a", year="2024",
                 venue="v", url="u", abstract="macro regime asset allocation")
    kws = ["risk", "parity", "portfolio", "research", "macro", "regime", "asset", "allocation",
           "factor", "investing", "performance", "update", "rebalancing", "strategy", "tax", "efficiency"]
    # title+abstract contain: risk, parity, portfolio, research, macro, regime, asset, allocation => 8/16
    assert e.relevance_score(kws) == pytest.approx(8 / 16)


def test_relevance_score_empty_keywords():
    e = ku.Entry(title="x", authors="a", year="2024", venue="v", url="u")
    assert e.relevance_score([]) == 0.0


def test_recency_score_current_year_is_one():
    e = ku.Entry(title="t", authors="a", year=str(_dt.date.today().year),
                 venue="v", url="u")
    assert e.recency_score() == 1.0


def test_recency_score_decays_and_floors():
    today = _dt.date.today()
    e_old = ku.Entry(title="t", authors="a", year=str(today.year - 20),
                     venue="v", url="u")
    assert e_old.recency_score() == 0.1
    e_mid = ku.Entry(title="t", authors="a", year=str(today.year - 3),
                     venue="v", url="u")
    assert e_mid.recency_score() == pytest.approx(0.7)


def test_recency_score_bad_year_floors():
    e = ku.Entry(title="t", authors="a", year="n/a", venue="v", url="u")
    assert e.recency_score() == 0.1


# --------------------------------------------------------------------------- #
# Atom parsing
# --------------------------------------------------------------------------- #

ATOM_XML = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">'
    '<entry>'
    '<id>http://arxiv.org/abs/2401.00001v1</id>'
    '<updated>2024-01-05T00:00:00Z</updated>'
    '<published>2024-01-02T00:00:00Z</published>'
    '<title>Risk Parity &amp; Portfolio Diversification</title>'
    '<summary>A study of risk-budgeted allocation and rebalancing strategy tax efficiency.</summary>'
    '<author><name>Alice Author</name></author>'
    '<author><name>Bob Author</name></author>'
    '<arxiv:doi>10.1234/abcd</arxiv:doi>'
    '</entry>'
    '<entry>'
    '<id>http://arxiv.org/abs/2401.00002v1</id>'
    '<published>2023-06-01T00:00:00Z</published>'
    '<title>Factor Investing Performance Update</title>'
    '<summary>Macro regime asset allocation evidence.</summary>'
    '<author><name>Carol Author</name></author>'
    '</entry>'
    '</feed>'
)


def test_parse_arxiv_atom_basic():
    entries = ku.parse_arxiv_atom(ATOM_XML)
    assert len(entries) == 2
    e0 = entries[0]
    assert e0.title == "Risk Parity & Portfolio Diversification"  # html.unescaped
    assert e0.authors == "Alice Author, Bob Author"
    assert e0.year == "2024"
    assert e0.venue == "arXiv"
    assert e0.url == "https://arxiv.org/abs/2401.00001v1"
    assert e0.doi == "10.1234/abcd"
    assert "risk-budgeted" in e0.abstract
    assert e0.published == "2024-01-02"
    e1 = entries[1]
    assert e1.year == "2023"
    assert e1.doi == ""


def test_parse_arxiv_atom_invalid_xml_returns_empty():
    assert ku.parse_arxiv_atom("not xml") == []


def test_parse_year_helper():
    assert ku._parse_year("2024-01-02T00:00:00Z") == "2024"
    assert ku._parse_year("") == ""
    assert ku._parse_year("garbage") == ""


# --------------------------------------------------------------------------- #
# Dedup + append
# --------------------------------------------------------------------------- #

def test_existing_hashes_finds_markers():
    text = "blah <!--hash:abcdef0123456789--> more"
    assert ku.existing_hashes(text) == {"abcdef0123456789"}
    assert ku.existing_hashes("no markers here") == set()


def test_append_entries_dedups_and_writes(tmp_path):
    brain = tmp_path / "BRAIN.md"
    brain.write_text("# Brain\n\n## Core\n- seed\n", encoding="utf-8")
    cfg = ku.Config(brain_path=str(brain))
    e = ku.Entry(title="Risk parity portfolio research", authors="A", year="2024",
                 venue="arXiv", url="https://arxiv.org/abs/2401.00099",
                 abstract="macro regime asset allocation rebalancing strategy tax efficiency factor investing performance update")
    added = ku.append_entries([e], cfg)
    assert added == 1
    out = brain.read_text(encoding="utf-8")
    assert "### Auto-crawl" in out
    assert e.dedup_key in out
    # second append -> deduped
    assert ku.append_entries([e], cfg) == 0


def test_append_entries_dry_run_does_not_write(tmp_path):
    brain = tmp_path / "BRAIN.md"
    original = "# Brain\n- seed\n"
    brain.write_text(original, encoding="utf-8")
    cfg = ku.Config(brain_path=str(brain), dry_run=True)
    e = ku.Entry(title="Risk parity portfolio research", authors="A", year="2024",
                 venue="arXiv", url="https://arxiv.org/abs/2401.00098",
                 abstract="macro regime asset allocation rebalancing strategy tax efficiency factor investing performance update")
    assert ku.append_entries([e], cfg) == 1
    assert brain.read_text(encoding="utf-8") == original


def test_append_entries_zero_relevance_skipped(tmp_path):
    brain = tmp_path / "BRAIN.md"
    brain.write_text("# Brain\n", encoding="utf-8")
    cfg = ku.Config(brain_path=str(brain))
    e = ku.Entry(title="Unrelated topic", authors="A", year="2024",
                 venue="arXiv", url="https://arxiv.org/abs/2401.00097",
                 abstract="nothing relevant here at all")
    assert ku.append_entries([e], cfg) == 0


def test_append_entries_missing_brain_returns_zero(tmp_path):
    cfg = ku.Config(brain_path=str(tmp_path / "missing.md"))
    e = ku.Entry(title="t", authors="a", year="2024", venue="v",
                 url="https://arxiv.org/abs/2401.00096")
    assert ku.append_entries([e], cfg) == 0


def test_append_entries_empty_list_returns_zero(tmp_path):
    brain = tmp_path / "BRAIN.md"
    brain.write_text("# Brain\n", encoding="utf-8")
    cfg = ku.Config(brain_path=str(brain))
    assert ku.append_entries([], cfg) == 0


# --------------------------------------------------------------------------- #
# Ranking
# --------------------------------------------------------------------------- #

def test_rank_entries_orders_by_relevance_times_recency():
    kws = ["risk", "parity", "portfolio", "research", "macro", "regime", "asset",
           "allocation", "rebalancing", "strategy", "tax", "efficiency", "factor",
           "investing", "performance", "update"]
    today = _dt.date.today()
    high = ku.Entry(title="Risk parity portfolio research macro regime asset allocation rebalancing strategy tax efficiency factor investing performance update",
                    authors="a", year=str(today.year), venue="v", url="https://arxiv.org/abs/1")
    low = ku.Entry(title="Unrelated", authors="a", year=str(today.year - 5),
                   venue="v", url="https://arxiv.org/abs/2")
    ranked = ku.rank_entries([low, high], kws)
    assert ranked[0].url == high.url


# --------------------------------------------------------------------------- #
# Config / CLI
# --------------------------------------------------------------------------- #

def test_config_default_relevance_keywords_nonempty():
    cfg = ku.Config()
    assert "risk" in cfg.relevance_keywords
    assert "efficiency" in cfg.relevance_keywords


def test_config_from_args_parses_flags():
    cfg = ku.config_from_args(["--dry-run", "--no-web", "--limit", "5", "--brain", "X.md"])
    assert cfg.dry_run is True
    assert cfg.web is False
    assert cfg.arxiv is True
    assert cfg.limit == 5
    assert os.path.basename(cfg.brain_path) == "X.md"


def test_run_no_arxiv_no_web_noop(tmp_path):
    brain = tmp_path / "BRAIN.md"
    brain.write_text("# Brain\n", encoding="utf-8")
    cfg = ku.Config(brain_path=str(brain), arxiv=False, web=False, crawl4ai=False)
    assert ku.run(cfg) == 0
    assert brain.read_text(encoding="utf-8") == "# Brain\n"


def test_format_entry_truncates_long_abstract():
    e = ku.Entry(title="t", authors="a", year="2024", venue="v",
                 url="https://arxiv.org/abs/1", abstract="x" * 500)
    line = ku.format_entry(e, 0.5)
    assert "..." in line
    assert len(e.abstract) > 240
    assert f"<!--hash:{e.dedup_key}-->" in line
