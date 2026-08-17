> **ARCHIVED, SUPERSEDED.** This document predates `SPEC.md` and is no longer the build
> authority for this repo. `SPEC.md` at the repo root is, and `CLAUDE.md` is the
> operating brief. Kept because it is the written record of the legacy pairwise design
> whose hedge ratio path, signals, and equity curve the D3 parity gate must reproduce
> exactly. Read it as evidence of what the refactor has to preserve, never as instructions.
> Archived 17 August 2026.

---

# CLAUDE.md — Adaptive Statistical Arbitrage in Commodity Spreads

## Session Protocol

Every session, follow this exact workflow:

### 1. Check Progress
- Read `.claude/PROGRESS.md` to see what phase/task was last completed
- Read the relevant section of `.claude/development_plan.md` for full context on the current phase
- Briefly tell the user: current phase, what was last completed, what's next

### 2. Pick Up the Next Task
- Identify the next incomplete task from `.claude/PROGRESS.md`
- If starting a new phase, confirm with the user before proceeding
- If resuming mid-phase, continue from where we left off

### 3. Execute the Task
- Work through one task at a time, fully completing it before moving on
- For each source file: read the relevant config YAML, read `.claude/development_plan.md` for specs, then implement
- After implementing, run tests if they exist (`make test`)
- After a task is done, update `.claude/PROGRESS.md` immediately

### 4. Validate Before Moving On
- Every module must have: working imports, no syntax errors, type-consistent interfaces
- Every phase must end with: all deliverables checked off, integration test passing
- Run `python -c "from adaptive_stat_arb.{module} import {class/function}"` to verify imports

### 5. Commit Completed Work
- After completing a logical unit of work (a full module or a phase), ask the user if they want to commit
- Use conventional commit messages: `feat:`, `fix:`, `test:`, `docs:`

---

## Project Architecture

**Package:** `src/adaptive_stat_arb/`
**Configs:** `configs/*.yaml` (8 files, all populated)
**Data:** `data/{raw,cache,processed}/` (git-ignored)
**Results:** `results/{figures,tables,tearsheets}/` (git-ignored)
**Tests:** `tests/{unit,integration,fixtures}/`
**Pipeline:** `Makefile` orchestrates `data → spreads → models → signals → backtest → evaluate → report → website`

### Module Dependency Chain
```
data/ → spreads/ → models/ → signals/ → backtest/ → evaluation/ → visualization/
  ↑                    ↑          ↑
utils/ (config, paths, constants) — used everywhere
```

Modules must be built in dependency order. Never implement a downstream module before its upstream dependency is complete and tested.

---

## Implementation Standards

### Code Style
- Python 3.10+, type hints on all public functions
- Use numpy/pandas idioms, avoid loops where vectorized ops work
- All parameters from YAML configs — never hardcode thresholds or magic numbers
- Load configs via `from adaptive_stat_arb.utils.config import load_config`

### Data Flow
- All intermediate data stored as Parquet in `data/processed/`
- Functions accept and return pandas DataFrames/Series
- Date indices must be `pd.DatetimeIndex`, timezone-naive

### Testing
- Unit tests in `tests/unit/test_{module}.py`
- Test against known values (e.g., Kalman filter on synthetic data with known beta)
- No tests that require live data downloads — use fixtures in `tests/fixtures/`

### Key Risk Mitigations (build these in as you implement)
- **No lookahead:** All signals use expanding/trailing windows only
- **Negative oil prices (Apr 2020):** Handle CL going to -$37.63 — cap or flag as outlier
- **Cointegration breakdown:** Rolling tests must flag "broken" spreads and halt trading
- **Transaction costs:** Always model both legs; default 2 bps commission + 2 bps slippage per leg

---

## Config Reference

| Config | Key Contents |
|--------|-------------|
| `universe.yaml` | 11 spreads, their components, date range (2005-2024) |
| `cointegration.yaml` | ADF/Johansen params, rolling window, quality filters (half-life 5-60d, Hurst < 0.45) |
| `kalman.yaml` | Default delta=1e-4, R=1e-3, tuning grid, OLS baselines (60/120/252d) |
| `signals.yaml` | Entry z=2.0, exit z=0.3, stop z=4.0, max holding 60d, confirmation filters |
| `regime.yaml` | VIX thresholds (15/25), spread vol percentiles (33/80), regime-conditioned params |
| `strategy.yaml` | 8% vol target, max 3 positions/spread, sector limits, category allocation |
| `backtest.yaml` | Per-leg costs 2+2 bps, spread overrides, cost sensitivity 0-30 bps |
| `evaluation.yaml` | Metrics list, bootstrap 10k samples, benchmarks, stress periods |

---

## Target File Structure (what to create per phase)

### Phase 2 — Data Pipeline
- `src/adaptive_stat_arb/data/futures_loader.py` — Stooq primary, Nasdaq Data Link for back months, yfinance validation
- `src/adaptive_stat_arb/data/spread_builder.py` — Simple, ratio, processing (crack 3:2:1, crush), calendar spreads
- `src/adaptive_stat_arb/data/storage.py` — Parquet read/write helpers

### Phase 3 — Cointegration & Spread Quality
- `src/adaptive_stat_arb/spreads/cointegration.py` — Engle-Granger, ADF, Johansen, rolling tests
- `src/adaptive_stat_arb/spreads/half_life.py` — OU half-life, Hurst exponent, variance ratio
- `src/adaptive_stat_arb/spreads/quality.py` — Tradability score combining all tests

### Phase 4 — Adaptive Hedge Ratios
- `src/adaptive_stat_arb/models/kalman_filter.py` — KalmanHedgeRatio class, Q/R tuning, P matrix uncertainty
- `src/adaptive_stat_arb/models/rolling_ols.py` — Rolling OLS with 60/120/252d windows
- `src/adaptive_stat_arb/models/regime.py` — VIX-based + spread-level regime detection

### Phase 5 — Signal Construction
- `src/adaptive_stat_arb/signals/zscore.py` — Expanding z-score of Kalman residual
- `src/adaptive_stat_arb/signals/entry_exit.py` — Entry/exit/stop with regime-conditioned thresholds
- `src/adaptive_stat_arb/signals/confirmation.py` — Half-life, cointegration, regime filters
- `src/adaptive_stat_arb/signals/sizing.py` — Vol-target, regime scalar, Kalman confidence

### Phase 6 — Backtesting
- `src/adaptive_stat_arb/backtest/engine.py` — Spread-aware backtest engine
- `src/adaptive_stat_arb/backtest/costs.py` — Per-leg cost model with spread overrides
- `src/adaptive_stat_arb/backtest/benchmarks.py` — No-trade, static OLS, equal-weight

### Phase 7 — Evaluation & Visualization
- `src/adaptive_stat_arb/evaluation/metrics.py` — Sharpe, Sortino, Calmar, max DD, CAGR, hit rate, profit factor
- `src/adaptive_stat_arb/evaluation/spread_metrics.py` — Half-life, Hurst, cointegration p-value, Kalman beta stability
- `src/adaptive_stat_arb/evaluation/attribution.py` — Performance by spread, category, regime
- `src/adaptive_stat_arb/evaluation/report.py` — Tearsheet generation
- `src/adaptive_stat_arb/visualization/spreads.py` — Spread time series, z-score charts
- `src/adaptive_stat_arb/visualization/kalman.py` — Hedge ratio evolution, uncertainty bands
- `src/adaptive_stat_arb/visualization/performance.py` — Cumulative return, drawdown, rolling Sharpe
- `src/adaptive_stat_arb/visualization/tearsheet.py` — Full strategy tearsheet

### Phase 8 — Research Website
- `website/index.html`, `website/css/style.css`, `website/js/main.js`
