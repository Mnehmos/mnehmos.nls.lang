"""Structured JSON error output for CLI commands."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from nlsc.cli import main


REPO_ROOT = Path(__file__).resolve().parents[1]


def _run_nlsc(
    argv: list[str], *, cwd: Path, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "nlsc", *argv],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env=env,
    )


def _load_json_output(result: subprocess.CompletedProcess[str]) -> dict:
    assert result.stdout.strip(), f"expected JSON stdout, got stderr={result.stderr!r}"
    return json.loads(result.stdout)


def _treesitter_unavailable_env(tmp_path: Path) -> dict[str, str]:
    hook_dir = tmp_path / "sitecustomize"
    hook_dir.mkdir()
    (hook_dir / "sitecustomize.py").write_text(
        "import nlsc.parser_treesitter as parser_treesitter\n"
        "parser_treesitter.is_available = lambda: False\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    pythonpath_parts = [str(hook_dir), str(REPO_ROOT)]
    existing_pythonpath = env.get("PYTHONPATH")
    if existing_pythonpath:
        pythonpath_parts.append(existing_pythonpath)
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)
    return env


def test_verify_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.nl"

    result = _run_nlsc(["verify", str(missing_path), "--json"], cwd=REPO_ROOT)

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


def test_verify_json_reports_missing_required_file_argument() -> None:
    result = _run_nlsc(["verify", "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["ok"] is False
    assert payload["command"] == "verify"
    assert payload["diagnostics"] == [
        {
            "code": "ECLI001",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "the following arguments are required: file",
            "hint": "Rerun the command with --help to inspect the required arguments and valid options.",
        }
    ]
    assert payload["usage"].startswith("usage: nlsc verify")


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
        ["--parser", "regex", "verify", str(source_path), "--json"], cwd=REPO_ROOT
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


def test_verify_json_reports_parser_backend_unavailable(tmp_path: Path) -> None:
    source_path = tmp_path / "verify_source.nl"
    source_path.write_text(
        "@module verify-source\n@target python\n\n[main]\nPURPOSE: Ok\nRETURNS: 1\n",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "treesitter", "verify", str(source_path), "--json"],
        cwd=REPO_ROOT,
        env=_treesitter_unavailable_env(tmp_path),
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "verify"
    assert payload["parser"] == "treesitter"
    assert payload["diagnostics"] == [
        {
            "code": "EPARSE002",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "Parser backend 'treesitter' is unavailable: tree-sitter is not installed",
            "hint": "Install with: pip install nlsc[treesitter], or rerun with --parser auto or --parser regex.",
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
        ["--parser", "regex", "verify", str(source_path), "--json"], cwd=REPO_ROOT
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
        ["--parser", "regex", "verify", str(source_path), "--json"], cwd=REPO_ROOT
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

    result = _run_nlsc(["compile", str(missing_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "compile"
    assert payload["diagnostics"][0]["code"] == "EFILE001"


def test_compile_json_reports_invalid_target_choice(tmp_path: Path) -> None:
    source_path = tmp_path / "compile_source.nl"
    source_path.write_text(
        "@module compile-source\n@target python\n\n[main]\nPURPOSE: Ok\nRETURNS: 1\n",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["compile", str(source_path), "--target", "ruby", "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "compile"
    assert payload["diagnostics"] == [
        {
            "code": "ECLI001",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "argument -t/--target: invalid choice: 'ruby' (choose from python, typescript)",
            "hint": "Rerun the command with --help to inspect the required arguments and valid options.",
        }
    ]
    assert payload["usage"].startswith("usage: nlsc compile")


def test_unknown_subcommand_with_json_reports_structured_diagnostic() -> None:
    result = _run_nlsc(["frobnicate", "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "frobnicate"
    assert payload["diagnostics"] == [
        {
            "code": "ECLI001",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "argument command: invalid choice: 'frobnicate' (choose from init, compile, run, verify, explain, graph, test, atomize, diff, dif, watch, lock:check, lock:update, lsp, assoc)",
            "hint": "Rerun the command with --help to inspect the required arguments and valid options.",
        }
    ]
    assert payload["usage"].startswith("usage: nlsc")


def test_main_argv_json_parse_errors_use_supplied_argv(capsys: Any) -> None:
    exit_code = main(["verify", "--json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["command"] == "verify"
    assert payload["diagnostics"] == [
        {
            "code": "ECLI001",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "the following arguments are required: file",
            "hint": "Rerun the command with --help to inspect the required arguments and valid options.",
        }
    ]
    assert payload["usage"].startswith("usage: nlsc verify")
    assert captured.err == ""


def test_compile_json_reports_parser_backend_unavailable(tmp_path: Path) -> None:
    source_path = tmp_path / "compile_source.nl"
    source_path.write_text(
        "@module compile-source\n@target python\n\n[main]\nPURPOSE: Ok\nRETURNS: 1\n",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "treesitter", "compile", str(source_path), "--json"],
        cwd=REPO_ROOT,
        env=_treesitter_unavailable_env(tmp_path),
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "compile"
    assert payload["parser"] == "treesitter"
    assert payload["diagnostics"] == [
        {
            "code": "EPARSE002",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "Parser backend 'treesitter' is unavailable: tree-sitter is not installed",
            "hint": "Install with: pip install nlsc[treesitter], or rerun with --parser auto or --parser regex.",
        }
    ]


def test_run_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_run.nl"

    result = _run_nlsc(["run", str(missing_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "run"
    assert payload["diagnostics"][0]["code"] == "EFILE001"


def test_graph_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_graph.nl"

    result = _run_nlsc(["graph", str(missing_path), "--json"], cwd=REPO_ROOT)

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
        ["graph", str(source_path), "--json", "--anlu", "helper"], cwd=REPO_ROOT
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
        cwd=REPO_ROOT,
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


def test_atomize_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_atomize.py"

    result = _run_nlsc(["atomize", str(missing_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "atomize"
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


def test_atomize_json_reports_python_syntax_error(tmp_path: Path) -> None:
    source_path = tmp_path / "broken.py"
    source_path.write_text(
        "def broken(:\n    return 1\n",
        encoding="utf-8",
    )

    result = _run_nlsc(["atomize", str(source_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "atomize"
    assert payload["diagnostics"] == [
        {
            "code": "EATOM001",
            "file": str(source_path),
            "line": 1,
            "col": 12,
            "message": "Python syntax error: invalid syntax",
            "hint": "Fix the Python syntax and rerun `nlsc atomize`.",
        }
    ]


def test_atomize_json_reports_write_failure(tmp_path: Path) -> None:
    source_path = tmp_path / "ok.py"
    source_path.write_text(
        "def add(a: int, b: int) -> int:\n    return a + b\n",
        encoding="utf-8",
    )
    output_path = tmp_path / "missing" / "out.nl"

    result = _run_nlsc(
        ["atomize", str(source_path), "--output", str(output_path), "--json"],
        cwd=REPO_ROOT,
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "atomize"
    assert payload["diagnostics"] == [
        {
            "code": "EATOM002",
            "file": str(source_path),
            "line": None,
            "col": None,
            "message": payload["diagnostics"][0]["message"],
            "hint": "Check the output path and local filesystem permissions, then rerun `nlsc atomize`.",
        }
    ]
    assert str(output_path) in payload["diagnostics"][0]["message"]
    assert "No such file or directory" in payload["diagnostics"][0]["message"]


def test_diff_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_diff.nl"

    result = _run_nlsc(["diff", str(missing_path), "--json"], cwd=REPO_ROOT)

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
        ["--parser", "regex", "diff", str(source_path), "--json"], cwd=REPO_ROOT
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


def test_test_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_test.nl"

    result = _run_nlsc(["test", str(missing_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "test"
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


def test_test_json_reports_parse_error(tmp_path: Path) -> None:
    source_path = tmp_path / "broken_test.nl"
    source_path.write_text(
        """\
@module broken-test
@target python

[main]
PURPOSE: Broken test file
LOGIC:
  bad step
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "test", str(source_path), "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "test"
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


def test_lock_check_json_reports_missing_lockfile(tmp_path: Path) -> None:
    source_path = tmp_path / "lock_missing.nl"
    source_path.write_text(
        """\
@module lock-missing
@target python

[main]
PURPOSE: Missing lock
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(["lock:check", str(source_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "lock:check"
    assert payload["diagnostics"] == [
        {
            "code": "ELOCK001",
            "file": str(source_path.with_suffix(".nl.lock")),
            "line": None,
            "col": None,
            "message": f"Lockfile not found: {source_path.with_suffix('.nl.lock')}",
            "hint": "Run `nlsc compile <file>` or `nlsc lock:update <file>` to generate a lockfile.",
        }
    ]


def test_lock_check_json_reports_outdated_lockfile(tmp_path: Path) -> None:
    source_path = tmp_path / "lock_outdated.nl"
    source_path.write_text(
        """\
@module lock-outdated
@target python

[main]
PURPOSE: Updated lock
RETURNS: 2
""",
        encoding="utf-8",
    )
    lock_path = source_path.with_suffix(".nl.lock")
    lock_path.write_text(
        """\
# DO NOT EDIT - Generated by nlsc
schema_version: 1
generated_at: 2026-04-02T00:00:00+00:00
compiler_version: 0.0.0
llm_backend: mock

modules:
  lock-outdated:
    source_hash: sha256:deadbeefcafe
    anlus:
      main:
        source_hash: sha256:oldoldoldold
        output_hash: sha256:outdatedcode
        output_lines: 1

targets:
  python:
    file: lock_outdated.py
    hash: sha256:outdatedcode
    lines: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "lock:check", str(source_path), "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "lock:check"
    assert payload["diagnostics"] == [
        {
            "code": "ELOCK002",
            "file": str(source_path),
            "line": 4,
            "col": 1,
            "message": "ANLU main has changed since lock",
            "hint": "Run `nlsc compile <file>` or `nlsc lock:update <file>` to regenerate the lockfile.",
        }
    ]


def test_lock_update_json_reports_parse_error(tmp_path: Path) -> None:
    source_path = tmp_path / "lock_update_broken.nl"
    source_path.write_text(
        """\
@module lock-update-broken
@target python

[main]
PURPOSE: Broken lock update
LOGIC:
  bad step
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "lock:update", str(source_path), "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "lock:update"
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


def test_test_json_reports_resolution_error(tmp_path: Path) -> None:
    source_path = tmp_path / "missing_dep_test.nl"
    source_path.write_text(
        """\
@module missing-dep-test
@target python

[main]
PURPOSE: Needs helper
DEPENDS: [helper]
RETURNS: 1

@test [main] {
  main() == 1
}
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "test", str(source_path), "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "test"
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


def test_test_json_reports_stdlib_use_error(tmp_path: Path) -> None:
    source_path = tmp_path / "use_missing_test.nl"
    source_path.write_text(
        """\
@module use-missing-test
@target python
@use math.missing

[main]
PURPOSE: No-op
RETURNS: 1

@test [main] {
  main() == 1
}
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "test", str(source_path), "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "test"
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


def test_test_json_reports_pytest_failures(tmp_path: Path) -> None:
    source_path = tmp_path / "failing_test.nl"
    source_path.write_text(
        """\
@module failing-test
@target python

[always-one]
PURPOSE: Always returns one
INPUTS:
  - value: number
RETURNS: 1

@test [always-one] {
  always_one(5) == 5
}
""",
        encoding="utf-8",
    )

    result = _run_nlsc(["test", str(source_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "test"
    assert payload["ok"] is False
    assert payload["diagnostics"] == [
        {
            "code": "ETEST001",
            "file": str(source_path),
            "line": None,
            "col": None,
            "message": "Generated tests failed with pytest exit code 1.",
            "hint": "Inspect pytest_stdout and pytest_stderr for failing assertions or setup errors.",
        }
    ]
    assert payload["total_cases"] == 1
    assert payload["pytest_exit_code"] == 1
    assert "assert 1 == 5" in payload["pytest_stdout"]


def test_test_json_reports_success_metadata(tmp_path: Path) -> None:
    source_path = tmp_path / "passing_test.nl"
    source_path.write_text(
        """\
@module passing-test
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

@test [add] {
  add(2, 3) == 5
  add(4, 1) == 5
}
""",
        encoding="utf-8",
    )

    result = _run_nlsc(["test", str(source_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 0
    payload = _load_json_output(result)
    assert payload["ok"] is True
    assert payload["command"] == "test"
    assert payload["diagnostics"] == []
    assert payload["file"] == str(source_path)
    assert payload["total_cases"] == 2
    assert payload["pytest_exit_code"] == 0
    assert payload["pytest_stdout"]


def test_watch_json_reports_missing_directory(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_watch_dir"

    result = _run_nlsc(["watch", str(missing_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "watch"
    assert payload["diagnostics"] == [
        {
            "code": "EFILE001",
            "file": str(missing_path),
            "line": None,
            "col": None,
            "message": f"Directory not found: {missing_path}",
            "hint": "Check that the path exists and try again.",
        }
    ]


def test_watch_json_reports_not_a_directory(tmp_path: Path) -> None:
    source_path = tmp_path / "not_a_dir.nl"
    source_path.write_text("@module watch\n@target python\n", encoding="utf-8")

    result = _run_nlsc(["watch", str(source_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "watch"
    assert payload["diagnostics"] == [
        {
            "code": "EWATCH001",
            "file": str(source_path),
            "line": None,
            "col": None,
            "message": f"Watch path is not a directory: {source_path}",
            "hint": "Pass a directory path to `nlsc watch` and try again.",
        }
    ]
