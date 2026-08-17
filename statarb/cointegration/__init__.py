"""Johansen and VECM machinery. SPEC Part D deliverables D4 and D6, methods in Part G.

D4  Per basket: trace and maximum eigenvalue tests, on the full sample and on a rolling
    3 year window. The deterministic term is chosen per basket and the choice is justified
    in config/cointegration.yaml, not picked in a notebook. Cointegrating vectors are
    normalized with the first leg equal to 1. VECM adjustment speeds, meaning which leg
    does the adjusting, are a reported finding per basket and not a diagnostic. AR(1) half
    life on the residual with a stationary block bootstrap confidence interval, block
    length tied to the half life estimate and iterated once.
    Gate: NEGATIVE RESULTS SHIP AS FINDINGS. A basket that returns rank 0 in recent
    windows is reported as that, the strategy runs on the baskets that pass, and crush is
    the anchor because it is a mechanical processing identity.

D6  3 notes, 2 pages each, on crush, crack, and gas hubs: the rank, the vectors, which leg
    adjusts, the half life confidence interval, the rolling stability, and the mechanism
    sentence that says why the relationship exists physically.
    Gate: every number regenerable.

Order of work per SPEC Part F step 4: crush first because it is the near certain anchor,
then crack, then gas.
"""
