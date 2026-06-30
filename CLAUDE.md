# CLAUDE.md ? Financial Market Trend Analysis & Portfolio Allocation (Skill #143)

**Slug:** `market-trend-portfolio-allocation`  ?  **Cluster:** `finance-insurance`  ?  **Source idea:** 143  ?  **Phase:** Built & production-ready (v1)

## Tagline
Analyzes market trends and proposes risk-aligned portfolio allocations using classical risk-management theory plus macro updates.

## Problem This Skill Solves
Investors chase trends and concentrate risk without aligning allocations to their risk capacity or using diversification theory. This skill provides educational, theory-grounded allocation analysis.

## Harness Flow Summary
1. **Intake** (`sub-intake`) ? gather structured inputs, scope, goals; ask batched clarifying questions if key facts are missing.
2. **Framework selection** (`sub-framework-selector`) ? choose and justify named world-renowned framework(s); map case facts ? assumptions ? choice.
3. **Research** (WebSearch/WebFetch + `SECOND-KNOWLEDGE-BRAIN.md`) ? gather highest-tier evidence; degrade gracefully when offline.
4. **Scoring** (`sub-scoring-engine`) ? five-dimension weighted scores (0?100) with citations; weighted total ? letter grade.
5. **Challenge** ? devil's-advocate review of assumptions and weak evidence; grade certainty (mandatory).
6. **Roadmap** (`sub-improvement-roadmap`) ? prioritized effort/impact recommendations traceable to findings (educational only).
7. **Compliance check** (`sub-compliance-check`) ? MANDATORY and BLOCKING before final output; attaches jurisdiction-aware disclaimer.
8. **Synthesize** ? assemble the professional deliverable; pass Quality Gates.

## Gates
- **Compliance gate:** `sub-compliance-check` MUST run before the final deliverable, attaching required disclaimers. If it returns `block`, the harness applies remediation and re-runs; it never presents a blocked deliverable.
- **Quality gates:** every score cites a source/framework (or is marked `evidence_basis = "none"`); challenge stage completed; roadmap traceable and prioritized; limitations/certainty stated.

## Sub-skills
- `skills/sub-compliance-check.md` ? Compliance Check (BLOCKING): jurisdiction-aware disclaimers, disallowed-pattern detection, remediation.
- `skills/sub-intake.md` ? Intake & Context Gathering: structured schema, archetype classification, degraded-mode detection, batched clarifying questions.
- `skills/sub-framework-selector.md` ? Evaluation Framework Selector: candidate-framework fit scoring, archetype?framework mapping, operationalization.
- `skills/sub-scoring-engine.md` ? Scoring Engine: anchored 0?100 rubric, weighted total, letter grade, citation enforcement.
- `skills/sub-improvement-roadmap.md` ? Improvement Roadmap: effort/impact rubric, `priority = impact/effort` ordering, finding traceability.

## Tools Required
- `WebSearch`, `WebFetch` ? live evidence and standards updates
- `Read`, `Write` ? load knowledge base, emit deliverables
- `Bash` ? run `tools/knowledge_updater.py`
- Skill tool ? invoke sub-skills in sequence

## Knowledge Sources
- ArXiv: `q-fin.PM`, `q-fin.RM` (fetched via the ArXiv Atom API in `tools/knowledge_updater.py`)
- Authoritative domain sources:
  - https://www.cfainstitute.org
  - https://www.morningstar.com
  - https://www.imf.org
  - https://www.bis.org
- Crawl queries: factor investing performance update; risk parity portfolio research; macro regime asset allocation; rebalancing strategy tax efficiency

## Supporting Tools
- `tools/knowledge_updater.py` ? ArXiv API + optional crawl4ai pipeline that grows `SECOND-KNOWLEDGE-BRAIN.md` (weekly cron recommended). Stdlib by default; graceful degradation when offline/crawl4ai absent. CLI: `--dry-run`, `--limit`, `--no-arxiv`, `--no-web`, `--no-crawl4ai`, `--verbose`.

## Cross-Skill Composition (finance-insurance cluster)
This skill is designed for reuse within the `finance-insurance` cluster. Sibling skills may compose with it as follows:
- **Reuse `sub-compliance-check`** as the canonical blocking safety gate for any finance/insurance skill that emits regulated-domain output (disclaimers, disallowed-pattern detection, jurisdiction awareness). It is jurisdiction-parameterized so it generalizes beyond portfolio allocation.
- **Reuse `sub-intake`** as a structured intake template (schema + archetype + degraded-mode detection) for adjacent skills (e.g., insurance needs analysis, retirement glidepath), swapping the archetype enum and intake questions.
- **Reuse `sub-scoring-engine`** pattern (anchored rubric + weighted total + citation enforcement) by replacing the dimension table; the engine logic is dimension-agnostic.
- **Reuse `SECOND-KNOWLEDGE-BRAIN.md` + `tools/knowledge_updater.py`** as the shared self-improving knowledge backbone for the cluster: point additional skills' updaters at category-scoped ArXiv feeds and a shared or per-skill brain file.
- **Compose as a sub-step:** a broader financial-planning skill may invoke this skill as its "investment allocation" stage and consume the scored output + roadmap as inputs to a plan-level synthesis.

When composing, preserve the data contract (`stage`, `status`, `certainty`, `limitations` on every payload) so upstream/downstream skills can interoperate.

## Active Development Tasks
- [x] Scaffold full deliverable set
- [x] Define 5 sub-skills with real stage logic, schemas, and decision rules
- [x] Seed SECOND-KNOWLEDGE-BRAIN with real, citable canonical literature
- [x] Production-grade `tools/knowledge_updater.py` (ArXiv API, dedup, CLI, logging, graceful degradation)
- [x] Offline pytest suite (`tests/test_knowledge_updater.py`) + behavior-spec scenarios (`tests/test-scenarios.md`)
- [x] Open-source scaffolding (README, LICENSE, requirements)
- [x] Cross-skill cluster composition documented
- [ ] Expand SECOND-KNOWLEDGE-BRAIN via first live crawl (operational, post-release; weekly cron)

## Related Root Docs
- `PROJECT-detail.md` ? full technical spec
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` ? phase roadmap (all phases 100%)
- `SECOND-KNOWLEDGE-BRAIN.md` ? self-improving knowledge base
- `README.md` ? user-facing overview and quickstart
