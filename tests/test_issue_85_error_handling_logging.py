"""Red-phase tests for Issue #85: standardized CLI/compiler error handling and logging."""

from __future__ import annotations

from argparse import Namespace
from types import SimpleNamespace

import pytest

from nlsc import cli
from nlsc.parser import ParseError


def _write_minimal_nl(tmp_path, stem: str = "issue_85"):
    nl_file = tmp_path / f"{stem}.nl"
    nl_file.write_text(
        """\
@module issue_85
@target python

[main]
PURPOSE: return value
RETURNS: "ok"
""",
        encoding="utf-8",
    )
    return nl_file


def test_should_include_standard_error_prefix_and_actionable_hint_when_compile_source_is_missing(capsys, tmp_path):
    """User-facing compile errors should be consistently prefixed and actionable."""
    missing_file = tmp_path / "missing_input.nl"
    args = Namespace(file=str(missing_file), target="python", output=None)

    exit_code = cli.cmd_compile(args)
    captured = capsys.readouterr()
    stderr = captured.err

    assert exit_code == 1, "Missing source file must return deterministic non-zero exit code 1."
    assert "Error:" in stderr, "Compile error output must include a standard 'Error:' prefix."
    assert "File not found" in stderr, "Compile error output must identify that the source file is missing."
    assert "Check that the path exists" in stderr, (
        "Compile error output must include an actionable next step for fixing a missing file path."
    )


def test_should_use_standard_error_prefix_when_run_parse_fails(monkeypatch, capsys, tmp_path):
    """Run command parse failures should use a consistent error prefix for user-facing output."""
    nl_file = _write_minimal_nl(tmp_path, stem="parse_failure")

    def _raise_parse_error(_source_path):
        raise ParseError("invalid section", line_number=5, line_content="BAD")

    monkeypatch.setattr(cli, "parse_nl_file_auto", _raise_parse_error)

    args = Namespace(file=str(nl_file), keep=None, target="python", verbose=False)
    exit_code = cli.cmd_run(args)
    captured = capsys.readouterr()
    stderr = captured.err

    assert exit_code == 1, "Parse failure in run path must return deterministic non-zero exit code 1."
    assert stderr.lstrip().startswith("Error:"), (
        "Run parse failure output must start with standardized 'Error:' prefix for consistency across commands."
    )
    assert "Parse error" in stderr, "Run parse failure output must preserve parse context for operators."


def test_should_include_stable_automation_error_token_when_run_dependency_resolution_fails(monkeypatch, capsys, tmp_path):
    """Dependency-resolution failures should emit stable machine-readable error text for automation."""
    nl_file = _write_minimal_nl(tmp_path, stem="resolution_failure")

    monkeypatch.setattr(cli, "parse_nl_file_auto", lambda _source_path: SimpleNamespace(anlus=[]))
    monkeypatch.setattr(
        cli,
        "resolve_dependencies",
        lambda _nl_file: SimpleNamespace(
            success=False,
            errors=[SimpleNamespace(anlu_id="main", message="cycle detected")],
        ),
    )

    args = Namespace(file=str(nl_file), keep=None, target="python", verbose=False)
    exit_code = cli.cmd_run(args)
    captured = capsys.readouterr()
    stderr = captured.err

    assert exit_code == 1, "Resolution failure must return deterministic non-zero exit code 1."
    assert "E_RESOLUTION" in stderr, (
        "Resolution failure output must contain stable token 'E_RESOLUTION' for automation matching."
    )
    assert "main" in stderr and "cycle detected" in stderr, (
        "Resolution failure output must still include ANLU id and message for debugging context."
    )


def test_should_return_deterministic_nonzero_code_instead_of_raising_when_run_hits_unexpected_exception(monkeypatch, tmp_path):
    """Unexpected run-path exceptions should be normalized into deterministic non-zero exit codes."""
    nl_file = _write_minimal_nl(tmp_path, stem="unexpected_exception")

    def _raise_unexpected(_source_path):
        raise RuntimeError("unexpected parser backend failure")

    monkeypatch.setattr(cli, "parse_nl_file_auto", _raise_unexpected)

    args = Namespace(file=str(nl_file), keep=None, target="python", verbose=False)

    try:
        exit_code = cli.cmd_run(args)
    except Exception as exc:  # pragma: no cover - intentional red assertion path
        pytest.fail(
            "Run path should not re-raise unexpected exceptions; expected deterministic non-zero code instead, "
            f"but raised {type(exc).__name__}: {exc}"
        )

    assert exit_code == 1, (
        "Unexpected run-path failures should normalize to deterministic non-zero exit code 1 for tooling reliability."
    )

