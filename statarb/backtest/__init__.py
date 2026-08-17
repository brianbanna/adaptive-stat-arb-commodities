"""Backtest engine and attribution. SPEC Part D deliverables D16, D17, D18.

D16 The engine. Point in time timestamps throughout. T+0 close is the base case with a
    T+1 open sensitivity. Costs per market from config, roll cost accounting per leg,
    volatility targeted sizing at 50 bps per day per basket, and a portfolio layer at
    equal risk with a 4x gross cap and 1.5x per basket.
    Gate: a timestamp audit on a sampled month. Every input must have been knowable at the
    timestamp the backtest uses it at.

D17 Attribution. P&L split 3 ways:
      (a) GREEN mean reversion,
      (b) AMBER and RED losses avoided, measured against the shadow ungated run,
      (c) RED optionality entries.
    Plus the honest answer on whether the overlay earns its complexity. If (b) plus (c) is
    at or below the shadow run, that is the finding: it is reported, the catalogue and the
    lead and lag validation stand as research, and the external framing moves to
    measurement. It is not re engineered until it looks better.
    Gate: the shadow ungated run is reproducible.

D18 The strategy note, 6 to 8 pages, carrying THE PROTOCOL verbatim:
      thresholds frozen on data through 2021, or the first 60 percent,
      1 documented validation iteration, exactly 1,
      THE TEST SET, 2025 onward, RUN ONCE,
      the execution count logged and stated in the note.
    Plus per basket and portfolio results after costs, the mandatory 1x, 2x, 4x cost
    sensitivity table, the attribution, and the limitations: free data, capacity, thin
    markets.
    T5 trigger: if the Sharpe sign flips between 1x and 2x, the strategy is labeled not
    robust to costs and excluded from every headline. The table ships regardless.

RERUNNING THE TEST SET IS A REFUSAL POINT. See CLAUDE.md section 5.
"""
