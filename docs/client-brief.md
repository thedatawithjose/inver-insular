# Client Brief – Portfolio Risk Analytics Engine

Issued by: Inversiones Insular  
Location: Caracas, Venezuela  
Request: Services for a portfolio risk analytics engine

## 1. Client and context

- Client: Inversiones Insular, an investment firm based in Caracas, Venezuela, managing a USD-denominated portfolio of US-listed assets.
- Problem: The investment committee holds a long-only portfolio of US equities and ETFs. Risk is currently reviewed manually in spreadsheets, with no reproducibility. The firm needs a reliable, tested engine that reports portfolio holdings, total risk, and behavior under adverse scenarios.

## 2. Portfolio in scope

- 10 to 12 positions: US large-cap stocks and broad ETFs (equity, Treasuries, gold).
- Daily prices with at least 10 years of history.
- Initial capital: USD 10,000,000.
- Target weights defined by the client and provided as a CSV file.

## 3. Deliverables

1. Data pipeline
   - Download daily prices.
   - Clean data (missing days, splits, outliers).
   - Store results in Parquet.
   - Log all data-quality issues.

2. Portfolio construction
   - Convert target weights into positions.
   - Compute market value and current weights.

3. Risk engine
   - Volatility.
   - Correlation matrix.
   - Maximum drawdown.
   - VaR and CVaR.
   - Contribution to risk by position.

4. Rebalancing backtest
   - Compare:
     - never rebalance
     - rebalance monthly
     - rebalance when weight drift exceeds 5%
   - Include transaction costs.

5. Monte Carlo simulation
   - Simulate 10,000 possible one-year portfolio paths.
   - Report the distribution of outcomes.
   - Document assumptions behind the return model.

6. Stress tests
   - Apply historical shocks including 2008, March 2020, and the 2022 rate shock.
   - Evaluate the current portfolio under each scenario.

7. Report
   - Deliver one reproducible report with results, assumptions, and limitations.

## 4. Technical stack

| Area | Tool |
| --- | --- |
| Language | Python 3.12 |
| Environment and dependencies | uv |
| Data processing | Polars, DuckDB |
| Storage | Parquet |
| Numerical work | NumPy, SciPy |
| Testing | pytest |
| Code quality | Ruff (lint and format), mypy |
| Automation | Makefile, pre-commit, GitHub Actions |
| Editor | VS Code |

## 5. Working method

- Git from day one. Every change must go through a branch, a pull request, and then merge into `main`.
- Direct commits to `main` are not allowed.
- Small, clear commits with descriptive messages, for example: `feat: add max drawdown` or `fix: handle missing prices`.
- Quality gate before every commit: run `make lint` and `make test`; code is only committed once both pass.
- Tests use known results: every formula is checked against a small example calculated by hand.
- Continuous integration: GitHub automatically runs quality checks and tests on every push.

## 6. Acceptance criteria

Inversiones Insular will accept the deliverable when:

- A new analyst can clone the repository and reproduce the full report with one command.
- All tests pass and CI is green.
- Every metric is documented: what it measures, when it fails, and what it does not measure.
- Assumptions such as costs, data source, and risk-free rate are explicitly documented.
- Missing or bad data is handled and reported, never silently ignored.

## 7. Out of scope

- Live trading or order execution.
- Cloud deployment, dashboards, or web applications.
- Machine learning models.
- Tax analytics and options (planned as future phases).

## 8. Milestones

1. Repository setup, environment, quality tools, and CI.
2. Data pipeline and cleaning.
3. Portfolio construction.
4. Risk engine.
5. Rebalancing backtest.
6. Monte Carlo and stress tests.
7. Final report and README.
 