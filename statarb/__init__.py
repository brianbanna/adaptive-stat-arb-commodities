"""statarb: multi leg relative value with break detection and the shared pricing engine.

SPEC.md at the repo root is the build authority. Read it before writing code.

Subpackage map, keyed to the SPEC Part D deliverable table:

    data          D2 continuous futures, point in time loading, roll calendars
    cointegration D4 Johansen and VECM, D6 the 3 cointegration notes
    filters       D5 multivariate Kalman
    breaks        D7 layer 1, D8 layer 2, D9 layer 3 and the catalogue, D10 traffic light
    pricing       D11 closed forms, D12 processes, D13 Monte Carlo and variance reduction
    corridors     D15 physical arbitrage corridors
    backtest      D16 backtest engine, D17 attribution
    reporting     the notes, tables, and figures every deliverable ships with

`statarb.pricing` IS THE SHARED ENGINE. Its API freezes 20 December 2026 and 2 other
projects import it from that date: the power price formation project for the congestion
rent valuation, and the volatility trading project for every Greek it uses. After the
freeze the package is additive only. Signatures never change. See CLAUDE.md section 6.
"""

__version__ = "0.0.0"
