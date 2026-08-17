"""The break overlay, 3 layers plus the traffic light. SPEC Part D deliverables D7 to D10.

This is the project's slogan turned into machinery: the strategy is built around when the
relationship breaks, so the detector gates the trading rather than annotating it.

D7  Layer 1, slow. Rolling Johansen on a 3 year window, monthly, plus a recursive ADF on
    the residual of the fixed vector.
    Gate: catches the catalogued breaks retrospectively.

D8  Layer 2, fast. CUSUM on standardized Kalman innovations is primary. A rolling 20 day
    mean absolute innovation runs as the cross check. Thresholds are calibrated by block
    bootstrap to 2 false alarms per year, and the calibration is documented rather than
    tuned until the backtest improves.

D9  Layer 3, retrospective. Bai Perron, or ruptures with BIC and the choice documented, on
    the full history. Every break dated and attributed to a named physical event where 1
    exists.
    Gate: lead and lag validation, meaning would layers 1 and 2 have caught each
    catalogued break, REPORTED HONESTLY. A layer that misses breaks is reported as missing
    them.

D10 The traffic light, daily state per basket:
      GREEN  trade normally
      AMBER  no new entries, halve existing positions
      RED    flat, and raise the optionality flag
    The optionality flag carries its own documented rule, a poor man's straddle: long the
    spread with a stop and reverse. The moment a relationship breaks is when an option on
    the spread is worth owning, which is why the logic is 2 sided.
    Gate: the 2 sided logic is backtestable, so the flag is a rule and not a comment.

The honest question this layer must answer, in D17: does the overlay earn its complexity.
If attribution says no, that is the finding and it ships as the finding.
"""
