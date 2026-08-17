"""The config layer holds. SPEC Part K: every threshold and factor lives in config."""

from __future__ import annotations

import importlib

import pytest

from statarb.utils import config as config_module

SPEC_CONFIGS = (
    "baskets",
    "cointegration",
    "filters",
    "breaks",
    "pricing",
    "corridors",
    "backtest",
)

LEGACY_CONFIGS = (
    "backtest",
    "cointegration",
    "evaluation",
    "kalman",
    "regime",
    "signals",
    "strategy",
    "universe",
)

SUBPACKAGES = (
    "data",
    "cointegration",
    "filters",
    "breaks",
    "pricing",
    "corridors",
    "backtest",
    "reporting",
    "utils",
)


@pytest.mark.parametrize("name", SPEC_CONFIGS)
def test_spec_config_loads(name: str) -> None:
    loaded = config_module.load_config(name)
    assert loaded, f"{name}.yaml parsed to something empty"
    assert "meta" in loaded, f"{name}.yaml has no meta block recording its deliverable IDs"


@pytest.mark.parametrize("name", LEGACY_CONFIGS)
def test_legacy_config_loads(name: str) -> None:
    """The pre refactor parameters are inputs to the D3 parity gate and must stay loadable."""
    assert config_module.load_legacy_config(name)


def test_missing_config_raises_rather_than_returning_empty() -> None:
    """A silently missing config is how a hardcoded default gets used unnoticed."""
    with pytest.raises(FileNotFoundError):
        config_module.load_config("does-not-exist")


def test_config_hash_is_stable_and_covers_content() -> None:
    first = config_module.config_hash("baskets", "backtest")
    second = config_module.config_hash("backtest", "baskets")
    assert first == second, "config_hash must not depend on argument order"
    assert first != config_module.config_hash("baskets"), "hash must cover every named config"
    assert len(first) == 16


@pytest.mark.parametrize("name", SUBPACKAGES)
def test_subpackage_imports(name: str) -> None:
    module = importlib.import_module(f"statarb.{name}")
    assert module.__doc__, f"statarb.{name} has no module docstring stating its deliverables"


@pytest.mark.parametrize("name", SPEC_CONFIGS)
def test_config_keys_are_all_strings(name: str) -> None:
    """No YAML 1.1 boolean keys.

    A bare `on`, `off`, `yes`, or `no` key resolves to a boolean under YAML 1.1, producing
    a mapping whose keys are silently not what the file appears to say. This catches it at
    the file rather than at the first thing that tries to serialize the config.
    """
    offenders: list[str] = []

    def walk(node: object, path: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if not isinstance(key, str):
                    offenders.append(f"{path}: {key!r} ({type(key).__name__})")
                walk(value, f"{path}.{key}")
        elif isinstance(node, list):
            for index, item in enumerate(node):
                walk(item, f"{path}[{index}]")

    walk(config_module.load_config(name), name)
    assert not offenders, f"non string keys in {name}.yaml:\n" + "\n".join(offenders)
