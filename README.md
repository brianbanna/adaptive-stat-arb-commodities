# Adaptive statistical arbitrage in commodity spreads

Multi leg relative value with break detection, and the shared spread option pricing
engine.

## The sentence this project is built to support

> I trade the stationary residual of 3 leg commodity baskets, gated by a break detector
> that distinguishes noise from structural change, with the physical arbitrage corridor as
> the boundary, and the same pricing engine that values the optionality when the
> relationship breaks.

That sentence is the target, not a current claim. No part of it is quotable with numbers
until the artifact behind it has passed its acceptance gate and its numbers regenerate.

## Status

**In progress.** As of 17 August 2026 the repo is at Phase 0, the data audit week. It
holds the package skeleton, the config scaffolds, the specification, and the archived
legacy material the parity gate has to reproduce. There is no science code, no result, and
no number to quote.

Definition of done, from SPEC Part J:

- Minimum viable, 20 December 2026: D1 to D14, the parity gate green, 3 cointegration
  notes, the break overlay live with its catalogue, and the pricing engine frozen with its
  harness green and 2 other projects able to import it.
- Full, April 2027: D15 to D18, corridors on at least 2 baskets, and the strategy note
  with its protocol statement.

## Build authority

[SPEC.md](SPEC.md) governs this repo: goals, the deliverables table with dates and
acceptance gates, the phase plan, the methods core, the hard rules, the risks with their
pre committed fallbacks, and the definition of done. Read it before writing code.
[CLAUDE.md](CLAUDE.md) is the operating brief for an agent session opened here.

## statarb.pricing is a shared component

`statarb.pricing` is not a private module of this project. Its API freezes on **20
December 2026** and from that date 2 other projects import it at a pinned tag: the day
ahead power price formation project for its congestion rent valuation, and the commodity
volatility trading project for every Greek and option value it uses.

After the freeze the package is additive only and signatures never change. Any post freeze
bug that touches a published number follows the re publication rule: patch, harness green,
regenerate everything downstream, dated correction note. Silent fixes are prohibited.

## Layout

```
statarb/
  data/           D1 audit, D2 continuous futures and rolls
  cointegration/  D4 Johansen and VECM, D6 the 3 basket notes
  filters/        D5 multivariate Kalman
  breaks/         D7 layer 1, D8 layer 2, D9 catalogue, D10 traffic light
  pricing/        D11 closed forms, D12 processes, D13 Monte Carlo, THE SHARED ENGINE
  corridors/      D15 physical arbitrage corridors
  backtest/       D16 engine, D17 attribution, D18 the protocol
  reporting/      notes, tables, figures, all regenerable
config/           spec thresholds, nothing hardcoded in source
config/legacy/    the pre refactor parameters, retained as parity gate inputs
docs/legacy/      the pre refactor plan and README, archived, superseded by SPEC.md
tests/
data/raw/         gitignored
data/processed/   gitignored, always regenerable from raw
```

## The parity gate

The refactor's contract, SPEC deliverable D3: the restructured package reproduces the
legacy Brent WTI pair's hedge ratio path, signals, and equity curve to numerical
tolerance. No science change rides along with the restructure. Nothing downstream proceeds
until parity is green. The legacy design and its parameters are kept in `docs/legacy/` and
`config/legacy/` for exactly this reason.

## License

MIT. Research code, not investment advice. Backtested results do not guarantee future
results, and no result here is a claim about the conduct of any market participant.
