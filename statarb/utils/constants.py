"""Constants.

The spread definitions below are LEGACY: the 11 pair and calendar spreads of the pre
refactor project. They are retained because the D3 parity gate has to reproduce the legacy
Brent WTI pair exactly, and because the legacy universe is the record of what the refactor
started from. They are not the spec universe.

The spec universe is 3 baskets with physical mechanisms, defined in config/baskets.yaml:
crush, crack, and gas hubs, plus the Brent WTI pair carried forward as the parity anchor.
New work reads that file. Nothing new should import LEGACY_SPREAD_CATEGORIES.
"""

from __future__ import annotations

TRADING_DAYS_PER_YEAR = 252

LEGACY_SPREAD_CATEGORIES: dict[str, list[str]] = {
    "cross_commodity": [
        "wti_brent",
        "gold_silver",
        "corn_wheat",
        "copper_gold",
    ],
    "processing": [
        "crack_spread",
        "crush_spread",
    ],
    "calendar": [
        "cl_1_6",
        "cl_1_12",
        "ng_1_6",
        "zc_1_3",
        "gc_1_6",
    ],
}

LEGACY_ALL_SPREADS: list[str] = [s for group in LEGACY_SPREAD_CATEGORIES.values() for s in group]

# The pair the D3 parity gate runs on. SPEC Part D deliverable D3 and Part F step 3.
PARITY_PAIR = "wti_brent"

# Traffic light states. SPEC Part D deliverable D10.
TRAFFIC_LIGHT_STATES: tuple[str, ...] = ("GREEN", "AMBER", "RED")

FIGURE_DPI = 300
