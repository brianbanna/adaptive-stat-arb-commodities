"""Multivariate Kalman filter. SPEC Part D deliverable D5, methods in Part G.

State is the n minus 1 free weights of the cointegrating vector, evolving as a random
walk. Fixed q is the default mode; the likelihood estimated alternative is the second
mode and both stay available. Daily outputs: the weights, the residual, the innovations,
and the innovation variance. The innovations feed break layer 2 directly, so their
scaling is not an internal detail.

T3 STABILITY TRIGGER, watched from day 1, not evaluated at the end:
    the weight cap binds on more than 5 percent of days, OR
    the residual variance ratio exceeds 2 against the fixed vector.
On trigger the demotion path is pre committed and is executed without renegotiating it:
demote to a quarterly re estimated Johansen vector plus a scalar Kalman on the residual,
and the multivariate attempt ships as a methods comparison rather than being deleted.
Log the trigger evaluation either way, including when it does not fire.
"""
