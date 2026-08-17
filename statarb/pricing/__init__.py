"""THE SHARED PRICING ENGINE. SPEC Part D deliverables D11, D12, D13, D14.

READ THIS BEFORE CHANGING ANYTHING IN THIS SUBPACKAGE.

This is not a private module of this project. 2 other projects import it:
    the power price formation project, for the congestion rent valuation (its D18),
    the volatility trading project, for every Greek and every option value it uses.

**The API freezes 20 December 2026.** From that date the package is ADDITIVE ONLY.
Signatures never change. A new argument gets a default that preserves existing behavior,
or it gets a new function. Renaming, reordering, retyping, or changing the meaning of an
existing parameter is a breaking change and is prohibited, regardless of how much better
the new shape would be.

D11 closed_forms.py: black76, margrabe, kirk with its validity note written where a caller
    will see it, Greeks either analytic or by controlled finite difference.
    Gate: unit tests against published reference values.

D12 processes.py: correlated GBM by Cholesky; seasonal Ornstein Uhlenbeck with exact
    discretization and its estimation code; 2 correlated OU; a reserved interface for
    Schwartz 2 factor.
    Gate: the OU estimator recovers known parameters on simulated data.

D13 monte_carlo.py and variance_reduction.py: a path engine where STANDARD ERRORS ARE
    MANDATORY on every estimate, antithetic variates, control variates using the closed
    forms as controls, Sobol via scipy qmc with a Brownian bridge, and importance sampling
    with the likelihood ratio correction.
    THE ENGINE GATE: Monte Carlo reproduces Black 76 and Margrabe within 3 standard errors
    at 100000 paths, and Kirk within its stated validity regime. The efficiency table is
    produced, not promised.

D14 The engine note, 3 pages: the API, the validation table, the efficiency table, and the
    paragraph on when a closed form is right and when simulation is.

If the December sprint runs late, the pre committed minimum freeze scope is closed forms
plus antithetic plus control variates. Sobol and importance sampling then land additively
in February without touching the API. Do not descope by weakening the engine gate.

THE RE PUBLICATION RULE, for any post freeze bug that touches a published number:
patch the engine, run the harness green, regenerate everything downstream that the bug
affected, publish a dated correction note. A silent fix is prohibited. See CLAUDE.md.
"""
