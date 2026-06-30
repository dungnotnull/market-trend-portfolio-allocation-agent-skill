# SECOND-KNOWLEDGE-BRAIN.md ? Financial Market Trend Analysis & Portfolio Allocation (Skill #143)

> Self-improving domain knowledge base for the `market-trend-portfolio-allocation` skill. Grown by `tools/knowledge_updater.py` (weekly cron recommended). Newest evidence is preferred per the evidence hierarchy: Systematic Review > Meta-Analysis > RCT > Cohort > Expert Opinion > Blog. Every entry below is real and citable; the updater only appends deduplicated, dated, source-linked entries.

## Core Concepts & Frameworks
- **Modern Portfolio Theory (Markowitz, 1952)** ? Select portfolios that maximize expected return for a given variance; the efficient frontier is the set of portfolios that dominate all others on the mean?variance plane.
- **CAPM (Sharpe 1964, Lintner 1965, Mossin 1966)** ? Equilibrium model where expected excess return of an asset equals its beta times the market risk premium.
- **Fama?French Three/Five-Factor Models (Fama & French 1993, 2015)** ? Extends CAPM with size, value (and later profitability and investment) factors to explain cross-sectional returns.
- **Black?Litterman (Black & Litterman 1992)** ? Combines the market-implied equilibrium returns with an investor's subjective views in a Bayesian manner to produce posterior expected returns for optimization.
- **Risk Parity / Equal Risk Contribution (Maillard, Roncalli, Te?letche 2010)** ? Allocates so each asset contributes equally to portfolio volatility, producing a risk-budgeted rather than capital-budgeted portfolio.
- **Sharpe ratio / Sortino ratio / Maximum drawdown** ? Risk-adjusted performance metrics: Sharpe uses total volatility, Sortino uses downside deviation, max drawdown captures tail loss.

## Key Research Papers (seed literature ? real, citable)
| Title | Authors | Year | Venue | DOI/Link | Relevance |
|---|---|---|---|---|---|
| Portfolio Selection | H. Markowitz | 1952 | The Journal of Finance, 7(1) | https://doi.org/10.2307/2975974 | Foundational MPT / mean?variance optimization. |
| Capital Asset Prices: A Theory of Market Equilibrium Under Conditions of Risk | W. F. Sharpe | 1964 | The Journal of Finance, 19(3) | https://doi.org/10.2307/2977928 | CAPM ? beta and the market risk premium. |
| Common risk factors in the returns on stocks and bonds | E. F. Fama, K. R. French | 1993 | Journal of Financial Economics, 33(1) | https://doi.org/10.1016/0304-405X(93)90023-5 | Three-factor model (market, size, value). |
| A five-factor asset pricing model | E. F. Fama, K. R. French | 2015 | Journal of Financial Economics, 116(1) | https://doi.org/10.1016/j.jfineco.2014.10.015 | Adds profitability and investment factors. |
| Global Portfolio Optimization | F. Black, R. Litterman | 1992 | Financial Analysts Journal, 48(5) | https://doi.org/10.2469/faj.v48.n5.51 | Black?Litterman view-blending. |
| The Properties of Equally Weighted Risk Contribution Portfolios | S. Maillard, T. Roncalli, J. Te?letche | 2010 | The Journal of Portfolio Management, 36(4) | https://doi.org/10.3905/jpm.2010.36.4.060 | Formal properties of risk-parity / ERC. |
| The Sharpe Ratio | W. F. Sharpe | 1994 | The Journal of Portfolio Management, 21(1) | https://doi.org/10.3905/jpm.1994.409501 | Canonical risk-adjusted return measure. |
| The Statistics of Sharpe Ratios | A. Lo | 2002 | Financial Analysts Journal, 58(4) | https://doi.org/10.2469/faj.v58.n4.2453 | Distribution/estimation of Sharpe ratios. |

## State-of-the-Art Methods & Tools
- Apply the frameworks above as the scoring backbone; never score a dimension without a named framework or cited source.
- Prefer primary standards documents and peer-reviewed sources over secondary blogs; the updater ranks by recency ? domain-keyword relevance.
- Combine quantitative scoring with a qualitative challenge (devil's-advocate) stage to counter confirmation bias.
- For live data, prefer programmatic, documented APIs (e.g., ArXiv `q-fin.PM`/`q-fin.RM`) over screen-scraping where possible.

## Authoritative Data Sources
- https://www.cfainstitute.org ? professional standards and curriculum readings.
- https://www.morningstar.com ? fund/ETF data and research.
- https://www.imf.org ? macro outlook and financial stability reports.
- https://www.bis.org ? central-bank research, market liquidity, and Basel standards.
- ArXiv: q-fin.PM (Portfolio Management) and q-fin.RM (Risk Management).

## Analytical Frameworks (Scoring Backbone)
| Framework / Standard | Role in this skill |
|---|---|
| Modern Portfolio Theory (Markowitz) | Mean-variance efficient frontier. |
| CAPM & Fama-French factors | Risk premia and factor exposures. |
| Black-Litterman | Blending market equilibrium with views. |
| Risk parity & diversification | Risk-budgeted allocation. |
| Sharpe/Sortino & max-drawdown | Risk-adjusted performance metrics. |

## Self-Update Protocol (crawl4ai / ArXiv API config)
- **Sources:** the authoritative URLs above + ArXiv categories `q-fin.PM`, `q-fin.RM`.
- **Search queries:**
  - `factor investing performance update`
  - `risk parity portfolio research`
  - `macro regime asset allocation`
  - `rebalancing strategy tax efficiency`
- **Frequency:** weekly (cron: `0 3 * * 1` recommended).
- **Append format:** dated section with Title, Authors, Year, Venue, DOI/URL, key finding, relevance note, and a hidden `<!--hash:...-->` dedup marker.
- **Dedup:** skip entries whose URL/DOI SHA-256 hash (first 16 hex chars) already exists in the brain.

## Knowledge Update Log
- 2026-06-18 ? Knowledge base seeded at skill creation (frameworks + sources).
- 2026-06-30 ? Seed literature replaced with real, citable canonical papers (Markowitz, Sharpe, Fama?French, Black?Litterman, Maillard et al., Lo). Placeholders removed. Pipeline code hardened for production.
