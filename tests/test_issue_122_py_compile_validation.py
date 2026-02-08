"""Regression tests for Issue #122: compile path must validate emitted Python via py_compile."""

from __future__ import annotations

from argparse import Namespace

from nlsc import cli


def _write_minimal_nl(tmp_path, stem: str = "issue_122"):
    nl_file = tmp_path / f"{stem}.nl"
    nl_file.write_text(
        """\
@module issue_122
@target python

[hello]
PURPOSE: return greeting
RETURNS: "hello"
""",
        encoding="utf-8",
    )
    return nl_file


def test_should_fail_compile_when_emitted_python_is_syntactically_invalid(monkeypatch, tmp_path, capsys):
    """Compile should return non-zero when emitted Python cannot pass py_compile validation."""
    nl_file = _write_minimal_nl(tmp_path, stem="invalid_emission")

    def _emit_invalid_python(_nl_file, mode="mock"):
        return "def broken(:\n    return 1\n"

    monkeypatch.setattr(cli, "emit_python", _emit_invalid_python)

    args = Namespace(file=str(nl_file), target="python", output=None)
    exit_code = cli.cmd_compile(args)
    captured = capsys.readouterr()
    combined_output = f"{captured.out}\n{captured.err}"

    assert exit_code == 1, (
        "Expected cmd_compile to fail (exit code 1) when emitted Python is syntactically invalid, "
        f"but got {exit_code}."
    )
    assert "py_compile" in combined_output or "SyntaxError" in combined_output, (
        "Expected compile output to clearly indicate py_compile/SyntaxError validation failure."
    )


def test_should_include_generated_file_context_when_py_compile_validation_fails(monkeypatch, tmp_path, capsys):
    """Compile failure output should include generated file path/context for invalid emitted Python."""
    nl_file = _write_minimal_nl(tmp_path, stem="context_emission")
    expected_generated_path = str(nl_file.with_suffix(".py"))

    def _emit_invalid_python(_nl_file, mode="mock"):
        return "if True print('missing colon')\n"

    monkeypatch.setattr(cli, "emit_python", _emit_invalid_python)

    args = Namespace(file=str(nl_file), target="python", output=None)
    exit_code = cli.cmd_compile(args)
    captured = capsys.readouterr()
    combined_output = f"{captured.out}\n{captured.err}"

    assert exit_code == 1, (
        "Expected cmd_compile to fail when py_compile validation detects invalid generated Python, "
        f"but got {exit_code}."
    )
    assert "py_compile" in combined_output or "SyntaxError" in combined_output, (
        "Expected compile-time output to explicitly mention py_compile/SyntaxError validation failure."
    )
    assert expected_generated_path in combined_output, (
        "Expected compile-time validation failure output to include the generated Python file path."
    )
    assert "line" in combined_output.lower(), (
        "Expected compile-time validation failure output to include line context for the syntax failure."
    )


def test_should_succeed_compile_when_emitted_python_is_valid(monkeypatch, tmp_path):
    """Compile should continue succeeding for valid emitted Python."""
    nl_file = _write_minimal_nl(tmp_path, stem="valid_emission")

    def _emit_valid_python(_nl_file, mode="mock"):
        return "def hello():\n    return 'ok'\n"

    monkeypatch.setattr(cli, "emit_python", _emit_valid_python)

    args = Namespace(file=str(nl_file), target="python", output=None)
    exit_code = cli.cmd_compile(args)

    assert exit_code == 0, "Expected cmd_compile to succeed when emitted Python is syntactically valid."
