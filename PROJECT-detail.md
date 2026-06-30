# PROJECT-detail.md — Financial Market Trend Analysis & Portfolio Allocation (Skill #143)

## Executive Summary
Analyzes market trends and proposes risk-aligned portfolio allocations using classical risk-management theory plus macro updates. This skill is a full Claude harness in the **finance-insurance** cluster. It runs a research-first, framework-grounded workflow that scores the subject against named world-renowned methodologies and returns a prioritized improvement roadmap, while continuously updating its knowledge base.

## Problem Statement
Investors chase trends and concentrate risk without aligning allocations to their risk capacity or using diversification theory. This skill provides educational, theory-grounded allocation analysis.

## Target Users & Use Cases
Practitioners, reviewers, and decision-makers who need an expert-grade, evidence-based assessment in this domain. Trigger examples:
1. **Allocation** — User: "I'm 35, moderate risk — how to allocate?" → Educational disclaimer; sub-profile-intake + MPT allocation, diversification score, rebalancing plan.
2. **Concentration risk** — User: "I'm 80% in one tech stock" → Skill flags concentration, models drawdown, diversification roadmap.
3. **Factor tilt** — User: "Should I tilt to value?" → Skill explains Fama-French value factor evidence/risks, scores fit.
4. **Compliance gate** — User: "Just tell me what to buy to get rich" → COMPLIANCE: declines individualized advice/guarantees, gives educational framework, suggests advisor.
5. **Degraded mode** — User: "Allocate offline" → Falls back to SECOND-KNOWLEDGE-BRAIN, signals it can't fetch live prices/macro data.

## Harness Architecture
```
/market-trend-portfolio-allocation (main.md)
   ├── sub-intake .................... gather inputs & scope
   ├── sub-framework-selector ........ choose world-renowned framework(s)
   ├── [research] WebSearch/WebFetch + SECOND-KNOWLEDGE-BRAIN
   ├── sub-scoring-engine ............ multi-dimensional weighted scoring
   ├── [challenge] devil's-advocate assumption review
   ├── sub-improvement-roadmap ....... prioritized effort/impact actions
   ├── [GATE] sub-compliance-check (BLOCKING)
   └── synthesize ................... professional deliverable + quality gates
```

## Full Sub-Skill Catalog
### sub-compliance-check — Compliance Check
- **Purpose:** Verify outputs against applicable regulations/standards and attach the required informational/non-advice disclaimers before final delivery.
- **Inputs:** case context from prior stage.
- **Outputs:** structured result passed to the next stage.
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** output is complete, evidence-cited, and consistent with frameworks before proceeding.

### sub-intake — Intake & Context Gathering
- **Purpose:** Collect the structured inputs, scope, and goals needed to run the analysis; ask clarifying questions when key facts are missing.
- **Inputs:** case context from prior stage.
- **Outputs:** structured result passed to the next stage.
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** output is complete, evidence-cited, and consistent with frameworks before proceeding.

### sub-framework-selector — Evaluation Framework Selector
- **Purpose:** Pick the most appropriate named world-renowned framework(s) for the case and justify the choice.
- **Inputs:** case context from prior stage.
- **Outputs:** structured result passed to the next stage.
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** output is complete, evidence-cited, and consistent with frameworks before proceeding.

### sub-scoring-engine — Scoring Engine
- **Purpose:** Apply the multi-dimensional rubric to produce weighted scores with evidence citations for each dimension.
- **Inputs:** case context from prior stage.
- **Outputs:** structured result passed to the next stage.
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** output is complete, evidence-cited, and consistent with frameworks before proceeding.

### sub-improvement-roadmap — Improvement Roadmap
- **Purpose:** Generate a prioritized, effort/impact-ranked set of recommendations traceable to the scored findings.
- **Inputs:** case context from prior stage.
- **Outputs:** structured result passed to the next stage.
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** output is complete, evidence-cited, and consistent with frameworks before proceeding.


## Evaluation Frameworks (World-Renowned, Citable)
| Framework / Standard | Role in this skill |
|---|---|
| Modern Portfolio Theory (Markowitz) | Mean-variance efficient frontier. |
| CAPM & Fama-French factors | Risk premia and factor exposures. |
| Black-Litterman | Blending market equilibrium with views. |
| Risk parity & diversification | Risk-budgeted allocation. |
| Sharpe/Sortino & max-drawdown | Risk-adjusted performance metrics. |

## Scoring Model
| Dimension | Weight | What is assessed |
|---|---|---|
| Risk-tolerance alignment | 25% | allocation vs capacity/horizon |
| Diversification quality | 25% | correlation, factor/geographic spread |
| Risk-adjusted return | 20% | Sharpe/Sortino, efficient-frontier fit |
| Cost & tax efficiency | 15% | fees, turnover, tax drag |
| Rebalancing & discipline | 15% | rules, drift bands |
Each dimension is scored 0-100 with cited evidence; the weighted total yields an overall grade (A: 90+, B: 75-89, C: 60-74, D: <60).

## Skill File Format Specification
- Frontmatter: `name`, `description`.
- Required sections: Role & Persona, Workflow (Harness Flow), Sub-skills Available, Tools, Output Format, Quality Gates.

## E2E Execution Flow
1. Parse user request; if inputs are insufficient, `sub-intake` asks targeted questions.
2. `sub-framework-selector` picks framework(s) and justifies the choice.
3. Research stage gathers highest-tier evidence (see evidence hierarchy); degrade gracefully to SECOND-KNOWLEDGE-BRAIN if offline.
4. `sub-scoring-engine` scores each dimension with citations.
5. Challenge stage stress-tests conclusions.
6. `sub-improvement-roadmap` produces ranked actions.
7. `sub-compliance-check` attaches disclaimers and verifies regulatory alignment.\n8. Synthesize deliverable; run Quality Gates; present.

**Error handling:** missing inputs → ask; conflicting evidence → present both and grade certainty; tool failure → fallback + explicit limitation notice.

## SECOND-KNOWLEDGE-BRAIN Integration
- Sources: https://www.cfainstitute.org, https://www.morningstar.com, https://www.imf.org, https://www.bis.org
- ArXiv categories: q-fin.PM, q-fin.RM
- Crawl queries: factor investing performance update; risk parity portfolio research; macro regime asset allocation; rebalancing strategy tax efficiency
- Append format: dated entries with Title, Authors, Year, Venue, DOI/URL, key finding, relevance.

## Supporting Tools Spec
`tools/knowledge_updater.py`: inputs = source list + queries; outputs = appended SECOND-KNOWLEDGE-BRAIN entries; schedule = weekly cron; dedup by URL/DOI hash.

## Quality Gates (must all pass before final output)
- Every score cites at least one source or the chosen framework.
- Compliance check passed; disclaimers attached.\n- Challenge stage completed; key assumptions tested.
- Roadmap items are prioritized by effort and impact and traceable to findings.
- Limitations and evidence certainty are stated explicitly.

## Test Scenarios
1. **Allocation** — User: "I'm 35, moderate risk — how to allocate?" → Educational disclaimer; sub-profile-intake + MPT allocation, diversification score, rebalancing plan.
2. **Concentration risk** — User: "I'm 80% in one tech stock" → Skill flags concentration, models drawdown, diversification roadmap.
3. **Factor tilt** — User: "Should I tilt to value?" → Skill explains Fama-French value factor evidence/risks, scores fit.
4. **Compliance gate** — User: "Just tell me what to buy to get rich" → COMPLIANCE: declines individualized advice/guarantees, gives educational framework, suggests advisor.
5. **Degraded mode** — User: "Allocate offline" → Falls back to SECOND-KNOWLEDGE-BRAIN, signals it can't fetch live prices/macro data.

## Key Design Decisions
1. Framework-grounded scoring (no ad-hoc criteria).
2. Research-first with graceful degradation to the local knowledge brain.
3. Mandatory challenge stage to counter confirmation bias.
4. Hard safety/compliance gates for this regulated/sensitive domain.
5. Self-improving knowledge base via weekly crawl.
