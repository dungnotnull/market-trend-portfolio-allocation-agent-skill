# Financial Market Trend Analysis & Portfolio Allocation ? Agent Skill #143

> A research-first, framework-grounded Claude agent skill that analyzes market trends and proposes **risk-aligned, diversified portfolio allocations** using classical risk-management theory ? Modern Portfolio Theory (Markowitz), CAPM, Fama-French, Black-Litterman, and Risk Parity ? plus a self-improving knowledge pipeline.

**Cluster:** `finance-insurance` &nbsp;?&nbsp; **Skill idea:** 143 &nbsp;?&nbsp; **Status:** Production-ready (v1) &nbsp;?&nbsp; **License:** MIT

> **Disclaimer:** This skill is **educational only**. It is not investment, tax, or legal advice and never issues individualized buy/sell directives or guarantees. Outcomes are uncertain and you can lose money. Past performance does not guarantee future results. Consult a licensed, fiduciary advisor registered in your jurisdiction before acting.

---

## Table of contents
1. [Why this skill](#why-this-skill)
2. [How it works](#how-it-works)
3. [Harness architecture](#harness-architecture)
4. [Scoring model](#scoring-model)
5. [Sub-skills](#sub-skills)
6. [Quickstart](#quickstart)
7. [Using the skill](#using-the-skill)
8. [Knowledge pipeline](#knowledge-pipeline)
9. [Testing](#testing)
10. [Degraded mode & error handling](#degraded-mode--error-handling)
11. [Safety & compliance](#safety--compliance)
12. [Repository layout](#repository-layout)
13. [Frameworks referenced](#frameworks-referenced)
14. [Roadmap](#roadmap)
15. [Contributing](#contributing)
16. [License](#license)

---

## Why this skill

Investors commonly chase trends and concentrate risk without aligning allocations to their **risk capacity** or applying diversification theory. This skill provides an expert-grade, evidence-based, **theory-grounded** allocation analysis that:

- selects and justifies a **named, citable** framework for each case (never ad-hoc criteria),
- scores a portfolio across five weighted dimensions with cited evidence,
- runs a **mandatory devil's-advocate challenge** stage to counter confirmation bias,
- enforces a **blocking compliance gate** with jurisdiction-aware disclaimers before any output, and
- keeps itself current via a **self-improving knowledge pipeline** (ArXiv + authoritative sources).

It is part of the `finance-insurance` agent-skill cluster and is designed to be **reusable and composable** by sibling skills.

## How it works

The skill is a **markdown harness** (`skills/main.md`) that orchestrates sub-skills in a fixed, gated order. Each stage emits a structured JSON-shaped payload carrying `stage`, `status`, `certainty`, and `limitations`, and downstream stages consume ? but never mutate ? upstream payloads.

```
user request
    |
    v
[sub-intake] -- ask batched clarifying questions if facts missing --+
    |                                                               |
    v                                                               |
[sub-framework-selector] -- choose & justify named framework(s)      |
    |                                                               |
    v                                                               |
[research] -- WebSearch/WebFetch + SECOND-KNOWLEDGE-BRAIN            |
    |                                                               |
    v                                                               |
[sub-scoring-engine] -- 0-100 per dimension, weighted total, grade  |
    |                                                               |
    v                                                               |
[challenge] -- devil's advocate, test assumptions, grade certainty   |
    |                                                               |
    v                                                               |
[sub-improvement-roadmap] -- prioritized impact/effort actions       |
    |                                                               |
    v                                                               |
[sub-compliance-check]  *** BLOCKING GATE *** -- disclaimers + rules |
    |                                                               |
    v                                                               |
[synthesize] -- assemble professional report, run Quality Gates       |
    |                                                               |
    +<-- if gate blocks: apply remediation, re-run affected stage <---+
    |
    v
final deliverable (with disclaimer)
```

## Harness architecture

| Stage | Sub-skill | Responsibility |
|---|---|---|
| 1 | `sub-intake` | Gather structured inputs, scope, goals; classify archetype; detect degraded mode. |
| 2 | `sub-framework-selector` | Pick & justify named framework(s); map facts to assumptions to choice. |
| 3 | research | Gather highest-tier evidence; fall back to knowledge brain when offline. |
| 4 | `sub-scoring-engine` | Score 5 dimensions 0-100 with citations; weighted total; letter grade. |
| 5 | challenge | Devil's advocate: test weak assumptions, weigh disconfirming evidence. |
| 6 | `sub-improvement-roadmap` | Prioritized, traceable, educational recommendations (impact / effort). |
| 7 | `sub-compliance-check` | **BLOCKING**: disclaimers, disallowed-pattern detection, remediation. |
| 8 | synthesize | Assemble the professional report; enforce all Quality Gates. |

**Evidence hierarchy** (preferred first): Systematic Review > Meta-Analysis > RCT > Cohort > Expert Opinion > Blog.

## Scoring model

| Dimension | Weight | What is assessed |
|---|---|---|
| Risk-tolerance alignment | 25% | allocation vs capacity/horizon |
| Diversification quality | 25% | correlation, factor/geographic spread |
| Risk-adjusted return | 20% | Sharpe/Sortino, efficient-frontier fit |
| Cost & tax efficiency | 15% | fees, turnover, tax drag |
| Rebalancing & discipline | 15% | rules, drift bands |

Each dimension is scored 0-100 with at least one cited source or named framework (or explicitly marked `evidence_basis = "none"` with a limitation). The weighted total maps to a letter grade:

| Grade | Weighted total |
|---|---|
| A | 90+ |
| B | 75 - 89 |
| C | 60 - 74 |
| D | below 60 |

## Sub-skills

- **`sub-intake`** ? structured intake schema, archetype classification (`allocation` / `concentration-risk` / `factor-tilt` / `compliance-block` / `degraded` / `other`), degraded-mode detection, batched clarifying questions.
- **`sub-framework-selector`** ? candidate-framework fit scoring, archetype-to-framework mapping, operationalization (what each framework consumes and feeds).
- **`sub-scoring-engine`** ? anchored 0-100 rubric with band descriptors, weighted total, citation enforcement, letter grade.
- **`sub-improvement-roadmap`** ? effort (1-5) / impact (1-5) rubric, `priority = impact / effort` ordering, finding traceability, educational-only enforcement.
- **`sub-compliance-check`** ? jurisdiction-aware disclaimers (generic / US SEC-FINRA / EU MiFID II-ESMA), disallowed-pattern detection, mandatory challenge-stage verification, remediation instructions on block.

## Quickstart

```bash
# 1) (optional) create a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# 2) install dev/test deps (runtime is stdlib-only by default)
pip install -r requirements-dev.txt

# 3) run the offline test suite (no network needed)
pytest tests/test_knowledge_updater.py -q
```

## Using the skill

Load `skills/main.md` and its sub-skills into a Claude session, then ask an allocation question. Example prompts (all educational):

- *"I'm 35, moderate risk ? how to allocate?"*
- *"I'm 80% in one tech stock ? how concentrated is my risk?"*
- *"Should I tilt my portfolio to value?"*
- *"Allocate my portfolio offline (no live data)."*

The harness runs the stages in order, honors the **blocking compliance gate**, and returns a professional report with a disclaimer. If key facts are missing, `sub-intake` asks targeted clarifying questions in a single batched round before proceeding.

## Knowledge pipeline

`tools/knowledge_updater.py` is a self-improving pipeline that grows `SECOND-KNOWLEDGE-BRAIN.md`. It uses the **ArXiv Atom API** for `q-fin.PM` / `q-fin.RM` (stdlib only) and optionally `crawl4ai` for authoritative web sources.

```bash
# Offline check: fetch, parse, score, print ? but do NOT write
python tools/knowledge_updater.py --dry-run --limit 10

# Live append to the knowledge brain (ArXiv API; crawl4ai if installed)
python tools/knowledge_updater.py

# ArXiv only (disable optional crawl4ai web fetcher)
python tools/knowledge_updater.py --no-crawl4ai

# Verbose/debug logging
python tools/knowledge_updater.py --verbose
```

**Recommended schedule:** weekly cron, e.g. `0 3 * * 1 python tools/knowledge_updater.py`.

**Graceful degradation:** if the network or `crawl4ai` is unavailable, the tool logs once and exits `0` so the skill keeps working off the existing knowledge base. Deduplication is by SHA-256 hash (first 16 hex chars) of the URL or DOI, stored as hidden `<!--hash:...-->` markers in the brain file.

## Testing

Two layers of validation:

1. **Automated (offline, no network):** `tests/test_knowledge_updater.py` ? 21 tests covering ArXiv Atom parsing, dedup, relevance/recency scoring, ranking, dry-run behavior, append/dedup, and CLI config.
   ```bash
   pip install -r requirements-dev.txt
   pytest tests/test_knowledge_updater.py -q   # 21 passed
   ```
2. **Behavior spec (for the LLM harness):** `tests/test-scenarios.md` ? 5 core scenarios (allocation, concentration risk, factor tilt, compliance gate, degraded mode) plus isolated gate tests, each with scenario-specific pass criteria mapped to the harness Quality Gates.

## Degraded mode & error handling

- **Degraded mode** triggers when `live_data_available = false` (explicit "offline" request or tool failure): live research is skipped, data-hungry frameworks are dropped (defaults to MPT + Risk Parity with textbook parameters), `Risk-adjusted return` is capped at 50 when no history exists, the deliverable opens with a prominent **"Degraded mode"** notice, and the roadmap includes an item to gather the missing live data.
- **Missing inputs** ? `sub-intake` asks; the harness never guesses personal/financial facts.
- **Conflicting evidence** ? present both, grade certainty, let the challenge stage weigh them.
- **Tool failure** ? fall back to the knowledge base, set `live_data_available = false`, state the limitation.
- **Compliance `block`** ? apply remediation and re-run from the affected stage; a blocked deliverable is never presented.

## Safety & compliance

This is a regulated/sensitive domain, so the bar is high:

- The **compliance gate is BLOCKING** ? it runs before every final deliverable and attaches a jurisdiction-aware disclaimer (generic, US SEC/FINRA, or EU MiFID II/ESMA).
- It detects and blocks disallowed patterns: individualized buy/sell directives, guaranteed returns, "risk-free / can't lose" claims, and market-manipulation framing.
- No guarantees of outcomes; downside and loss-of-principal are stated explicitly.
- The challenge stage is mandatory; skipping it is a compliance-gate failure.

**Nothing here is a recommendation of a specific security or strategy.** Consult a licensed, fiduciary advisor registered in your jurisdiction before acting.

## Repository layout

```
.
+- CLAUDE.md                            # skill index + cluster composition
+- PROJECT-detail.md                    # full technical spec
+- PROJECT-DEVELOPMENT-PHASE-TRACKING.md# phase roadmap (all 100%)
+- README.md                            # this file
+- LICENSE                              # MIT
+- requirements.txt                     # runtime (stdlib by default; crawl4ai optional)
+- requirements-dev.txt                 # pytest
+- .gitignore
+- SECOND-KNOWLEDGE-BRAIN.md            # self-improving knowledge base (real citable seed)
+- skills/
|  +- main.md                           # harness orchestrator
|  +- sub-intake.md
|  +- sub-framework-selector.md
|  +- sub-scoring-engine.md
|  +- sub-improvement-roadmap.md
|  +- sub-compliance-check.md
+- tools/
|  +- knowledge_updater.py             # ArXiv API + optional crawl4ai pipeline
+- tests/
   +- test-scenarios.md                # behavior spec for the harness
   +- test_knowledge_updater.py         # offline pytest suite
```

## Frameworks referenced

| Framework / Standard | Role in this skill | Canonical reference |
|---|---|---|
| Modern Portfolio Theory (Markowitz) | Mean-variance efficient frontier | Markowitz, 1952 |
| CAPM | Single-factor risk premium via beta | Sharpe, 1964 |
| Fama-French 3/5-Factor | Cross-sectional factor exposures | Fama & French, 1993 / 2015 |
| Black-Litterman | Bayesian blend of equilibrium with views | Black & Litterman, 1992 |
| Risk Parity / ERC | Risk-budgeted allocation | Maillard, Roncalli & Teiletche, 2010 |
| Sharpe / Sortino / Max-Drawdown | Risk-adjusted performance metrics | Sharpe, 1994; Lo, 2002 |

Full citations with DOIs are recorded in `SECOND-KNOWLEDGE-BRAIN.md`.

## Roadmap

All development phases (0-5) are 100% complete and production-ready. Operational (post-release) activities:

- Run the first live `knowledge_updater.py` crawl (weekly cron) to grow the knowledge base.
- Expand the `finance-insurance` cluster with sibling skills that compose with this one.

## Contributing

Contributions are welcome. Please:

1. Run the offline test suite before submitting: `pytest tests/test_knowledge_updater.py -q`.
2. Keep sub-skill payloads conforming to the data contract (`stage`, `status`, `certainty`, `limitations`).
3. Never introduce individualized buy/sell directives or guarantees ? the compliance gate must keep passing.
4. Add citations (DOI/URL) for any new framework or score basis.

## License

MIT ? see [LICENSE](LICENSE).
