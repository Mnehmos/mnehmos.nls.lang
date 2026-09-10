"""CLI tests for `nlsc ir` and parser-parity for the shared lowering contract."""

from __future__ import annotations

import json

from nlsc.cli import main
from nlsc.ir import module_to_canonical
from nlsc.lowering import lower_module
from nlsc.parser import parse_nl_file
from nlsc.parser_treesitter import is_available, parse_nl_file_treesitter

SIMPLE_SOURCE = """@module cli_probe
[add]
PURPOSE: add
INPUTS:
  - a: number
  - b: number
LOGIC:
  1. total = a + b
RETURNS: total
"""

PROSE_SOURCE = """@module payment_probe
[checkout]
PURPOSE: Process a payment
LOGIC:
  1. Process customer payment -> payment
RETURNS: payment
"""


def _write(tmp_path, source: str):
    path = tmp_path / "probe.nl"
    path.write_text(source, encoding="utf-8")
    return path


def test_cli_ir_prints_canonical_text(tmp_path, capsys):
    path = _write(tmp_path, SIMPLE_SOURCE)
    exit_code = main(["ir", str(path)])
    out = capsys.readouterr()
    assert exit_code == 0
    assert out.out.startswith(";; nls-ir ")
    assert "(binary add (ref a) (ref b))" in out.out


def test_cli_ir_json_payload(tmp_path, capsys):
    path = _write(tmp_path, SIMPLE_SOURCE)
    exit_code = main(["ir", "--json", str(path)])
    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["ok"] is True
    assert payload["command"] == "ir"
    assert payload["ir"]["module"] == "cli_probe"
    assert payload["ir"]["ir_version"]
    assert payload["canonical"].startswith(";; nls-ir ")


def test_cli_ir_strict_fails_on_prose_binding(tmp_path, capsys):
    path = _write(tmp_path, PROSE_SOURCE)
    exit_code = main(["ir", "--strict", str(path)])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "EIR002" in captured.err


def test_cli_ir_tolerant_mode_reports_warning_but_exits_zero(tmp_path, capsys):
    path = _write(tmp_path, PROSE_SOURCE)
    exit_code = main(["ir", str(path)])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "EIR002" in captured.err
    assert '(foreign reason=prose "Process customer payment")' in captured.out


def test_cli_ir_json_includes_diagnostics(tmp_path, capsys):
    path = _write(tmp_path, PROSE_SOURCE)
    exit_code = main(["ir", "--json", str(path)])
    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["ok"] is True
    codes = [d["code"] for d in payload["warnings"]]
    assert "EIR002" in codes


def test_cli_ir_missing_file(tmp_path, capsys):
    exit_code = main(["ir", "--json", str(tmp_path / "nope.nl")])
    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert payload["ok"] is False


def test_cli_ir_writes_output_file(tmp_path, capsys):
    path = _write(tmp_path, SIMPLE_SOURCE)
    out_path = tmp_path / "probe.ir"
    exit_code = main(["ir", "--output", str(out_path), str(path)])
    assert exit_code == 0
    written = out_path.read_text(encoding="utf-8")
    assert written.startswith(";; nls-ir ")


# --------------------------------------------------------------------------
# Both parser backends share one lowering contract
# --------------------------------------------------------------------------

PARITY_SOURCE = """@module parity_probe
[compute]
PURPOSE: compute
INPUTS:
  - flag: boolean
  - items: list of number
LOGIC:
  1. total = sum(items)
  2. IF flag THEN [notify](total) -> done
  3. Log the result for audit
RETURNS: total
DEPENDS: [notify]

[notify]
PURPOSE: notify
INPUTS:
  - value: number
RETURNS: value
"""


def test_both_parser_backends_lower_identically():
    if not is_available():
        import pytest

        pytest.skip("tree-sitter backend not installed")
    regex_module = lower_module(parse_nl_file(PARITY_SOURCE))
    ts_module = lower_module(parse_nl_file_treesitter(PARITY_SOURCE))
    assert module_to_canonical(regex_module) == module_to_canonical(ts_module)


def test_tree_sitter_steps_carry_line_numbers():
    if not is_available():
        import pytest

        pytest.skip("tree-sitter backend not installed")
    ts_file = parse_nl_file_treesitter(PARITY_SOURCE)
    steps = [s for anlu in ts_file.anlus for s in anlu.logic_steps]
    assert all(s.line_number > 0 for s in steps)
