"""Path resolution for statarb.

data/raw is the collected record and is gitignored. data/processed is always regenerable
from raw and is gitignored. A fix regenerates processed from raw; it never edits raw and
never patches a processed file in place.
"""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

CONFIG = PROJECT_ROOT / "config"
CONFIG_LEGACY = CONFIG / "legacy"

DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_CACHE = PROJECT_ROOT / "data" / "cache"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

RESULTS_FIGURES = PROJECT_ROOT / "results" / "figures"
RESULTS_TABLES = PROJECT_ROOT / "results" / "tables"
RESULTS_TEARSHEETS = PROJECT_ROOT / "results" / "tearsheets"

DOCS = PROJECT_ROOT / "docs"
