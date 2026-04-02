"""CLI error catalog and explain command tests."""

from __future__ import annotations

import subprocess
import sys


def _run_nlsc(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "nlsc", *args],
        capture_output=True,
        text=True,
    )


def test_error_catalog_covers_active_cli_error_codes() -> None:
    from nlsc.error_catalog import ERROR_CATALOG

    expected_codes = {
        "EFILE001",
        "EPARSE001",
        "EUSE001",
        "E_RESOLUTION",
        "ETEST001",
        "ECONTRACT001",
        "ETARGET001",
        "EVALIDATE001",
        "E_RUN",
        "EEXEC001",
        "EGRAPH001",
        "EGRAPH002",
    }

    assert expected_codes <= set(ERROR_CATALOG)


def test_explain_command_prints_known_error_details() -> None:
    result = _run_nlsc("explain", "EPARSE001")

    assert result.returncode == 0
    assert "EPARSE001" in result.stdout
    assert "Parse error" in result.stdout
    assert "verify" in result.stdout
    assert result.stderr == ""


def test_explain_command_rejects_unknown_error_code() -> None:
    result = _run_nlsc("explain", "ENOPE999")

    assert result.returncode == 1
    assert "Unknown error code: ENOPE999" in result.stderr
    assert "Known codes:" in result.stderr
