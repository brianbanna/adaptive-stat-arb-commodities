> **ARCHIVED, SUPERSEDED.** This document predates `SPEC.md` and is no longer the build
> authority for this repo. `SPEC.md` at the repo root is, and `CLAUDE.md` is the
> operating brief. Kept because it is the written record of the legacy pairwise design
> whose hedge ratio path, signals, and equity curve the D3 parity gate must reproduce
> exactly. Read it as evidence of what the refactor has to preserve, never as instructions.
> Archived 17 August 2026.

---

# Development Plan: Adaptive Statistical Arbitrage in Commodity Spreads

## Complete Technical Blueprint

# 1. Project Overview

## Research Question

> Can commodity spreads be traded systematically using adaptive hedge ratios and regime-aware position sizing to capture mean-reversion while avoiding structural breaks?

Commodity traders don't just trade price levels. They trade relationships - the price of WTI crude relative to Brent, the price of gasoline relative to crude, the price of corn relative to wheat. These relationships are grounded in physical economics: refining margins, shipping routes, substitution effects, seasonal demand patterns. When a spread deviates from its historical norm, there is often a fundamental reason it will revert.

The problem is that "historical norm" is not fixed. The WTI-Brent spread changed permanently around 2011 when US shale production shifted the logistics of North American crude. The gold-silver ratio drifts over decades. Static models break during these structural shifts.

This project builds a spread trading framework that adapts - the hedge ratios update in real time via Kalman filtering, the entry thresholds adjust by volatility regime, and the position sizing scales with model confidence. When the relationship breaks down entirely, the system detects it and stops trading.

## Why Spreads Matter in Commodity Trading

**Lower directional risk.** A WTI-Brent trade has minimal exposure to the overall oil price level. If oil goes from $70 to $100, both legs move together. The P&L comes from the relative move, not the absolute move.

**Fundamental anchoring.** Commodity spreads are tied to physical economics. The crack spread (crude vs products) reflects refining margins. The crush spread (soybeans vs meal + oil) reflects processing margins. These have economic floors and ceilings that pure price levels don't have.

**Mean-reversion.** Spreads tend to revert to fair value more reliably than outright prices. A barrel of WTI can go from $30 to $150 without any mean-reversion. But the WTI-Brent differential is bounded by transportation costs, pipeline capacity, and quality differentials.

**Lower margin.** Exchanges recognize that spread positions carry less risk and offer reduced margin requirements. A calendar spread in crude oil might require 20-30% of the margin of an outright position.

## Spread Categories

**Cross-commodity spreads** trade the price relationship between two different but related commodities:
- WTI vs Brent (same product, different location)
- Gold vs Silver (same sector, different fundamentals)
- Corn vs Wheat (substitution relationship)
- Heating Oil vs Crude (refining margin)
- Gasoline vs Crude (crack spread)

**Calendar spreads** trade the price relationship between two expiry dates of the same commodity:
- CL front vs CL 6-month
- NG front vs NG 6-month
- ZC front vs ZC 3-month

Calendar spreads are essentially a bet on curve shape - they trade contango and backwardation directly.

**Processing spreads** trade the input-output relationship:
- Crack spread: crude oil vs gasoline + heating oil
- Crush spread: soybeans vs soybean meal + soybean oil

## Connection to the Other Projects

This project sits downstream of both previous projects:

**From Project 1 (Regime Trading):** The regime detection framework identifies calm, moderate, and turbulent market states. Spread strategies perform differently across regimes - mean-reversion works in calm markets, breaks in turbulent ones. This project uses a VIX-based regime proxy (same approach as Project 2) to condition entry thresholds and position sizing.

**From Project 2 (Curve Factors):** The term structure data and curve construction from the curve project provide the raw material for calendar spreads. Carry and slope metrics help determine when calendar spread entry is favorable. The two projects share the same data pipeline for futures prices.

# 2. Spread Universe

## Cross-Commodity Spreads

| Spread | Long Leg | Short Leg | Economic Basis | Expected Behavior |
|--------|----------|-----------|----------------|-------------------|
| WTI-Brent | CL | CO (or BZ) | Location/quality differential | Mean-reverts around transport cost, ~$3-5 range historically |
| Gold-Silver Ratio | GC | SI (ratio-based) | Monetary vs industrial demand | Mean-reverts slowly, 60-90 range typical |
| Corn-Wheat | ZC | ZW | Feed substitution | Seasonal, reverts when one crop fails and other doesn't |
| Crack Spread | RB + HO | CL | Refining margin | Seasonal (summer gasoline, winter heating oil) |
| Crush Spread | ZM + ZL | ZS | Processing margin | Tied to soybean processor economics |
| Copper-Gold Ratio | HG | GC (ratio-based) | Risk-on/risk-off proxy | Tracks economic growth expectations |

## Calendar Spreads

| Spread | Near Leg | Far Leg | What It Trades |
|--------|----------|---------|----------------|
| CL 1-6 | CL front | CL 6-month | WTI curve shape (contango/backwardation) |
| CL 1-12 | CL front | CL 12-month | Full WTI curve tilt |
| NG 1-6 | NG front | NG 6-month | Natural gas seasonality and storage |
| ZC 1-3 | ZC front | ZC 3rd month | Corn old-crop vs new-crop |
| GC 1-6 | GC front | GC 6-month | Gold carry cost (reflects interest rates) |

## Total: 11 spreads across 3 categories

This gives enough diversification for a multi-spread portfolio without stretching into illiquid or poorly-cointegrated pairs.

# 3. Data Requirements

## Price Data

| Data | Source | Frequency | Role |
|------|--------|-----------|------|
| Continuous futures (front + second month) | Stooq | Daily | Primary price source |
| Back-month continuous contracts | Nasdaq Data Link (CHRIS) | Daily | Calendar spread far legs |
| Front-month validation | yfinance | Daily | Cross-check |

All futures data is shared with Project 2 where possible. If commodity-curve-factors has already downloaded and cached the data, this project reads from the same Parquet files. If running standalone, it downloads independently.

## Brent Crude

Brent requires special handling. It trades on ICE, not CME. Data sources:

| Symbol | Source | Notes |
|--------|--------|-------|
| `CHRIS/ICE_B1` | Nasdaq Data Link | Brent front month continuous |
| `BZ=F` | yfinance | Brent front month (validation) |

## Macro and Fundamental Data

| Data | Source | Purpose |
|------|--------|---------|
| VIX | yfinance | Regime proxy for position sizing |
| Risk-free rate | FRED (DGS3MO) | Sharpe calculation |
| US Dollar Index | FRED (DTWEXBGS) | Macro overlay |

## Data Pipeline

```
Step 1: Load futures prices (Stooq primary, Nasdaq Data Link for back months)
Step 2: Construct spread prices from component legs
Step 3: Download VIX for regime conditioning
Step 4: Download risk-free rate from FRED
Step 5: Validate spread prices against known levels
Step 6: Store as Parquet
```

# 4. Spread Construction

## Simple Spread

For most cross-commodity spreads:

```
spread(t) = price_A(t) - beta * price_B(t)
```

Where beta is the hedge ratio. The choice of beta matters enormously.

## Ratio Spread

For gold-silver and copper-gold, trade the ratio instead:

```
ratio(t) = price_A(t) / price_B(t)

Signal on: z-score of log(ratio)
```

Ratio spreads are better when the absolute price levels differ by orders of magnitude (gold at $2000, silver at $25).

## Processing Spreads

Crack spread (3:2:1):
```
crack = 2 * RB_price * 42 + 1 * HO_price * 42 - 3 * CL_price
```

Crush spread:
```
crush = ZM_price * 0.022 + ZL_price * 11 - ZS_price
```

The conversion factors come from exchange specifications and reflect physical processing ratios (bushels to pounds, barrels to gallons).

## Calendar Spreads

```
calendar_spread(t) = F_near(t) - F_far(t)
```

No hedge ratio needed - both legs are the same commodity at different tenors. The spread directly measures the slope of the term structure at that point.

# 5. Cointegration Analysis

## Why It Matters

A spread is only tradeable if it reverts to a stable mean. Cointegration is the statistical test for this property. Two price series are cointegrated if some linear combination of them is stationary (mean-reverting) even though each individual series is non-stationary (trending).

## Engle-Granger Test

```python
# Step 1: Regress Y on X
beta = OLS(Y ~ X).params[1]

# Step 2: Compute residual
residual = Y - beta * X

# Step 3: Test residual for stationarity
adf_stat, p_value = adfuller(residual)

# If p_value < 0.05: cointegrated (spread is mean-reverting)
# If p_value > 0.05: not cointegrated (spread may drift)
```

## Johansen Test

For multivariate spreads (crack spread with 3 legs):

```python
result = coint_johansen(data, det_order=0, k_ar_diff=1)
# Returns: trace statistics, eigenvalues, cointegrating vectors
```

## Rolling Cointegration

Cointegration can break over time. Test it on expanding windows:

```python
# At each quarter-end:
#   Run Engle-Granger on [start, current_date]
#   Record p-value
#   If p > 0.10 for 2+ consecutive quarters: flag spread as broken

cointegration_status = rolling_cointegration_test(spread, window="expanding", frequency="quarterly")
```

When cointegration breaks, the spread should stop trading. This is the regime detection component applied at the spread level.

## Spread Quality Metrics

For each spread, compute:

```
Half-life = -log(2) / log(phi)
    where phi = AR(1) coefficient of the spread

Hurst exponent: H < 0.5 means mean-reverting, H > 0.5 means trending

Variance ratio: VR < 1 means mean-reverting
```

Only trade spreads with:
- ADF p-value < 0.05
- Half-life between 5 and 60 trading days
- Hurst exponent < 0.45

# 6. Adaptive Hedge Ratios

## Why Static Ratios Fail

A static hedge ratio (from a single OLS regression over the full sample) assumes the relationship between two commodities is constant. It isn't. The WTI-Brent spread changed structurally in 2011-2013 as US shale production ramped up. A static hedge ratio calibrated on 2005-2010 data would have been wrong for the entire subsequent decade.

## Rolling OLS

The simplest adaptive approach:

```python
# At each date t, estimate beta on the trailing N days
beta(t) = OLS(Y[t-N:t] ~ X[t-N:t]).params[1]
spread(t) = Y(t) - beta(t) * X(t)
```

**Window choice matters.** Too short (30 days): noisy, whipsaw. Too long (500 days): too slow to adapt. Default: 120-day rolling window as a starting point.

## Kalman Filter

The Kalman filter treats the hedge ratio as a hidden state that evolves over time:

```
State equation:     beta(t) = beta(t-1) + eta(t)      eta ~ N(0, Q)
Observation:        Y(t) = alpha(t) + beta(t)*X(t) + eps(t)    eps ~ N(0, R)
```

The filter provides:
- **Time-varying beta(t)** that adapts to structural changes
- **Estimation uncertainty P(t)** from the state covariance - use this for position sizing
- **Filtered residual** that is cleaner than OLS residual

```python
class KalmanHedgeRatio:
    def __init__(self, delta=1e-4, R=1e-3):
        self.delta = delta  # State transition noise (how fast beta can change)
        self.R = R          # Observation noise

    def filter(self, Y, X):
        """
        Returns:
            betas: time-varying hedge ratios
            residuals: filtered spread residuals
            uncertainties: P matrix diagonal (confidence in beta estimate)
        """
```

**Tuning Q and R:** The ratio Q/R controls adaptation speed. High Q/R means beta can change quickly (more adaptive, more noise). Low Q/R means beta changes slowly (smoother, slower to adapt). Cross-validate on rolling windows.

## Comparison: Rolling OLS vs Kalman Filter

| Property | Rolling OLS | Kalman Filter |
|----------|-------------|---------------|
| Adaptation speed | Fixed (window length) | Continuous (Q/R ratio) |
| Confidence estimate | No | Yes (P matrix) |
| Smoothness | Jumps at window boundary | Smooth updates |
| Complexity | Low | Medium |
| When to use | Baseline, simplicity | Primary model, better signals |

Both should be implemented. Rolling OLS is the baseline. Kalman filter is the primary model. Compare their performance.

# 7. Regime Detection for Spreads

## Why Regime Matters for Spread Trading

Mean-reversion strategies work when the relationship is stable. During market stress, correlations spike, liquidity drops, and spreads can blow out far beyond historical norms. A z-score of -3 that normally signals "buy" can go to -8 during a crisis.

## Spread-Level Regime Detection

Apply a simple regime classifier directly to each spread:

```python
def classify_spread_regime(spread_vol, thresholds):
    """
    spread_vol = rolling 20-day std of spread changes

    Regimes:
        stable:     spread_vol < 33rd percentile (expanding)
        widening:   33rd < spread_vol < 80th percentile
        broken:     spread_vol > 80th percentile
    """
```

## Portfolio-Level Regime (VIX-Based)

Same approach as Project 2 - use VIX as a market-wide regime proxy:

```
VIX < 15:  calm     -> trade normally, full position sizes
VIX 15-25: moderate -> tighten entry thresholds, reduce size
VIX > 25:  stressed -> widen thresholds significantly, minimal sizing
```

## Regime-Conditioned Parameters

| Parameter | Calm | Moderate | Stressed |
|-----------|------|----------|----------|
| Entry z-score | 1.5 | 2.0 | 3.0 |
| Exit z-score | 0.3 | 0.5 | 0.5 |
| Position size scalar | 1.0 | 0.6 | 0.2 |
| Stop-loss z-score | 4.0 | 3.5 | 3.0 |
| Max holding period (days) | 60 | 40 | 20 |

In stressed regimes, the system requires more extreme dislocation before entering, takes smaller positions, and cuts faster.

# 8. Trading Signals

## Z-Score Signal

The core signal for all spread strategies:

```python
def compute_spread_zscore(spread, lookback=60, method="expanding"):
    """
    z(t) = (spread(t) - mean(spread[:t])) / std(spread[:t])

    Uses expanding window to prevent lookahead.
    Lookback param controls minimum observation count.
    """
```

## Entry and Exit Rules

```
LONG SPREAD (spread is cheap):
    Enter: z < -entry_threshold (e.g., -2.0 in calm regime)
    Exit:  z > -exit_threshold  (e.g., -0.3, spread reverting toward mean)
    Stop:  z < -stop_threshold  (e.g., -4.0, spread blowing out further)
    Time:  close after max_holding_period days regardless

SHORT SPREAD (spread is expensive):
    Enter: z > +entry_threshold
    Exit:  z < +exit_threshold
    Stop:  z > +stop_threshold
    Time:  close after max_holding_period days
```

## Confirmation Filters

Don't enter purely on z-score. Add confirmation:

```python
# 1. Half-life check: only trade if current half-life is reasonable
if half_life(spread, lookback=120) > 60:
    skip  # spread is too slow to mean-revert profitably

# 2. Cointegration check: only trade if still cointegrated
if adf_pvalue(spread, lookback=252) > 0.10:
    skip  # relationship may be broken

# 3. Regime check: apply regime-conditioned thresholds
entry_z = regime_thresholds[current_regime]["entry"]
```

## Kalman-Based Signal (Enhanced)

Use Kalman filter residual instead of simple spread:

```python
# Instead of: spread = Y - static_beta * X
# Use:        residual = Y - kalman_beta(t) * X

z_kalman(t) = (residual(t) - expanding_mean(residual)) / expanding_std(residual)
```

The Kalman residual is cleaner because the hedge ratio has already adapted to structural changes. This should produce better z-score signals.

## Position Sizing

```python
def compute_position_size(z_score, spread_vol, regime, kalman_uncertainty, config):
    """
    base_size = vol_target / spread_vol
    regime_scalar = config.regime_scalars[regime]
    confidence_scalar = 1.0 / (1.0 + kalman_uncertainty)  # smaller when model is unsure

    final_size = base_size * regime_scalar * confidence_scalar
    """
```

Position size is inversely proportional to spread volatility (vol-targeting), scaled down when the regime is stressed, and scaled down when the Kalman filter is uncertain about the hedge ratio.

# 9. Portfolio Construction

## Multi-Spread Portfolio

Trade all 11 spreads simultaneously. The portfolio construction handles:

```
Step 1: Generate z-score signals for each spread
Step 2: Apply confirmation filters (half-life, cointegration, regime)
Step 3: Compute position size per spread
Step 4: Apply portfolio-level constraints:
    - Max 3 concurrent positions per spread
    - Max 30% notional in any single sector (energy, metals, agriculture)
    - Max 60% total notional exposure
    - Portfolio-level vol target: 8% annualized
Step 5: Apply execution lag (1 day)
Step 6: Compute transaction costs (both legs per spread)
```

## Correlation Management

Spreads can be correlated. WTI-Brent and CL crack spread both have a CL leg. Check:

```python
spread_correlation = spread_returns.corr()
# If two spreads have > 0.6 correlation, reduce combined exposure
```

## Capital Allocation

```yaml
# In configs/strategy.yaml
allocation:
  cross_commodity: 0.50    # 50% to cross-commodity spreads
  calendar: 0.30           # 30% to calendar spreads
  processing: 0.20         # 20% to crack/crush spreads
```

# 10. Backtesting Framework

## Spread-Specific Backtest Requirements

Spread trading is different from single-instrument backtesting:

**Two legs per trade.** Every entry and exit involves two futures contracts. Transaction costs apply to both legs.

**Asynchronous rolls.** The two legs of a cross-commodity spread may roll on different dates. CL rolls on the 3rd business day before the 25th. Brent rolls differently. The backtest must handle this.

**Spread margin.** Exchanges offer margin offsets for recognized spread positions (intra-commodity calendar spreads get the largest offset). The backtest should track margin using spread margin rates, not the sum of outright margins.

## Cost Model

```yaml
# In configs/backtest.yaml
costs:
  per_leg:
    commission_bps: 2
    slippage_bps: 2
  spread_total_round_trip: ~16 bps  # 2 legs x 2 sides x (2+2) bps
  roll_cost_per_leg_bps: 2

  # Spread-specific overrides
  overrides:
    gold_silver:
      slippage_bps: 3  # silver is wider
    crack_spread:
      slippage_bps: 2  # all legs are liquid energy
    corn_wheat:
      slippage_bps: 3  # agriculture is wider
```

## Backtest Engine

```python
def run_spread_backtest(
    spread_signals: dict,          # {spread_name: signal_series}
    component_returns: pd.DataFrame,  # returns of individual futures
    hedge_ratios: dict,            # {spread_name: beta_series}
    config: dict
) -> pd.DataFrame:
    """
    For each spread:
    1. Compute spread return = return_A - beta * return_B
    2. Apply position signal with execution lag
    3. Compute per-leg transaction costs
    4. Track margin (with spread offsets)
    5. Aggregate across all spreads
    6. Compute portfolio-level metrics
    """
```

## Benchmarks

| Benchmark | Description |
|-----------|-------------|
| No-trade | Zero return (natural benchmark for mean-reversion) |
| Static OLS baseline | Same spreads, same signals, but static hedge ratios |
| Equal-weight spread | 1/N across all spreads with no signal, just carry |

The most important comparison is Kalman filter vs static OLS - this demonstrates the value of adaptive hedge ratios.

# 11. Performance Evaluation

## Standard Metrics

Same metrics as the other two projects, plus spread-specific:

| Metric | What It Measures |
|--------|------------------|
| Sharpe Ratio | Risk-adjusted return |
| Sortino Ratio | Downside risk-adjusted return |
| Calmar Ratio | Return per unit of max drawdown |
| Max Drawdown | Worst peak-to-trough |
| CAGR | Compounded annual growth |
| Annual Volatility | Risk level |
| Hit Rate | % of trades with positive P&L |
| Average Holding Period | Mean days per trade |
| Profit Factor | Gross profit / gross loss |
| Win/Loss Ratio | Average winner / average loser |

## Spread-Specific Metrics

| Metric | What It Measures |
|--------|------------------|
| Spread Half-Life | Mean-reversion speed (days) |
| Cointegration p-value | Stability of relationship |
| Hurst Exponent | Mean-reversion strength (< 0.5 is good) |
| Kalman Beta Stability | Std of hedge ratio changes |
| Signal Accuracy | % of entries that reach exit (vs stop or timeout) |
| Regime Hit Rate | Hit rate broken out by calm/moderate/stressed |

## Spread-Level Analysis

For each of the 11 spreads:
```
1. Cumulative P&L
2. Trade-level statistics (win rate, avg winner, avg loser)
3. Half-life stability over time
4. Hedge ratio evolution (Kalman beta timeline)
5. Z-score signal chart with entry/exit markers
6. Performance by regime
```

## Portfolio-Level Analysis

```
1. Portfolio cumulative return vs benchmarks
2. Drawdown chart
3. Rolling 1Y Sharpe
4. Monthly return heatmap
5. Performance by spread category (cross-commodity, calendar, processing)
6. Correlation of spread returns
7. Cost sensitivity (Sharpe vs cost level)
```

# 12. Visualizations

## Chart List

| # | Chart | Purpose |
|---|-------|---------|
| 1 | **Spread time series with z-score bands** | WTI-Brent spread with +/-2 std bands, entry/exit signals marked |
| 2 | **Kalman hedge ratio evolution** | Beta over time for 2-3 key spreads, with uncertainty bands |
| 3 | **Z-score signal chart** | Z-score timeline with entry (green), exit (blue), stop (red) markers |
| 4 | **Spread regime timeline** | Colored bands: stable (green), widening (amber), broken (red) |
| 5 | **Cointegration stability** | Rolling ADF p-value over time per spread |
| 6 | **Half-life distribution** | Histogram of spread half-lives across universe |
| 7 | **Portfolio cumulative return** | Strategy vs static OLS baseline vs no-trade |
| 8 | **Portfolio drawdown** | Underwater chart with regime overlay |
| 9 | **Rolling Sharpe** | 1Y rolling Sharpe for Kalman vs OLS strategies |
| 10 | **Monthly return heatmap** | Year x month for portfolio returns |
| 11 | **Trade scatter** | Each trade: holding period (x) vs return (y), colored by spread |
| 12 | **Performance by spread category** | Grouped bar: Sharpe by cross-commodity, calendar, processing |
| 13 | **Cost sensitivity** | Sharpe vs transaction cost assumption |
| 14 | **Regime-conditional performance** | Hit rate and Sharpe by regime (calm/moderate/stressed) |

### Hero Chart: WTI-Brent Spread with Kalman Beta

The most impressive chart for the website hero section shows the WTI-Brent spread over 15+ years with:
- The spread price series
- The Kalman-filtered hedge ratio (second y-axis), showing how it adapted through the 2011 shale revolution
- Entry/exit signals overlaid
- Regime bands in the background

This single chart demonstrates adaptive hedge ratios, regime awareness, and real trading signals all at once.

# 13. Research Website

## Structure

```
URL: brianbanna.github.io/adaptive-stat-arb-commodities

Sections:
- Hero: Title + WTI-Brent spread chart with Kalman beta overlay
- Key Metrics: Sharpe, Max DD, CAGR, Hit Rate badges
- Spread Intuition: Why commodity spreads mean-revert
- Methodology: OLS vs Kalman filter, with hedge ratio comparison chart
- Regime Conditioning: How parameters adapt to volatility
- Strategy Performance: Cumulative return + drawdown + performance table
- Spread Deep Dive: Individual spread analysis (WTI-Brent, Gold-Silver)
- Cost Sensitivity: Breakeven analysis
- Limitations
- Footer: Links to other projects
```

# 14. Target Architecture

```
adaptive-stat-arb-commodities/
|
├── configs/
│   ├── universe.yaml              # Spread definitions, component legs
│   ├── cointegration.yaml         # Test params, rolling windows, thresholds
│   ├── kalman.yaml                # State-space params, Q/R tuning
│   ├── signals.yaml               # Entry/exit thresholds, confirmation filters
│   ├── regime.yaml                # VIX thresholds, regime-conditioned params
│   ├── strategy.yaml              # Portfolio constraints, allocation, sizing
│   ├── backtest.yaml              # Per-spread costs, margin, execution lag
│   └── evaluation.yaml            # Metrics, benchmarks, stress periods
│
├── src/
│   └── adaptive_stat_arb/
│       ├── data/
│       │   ├── futures_loader.py      # Stooq + Nasdaq Data Link
│       │   ├── spread_builder.py      # Construct spreads from component prices
│       │   └── storage.py             # Parquet I/O
│       │
│       ├── spreads/
│       │   ├── cointegration.py       # Engle-Granger, Johansen, rolling tests
│       │   ├── half_life.py           # OU half-life, Hurst exponent, variance ratio
│       │   └── quality.py             # Spread tradability scoring
│       │
│       ├── models/
│       │   ├── kalman_filter.py       # Time-varying hedge ratio estimation
│       │   ├── rolling_ols.py         # Rolling OLS baseline
│       │   └── regime.py             # VIX-based + spread-level regime detection
│       │
│       ├── signals/
│       │   ├── zscore.py              # Z-score computation (expanding, rolling)
│       │   ├── entry_exit.py          # Entry/exit/stop logic with regime conditioning
│       │   ├── confirmation.py        # Half-life, cointegration, regime filters
│       │   └── sizing.py             # Vol-target, regime scalar, Kalman confidence
│       │
│       ├── backtest/
│       │   ├── engine.py              # Spread-aware backtest (both legs)
│       │   ├── costs.py               # Per-leg costs, spread margin offsets
│       │   └── benchmarks.py          # No-trade, static OLS, equal-weight
│       │
│       ├── evaluation/
│       │   ├── metrics.py             # Standard metrics
│       │   ├── spread_metrics.py      # Half-life, Hurst, trade-level stats
│       │   ├── attribution.py         # Performance by spread, category, regime
│       │   └── report.py              # Tearsheet generation
│       │
│       ├── visualization/
│       │   ├── spreads.py             # Spread time series, z-score charts
│       │   ├── kalman.py              # Hedge ratio evolution, uncertainty bands
│       │   ├── performance.py         # Cumulative, drawdown, rolling Sharpe
│       │   └── tearsheet.py           # Full strategy tearsheet
│       │
│       └── utils/
│           ├── config.py              # YAML config loader
│           ├── paths.py               # Project root, path resolution
│           └── constants.py           # Spread names, colors, sector mappings
│
├── notebooks/
│   ├── 01_data_pipeline.ipynb         # Download and validate futures data
│   ├── 02_spread_construction.ipynb   # Build spreads, validate levels
│   ├── 03_cointegration.ipynb         # Statistical tests, spread quality
│   ├── 04_kalman_filter.ipynb         # Adaptive hedge ratios
│   ├── 05_signals.ipynb               # Z-score, entry/exit, regime conditioning
│   ├── 06_backtest.ipynb              # Run all strategies
│   └── 07_tearsheet.ipynb             # Generate final outputs
│
├── data/
│   ├── raw/
│   ├── cache/
│   └── processed/
│
├── results/
│   ├── figures/
│   ├── tables/
│   └── tearsheets/
│
├── website/
│   ├── index.html
│   ├── css/style.css
│   ├── js/main.js
│   └── assets/figures/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── Makefile
├── pyproject.toml
└── README.md
```

# 15. Phase-by-Phase Development Plan

## Phase 1: Repository Setup (Days 1-2)

**Objective**: Initialize repository with target structure and configs.

### Tasks
- Create GitHub repo, clone, create dev branch
- Create full directory structure
- Write pyproject.toml, Makefile, .gitignore
- Write all YAML config files
- Write utils modules (config.py, paths.py, constants.py)
- Write README
- Commit and push

### Deliverables
- Installable package: `pip install -e .`
- All configs loading: `from adaptive_stat_arb.utils.config import load_config`

## Phase 2: Data Pipeline (Days 3-6)

**Objective**: Download futures data and construct spread prices.

### Tasks
- Implement futures_loader.py (Stooq primary, Nasdaq Data Link for back months)
- Implement spread_builder.py:
  - Simple spreads (WTI - beta * Brent)
  - Ratio spreads (Gold / Silver)
  - Processing spreads (crack, crush with conversion factors)
  - Calendar spreads (F_near - F_far)
- Download VIX and risk-free rate
- Validate: plot all 11 spreads, verify levels make sense
- Store as Parquet

### Deliverables
- `make data` downloads everything
- 11 spread price series validated and stored
- Data validation notebook

## Phase 3: Cointegration and Spread Quality (Days 7-10)

**Objective**: Test which spreads are tradable and characterize their mean-reversion.

### Tasks
- Implement cointegration.py (Engle-Granger, ADF, Johansen)
- Implement half_life.py (OU half-life, Hurst exponent, variance ratio)
- Implement quality.py (tradability score combining tests)
- Run rolling cointegration on all 11 spreads
- Compute half-life and Hurst exponent per spread
- Identify which spreads pass quality filters
- Flag spreads with structural breaks (WTI-Brent around 2011)

### Deliverables
- Cointegration status per spread over time
- Half-life and Hurst exponent time series
- Spread quality ranking
- Notebook with statistical analysis

## Phase 4: Adaptive Hedge Ratios (Days 11-15)

**Objective**: Implement and validate Kalman filter hedge ratios.

### Tasks
- Implement rolling_ols.py (60, 120, 252-day windows)
- Implement kalman_filter.py:
  - State-space model for time-varying beta
  - Q/R parameter tuning (grid search on training data)
  - Uncertainty extraction (P matrix)
  - Filtered residual computation
- Compare Kalman beta vs rolling OLS beta on all spreads
- Validate: does Kalman beta adapt through known structural breaks?
  - WTI-Brent 2011-2013 shale revolution
  - Gold-Silver ratio 2020 COVID spike
- Plot hedge ratio evolution with uncertainty bands

### Deliverables
- Kalman filter producing daily hedge ratios for all spreads
- Comparison notebook: Kalman vs OLS
- Tests for Kalman filter math

## Phase 5: Signal Construction (Days 16-20)

**Objective**: Build complete trading signal pipeline with regime conditioning.

### Tasks
- Implement zscore.py (expanding z-score of Kalman residual)
- Implement regime.py (VIX-based + spread-level regime detection)
- Implement entry_exit.py (entry/exit/stop with regime-conditioned thresholds)
- Implement confirmation.py (half-life, cointegration, regime filters)
- Implement sizing.py (vol-target, regime scalar, Kalman confidence scaling)
- Generate signals for all 11 spreads
- Analyze: signal frequency, holding period distribution, regime filtering rates

### Deliverables
- Daily signals for all spreads (Parquet)
- Signal analysis notebook with z-score charts and entry/exit markers
- Tests confirming no lookahead in signal computation

## Phase 6: Backtesting (Days 21-26)

**Objective**: Run backtests for all strategies with realistic costs.

### Tasks
- Implement backtest/engine.py:
  - Spread-aware backtest (track both legs)
  - Apply execution lag
  - Per-leg transaction costs
  - Roll cost handling
- Implement backtest/costs.py (per-spread cost model)
- Implement backtest/benchmarks.py (no-trade, static OLS, equal-weight)
- Run backtests:
  - Kalman z-score strategy (primary)
  - OLS z-score strategy (baseline)
  - Regime-conditioned Kalman (enhanced)
- Run cost sensitivity analysis (0 to 30 bps round-trip)
- Stress test through 2008, 2011 WTI-Brent break, 2020 COVID

### Deliverables
- Backtested returns for all strategy variants
- Performance comparison table
- Cost sensitivity analysis
- Stress test results

## Phase 7: Evaluation and Visualization (Days 27-32)

**Objective**: Full performance analysis and chart generation.

### Tasks
- Implement all evaluation modules (metrics, spread_metrics, attribution)
- Compute standard metrics + spread-specific metrics for all strategies
- Bootstrap Sharpe confidence intervals
- Implement all visualization modules
- Generate all 14 charts from Section 12
- Build tearsheet
- Analyze performance by spread category and by regime

### Deliverables
- Complete performance analysis
- 14 high-res charts
- Strategy tearsheet
- Attribution analysis by spread, category, regime

## Phase 8: Research Website (Days 33-35)

**Objective**: Build and deploy static website.

### Tasks
- Write index.html with all sections from Section 13
- Write CSS (same dark theme as other projects)
- Copy key figures to website assets
- Write content: spread intuition, methodology, results
- Deploy to GitHub Pages

### Deliverables
- Live website at brianbanna.github.io/adaptive-stat-arb-commodities
- Mobile-responsive, all images optimized

## Estimated Timeline

| Phase | Description | Days | Cumulative |
|-------|-------------|------|------------|
| 1 | Repository setup | 2 | Day 2 |
| 2 | Data pipeline and spread construction | 4 | Day 6 |
| 3 | Cointegration and spread quality | 4 | Day 10 |
| 4 | Kalman filter hedge ratios | 5 | Day 15 |
| 5 | Signal construction | 5 | Day 20 |
| 6 | Backtesting | 6 | Day 26 |
| 7 | Evaluation and visualization | 6 | Day 32 |
| 8 | Research website | 3 | Day 35 |

**Total: ~35 days / 5 weeks**

# 16. Risks and Pitfalls

## Risk 1: Cointegration Breakdown

**Problem**: The core assumption of stat arb is that spreads revert. When they don't, losses can be large and persistent. The WTI-Brent spread changed structurally in 2011. Gold-Silver ratio can trend for years.

**Mitigation**: Rolling cointegration testing with automatic stop. If ADF p-value exceeds 0.10 for two consecutive quarters, flag the spread as "broken" and stop trading. Resume only after cointegration re-establishes. Report broken periods explicitly.

## Risk 2: Kalman Filter Tuning

**Problem**: The Q and R matrices in the Kalman filter control adaptation speed. Wrong values produce either an over-reactive hedge ratio (too noisy) or an under-reactive one (too slow to catch breaks).

**Mitigation**: Grid search Q/R on expanding training windows. Evaluate by: (1) residual stationarity (ADF test), (2) residual half-life (shorter is better), (3) beta smoothness (fewer unnecessary jumps). Document the chosen Q/R and sensitivity around them.

## Risk 3: Overfitting Entry/Exit Thresholds

**Problem**: Optimizing z-score thresholds on historical data is pure curve-fitting. The "optimal" entry at z=-1.8 might just be noise.

**Mitigation**: Use simple round numbers (-2, +2) as defaults. If optimization is done, use walk-forward (optimize on trailing 3 years, test on next year). Report results at multiple threshold levels. If Sharpe varies wildly with small threshold changes, the signal is not robust.

## Risk 4: Transaction Cost Underestimation

**Problem**: Spread trades have double the legs of outright trades. Round-trip costs of 16+ bps eat into the thin mean-reversion alpha.

**Mitigation**: The cost model must account for both legs. Run cost sensitivity from 0 to 30 bps round-trip. Report breakeven cost. If breakeven is below 10 bps, the strategy is only viable for very low-cost execution.

## Risk 5: Survivorship Bias in Spread Selection

**Problem**: Choosing only spreads that "look good" historically is selection bias.

**Mitigation**: Define the spread universe based on economic fundamentals (refining margins, substitution, location differentials) before looking at any data. If a spread is included because of its fundamental basis, that's legitimate. If it's included because "the backtest looked good," that's snooping.

## Risk 6: Negative Oil Prices (April 2020)

**Problem**: WTI went to -$37.63 on April 20, 2020. Any spread involving CL will have extreme values on that date. Z-scores will spike. The Kalman filter may produce absurd hedge ratios.

**Mitigation**: Handle this date explicitly. Options: exclude the specific contract month from that week, cap CL price at $0.01 for spread calculation, or flag it as an outlier and skip signals for that period. Document whichever choice is made.

## Risk 7: Correlated Spread Losses

**Problem**: During a commodity-wide selloff (2008, 2020), all spreads may blow out simultaneously. Diversification across spreads provides less protection than expected.

**Mitigation**: Track rolling correlation of spread returns. Apply portfolio-level vol target (8% annualized) to prevent aggregate exposure from growing too large. During stressed regimes, the position sizing already reduces exposure across all spreads.
