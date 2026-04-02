"""Structured JSON error output for CLI commands."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _run_nlsc(argv: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "nlsc", *argv],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )


def _load_json_output(result: subprocess.CompletedProcess[str]) -> dict:
    assert result.stdout.strip(), f"expected JSON stdout, got stderr={result.stderr!r}"
    return json.loads(result.stdout)


def test_verify_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.nl"

    result = _run_nlsc(["verify", str(missing_path), "--json"], cwd=tmp_path)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["ok"] is False
    assert payload["command"] == "verify"
    assert payload["diagnostics"] == [
        {
            "code": "EFILE001",
            "file": str(missing_path),
            "line": None,
            "col": None,
            "message": f"File not found: {missing_path}",
            "hint": "Check that the path exists and try again.",
        }
    ]


def test_verify_json_reports_parse_error_location(tmp_path: Path) -> None:
    source_path = tmp_path / "broken.nl"
    source_path.write_text(
        """\
@module broken
@target python

[main]
PURPOSE: Broken
LOGIC:
  first step is not numbered
RETURNS: void
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "verify", str(source_path), "--json"], cwd=tmp_path
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["diagnostics"] == [
        {
            "code": "EPARSE001",
            "file": str(source_path),
            "line": 7,
            "col": None,
            "message": "Invalid LOGIC step format; expected numbered step like '1. ...'",
            "hint": "Rewrite the line as a numbered LOGIC step like '1. ...'.",
        }
    ]


def test_verify_json_reports_stdlib_use_error(tmp_path: Path) -> None:
    source_path = tmp_path / "use_missing.nl"
    source_path.write_text(
        """\
@module use-missing
@target python
@use math.missing

[main]
PURPOSE: No-op
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "verify", str(source_path), "--json"], cwd=tmp_path
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["diagnostics"] == [
        {
            "code": "EUSE001",
            "file": str(source_path),
            "line": 3,
            "col": 1,
            "message": "Missing stdlib domain: math.missing",
            "hint": "Add the module under an stdlib root or pass --stdlib-path.",
        }
    ]


def test_verify_json_reports_dependency_resolution_error(tmp_path: Path) -> None:
    source_path = tmp_path / "missing_dep.nl"
    source_path.write_text(
        """\
@module missing-dep
@target python

[main]
PURPOSE: Needs helper
DEPENDS: [helper]
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "verify", str(source_path), "--json"], cwd=tmp_path
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["diagnostics"] == [
        {
            "code": "E_RESOLUTION",
            "file": str(source_path),
            "line": 4,
            "col": 1,
            "message": "main: Missing dependency: helper",
            "hint": "Define [helper] or remove it from DEPENDS.",
        }
    ]


def test_compile_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_compile.nl"

    result = _run_nlsc(["compile", str(missing_path), "--json"], cwd=tmp_path)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "compile"
    assert payload["diagnostics"][0]["code"] == "EFILE001"


def test_run_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_run.nl"

    result = _run_nlsc(["run", str(missing_path), "--json"], cwd=tmp_path)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "run"
    assert payload["diagnostics"][0]["code"] == "EFILE001"


def test_graph_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_graph.nl"

    result = _run_nlsc(["graph", str(missing_path), "--json"], cwd=tmp_path)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "graph"
    assert payload["diagnostics"][0]["code"] == "EFILE001"


def test_graph_json_reports_missing_anlu(tmp_path: Path) -> None:
    source_path = tmp_path / "graph_source.nl"
    source_path.write_text(
        """\
@module graph-source
@target python

[main]
PURPOSE: Show graph
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["graph", str(source_path), "--json", "--anlu", "helper"], cwd=tmp_path
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "graph"
    assert payload["diagnostics"] == [
        {
            "code": "EGRAPH001",
            "file": str(source_path),
            "line": None,
            "col": None,
            "message": "ANLU 'helper' not found",
            "hint": "Choose one of the defined ANLUs: main.",
        }
    ]


def test_graph_json_reports_unsupported_dataflow_format(tmp_path: Path) -> None:
    source_path = tmp_path / "graph_dataflow.nl"
    source_path.write_text(
        """\
@module graph-dataflow
@target python

[main]
PURPOSE: Show graph
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["graph", str(source_path), "--json", "--anlu", "main", "--format", "dot"],
        cwd=tmp_path,
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "graph"
    assert payload["diagnostics"] == [
        {
            "code": "EGRAPH002",
            "file": str(source_path),
            "line": 4,
            "col": 1,
            "message": "Format 'dot' is not supported for ANLU dataflow graphs",
            "hint": "Use --format mermaid or --format ascii when selecting --anlu.",
        }
    ]


def test_diff_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_diff.nl"

    result = _run_nlsc(["diff", str(missing_path), "--json"], cwd=tmp_path)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "diff"
    assert payload["diagnostics"][0]["code"] == "EFILE001"


def test_diff_json_reports_parse_error(tmp_path: Path) -> None:
    source_path = tmp_path / "diff_broken.nl"
    source_path.write_text(
        """\
@module diff-broken
@target python

[main]
PURPOSE: Broken diff
LOGIC:
  bad step
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "diff", str(source_path), "--json"], cwd=tmp_path
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "diff"
    assert payload["diagnostics"] == [
        {
            "code": "EPARSE001",
            "file": str(source_path),
            "line": 7,
            "col": None,
            "message": "Invalid LOGIC step format; expected numbered step like '1. ...'",
            "hint": "Rewrite the line as a numbered LOGIC step like '1. ...'.",
        }
    ]
