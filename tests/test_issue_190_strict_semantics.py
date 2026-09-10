"""Issue #190: reject executable prose and implicit placeholder returns.

Strict verify/compile share one executable-contract boundary; default
(legacy scaffold) compilation stays available but is visibly marked.
"""

from __future__ import annotations

import json

import pytest

from nlsc.cli import main
from nlsc.emitter import emit_python
from nlsc.lockfile import generate_lockfile
from nlsc.lowering import lower_module
from nlsc.parser import parse_nl_file
from nlsc.pipeline import executable_contract_diagnostics

REPRODUCER = """@module payment_probe
[checkout]
PURPOSE: Process a payment
LOGIC:
  1. Process customer payment -> payment
RETURNS: payment
"""

DECLARED_TYPE_NO_IMPL = """@module typed
[answer]
PURPOSE: Give the answer
LOGIC:
  1. total = 42
RETURNS: number
"""

DESCRIPTIVE_RETURN = """@module desc_return
[explain]
PURPOSE: Explain the rule
RETURNS: The discounted total after promotion
"""

VALID_PROGRAM = """@module valid_probe
[add]
PURPOSE: add
INPUTS:
  - a: number
  - b: number
LOGIC:
  1. total = a + b
RETURNS: total

[nothing]
PURPOSE: do nothing
RETURNS: none

[narrative]
PURPOSE: narrate
LOGIC:
  1. Consider the customer's history
RETURNS: 0
"""

EXECUTABLE_EDGE_CASE = """@module edges
[grade]
PURPOSE: grade a score
INPUTS:
  - score: number
EDGE CASES:
  - score > 100 -> cap the score at 100
RETURNS: score
"""


def _write(tmp_path, source: str, name: str = "probe.nl"):
    path = tmp_path / name
    path.write_text(source, encoding="utf-8")
    return path


# --------------------------------------------------------------------------
# Shared boundary: one diagnostic set for every strict consumer
# --------------------------------------------------------------------------


def test_reproducer_produces_source_level_diagnostics():
    nl_file = parse_nl_file(REPRODUCER)
    diagnostics = executable_contract_diagnostics(nl_file)
    assert diagnostics
    checkout_diag = [d for d in diagnostics if "checkout" in d.message]
    assert checkout_diag, diagnostics
    assert checkout_diag[0].code == "EIR002"
    assert checkout_diag[0].line == 5
    assert "Process customer payment" in checkout_diag[0].message


def test_declared_return_type_without_value_expression_is_rejected():
    nl_file = parse_nl_file(DECLARED_TYPE_NO_IMPL)
    diagnostics = executable_contract_diagnostics(nl_file)
    codes = [d.code for d in diagnostics]
    assert "EIR004" in codes


def test_descriptive_return_text_is_rejected():
    nl_file = parse_nl_file(DESCRIPTIVE_RETURN)
    diagnostics = executable_contract_diagnostics(nl_file)
    assert any(d.code == "EIR002" for d in diagnostics)


def test_executable_edge_case_with_prose_behavior_is_rejected():
    nl_file = parse_nl_file(EXECUTABLE_EDGE_CASE)
    diagnostics = executable_contract_diagnostics(nl_file)
    assert any("edge case" in d.message.lower() for d in diagnostics)


def test_valid_programs_produce_no_contract_diagnostics():
    nl_file = parse_nl_file(VALID_PROGRAM)
    assert executable_contract_diagnostics(nl_file) == []


def test_explicit_zero_and_empty_literals_pass():
    source = """@module literals
[zero]
PURPOSE: zero
RETURNS: 0

[empty]
PURPOSE: empty
LOGIC:
  1. items = []
RETURNS: items
"""
    assert executable_contract_diagnostics(parse_nl_file(source)) == []


# --------------------------------------------------------------------------
# CLI: strict verify and compile share the diagnostic
# --------------------------------------------------------------------------


def test_strict_verify_fails_reproducer(tmp_path, capsys):
    path = _write(tmp_path, REPRODUCER)
    code = main(["verify", "--strict", str(path)])
    captured = capsys.readouterr()
    assert code == 1
    assert "EIR002" in captured.err
    assert "Process customer payment" in captured.err


def test_strict_compile_fails_reproducer_with_same_diagnostic(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, REPRODUCER)
    code = main(["compile", "--strict", str(path)])
    captured = capsys.readouterr()
    assert code == 1
    assert "EIR002" in captured.err
    assert "Process customer payment" in captured.err
    # No runnable artifact was produced.
    assert not (tmp_path / "probe.py").exists()


def test_strict_verify_json_reports_diagnostics(tmp_path, capsys):
    path = _write(tmp_path, REPRODUCER)
    code = main(["verify", "--strict", "--json", str(path)])
    payload = json.loads(capsys.readouterr().out)
    assert code == 1
    assert payload["ok"] is False
    codes = [d["code"] for d in payload["diagnostics"]]
    assert "EIR002" in codes


def test_strict_run_and_test_share_the_boundary(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, REPRODUCER)
    assert main(["run", "--strict", str(path)]) == 1
    assert main(["test", "--strict", str(path)]) == 1
    err = capsys.readouterr().err
    assert err.count("EIR002") >= 2


def test_valid_program_passes_strict_verify(tmp_path):
    path = _write(tmp_path, VALID_PROGRAM)
    assert main(["verify", "--strict", str(path)]) == 0


# --------------------------------------------------------------------------
# Default mode: scaffolds stay runnable but are visibly incomplete
# --------------------------------------------------------------------------


def test_default_compile_marks_scaffold_artifact(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, REPRODUCER)
    code = main(["compile", str(path)])
    captured = capsys.readouterr()
    assert code == 0
    assert "EIR002" in captured.err  # visible warning
    artifact = tmp_path / "probe.py"
    assert artifact.exists()
    content = artifact.read_text(encoding="utf-8")
    assert "INCOMPLETE SCAFFOLD" in content


def test_default_compile_of_valid_program_has_no_marker(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, VALID_PROGRAM)
    code = main(["compile", str(path)])
    captured = capsys.readouterr()
    assert code == 0
    artifact = tmp_path / "probe.py"
    content = artifact.read_text(encoding="utf-8")
    assert "INCOMPLETE SCAFFOLD" not in content
    assert "EIR002" not in captured.err


def test_scaffold_anlu_detection_is_per_anlu():
    two = """@module mixed
[good]
PURPOSE: fine
LOGIC:
  1. x = 1
RETURNS: x

[bad]
PURPOSE: not fine
LOGIC:
  1. Process customer payment -> payment
RETURNS: payment
"""
    from nlsc.pipeline import scaffold_anlus

    assert scaffold_anlus(parse_nl_file(two)) == {"bad"}
