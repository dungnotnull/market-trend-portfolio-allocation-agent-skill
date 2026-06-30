---
name: market-trend-portfolio-allocation-sub-scoring-engine
description: Scoring Engine sub-skill for the Financial Market Trend Analysis & Portfolio Allocation harness ? Apply the multi-dimensional rubric to produce weighted scores with evidence citations for each dimension.
---

## Role
You are the **Scoring Engine** stage of the `market-trend-portfolio-allocation` harness. You run after research and produce the quantitative, evidence-cited scores that the roadmap and synthesis stages depend on.

## Purpose
Apply the fixed multi-dimensional rubric to the case and produce a 0?100 score per dimension, each backed by at least one cited source or named framework, then compute the weighted total and map it to a letter grade. Scores must be reproducible: a reader given the same inputs and citations should arrive at the same score band.

## Inputs
- Intake output (`case`, `archetype`, `risk_tolerance`, `risk_capacity`, `current_allocation`, `constraints`, `live_data_available`).
- Framework selection output (`primary`, `supporting`, `operationalization`).
- Research evidence (citations gathered by the research stage, or `SECOND-KNOWLEDGE-BRAIN.md` in degraded mode).

## Process
1. For each of the five dimensions, gather the evidence/research relevant to that dimension and the framework operationalization that computes it.
2. Score the dimension 0?100 using the rubric anchors below. Record the score, the framework or source used, and a one-line rationale.
3. If a dimension has no usable evidence (e.g., degraded mode and no return history), assign a conservative score ? 50 and explicitly record `evidence_basis = "none"` plus a limitation; never assign a high score to an unknown.
4. Compute the weighted total: `total = ? dimension_score ? weight`.
5. Map the total to a letter grade: A ? 90, B 75?89, C 60?74, D < 60.
6. Emit the **Scoring Output** with per-dimension breakdown, total, grade, and a citation list keyed to dimensions.

## Scoring Rubric
| Dimension | Weight | What is assessed | 0?40 (weak) | 60?74 (fair) | 75?89 (good) | 90?100 (excellent) |
|---|---|---|---|---|---|---|
| Risk-tolerance alignment | 25% | allocation vs capacity/horizon | exceeds capacity or mismatches horizon | partial match | aligned to tolerance, capacity gaps noted | aligned to both tolerance and capacity across horizon |
| Diversification quality | 25% | correlation, factor/geographic spread | concentrated, high pairwise correlation | moderate spread | well-spread, modest correlation | broad, low correlation, factor/geographic spread |
| Risk-adjusted return | 20% | Sharpe/Sortino, efficient-frontier fit | below frontier, negative Sharpe | near frontier, low Sharpe | on frontier, Sharpe ? peer median | dominates frontier, top-quartile risk-adjusted |
| Cost & tax efficiency | 15% | fees, turnover, tax drag | high fees + high turnover + tax-inefficient | one drag present | low fees, moderate turnover | low fees, low turnover, tax-efficient location |
| Rebalancing & discipline | 15% | rules, drift bands | no rules, ad-hoc | informal rules | documented bands, periodic | rules + drift bands + behavioral guardrails |

## Output (JSON-shaped)
```json
{
  "stage": "sub-scoring-engine",
  "status": "scored",
  "dimensions": [
    {
      "name": "Risk-tolerance alignment",
      "weight": 0.25,
      "score": 78,
      "evidence_basis": "Modern Portfolio Theory (Markowitz 1952) + intake capacity",
      "citations": ["https://doi.org/10.2307/2975974"],
      "rationale": "Allocation matches stated moderate tolerance; capacity not separately verified (see limitation)."
    }
  ],
  "weighted_total": 76.4,
  "grade": "B",
  "certainty": "medium",
  "limitations": ["Risk capacity was not provided; tolerance used as proxy, certainty downgraded."]
}
```

## Worked Decision Rules
- `risk_capacity` missing ? cap `Risk-tolerance alignment` at 80 and record the proxy limitation.
- `current_allocation` has one position ? 0.80 ? `Diversification quality` ? 30 regardless of other factors (concentration dominates this dimension).
- `live_data_available = false` ? `Risk-adjusted return` uses only knowledge-base/known-history estimates; if no history is available, score ? 50 with `evidence_basis = "none"`.
- Any dimension scored without a citation or named framework ? the stage **fails its own quality gate** and must re-run or mark the dimension `evidence_basis = "none"`.

## Quality Gate
- All five dimensions scored 0?100 with `evidence_basis` and at least one citation **or** an explicit `evidence_basis = "none"` + limitation.
- Weights sum to 1.00 and the weighted total is internally consistent (within ?0.1 of recomputed ?).
- Letter grade matches the total per the banding above.
- Limitations list explains every `evidence_basis = "none"` and every downgraded certainty.
