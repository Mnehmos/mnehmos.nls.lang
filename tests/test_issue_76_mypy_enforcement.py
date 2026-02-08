"""Red-phase contract tests for Issue #76: mypy enforcement.

These tests intentionally fail until mypy enforcement is tightened.
"""

from __future__ import annotations

from pathlib import Path
import tomllib


def _load_mypy_config() -> dict[str, object]:
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    return data["tool"]["mypy"]


def test_should_disallow_untyped_defs_when_type_checking_is_enforced() -> None:
    mypy_config = _load_mypy_config()
    assert mypy_config.get("disallow_untyped_defs") is True, (
        "Expected mypy enforcement to set [tool.mypy].disallow_untyped_defs = true "
        "so untyped functions are blocked in CI."
    )


def test_should_check_untyped_defs_when_type_checking_is_enforced() -> None:
    mypy_config = _load_mypy_config()
    assert mypy_config.get("check_untyped_defs") is True, (
        "Expected mypy enforcement to set [tool.mypy].check_untyped_defs = true "
        "so bodies of untyped functions are type-checked."
    )

