"""Spread definitions, sector mappings, and shared constants."""

TRADING_DAYS_PER_YEAR = 252

SPREAD_CATEGORIES = {
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

ALL_SPREADS = [s for spreads in SPREAD_CATEGORIES.values() for s in spreads]

CATEGORY_COLORS = {
    "cross_commodity": "#4fc3f7",
    "processing": "#ffa726",
    "calendar": "#66bb6a",
}

REGIME_COLORS = {
    "calm": "#66bb6a",
    "moderate": "#ffa726",
    "stressed": "#ef5350",
}

FIGURE_DPI = 300
