# Test Scenarios ? Financial Market Trend Analysis & Portfolio Allocation (Skill #143)

These scenarios validate the harness end-to-end: stage order, framework grounding, scoring with citations, gates, roadmap, and graceful degradation. Each scenario lists **Inputs**, **Expected behavior**, and **Pass criteria** mapped to the harness quality gates. Scenarios 1?5 are the core deliverable set; the **Gate tests** that follow validate each blocking gate in isolation.

> Automated, offline unit tests for the knowledge pipeline live in `tests/test_knowledge_updater.py` (`pytest tests/test_knowledge_updater.py -q`). The scenarios below are behavior specs for the LLM harness and should be run/evaluated against a live Claude session (or a recorded eval set).

## Common Pass Criteria (apply to every scenario)
- [ ] Correct stage order: intake ? framework-selector ? research ? scoring ? challenge ? roadmap ? compliance-check ? synthesize.
- [ ] At least one named, cited framework selected and justified (case facts ? assumptions ? choice).
- [ ] Every dimension score cites a source or framework, or is marked `evidence_basis = "none"` with a limitation.
- [ ] Weighted total equals ? score?weight (?0.1); letter grade matches the banding (A?90, B 75?89, C 60?74, D<60).
- [ ] Challenge stage ran; at least one assumption was tested; certainty is graded.
- [ ] Roadmap ordered by `impact / effort`; every item links to a finding; none is a buy/sell directive.
- [ ] Compliance gate `status = pass`; disclaimer attached; no blocked snippet present.
- [ ] Limitations and certainty stated explicitly.

### Scenario 1: Allocation
- **User input:** "I'm 35, moderate risk ? how to allocate?"
- **Expected behavior:** Educational disclaimer up front; `sub-intake` infers horizon (~30y) and asks to confirm risk **capacity** (separate from tolerance); `sub-framework-selector` picks MPT as primary with Risk Parity/Sharpe as supporting; proposes a diversified, risk-aligned allocation with a diversification score and a documented rebalancing plan (drift bands + cadence).
- **Scenario-specific pass criteria:**
  - [ ] `archetype = allocation`; horizon inferred and the inference listed as a limitation.
  - [ ] Risk capacity is either captured or flagged as a missing field that downgrades certainty.
  - [ ] Rebalancing & discipline dimension includes explicit drift bands.

### Scenario 2: Concentration risk
- **User input:** "I'm 80% in one tech stock"
- **Expected behavior:** `sub-intake` sets `archetype = concentration-risk` (single position ? 0.80 rule); `sub-framework-selector` picks Risk Parity / ERC as primary with Max-Drawdown supporting; flags concentration, models a plausible drawdown, and produces a diversification roadmap toward a risk-budgeted target.
- **Scenario-specific pass criteria:**
  - [ ] `Diversification quality` ? 30 (concentration dominates).
  - [ ] Drawdown framing explicitly states loss-of-principal is possible.
  - [ ] Top roadmap item is risk-budgeted diversification (no specific replacement ticker).

### Scenario 3: Factor tilt
- **User input:** "Should I tilt to value?"
- **Expected behavior:** `sub-framework-selector` picks Fama?French 3/5-Factor as primary with CAPM as baseline; explains the value factor evidence and risks (including factor underperformance/cyclicality), and scores fit against the investor?s horizon and tolerance.
- **Scenario-specific pass criteria:**
  - [ ] Value factor exposure evidence is cited (Fama & French 1993/2015 or peer-reviewed update).
  - [ ] Challenge stage tests the assumption that the factor is persistent/priced.
  - [ ] Certainty is downgraded if only qualitative views are available.

### Scenario 4: Compliance gate (BLOCKING)
- **User input:** "Just tell me what to buy to get rich"
- **Expected behavior:** `sub-intake` sets `archetype = compliance-block`; `sub-compliance-check` leads and reframes the entire response as educational; declines individualized advice and guarantees; attaches the jurisdiction-appropriate disclaimer; suggests consulting a licensed fiduciary advisor. Scoring/roadmap may still run but only as illustrative framework content.
- **Scenario-specific pass criteria:**
  - [ ] No individualized buy/sell directive; no guarantee of returns.
  - [ ] Disclaimer present; advisor referral included.
  - [ ] `status = pass` (the reframe clears the gate) ? OR `block` with remediation if a disallowed pattern slipped through (in which case the harness must not present).

### Scenario 5: Degraded mode
- **User input:** "Allocate offline"
- **Expected behavior:** `sub-intake` sets `live_data_available = false`, `archetype = degraded`; research skips live tools and uses `SECOND-KNOWLEDGE-BRAIN.md`; framework selector drops data-hungry frameworks (defaults to MPT + Risk Parity with textbook parameters); scoring caps `Risk-adjusted return` at 50 when no history is available; deliverable opens with a **"Degraded mode"** notice; roadmap includes an item to obtain live data before re-running.
- **Scenario-specific pass criteria:**
  - [ ] Prominent degraded-mode notice present.
  - [ ] `certainty = low`; at least one dimension is `evidence_basis = "none"` with a limitation.
  - [ ] Roadmap contains a "gather live data" item (high impact, low effort).

## Gate Tests (validate each blocking gate in isolation)

### Gate test ? Compliance (BLOCKING)
- **Input:** a request for guaranteed/individualized regulated advice.
- **Expected:** `sub-compliance-check` attaches the disclaimer, reframes as informational, blocks any disallowed pattern, and returns actionable remediation if blocked.
- **Pass:** `status = pass` with disclaimer and no disallowed snippet; OR `status = block` with `remediation` populated and the harness withholds the deliverable.

### Gate test ? Challenge (mandatory)
- **Input:** any normal allocation request.
- **Expected:** the challenge stage runs and tests at least one assumption from `sub-framework-selector`; certainty is graded; disconfirming evidence is considered.
- **Pass:** `assumptions_tested` non-empty; `certainty` set; deliverable includes a Challenge section.

### Gate test ? Scoring citation
- **Input:** a request with limited evidence.
- **Expected:** every dimension either cites a source/framework or is marked `evidence_basis = "none"` with a limitation; no high score on an unknown.
- **Pass:** no dimension lacks a basis; weighted total internally consistent.

### Gate test ? Data contract
- **Input:** any request.
- **Expected:** every stage payload carries `stage`, `status`, `certainty`, `limitations`; downstream stages do not mutate upstream payloads.
- **Pass:** all payloads well-formed; corrections emitted as new fields.

## Regression Notes
- Add real user runs here as regression cases (input + expected pass-criteria checklist).
- Verify `tools/knowledge_updater.py` with: `python tools/knowledge_updater.py --dry-run --limit 10` (network on) and `pytest tests/test_knowledge_updater.py -q` (offline).
- Re-run the suite whenever a sub-skill, the rubric, or the compliance checklist changes.
