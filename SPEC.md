<!--
REDACTION NOTE. This file is PROJECT-2-COMPLETE-AZ.md reproduced verbatim with 1
token level redaction, at Part H rule 1, required by that rule itself: the prior
employer is not named anywhere in this repo. The same redaction is applied in the
other 2 project repos. Nothing else is altered: no sentence removed, no number
changed, no deliverable dropped. The unredacted master lives outside this repo.
-->

# PROJECT 2: MULTI LEG RELATIVE VALUE WITH BREAK DETECTION AND THE SHARED PRICING ENGINE
## The complete standalone document, A to Z
### Version 2, 10 August 2026. Incorporates all master spec amendments (C4, C5, C6, C8, C10, engine freeze 20 December). Self contained.

---

# PART A. WHAT THIS PROJECT IS, IN PLAIN WORDS

Some commodity prices are chained together by a physical process. Soybeans get crushed into meal and oil, so the price of beans cannot drift arbitrarily far from the combined price of what they become: if it did, crushers would earn absurd margins or shut down, and either response pulls the prices back together. Crude gets refined into gasoline and diesel, same chain. European, American, and Asian gas are connected by LNG ships that physically move molecules toward whichever market pays more.

This project trades those chains. It starts from Brian's existing statistical arbitrage project (pairwise cointegration, a Kalman filter estimating the hedge ratio as it drifts, mean reversion trading on the spread) and upgrades it 4 ways. First, from pairs to 3 leg baskets using the Johansen framework, which finds how many stable relationships exist inside a basket and estimates which leg does the adjusting when they dislocate. Second, the project's own slogan, "built around when the relationship breaks," becomes real machinery: a 3 layer break detector that gates the trading, stands the strategy down when a relationship stops holding, and flips into the opposite exposure, because the moment a relationship breaks is exactly when an option on the spread becomes valuable. Third, a production grade spread option pricing engine, closed forms plus variance reduced Monte Carlo, built as a shared library that project 1 and project 3 import. Fourth, a physical corridor layer that encodes, per basket, the arbitrage economics bounding how far the spread can wander, which is what lets the model tell statistical noise from genuine structural change.

**The 1 sentence the finished project supports:** "I trade the stationary residual of 3 leg commodity baskets, gated by a break detector that distinguishes noise from structural change, with the physical arbitrage corridor as the boundary, and the same pricing engine that values the optionality when the relationship breaks."

# PART B. GOALS, RANKED

1. **The refactored library.** The existing project restructured into an installable package that everything else plugs into, with a parity test proving the science did not change.
2. **Johansen basket machinery.** Cointegration rank, vectors, adjustment speeds, and half lives with confidence intervals, on 3 named baskets with physical mechanisms.
3. **The break overlay.** 3 detection layers, a traffic light, the historical break catalogue, and the measured answer to whether the overlay earns its complexity.
4. **The pricing engine.** Margrabe, Kirk, Black 76, correlated GBM and seasonal Ornstein Uhlenbeck simulators, antithetic variates, control variates, Sobol sequences, importance sampling, all validated against closed forms, API frozen 20 December 2026 because 2 other projects import it.
5. **The corridors.** Crush margin economics, refining economics, LNG diversion cost, each as an explicit banded bound with 2 uses: strengthening the mean reversion prior inside, and promoting exits to structural evidence outside.
6. **The realism backtest.** Point in time discipline, stated costs, volatility targeted sizing, portfolio layer, attribution, and the anti self deception protocol with the test set run exactly once.

# PART C. WORKED DATA SCENARIOS

**Scenario 1, a routine crush dislocation.** March 2027. The Johansen vector for the crush basket implies a stationary residual; today it sits at z = +2.3, beans rich against the meal and oil combination, while the traffic light is GREEN and the crush margin sits mid corridor. The system sells beans and buys meal and oil in the cointegrating weights, sized to the volatility budget. 11 trading days later the residual crosses z = 0.4 and the position exits. The VECM had said meal does most of the adjusting; the attribution confirms most of the convergence came from the meal leg.

**Scenario 2, the break that saves the book.** A policy shock changes biofuel mandates. The gas oil relationship in a basket starts drifting; the Kalman innovations run hot, the CUSUM alarm fires, AMBER halves the position, and 10 sustained days later RED forces flat. The naive ungated strategy, shadow run for attribution, keeps averaging into the move and bleeds for 6 weeks. The gated book sidesteps most of it, and the optionality flag's long volatility proxy entry captures part of the widening. This 1 episode is the overlay's existence proof, and the attribution table quantifies it.

**Scenario 3, the corridor verdict.** TTF minus Henry Hub, in EUR/MWh, exits the LNG diversion cost corridor upward and stays out for 25 consecutive days during a supply crisis. The corridor rule promotes it: this is not a mean reversion opportunity, it is structural evidence that the physical system changed, and it lands in the break catalogue with its named event rather than in the trade log as a losing fade.

# PART D. THE DELIVERABLES TABLE

| ID | Deliverable | Detail | Format | Acceptance gate | Target date |
|---|---|---|---|---|---|
| D1 | Data audit note | Every series in the universe: verified source, access method, history depth, license, PASS/CUT. Includes the DME Oman check (Dubai proxy) and confirms the Baltic CUT (C10). Includes the WRDS Datastream check for licensed futures history | 1 page note | Universe locked; no downstream work on unverified series | 17 Aug 2026 |
| D2 | Continuous futures builder | Per contract series where free sources allow, else documented source rolls; own rolls at N=5 business days pre expiry, back adjusted additive, unadjusted retained; roll calendars per market; lives in the shared platform repo (C8) | Platform component + parquet | Cointegration robustness later runs on BOTH adjusted and unadjusted | 20 Sep 2026 |
| D3 | The refactored statarb package | data / cointegration / filters / breaks / pricing / corridors / backtest / reporting skeleton; all thresholds to yaml configs; docstrings; 20 line quickstart | Installable package | PARITY GATE: reproduces the legacy Brent WTI pair's hedge ratio path, signals, and equity curve to numerical tolerance | 21 Sep 2026 (2 Sep weekends per C6) |
| D4 | Johansen + VECM per basket | Trace and max eigenvalue tests, full sample + rolling 3 year, deterministic term choice justified; vectors normalized first leg = 1; adjustment speeds; AR(1) half life with stationary block bootstrap CI | Code + tables | Negative results (r = 0) ship as findings | 31 Oct 2026 |
| D5 | Multivariate Kalman | State = n−1 free weights, random walk evolution, fixed q default + likelihood estimated alternative; outputs weights, residual, innovations, innovation variance daily | Code | T3 stability triggers evaluated; demotion path pre committed | 31 Oct 2026 |
| D6 | 3 cointegration notes | Crush, crack, gas hubs: r, vectors, which leg adjusts, half life CI, rolling stability, the mechanism sentence | 2 pages each | Every number regenerable | 31 Oct 2026 |
| D7 | Break layer 1 | Rolling Johansen (3 year, monthly) + recursive ADF on the fixed vector residual | Code + monthly indicator | Catches the catalogued breaks retrospectively | 30 Nov 2026 |
| D8 | Break layer 2 | CUSUM on standardized innovations (primary) + rolling 20 day mean absolute innovation (cross check); thresholds calibrated to 2 false alarms/year by block bootstrap | Code + daily alarm state | Calibration documented | 30 Nov 2026 |
| D9 | Break layer 3 + catalogue | Bai Perron (or ruptures with BIC, choice documented) on full history; every break dated and attributed to a named physical event where possible | The break catalogue | Lead/lag validation: would layers 1 to 2 have caught each, reported honestly | 14 Dec 2026 |
| D10 | The traffic light | GREEN trade / AMBER no new entries + halve / RED flat + optionality flag; the flag's long volatility proxy rule (documented poor man's straddle: long the spread with stop and reverse) | Code + daily state per basket | 2 sided logic backtestable | 14 Dec 2026 |
| D11 | closed_forms.py | black76, margrabe, kirk with the validity note, Greeks analytic or controlled finite difference | Engine module | Unit tests vs published reference values | 12 Dec 2026 |
| D12 | processes.py | Correlated GBM (Cholesky); seasonal OU with exact discretization + estimation code; 2 correlated OU; Schwartz 2 factor interface reserved | Engine module | OU estimator recovers known parameters on simulated data | 12 Dec 2026 |
| D13 | monte_carlo.py + variance_reduction.py | Path engine with mandatory standard errors; antithetic; control variates (closed form controls); Sobol via scipy qmc with Brownian bridge; importance sampling with likelihood ratio | Engine modules | THE ENGINE GATE: MC reproduces Black 76 and Margrabe within 3 SE at 100k paths, Kirk within its regime; efficiency table produced | 20 Dec 2026, API FROZEN |
| D14 | Engine note | API, validation table, efficiency table, the closed form vs simulation paragraph | 3 pages | Matches the shipped code | 20 Dec 2026 |
| D15 | Corridor models | Crush: 0.022xmeal + 0.11xoil − beans vs cost bands. Crack: 3:2:1 vs refinery cost + EIA utilization. Gas: TTF−HH vs liquefaction + shipping + regas bands. Brent WTI: pipeline + freight band. Sizing multiplier inside (1.25x default), 20 day promotion rule outside | Code + 4 corridor charts | Corridor break catalogue cross match complete | Mar 2027 (min 2 baskets) |
| D16 | Backtest engine | Point in time timestamps, T+0 close base + T+1 open sensitivity, costs per market from config, roll cost accounting, volatility targeted sizing (50 bps/day per basket), portfolio layer (equal risk, 4x gross cap, 1.5x per basket) | Code | Timestamp audit on a sampled month | Apr 2027 |
| D17 | Attribution | P&L split: GREEN mean reversion / AMBER RED losses avoided (vs the shadow ungated run) / RED optionality entries; the honest answer on whether the overlay earns its complexity | Tables in the note | Shadow run reproducible | Apr 2027 |
| D18 | The strategy note | 6 to 8 pages: method, per basket and portfolio results after costs, cost sensitivity at 1x/2x/4x, attribution, the protocol statement verbatim, limitations (free data, capacity, thin markets) | Note | THE PROTOCOL: thresholds frozen on data through 2021 (or first 60 percent), 1 documented validation iteration, test set 2025+ run ONCE, execution count logged and stated | Apr 2027 |
| D19 | Engine contribution log | Any additive PRs from projects 1 and 3 post freeze, harness green on each | Changelog | Additive only; signatures never change | ongoing |

# PART E. DATA REGISTER

| Series | Basket | Verdict | Notes |
|---|---|---|---|
| ZS, ZM, ZL (beans complex) | Crush | PLAUSIBLE free (stooq/Yahoo/CME delayed) | WRDS Datastream history upgrade if subscribed; free feed stays the living source |
| CL, RB, HO | Crack | PLAUSIBLE free | Same |
| TTF daily | Gas | PLAUSIBLE free | EUR/MWh native |
| Henry Hub | Gas | VERIFIED (EIA) | Convert at 1 MMBtu = 0.293071 MWh, factor in config |
| NBP | Gas third leg | PLAUSIBLE free | JKM only if a free daily series verifies, else NBP stands |
| Brent | Legacy pair | PLAUSIBLE free | |
| DME Oman | Crude third leg candidate | UNVERIFIED, D1 item | If fails, crude stays 2 leg, documented |
| Baltic indices | Freight stretch | CUT (C10) | No sustainable free path; freight survives inside the gas corridor shipping band |
| EIA utilization, stocks | Corridors | VERIFIED | |
| AGSI+ | Gas corridor context | VERIFIED | Attribution |
| ECB FX | All | VERIFIED | |
| WRDS Datastream | History block | CONDITIONAL, week 1 check | Academic use only; never republished; never a daily dependency; splice dates in manifest |

# PART F. THE STEP BY STEP PLAN, A TO Z

**Phase 0, week of 11 to 17 August (audit only, 1 hour, per C6).**
Step 1: the D1 data audit including DME Oman, JKM, and the WRDS subscription check. Universe locked at the end of the week.

**Phase 1, September weekends (the refactor, per C6).**
Step 2: weekend 1, package skeleton, configs extracted, data layer pointed at the platform's continuous futures builder (D2 built in the platform repo alongside).
Step 3: weekend 2, port the pairwise science untouched, run the parity gate on Brent WTI. Nothing proceeds until parity is green.

**Phase 2, late September to October (Johansen months, ≤ 2 to 3 hours/week).**
Step 4: Johansen and VECM on crush, then crack, then gas, in that order (crush is the near certain anchor, a mechanical processing identity).
Step 5: multivariate Kalman, fixed q mode first, T3 triggers watched from day 1.
Step 6: the 3 cointegration notes, honest negatives included.

**Phase 3, November (the overlay).**
Step 7: layers 1 and 2 built and calibrated (2 false alarms/year by bootstrap).
Step 8: layer 3 catalogue, every break dated and named where possible.
Step 9: lead/lag validation of the live layers against the catalogue, reported as is.
Step 10: the traffic light and the optionality flag rule.

**Phase 4, 1 to 20 December (the engine sprint, the only immovable deadline).**
Step 11: closed forms with reference value tests (D11).
Step 12: processes with the OU estimator recovery test (D12).
Step 13: Monte Carlo + all 4 variance reduction techniques + the engine gate + the efficiency table (D13).
Step 14: 20 December, API frozen, tag cut, engine note shipped, down tools.

**Phase 5, the frozen window, 21 December to 6 February.** Nothing. Pipelines and collection run themselves.

**Phase 6, February (internship mode base case, ~1 hour/week here: project 1's rent valuation is importing the engine this month; this project's only job is supporting that import and landing Sobol/importance sampling refinements additively if they slipped).**

**Phase 7, March (corridors, ~2 hours/week).**
Step 15: crush and crack corridors minimum (the C5 compression allows stopping at 2), gas and Brent WTI if hours allow.
Step 16: corridor break catalogue cross match; the 20 day promotion rule live.

**Phase 8, April (the backtest month, ~3 hours/week).**
Step 17: backtest engine with the timestamp audit.
Step 18: training window fit, thresholds frozen, the 1 permitted validation iteration, documented.
Step 19: the shadow ungated run for attribution.
Step 20: THE TEST SET, ONCE. Execution logged.
Step 21: the strategy note with the protocol statement verbatim, cost sensitivities, attribution, limitations.
Step 22: portfolio site update; the Part A sentence goes live under the claims rule.

# PART G. METHODS CORE (COMPRESSED)

Johansen via statsmodels coint_johansen, deterministic term per basket justified in config; vector normalized first leg = 1; VECM adjustment speeds are a reported finding per basket. Half life from AR(1) on the residual with stationary block bootstrap CI, block length tied to the half life estimate, iterated once. Kalman state = free weights, random walk, fixed q default. Signal: z of the Kalman residual on a 120 day trailing window, entry |z| > 2.0 gated GREEN, exit at 0.5 toward 0, time stop at 3x half life, forced flat on RED. Breaks: CUSUM primary, calibrated by bootstrap; Bai Perron or ruptures BIC for the catalogue. Engine: Margrabe zero strike, Kirk nonzero with the validity note, Black 76 base; correlated GBM and exact discretization seasonal OU; antithetic, control variates on closed form controls, Sobol with Brownian bridge, exponential tilting importance sampling with likelihood correction; standard errors mandatory. Corridors: crush 0.022m + 0.11o − b; crack 3:2:1; gas TTF−HH vs diversion cost band; inside multiplier 1.25x, outside 20 day promotion. Costs: 1 tick + 0.5 tick slippage per side on the CME complex, TTF at 2x the liquid assumption from the start (T5), roll crossing per leg. Sizing: 50 bps daily vol per basket, equal risk portfolio, 4x gross cap.

# PART H. RULES

1. Zero [prior employer redacted], ever; unclear provenance excluded; the freight content uses only the corridor's banded public shipping assumptions.
2. No conduct language about any market participant anywhere.
3. The engine freeze (20 December) is additive only afterward; the harness runs as CI here and as an import check in projects 1 and 3; the re publication rule applies to any post freeze bug touching published numbers (patch, harness green, regenerate everything affected, dated correction notes, silent fixes prohibited).
4. WRDS: history block only, academic use, never republished, never a daily dependency.
5. The test set is run once; any rerun request requires flagging the protocol and explicit confirmation; every execution logged.
6. Honest negatives ship: failed cointegration, an overlay that does not add value, Kirk breaking down somewhere relevant.
7. Style: numerals, no hyphens in prose, no marketing language, no emojis. Presentation order: after the auction project for power and gas audiences, always before curve factors.

# PART I. RISKS AND PRE COMMITTED FALLBACKS

| Risk | Trigger | Fallback |
|---|---|---|
| T3 Kalman instability | Weight cap binding > 5 percent of days, or residual variance ratio > 2 vs fixed vector | Demote to quarterly re estimated Johansen vector + scalar Kalman on the residual; the multivariate attempt ships as a methods comparison |
| A basket fails cointegration | r = 0 in recent windows | Ships as a finding; strategy runs on passing baskets; crush is the anchor |
| T5 cost flattery | Sharpe sign flips 1x → 2x | Strategy labeled not robust to costs, excluded from headlines; the 1x/2x/4x table is mandatory regardless |
| Engine slips into the report crunch | Behind by 12 December | Minimum freeze scope = closed forms + antithetic + control variates; Sobol and importance sampling land additively in February without breaking the API |
| Overlay adds no value | Attribution (b)+(c) ≤ shadow | Reported as the finding; the catalogue and lead/lag validation stand as research; external framing shifts to measurement |
| Free source dies | Manifest gap alarm | Documented substitute leg per basket or documented cut; checksums catch silent changes |

# PART J. DEFINITION OF DONE

Minimum viable (20 December 2026): D1 to D14, parity green, 3 cointegration notes, overlay live with catalogue, engine frozen with harness green and 2 projects able to import it.
Full (April 2027 in internship mode): D15 to D18, corridors on at least 2 baskets, the strategy note with the protocol statement, test set executed once, the Part A sentence claimable with every number BUILT.

# PART K. EXECUTOR NOTES

The parity gate is the contract for the refactor: no science changes ride along. Every threshold and factor lives in config; changing one regenerates downstream under a new hash. The engine's post freeze discipline and the single test set execution are the 2 places an executing model must refuse and escalate rather than comply. Honest negatives are deliverables; do not engineer around them.
