> **ARCHIVED, SUPERSEDED.** This document predates `SPEC.md` and is no longer the build
> authority for this repo. `SPEC.md` at the repo root is, and `CLAUDE.md` is the
> operating brief. Kept because it is the written record of the legacy pairwise design
> whose hedge ratio path, signals, and equity curve the D3 parity gate must reproduce
> exactly. Read it as evidence of what the refactor has to preserve, never as instructions.
> Archived 17 August 2026.

---

# Progress Tracker

> **Current Phase:** Phase 2 — Data Pipeline
> **Last Completed:** Phase 1 (repo setup)
> **Next Task:** Implement `futures_loader.py`

---

## Phase 1: Repository Setup [COMPLETE]
- [x] Create GitHub repo, clone, create dev branch
- [x] Create full directory structure
- [x] Write pyproject.toml, Makefile, .gitignore
- [x] Write all 8 YAML config files
- [x] Write utils modules (config.py, paths.py, constants.py)
- [x] Write README
- **Deliverables:**
  - [x] Installable package structure
  - [x] All configs loading via `load_config()`

## Phase 2: Data Pipeline [NOT STARTED]
- [ ] Implement `data/futures_loader.py` (Stooq primary, Nasdaq Data Link back months, yfinance validation)
- [ ] Implement `data/spread_builder.py` (simple, ratio, processing, calendar spreads)
- [ ] Implement `data/storage.py` (Parquet I/O helpers)
- [ ] Download VIX and risk-free rate
- [ ] Validate: plot all 11 spreads, verify levels
- [ ] Store all data as Parquet
- **Deliverables:**
  - [ ] `make data` downloads everything
  - [ ] 11 spread price series validated and stored
  - [ ] Data validation notebook

## Phase 3: Cointegration & Spread Quality [NOT STARTED]
- [ ] Implement `spreads/cointegration.py` (Engle-Granger, ADF, Johansen, rolling tests)
- [ ] Implement `spreads/half_life.py` (OU half-life, Hurst exponent, variance ratio)
- [ ] Implement `spreads/quality.py` (tradability score)
- [ ] Run rolling cointegration on all 11 spreads
- [ ] Compute half-life and Hurst per spread
- [ ] Identify spreads passing quality filters
- [ ] Flag structural breaks (WTI-Brent ~2011)
- **Deliverables:**
  - [ ] Cointegration status per spread over time
  - [ ] Half-life and Hurst time series
  - [ ] Spread quality ranking

## Phase 4: Adaptive Hedge Ratios [NOT STARTED]
- [ ] Implement `models/rolling_ols.py` (60, 120, 252-day windows)
- [ ] Implement `models/kalman_filter.py` (state-space model, Q/R tuning, P matrix, filtered residuals)
- [ ] Implement `models/regime.py` (VIX-based + spread-level regime detection)
- [ ] Compare Kalman vs OLS on all spreads
- [ ] Validate adaptation through structural breaks (WTI-Brent 2011, Gold-Silver 2020)
- [ ] Plot hedge ratio evolution with uncertainty bands
- **Deliverables:**
  - [ ] Daily hedge ratios for all spreads
  - [ ] Kalman vs OLS comparison
  - [ ] Kalman filter unit tests

## Phase 5: Signal Construction [NOT STARTED]
- [ ] Implement `signals/zscore.py` (expanding z-score of Kalman residual)
- [ ] Implement `signals/entry_exit.py` (entry/exit/stop with regime thresholds)
- [ ] Implement `signals/confirmation.py` (half-life, cointegration, regime filters)
- [ ] Implement `signals/sizing.py` (vol-target, regime scalar, Kalman confidence)
- [ ] Generate signals for all 11 spreads
- [ ] Analyze signal frequency, holding periods, regime filtering rates
- **Deliverables:**
  - [ ] Daily signals for all spreads (Parquet)
  - [ ] Signal analysis with z-score charts
  - [ ] No-lookahead tests

## Phase 6: Backtesting [NOT STARTED]
- [ ] Implement `backtest/engine.py` (spread-aware, both legs, execution lag, costs)
- [ ] Implement `backtest/costs.py` (per-leg costs with spread overrides)
- [ ] Implement `backtest/benchmarks.py` (no-trade, static OLS, equal-weight)
- [ ] Run backtests: Kalman, OLS baseline, regime-conditioned Kalman
- [ ] Cost sensitivity analysis (0–30 bps)
- [ ] Stress test: 2008, 2011 WTI-Brent break, 2020 COVID, 2022 energy spike
- **Deliverables:**
  - [ ] Backtested returns for all variants
  - [ ] Performance comparison table
  - [ ] Cost sensitivity + stress test results

## Phase 7: Evaluation & Visualization [NOT STARTED]
- [ ] Implement `evaluation/metrics.py` (Sharpe, Sortino, Calmar, max DD, CAGR, hit rate, profit factor)
- [ ] Implement `evaluation/spread_metrics.py` (half-life, Hurst, coint p-value, Kalman beta stability)
- [ ] Implement `evaluation/attribution.py` (by spread, category, regime)
- [ ] Implement `evaluation/report.py` (tearsheet generation)
- [ ] Bootstrap Sharpe confidence intervals (10k samples)
- [ ] Implement `visualization/spreads.py` (spread time series, z-score charts)
- [ ] Implement `visualization/kalman.py` (hedge ratio evolution, uncertainty bands)
- [ ] Implement `visualization/performance.py` (cumulative, drawdown, rolling Sharpe)
- [ ] Implement `visualization/tearsheet.py` (full strategy tearsheet)
- [ ] Generate all 14 charts
- **Deliverables:**
  - [ ] Complete performance analysis
  - [ ] 14 high-res charts
  - [ ] Strategy tearsheet
  - [ ] Attribution by spread, category, regime

## Phase 8: Research Website [NOT STARTED]
- [ ] Write `website/index.html` (all sections from dev plan)
- [ ] Write `website/css/style.css` (dark theme)
- [ ] Write `website/js/main.js`
- [ ] Copy key figures to website assets
- [ ] Write content: spread intuition, methodology, results
- [ ] Deploy to GitHub Pages
- **Deliverables:**
  - [ ] Live website at brianbanna.github.io/adaptive-stat-arb-commodities
  - [ ] Mobile-responsive, images optimized
