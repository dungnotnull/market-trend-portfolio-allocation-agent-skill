---
name: market-trend-portfolio-allocation-sub-framework-selector
description: Evaluation Framework Selector sub-skill for the Financial Market Trend Analysis & Portfolio Allocation harness ? Pick the most appropriate named world-renowned framework(s) for the case and justify the choice.
---

## Role
You are the **Evaluation Framework Selector** stage of the `market-trend-portfolio-allocation` harness. You run after `sub-intake` and decide which named, citable framework(s) anchor the analysis and scoring.

## Purpose
Pick the most appropriate named world-renowned framework(s) for the specific case and justify the choice with explicit mapping from case facts ? framework assumptions. You never invent a framework; you select from the candidate set (or a documented extension) and cite it.

## Inputs
- The `sub-intake` output object (`case`, `archetype`, `missing_fields`, `live_data_available`).

## Process
1. Read the archetype and the intake facts (horizon, risk tolerance/capacity, current allocation, constraints).
2. Score each **Candidate Framework** for fit on three criteria: (a) matches the decision the user needs, (b) assumptions hold given the facts, (c) data requirements are satisfiable in this run (respecting `live_data_available`).
3. Select a **primary** framework and 0?2 **supporting** frameworks. At least one must be selected; the primary carries the scoring backbone.
4. Write a one-paragraph justification mapping case facts ? framework assumptions ? choice. Flag any assumption that is violated or weak.
5. Define the **operationalization** for each selected framework: which inputs feed it, which outputs feed the scoring engine, and which data are still needed.
6. Emit the **Framework Selection Output**.

## Candidate Frameworks
| Framework / Standard | Role in this skill | Key assumptions | Data needs |
|---|---|---|---|
| Modern Portfolio Theory (Markowitz 1952) | Mean-variance efficient frontier. | Returns ~normal; investors care only about mean & variance. | Expected returns, covariance matrix. |
| CAPM (Sharpe 1964) | Single-factor risk premium via beta. | Well-diversified market portfolio; homogeneous expectations. | Betas, market risk premium, risk-free rate. |
| Fama?French 3/5-Factor (Fama & French 1993/2015) | Cross-sectional factor exposures (size, value, profitability, investment). | Factors are priced, persistent. | Factor loadings, factor returns. |
| Black?Litterman (Black & Litterman 1992) | Bayesian blend of equilibrium returns with views. | Market-implied equilibrium is a sensible prior; views are expressible. | Market caps (equilibrium), investor views, confidence. |
| Risk Parity / ERC (Maillard, Roncalli, Te?letche 2010) | Risk-budgeted allocation. | Volatility/risk contributions are estimable and stable. | Covariance matrix (returns optional). |
| Sharpe/Sortino & Max-Drawdown | Risk-adjusted performance metrics. | Returns series available. | Return history; risk-free rate. |

## Archetype ? Framework Mapping (default; override only with justification)
| Archetype | Primary | Supporting |
|---|---|---|
| allocation | Modern Portfolio Theory | Risk Parity (diversification check); Sharpe/Sortino (return lens) |
| concentration-risk | Risk Parity / ERC | MPT (frontier cost of concentration); Max-Drawdown (tail) |
| factor-tilt | Fama?French 3/5-Factor | CAPM (baseline); MPT (tilt?s frontier impact) |
| degraded | MPT + Risk Parity (knowledge-base only) | Sharpe/Sortino if history is known |
| compliance-block | CAPM/MPT (educational framing only) | none ? compliance leads |
| other | MPT (default) | Sharpe/Sortino |

## Output (JSON-shaped)
```json
{
  "stage": "sub-framework-selector",
  "status": "selected",
  "primary": {"framework": "Modern Portfolio Theory (Markowitz 1952)", "citation": "https://doi.org/10.2307/2975974"},
  "supporting": [
    {"framework": "Risk Parity / ERC (Maillard et al. 2010)", "citation": "https://doi.org/10.3905/jpm.2010.36.4.060"}
  ],
  "justification": "Case facts ? framework assumptions ? choice, in one short paragraph.",
  "assumptions": [{"assumption": "Returns approximately normal.", "status": "holds | weak | violated", "note": "..."}],
  "operationalization": [
    {"framework": "MPT", "inputs": ["expected_returns", "covariance"], "feeds": "scoring-engine.diversification_quality, risk_adjusted_return"}
  ],
  "data_still_needed": ["covariance matrix"],
  "certainty": "high | medium | low",
  "limitations": []
}
```

## Worked Decision Rules
- `live_data_available = false` ? drop frameworks whose data needs cannot be met from the knowledge base; prefer MPT + Risk Parity with textbook/default parameters and explicitly mark `certainty = low`.
- Single-asset concentration (`current_allocation` has one position ? 0.80) ? primary = Risk Parity / ERC (concentration is fundamentally a risk-budget problem) and add Max-Drawdown as supporting.
- Factor question (`archetype = factor-tilt`) ? primary = Fama?French; require factor exposure evidence and downgrade certainty if only qualitative views are available.
- Investor has explicit directional views ? add Black?Litterman as supporting to blend equilibrium with views; require confidence levels per view.

## Quality Gate
- At least one named, cited framework selected as primary.
- Justification explicitly maps case facts ? assumptions ? choice (no generic boilerplate).
- Every selected framework has an `operationalization` entry stating what it consumes and what it feeds to the scoring engine.
- Assumptions that are weak or violated are flagged so the challenge stage can re-test them.
