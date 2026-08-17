"""Physical arbitrage corridors. SPEC Part D deliverable D15, methods in Part G.

A corridor encodes, per basket, the arbitrage economics that bound how far the spread can
wander before a physical response pulls it back. That bound is what lets the model tell
statistical noise from genuine structural change, so the corridor has 2 distinct uses and
they must not be conflated:

    INSIDE the corridor, the mean reversion prior is stronger. Sizing multiplier 1.25x by
        default.
    OUTSIDE the corridor, a sustained excursion is promoted to structural evidence rather
        than treated as a bigger opportunity. The promotion rule is 20 consecutive days.
        A promoted excursion lands in the break catalogue with its named event, not in the
        trade log as a losing fade.

The 4 corridors, minimum 2 shipped per the compressed scope:
    crush      0.022 x meal + 0.11 x oil minus beans, against cost bands
    crack      3:2:1, against refinery cost and EIA utilization
    gas        TTF minus Henry Hub, against liquefaction plus shipping plus regas bands
    brent wti  against a pipeline plus freight band

Freight enters only here, as the corridor's banded public shipping assumptions. The Baltic
indices are CUT from the universe and freight survives nowhere else in the project.

Gate: the corridor break catalogue cross match is complete, meaning every promoted
excursion is checked against the D9 catalogue.
"""
