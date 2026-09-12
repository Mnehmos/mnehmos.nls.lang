"""Issue #202: the target capability matrix fails explicitly.

Content a target cannot represent must produce diagnostics instead of
silently incomplete output: dropped @literal blocks leave undefined
function calls in TypeScript, and a dropped @main block loses the entry
point.  Coverage-only losses (@property specifications) are strict-only.
"""

from __future__ import annotations

import json

import pytest

from nlsc.capabilities import TARGET_CAPABILITIES, capability_gaps
from nlsc.cli import main
from nlsc.parser import parse_nl_file

LITERAL_FILE = """@module cap_literal
@target typescript

@literal python {
def helper(x):
    return x * 2
}

[use-it]
PURPOSE: use the literal helper
INPUTS:
  - x: number
RETURNS: helper(x)
"""

MAIN_FILE = """@module cap_main
@target typescript

[add]
PURPOSE: add
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

@main {
  PRINT add(1, 2)
}
"""

PROPERTY_FILE = """@module cap_property
@target typescript

[add]
PURPOSE: add
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

@property [add] {
  add(a, b) == add(b, a)
}
"""


def _write(tmp_path, source: str, name: str):
    path = tmp_path / name
    path.write_text(source, encoding="utf-8")
    return path


# --------------------------------------------------------------------------
# Matrix
# --------------------------------------------------------------------------


def test_matrix_declares_python_and_typescript():
    assert TARGET_CAPABILITIES["python"]["literal_blocks"] is True
    assert TARGET_CAPABILITIES["typescript"]["literal_blocks"] is False
    assert TARGET_CAPABILITIES["typescript"]["main_block"] is False


def test_gaps_are_empty_for_supported_content():
    nl_file = parse_nl_file(LITERAL_FILE)
    assert capability_gaps(nl_file, "python") == []
    assert [g.feature for g in capability_gaps(nl_file, "typescript")] == [
        "literal_blocks"
    ]


# --------------------------------------------------------------------------
# Fatal: dropped program content
# --------------------------------------------------------------------------


def test_typescript_compile_with_literal_fails_and_writes_nothing(tmp_path, capsys):
    path = _write(tmp_path, LITERAL_FILE, "cap_literal.nl")
    assert main(["compile", str(path), "-t", "typescript"]) == 1
    err = capsys.readouterr().err
    assert "ETARGET002" in err
    assert "@literal blocks" in err
    assert not (tmp_path / "cap_literal.ts").exists()


def test_typescript_compile_with_main_block_fails(tmp_path, capsys):
    path = _write(tmp_path, MAIN_FILE, "cap_main.nl")
    assert main(["compile", str(path), "-t", "typescript"]) == 1
    assert "@main block" in capsys.readouterr().err


def test_python_compile_with_literal_still_succeeds(tmp_path, capsys):
    path = _write(tmp_path, LITERAL_FILE, "cap_literal.nl")
    assert main(["compile", str(path), "-t", "python"]) == 0
    code = (tmp_path / "cap_literal.py").read_text(encoding="utf-8")
    assert "def helper(x):" in code


def test_ci_refuses_unrepresentable_target(tmp_path, capsys):
    path = _write(tmp_path, LITERAL_FILE, "cap_literal.nl")
    # Produce a lock for the python target first so only the capability
    # gate can be responsible for the failure.
    assert main(["compile", str(path), "-t", "python"]) == 0
    capsys.readouterr()
    assert main(["ci", str(path), "--compile", "-t", "typescript"]) == 1
    assert "ETARGET002" in capsys.readouterr().err


# --------------------------------------------------------------------------
# Strict-only: dropped test coverage
# --------------------------------------------------------------------------


def test_property_drop_warns_by_default_and_fails_strict(tmp_path, capsys):
    path = _write(tmp_path, PROPERTY_FILE, "cap_property.nl")
    assert main(["compile", str(path), "-t", "typescript"]) == 0
    captured = capsys.readouterr()
    assert "ETARGET002" in captured.err
    assert "@property" in captured.err

    assert main(["compile", str(path), "-t", "typescript", "--strict"]) == 1
    assert "ETARGET002" in capsys.readouterr().err


def test_capability_json_payload(tmp_path, capsys):
    path = _write(tmp_path, LITERAL_FILE, "cap_literal.nl")
    assert main(["compile", "--json", str(path), "-t", "typescript"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is False
    assert "ETARGET002" in [d["code"] for d in payload["diagnostics"]]


# --------------------------------------------------------------------------
# The feature corpus stays within representable content
# --------------------------------------------------------------------------


def test_feature_examples_are_typescript_representable_except_documented():
    from pathlib import Path

    features = Path(__file__).resolve().parent.parent / "examples" / "features"
    gaps_by_file = {}
    for path in sorted(features.glob("*.nl")):
        nl_file = parse_nl_file(path.read_text(encoding="utf-8"), source_path=str(path))
        fatal = [g for g in capability_gaps(nl_file, "typescript") if g.fatal]
        if fatal:
            gaps_by_file[path.stem] = sorted(g.feature for g in fatal)
    # Every example carries an @main entry point (a Python-target
    # feature), and the deliberate escape-hatch example additionally uses
    # @literal blocks; nothing else is TypeScript-unrepresentable.
    assert "literals" in gaps_by_file
    assert gaps_by_file.pop("literals") == ["literal_blocks", "main_block"]
    assert {stem: gaps for stem, gaps in gaps_by_file.items()} == {
        stem: ["main_block"] for stem in gaps_by_file
    }
