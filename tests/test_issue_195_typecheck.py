"""Issue #195: resolve operation signatures and type-check the IR.

Two severity tiers, matching the CLI contract:

- Tier A (always fatal): unknown ANLU calls, undefined value uses, unknown
  fields/constructor fields, duplicate identifiers, target-name collisions,
  arity mismatches, incompatible binary operands.
- Tier B (fatal under --strict, warnings otherwise): argument type
  mismatches, return/condition type mismatches, DEPENDS contract drift,
  undeclared foreign calls.
"""

from __future__ import annotations

import json

import pytest

from nlsc.cli import main
from nlsc.parser import parse_nl_file
from nlsc.typecheck import check_module

UNKNOWN_CALL = """@module unknown_call
[increment]
PURPOSE: add one
INPUTS:
  - value: number
RETURNS: value + 1

[probe]
PURPOSE: call something missing
LOGIC:
  1. [missing](1) -> result
RETURNS: result
"""

UNDEFINED_USE = """@module undefined_use
[probe]
PURPOSE: use a value that never exists
LOGIC:
  1. total = 1
RETURNS: missing_value
"""

UNKNOWN_FIELD = """@module unknown_field
@type Point {
  x: number
  y: number
}

[probe]
PURPOSE: read a missing field
INPUTS:
  - p: Point
LOGIC:
  1. z = p.z
RETURNS: z
"""

UNKNOWN_CONSTRUCTOR_FIELD = """@module bad_ctor
@type Point {
  x: number
  y: number
}

[make]
PURPOSE: build a point badly
LOGIC:
  1. p = Point(x=1, w=2)
RETURNS: p
"""

DUPLICATE_IDENTIFIERS = """@module dup
[same]
PURPOSE: one
RETURNS: 0

[same]
PURPOSE: two
RETURNS: 0
"""

TARGET_NAME_COLLISION = """@module collide
[foo-bar]
PURPOSE: one
RETURNS: 0

[foo_bar]
PURPOSE: two
RETURNS: 0
"""

ARITY_MISMATCH = """@module arity
[increment]
PURPOSE: add one
INPUTS:
  - value: number
RETURNS: value + 1

[probe]
PURPOSE: too many arguments
LOGIC:
  1. r = [increment](1, 2)
RETURNS: r
DEPENDS: [increment]
"""

ARG_TYPE_MISMATCH = """@module arg_types
[increment]
PURPOSE: add one
INPUTS:
  - value: number
RETURNS: value + 1

[probe]
PURPOSE: pass the wrong type
LOGIC:
  1. r = [increment]("hello")
RETURNS: r
DEPENDS: [increment]
"""

BINARY_MISMATCH = """@module binary_probe
[broken]
PURPOSE: add mismatched operands
INPUTS:
  - name: string
LOGIC:
  1. total = name + 1
RETURNS: total
"""

DEPENDS_DRIFT = """@module depends_drift
[increment]
PURPOSE: add one
INPUTS:
  - value: number
RETURNS: value + 1

[probe]
PURPOSE: forget to declare the dependency
LOGIC:
  1. r = [increment](1)
RETURNS: r
DEPENDS: None

[declared-unused]
PURPOSE: declare but never call
LOGIC:
  1. x = 1
RETURNS: x
DEPENDS: [increment]
"""

VALID_PROGRAM = """@module valid_calls
@type Point {
  x: number
  y: number
}

[distance]
PURPOSE: distance from origin
INPUTS:
  - p: Point
RETURNS: sqrt(p.x * p.x + p.y * p.y)

[add]
PURPOSE: add numbers
INPUTS:
  - a: number
  - b: number
LOGIC:
  1. total = a + b
RETURNS: total

[compute]
PURPOSE: compose valid calls
INPUTS:
  - p: Point
LOGIC:
  1. raw = [add](p.x, p.y)
  2. count = len([1, 2, 3])
  3. total = sum([1, 2, 3])
  4. origin = Point(x=0, y=0)
RETURNS: raw
DEPENDS: [add]

[fib]
PURPOSE: recurse
INPUTS:
  - n: number
LOGIC:
  1. IF n <= 1 THEN n -> result ELSE n + [fib](n - 1) -> result
RETURNS: result
DEPENDS: [fib]

[uses-optional]
PURPOSE: call with optional omitted
INPUTS:
  - greeting: string, optional
RETURNS: greeting

[calls-optional]
PURPOSE: caller
LOGIC:
  1. text = [uses-optional]()
RETURNS: text
DEPENDS: [uses-optional]
"""


def _codes(result, field: str) -> list[str]:
    return [d.code for d in getattr(result, field)]


# --------------------------------------------------------------------------
# Tier A: always-fatal diagnostics
# --------------------------------------------------------------------------


def test_unknown_anlu_call_is_fatal():
    result = check_module(parse_nl_file(UNKNOWN_CALL))
    assert "ESEM001" in _codes(result, "errors")
    diag = [d for d in result.errors if d.code == "ESEM001"][0]
    assert diag.line is not None
    assert "missing" in diag.message


def test_undefined_value_use_is_fatal():
    result = check_module(parse_nl_file(UNDEFINED_USE))
    assert "ESEM004" in _codes(result, "errors")


def test_unknown_field_on_declared_type_is_fatal():
    result = check_module(parse_nl_file(UNKNOWN_FIELD))
    assert "ESEM005" in _codes(result, "errors")


def test_unknown_constructor_field_is_fatal():
    result = check_module(parse_nl_file(UNKNOWN_CONSTRUCTOR_FIELD))
    assert "ESEM005" in _codes(result, "errors")


def test_duplicate_identifiers_are_fatal():
    result = check_module(parse_nl_file(DUPLICATE_IDENTIFIERS))
    assert "ESEM007" in _codes(result, "errors")


def test_target_name_collision_is_fatal():
    result = check_module(parse_nl_file(TARGET_NAME_COLLISION))
    assert "ESEM007" in _codes(result, "errors")
    diag = [d for d in result.errors if d.code == "ESEM007"][0]
    assert "foo-bar" in diag.message and "foo_bar" in diag.message


def test_arity_mismatch_is_fatal():
    result = check_module(parse_nl_file(ARITY_MISMATCH))
    assert "ESEM002" in _codes(result, "errors")


def test_incompatible_binary_operands_are_fatal():
    result = check_module(parse_nl_file(BINARY_MISMATCH))
    assert "ESEM006" in _codes(result, "errors")


# --------------------------------------------------------------------------
# Tier B: strict-only diagnostics
# --------------------------------------------------------------------------


def test_argument_type_mismatch_warns_by_default():
    result = check_module(parse_nl_file(ARG_TYPE_MISMATCH))
    assert "ESEM003" in _codes(result, "warnings")
    assert not any(d.code == "ESEM003" for d in result.errors)


def test_depends_drift_reports_both_directions():
    result = check_module(parse_nl_file(DEPENDS_DRIFT))
    warnings = _codes(result, "warnings")
    assert warnings.count("ESEM008") >= 2  # undeclared call + unused declaration


# --------------------------------------------------------------------------
# Valid programs pass everything
# --------------------------------------------------------------------------


def test_valid_program_has_no_diagnostics():
    result = check_module(parse_nl_file(VALID_PROGRAM))
    assert result.errors == []
    assert result.warnings == []


def test_self_recursion_is_supported():
    source = """@module recurse
[fib]
PURPOSE: fib
INPUTS:
  - n: number
LOGIC:
  1. IF n <= 1 THEN n -> result ELSE n + [fib](n - 1) -> result
RETURNS: result
"""
    result = check_module(parse_nl_file(source))
    assert result.errors == []


def test_snake_case_alias_resolves_kebab_anlu():
    source = """@module aliasing
[priority-to-weight]
PURPOSE: weight
INPUTS:
  - priority: string
RETURNS: 1

[compare]
PURPOSE: use the snake spelling
INPUTS:
  - p: string
LOGIC:
  1. w = priority_to_weight(p)
RETURNS: w
"""
    result = check_module(parse_nl_file(source))
    assert result.errors == []


# --------------------------------------------------------------------------
# CLI wiring: same diagnostic for every target, both modes behave
# --------------------------------------------------------------------------


def _write(tmp_path, source: str):
    path = tmp_path / "probe.nl"
    path.write_text(source, encoding="utf-8")
    return path


def test_unknown_call_fails_default_verify(tmp_path, capsys):
    path = _write(tmp_path, UNKNOWN_CALL)
    assert main(["verify", str(path)]) == 1
    assert "ESEM001" in capsys.readouterr().err


def test_unknown_call_fails_default_compile_before_generation(
    tmp_path, capsys, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, UNKNOWN_CALL)
    assert main(["compile", str(path)]) == 1
    assert "ESEM001" in capsys.readouterr().err
    assert not (tmp_path / "probe.py").exists()


def test_tier_b_fails_strict_verify_but_warns_by_default(tmp_path, capsys):
    path = _write(tmp_path, ARG_TYPE_MISMATCH)
    assert main(["verify", "--strict", str(path)]) == 1
    assert "ESEM003" in capsys.readouterr().err

    assert main(["verify", str(path)]) == 0
    captured = capsys.readouterr()
    assert "ESEM003" in captured.err


def test_same_diagnostic_for_every_target(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, UNKNOWN_CALL)
    messages = []
    for extra in ([], ["-t", "typescript"]):
        assert main(["compile", *(extra), str(path)]) == 1
        err = capsys.readouterr().err
        line = [l for l in err.splitlines() if "ESEM001" in l][0]
        messages.append(line.strip())
    assert messages[0] == messages[1]


def test_verify_json_reports_semantic_diagnostics(tmp_path, capsys):
    path = _write(tmp_path, UNKNOWN_CALL)
    code = main(["verify", "--json", str(path)])
    payload = json.loads(capsys.readouterr().out)
    assert code == 1
    assert payload["ok"] is False
    assert "ESEM001" in [d["code"] for d in payload["diagnostics"]]


def test_valid_program_passes_strict_compile(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, VALID_PROGRAM)
    assert main(["compile", "--strict", str(path)]) == 0
    assert (tmp_path / "probe.py").exists()
