"""YAML config loading and config hashing for statarb.

SPEC Part K: every threshold and factor lives in config, and changing 1 of them
regenerates everything downstream under a new hash. That is why loading goes through here
and why `config_hash` exists: a generated artifact records the hash of the exact
configuration that produced it, so any published number traces back to its inputs.

A science module never opens a yaml file directly and never hardcodes a threshold.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
LEGACY_CONFIG_DIR = CONFIG_DIR / "legacy"


def load_config(name: str) -> dict[str, Any]:
    """Load a spec config by name, without the .yaml extension.

    Raises FileNotFoundError rather than returning an empty dict, because a silently
    missing config is how a hardcoded default gets used without anyone noticing.
    """
    path = CONFIG_DIR / f"{name}.yaml"
    if not path.is_file():
        available = sorted(p.stem for p in CONFIG_DIR.glob("*.yaml"))
        raise FileNotFoundError(f"no config named {name!r} in {CONFIG_DIR}; available: {available}")
    with path.open(encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle)
    if not isinstance(loaded, dict):
        raise TypeError(f"config {name!r} did not parse to a mapping, got {type(loaded).__name__}")
    return loaded


def load_legacy_config(name: str) -> dict[str, Any]:
    """Load a config from config/legacy/, the parameters of the pre refactor pairwise code.

    These exist for 1 reason: the D3 parity gate has to reproduce the legacy Brent WTI
    pair's hedge ratio path, signals, and equity curve to numerical tolerance, and it has
    to do that under the parameters the legacy code actually ran with. They are inputs to
    the parity test, not defaults for new work. New work reads the spec configs.
    """
    path = LEGACY_CONFIG_DIR / f"{name}.yaml"
    if not path.is_file():
        available = sorted(p.stem for p in LEGACY_CONFIG_DIR.glob("*.yaml"))
        raise FileNotFoundError(
            f"no legacy config named {name!r} in {LEGACY_CONFIG_DIR}; available: {available}"
        )
    with path.open(encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle)
    if not isinstance(loaded, dict):
        raise TypeError(f"legacy config {name!r} did not parse to a mapping")
    return loaded


def _canonicalize(node: Any) -> Any:
    """Coerce mapping keys to strings so serialization cannot depend on key types.

    YAML 1.1 resolves a bare `on`, `off`, `yes`, or `no` key to a boolean, which produces a
    mapping with mixed key types and breaks any sorted serialization. Configs should not
    contain such keys, and `tests/unit/test_config.py` fails if one appears, but hashing
    must not be the thing that discovers it.
    """
    if isinstance(node, dict):
        return {str(key): _canonicalize(value) for key, value in node.items()}
    if isinstance(node, list):
        return [_canonicalize(item) for item in node]
    return node


def config_hash(*names: str) -> str:
    """Stable short hash of 1 or more spec configs, to stamp onto generated artifacts.

    Hashes the parsed and canonically serialized content rather than the file bytes, so
    that a comment edit or a reformat does not invalidate every downstream artifact while
    a changed value always does.
    """
    if not names:
        raise ValueError("config_hash needs at least 1 config name")
    payload = {name: _canonicalize(load_config(name)) for name in sorted(names)}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def get_path(relative: str) -> Path:
    """Resolve a path relative to the project root."""
    return PROJECT_ROOT / relative
