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
        "ECLI001",
        "EEXPLAIN001",
        "EINIT001",
        "EINIT002",
        "EINIT003",
        "EATOM001",
        "EATOM002",
        "EFILE001",
        "EPARSE001",
        "EPARSE002",
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
        "ELOCK001",
        "ELOCK002",
        "ELSP001",
        "ELSP002",
        "EASSOC001",
        "EASSOC002",
        "EASSOC003",
        "EASSOC004",
        "EWATCH001",
        "EWATCH002",
    }

    assert expected_codes <= set(ERROR_CATALOG)


def test_explain_command_prints_known_error_details() -> None:
    result = _run_nlsc("explain", "EPARSE001")

    assert result.returncode == 0
    assert "EPARSE001" in result.stdout
    assert "Parse error" in result.stdout
    assert "verify" in result.stdout
    assert result.stderr == ""


def test_explain_command_prints_cli_usage_error_details() -> None:
    result = _run_nlsc("explain", "ECLI001")

    assert result.returncode == 0
    assert "ECLI001" in result.stdout
    assert "CLI usage error" in result.stdout
    assert "--json" in result.stdout
    assert "lsp" in result.stdout
    assert result.stderr == ""


def test_explain_command_prints_parser_backend_unavailable_details() -> None:
    result = _run_nlsc("explain", "EPARSE002")

    assert result.returncode == 0
    assert "EPARSE002" in result.stdout
    assert "Parser backend unavailable" in result.stdout
    assert "atomize" in result.stdout
    assert "init" in result.stdout
    assert "assoc" in result.stdout
    assert "treesitter" in result.stdout
    assert result.stderr == ""


def test_explain_command_prints_init_write_failure_details() -> None:
    result = _run_nlsc("explain", "EINIT003")

    assert result.returncode == 0
    assert "EINIT003" in result.stdout
    assert "Init project file write failed" in result.stdout
    assert "filesystem permissions" in result.stdout
    assert result.stderr == ""


def test_explain_command_prints_artifact_io_failure_details() -> None:
    result = _run_nlsc("explain", "EARTIFACT001")

    assert result.returncode == 0
    assert "EARTIFACT001" in result.stdout
    assert "Artifact I/O failed" in result.stdout
    assert "graph" in result.stdout
    assert "lock:update" in result.stdout
    assert result.stderr == ""


def test_explain_command_prints_lsp_dependency_error_details() -> None:
    result = _run_nlsc("explain", "ELSP001")

    assert result.returncode == 0
    assert "ELSP001" in result.stdout
    assert "LSP optional dependencies unavailable" in result.stdout
    assert "nlsc[lsp]" in result.stdout
    assert result.stderr == ""


def test_explain_command_prints_assoc_permission_error_details() -> None:
    result = _run_nlsc("explain", "EASSOC003")

    assert result.returncode == 0
    assert "EASSOC003" in result.stdout
    assert "Association permission denied" in result.stdout
    assert "--user" in result.stdout
    assert result.stderr == ""


def test_explain_command_prints_watch_runtime_error_details() -> None:
    result = _run_nlsc("explain", "EWATCH002")

    assert result.returncode == 0
    assert "EWATCH002" in result.stdout
    assert "Watch runtime compile failed" in result.stdout
    assert "save the file again" in result.stdout
    assert result.stderr == ""


def test_explain_command_prints_explain_unknown_code_details() -> None:
    result = _run_nlsc("explain", "EEXPLAIN001")

    assert result.returncode == 0
    assert "EEXPLAIN001" in result.stdout
    assert "Unknown explain error code" in result.stdout
    assert "nlsc explain" in result.stdout
    assert result.stderr == ""


def test_explain_command_rejects_unknown_error_code() -> None:
    result = _run_nlsc("explain", "ENOPE999")

    assert result.returncode == 1
    assert "Error [EEXPLAIN001]: Unknown error code: ENOPE999" in result.stderr
    assert "Known codes:" in result.stderr
