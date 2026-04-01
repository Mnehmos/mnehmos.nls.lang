"""Regression test for portable pytest basetemp configuration."""

from __future__ import annotations

from pathlib import Path
import re
import tomllib


def test_pytest_basetemp_should_not_be_hardcoded_to_windows_drive_path() -> None:
    """Pytest basetemp should work on Linux, macOS, and Windows CI."""
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))

    addopts = data["tool"]["pytest"]["ini_options"]["addopts"]

    match = re.search(r"--basetemp=(\S+)", addopts)
    assert match is not None, (
        "pytest addopts should define --basetemp for deterministic temp paths"
    )

    basetemp = match.group(1)
    assert not re.match(r"^[A-Za-z]:[\\/]", basetemp), (
        "pytest --basetemp must not be hardcoded to a Windows drive path; "
        f"found {basetemp!r}"
    )
    assert not basetemp.startswith("/"), (
        "pytest --basetemp should stay repo-relative so it remains portable across CI environments; "
        f"found {basetemp!r}"
    )
