# Adaptive Statistical Arbitrage in Commodity Spreads

**A Quantitative Research Framework**

Trade commodity spread mean-reversion with adaptive hedge ratios and regime-aware position sizing. Detect when relationships break and stop trading.

This framework builds and trades 11 commodity spreads - cross-commodity pairs, calendar spreads, and processing margins - using Kalman filter hedge ratios that adapt to structural changes, z-score signals with regime-conditioned thresholds, and a spread-aware backtest that tracks both legs with realistic costs.

<!--
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)]()
-->

## Overview

Commodity traders don't just trade price levels. They trade relationships - WTI vs Brent, gasoline vs crude, corn vs wheat. These spreads are anchored by physical economics: transportation costs, refining margins, crop substitution. When a spread deviates from its norm, there's usually a reason it will come back.

The problem is that "normal" changes over time. The WTI-Brent spread shifted permanently when US shale ramped up in 2011. A static model trained on pre-shale data would have been wrong for the next decade. This framework adapts - hedge ratios update via Kalman filtering, entry thresholds shift with volatility regime, and when a relationship breaks entirely, the system detects it and steps aside.

**What it does:**

- Constructs 11 commodity spreads across 3 categories (cross-commodity, calendar, processing)
- Tests cointegration and mean-reversion quality on a rolling basis
- Estimates time-varying hedge ratios via Kalman filter (vs rolling OLS baseline)
- Generates z-score trading signals with regime-conditioned entry/exit thresholds
- Sizes positions by spread volatility, regime state, and model confidence
- Runs spread-aware backtests with per-leg transaction costs

**What it produces:**

- Cointegration analysis and spread quality rankings for all pairs
- Kalman filter hedge ratio evolution with uncertainty bands
- Strategy backtests comparing adaptive (Kalman) vs static (OLS) approaches
- Performance tearsheet with trade-level statistics and regime analysis
- Static research website with spread visualization

## Research Pipeline

```
            Futures Price Data
          (Stooq + Nasdaq Data Link)
                    |
          Spread Construction
    (difference, ratio, processing)
                    |
        Cointegration Analysis
     (ADF, Engle-Granger, rolling)
                    |
       Adaptive Hedge Ratios
        (Kalman filter vs OLS)
                    |
          Z-Score Signals
  (regime-conditioned thresholds)
                    |
         Position Sizing
  (vol-target, regime, confidence)
                    |
         Spread Backtest
    (both legs, roll costs, margin)
                    |
      Performance Evaluation
   (Sharpe, trade stats, attribution)
```

## Spread Universe

11 spreads across 3 categories:

| Category | Spread | What It Trades |
| --- | --- | --- |
| **Cross-Commodity** | WTI - Brent | Crude location/quality differential |
| | Gold / Silver ratio | Monetary vs industrial precious metals |
| | Corn - Wheat | Feed grain substitution |
| | Copper / Gold ratio | Risk-on / risk-off proxy |
| **Processing** | Crack Spread (3:2:1) | Crude oil refining margin |
| | Crush Spread | Soybean processing margin |
| **Calendar** | CL front vs 6-month | WTI curve shape |
| | CL front vs 12-month | WTI full curve tilt |
| | NG front vs 6-month | Natural gas seasonality |
| | ZC front vs 3-month | Corn old-crop vs new-crop |
| | GC front vs 6-month | Gold carry cost |

## Models

| Model | Purpose | How It Works |
| --- | --- | --- |
| **Kalman Filter** | Time-varying hedge ratios | State-space model that updates beta continuously as the relationship evolves. Provides uncertainty estimate for position sizing. |
| **Rolling OLS** | Baseline hedge ratios | Simple regression on trailing window (60, 120, 252 days). Comparison benchmark. |
| **Regime Detector** | Adapt trading parameters | VIX-based market regime + spread-level volatility regime. Tightens thresholds and shrinks positions in stress. |
| **Cointegration Tests** | Validate tradeability | Rolling ADF and Engle-Granger tests. Flags broken relationships before losses accumulate. |

## Signals

Z-score of the Kalman-filtered spread residual, with regime-conditioned parameters:

| Regime | Entry z | Exit z | Stop z | Position Scalar |
| --- | --- | --- | --- | --- |
| Calm (VIX < 15) | 1.5 | 0.3 | 4.0 | 1.0x |
| Moderate (VIX 15-25) | 2.0 | 0.5 | 3.5 | 0.6x |
| Stressed (VIX > 25) | 3.0 | 0.5 | 3.0 | 0.2x |

Confirmation filters require: active cointegration (ADF p < 0.05), reasonable half-life (5-60 days), and stable spread regime.

## Data

| Dataset | Source | Frequency |
| --- | --- | --- |
| Continuous futures (front + second month) | Stooq | Daily |
| Back-month contracts (calendar spread far legs) | Nasdaq Data Link | Daily |
| Brent crude | Nasdaq Data Link (ICE) | Daily |
| VIX | yfinance | Daily |
| Risk-free rate | FRED (3M T-bill) | Daily |

`make data` handles all downloads. API keys for Nasdaq Data Link read from environment variables.

## Key Research Outputs

- Cointegration stability analysis for all 11 spreads over time
- Kalman filter hedge ratio evolution with uncertainty bands
- Strategy comparison: adaptive Kalman vs static OLS vs no-trade
- Trade-level statistics (hit rate, holding period, win/loss ratio)
- Performance by spread category, by regime, by time period
- Transaction cost sensitivity and breakeven analysis
- Performance tearsheet with bootstrap confidence intervals
- Research website with spread visualization

## Quickstart

```bash
git clone https://github.com/brianbanna/adaptive-stat-arb-commodities.git
cd adaptive-stat-arb-commodities

pip install -e .

# Run the full pipeline
make all

# Or run stages individually
make data          # Download futures data
make spreads       # Construct spread prices
make models        # Fit Kalman filter and OLS hedge ratios
make signals       # Generate z-score signals with regime conditioning
make backtest      # Run spread backtests with per-leg costs
make evaluate      # Compute performance metrics and attribution
make report        # Generate tearsheet and charts

# Run tests
make test
```

Requires Python 3.10+. Free API key needed for Nasdaq Data Link.

## Project Structure

```
adaptive-stat-arb-commodities/
├── configs/
│   ├── universe.yaml          # Spread definitions, component legs
│   ├── cointegration.yaml     # Test params, rolling windows, quality filters
│   ├── kalman.yaml            # State-space params, Q/R tuning grid
│   ├── signals.yaml           # Entry/exit thresholds, confirmation filters
│   ├── regime.yaml            # VIX thresholds, regime-conditioned params
│   ├── strategy.yaml          # Portfolio constraints, allocation, sizing
│   ├── backtest.yaml          # Per-spread costs, margin, execution lag
│   └── evaluation.yaml        # Metrics, benchmarks, stress test periods
│
├── src/
│   └── adaptive_stat_arb/
│       ├── data/              # Futures loaders, spread builder, storage
│       ├── spreads/           # Cointegration, half-life, quality scoring
│       ├── models/            # Kalman filter, rolling OLS, regime detection
│       ├── signals/           # Z-score, entry/exit, confirmation, sizing
│       ├── backtest/          # Spread-aware engine, per-leg costs, benchmarks
│       ├── evaluation/        # Metrics, spread stats, attribution, reporting
│       ├── visualization/     # Spread charts, Kalman plots, tearsheet
│       └── utils/             # Config loader, paths, constants
│
├── notebooks/                 # Step-by-step research notebooks
├── data/                      # Raw + processed data (git-ignored)
├── results/                   # Figures, tables, tearsheets
├── website/                   # Static research site (GitHub Pages)
├── tests/                     # Unit and integration tests
├── Makefile                   # Pipeline orchestration
└── pyproject.toml             # Dependencies
```

All parameters live in YAML configs. No magic numbers in source code.

## License

MIT

## Disclaimer

Research code for educational and demonstration purposes. Not investment advice. Backtested performance does not guarantee future results.
