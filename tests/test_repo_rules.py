"""Mechanical enforcement of the SPEC Part H rules that can be checked by a machine.

SPEC Part K says the engine's post freeze discipline and the single test set execution are
the 2 places an executing model must refuse rather than comply. These tests are the
backstop for the parts of Part H a machine can check on its own.

They are heuristics, not proofs. Passing them is not permission.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

# Assembled at runtime so that this file, which has to search for the term, does not
# itself contain it. A plain text search of the repo must return nothing, including here.
RESTRICTED_TERMS: tuple[str, ...] = ("Car" + "gill",)


def _tracked_files() -> list[Path]:
    """Every file git tracks, which is exactly the set that becomes public."""
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files", "-z"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [REPO_ROOT / name for name in result.stdout.split("\0") if name]


def test_restricted_terms_absent_from_tracked_files() -> None:
    """SPEC Part H rule 1. No tracked file names the prior employer, in any casing."""
    offenders: list[str] = []
    for path in _tracked_files():
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue  # binary or unreadable; nothing to match on
        lowered = text.lower()
        for term in RESTRICTED_TERMS:
            if term.lower() in lowered:
                offenders.append(str(path.relative_to(REPO_ROOT)))
    assert not offenders, "SPEC Part H rule 1 violated in:\n" + "\n".join(offenders)


def test_test_set_execution_count_within_protocol() -> None:
    """SPEC Part H rule 5. The test set runs once, and the log matches the count.

    This does not stop a rerun. It makes an undeclared one fail loudly, which is what the
    protocol needs: the count and the log are the record that goes verbatim into D18.
    """
    protocol = yaml.safe_load((REPO_ROOT / "config" / "backtest.yaml").read_text())["protocol"]
    test_set = protocol["test_set"]

    executed = test_set["runs_executed"]
    permitted = test_set["runs_permitted"]
    log = test_set["execution_log"]

    assert executed <= permitted, (
        f"test set executed {executed} times against {permitted} permitted. "
        "A rerun requires flagging the protocol and explicit confirmation from the user."
    )
    assert len(log) == executed, (
        f"execution_log has {len(log)} entries but runs_executed is {executed}. "
        "Every execution is logged; the log and the count are the same record."
    )
    assert protocol["validation_iterations_used"] <= protocol["validation_iterations_permitted"], (
        "more validation iterations used than the protocol permits. SPEC deliverable D18 "
        "allows exactly 1 documented validation iteration."
    )
