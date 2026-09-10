"""Issue #202 slice 3: the Python emitter renders structural expressions
from the target-neutral IR.

The regex-based ANLU-call translation truncated nested arguments
(``result = identity(max(1, 2)`` — unclosed paren, EmitterError), and the
legacy ``==`` heuristic silently turned assignments with comparisons in
the right-hand side into comments.  Both now render from the IR.
"""

from __future__ import annotations

import pytest

from nlsc.emitter import emit_python
from nlsc.parser import parse_nl_file

NESTED_CALL = """@module nested_probe
[identity]
PURPOSE: id
INPUTS:
  - x: number
RETURNS: x

[probe]
PURPOSE: probe
LOGIC:
  1. [identity](max(1, 2)) -> result
RETURNS: result
DEPENDS: [identity]
"""


def _exec(source: str) -> dict:
    code = emit_python(parse_nl_file(source))
    namespace: dict = {}
    exec(code, namespace)  # noqa: S102
    return namespace


def test_bound_nested_anlu_call_compiles_and_executes():
    namespace = _exec(NESTED_CALL)
    assert namespace["probe"]() == 2


def test_kebab_anlu_target_renders_snake_case():
    code = emit_python(
        parse_nl_file(
            """@module kebab
[slow-charge]
PURPOSE: charge
INPUTS:
  - amount: number
RETURNS: amount

[run]
PURPOSE: run
LOGIC:
  1. [slow-charge](1) -> out
RETURNS: out
DEPENDS: [slow-charge]
"""
        )
    )
    assert "out = slow_charge(1)" in code


def test_comparison_in_rhs_is_executable_not_a_comment():
    source = """@module rhs_probe
[p]
PURPOSE: p
INPUTS:
  - items: list of number
LOGIC:
  1. flag = not len(items) == 0
RETURNS: flag
"""
    namespace = _exec(source)
    assert namespace["p"]([1]) is True
    assert namespace["p"]([]) is False
    code = emit_python(parse_nl_file(source))
    assert "# flag = not len(items) == 0" not in code


def test_operator_precedence_is_preserved():
    source = """@module prec
[p]
PURPOSE: p
INPUTS:
  - items: list of number
LOGIC:
  1. total = sum(items) + max(items) * 2
RETURNS: total
"""
    namespace = _exec(source)
    # sum([1,2,3])=6 + max=3*2=6 -> 12
    assert namespace["p"]([1, 2, 3]) == 12
    code = emit_python(parse_nl_file(source))
    assert "total = sum(items) + max(items) * 2" in code


def test_constructor_kwargs_render_as_python_kwargs():
    code = emit_python(
        parse_nl_file(
            """@module kw
@type Point {
  x: number
  y: number
}

[origin]
PURPOSE: origin
LOGIC:
  1. p = Point(x=0, y=0)
RETURNS: p
"""
        )
    )
    assert "p = Point(x=0, y=0)" in code


def test_right_associativity_and_grouping():
    source = """@module assoc
[p]
PURPOSE: p
INPUTS:
  - a: number
LOGIC:
  1. x = a - (a - 1)
  2. y = (a + 1) * 2
RETURNS: x + y
"""
    namespace = _exec(source)
    # x = 1, y = (a+1)*2 with a=3 -> 8; total 9
    assert namespace["p"](3) == 9


def test_foreign_expressions_still_fall_back_to_legacy():
    source = """@module foreign_probe
[p]
PURPOSE: p
INPUTS:
  - items: list of number
LOGIC:
  1. small = [x for x in items if x < 10]
RETURNS: small
"""
    namespace = _exec(source)
    assert namespace["p"]([5, 50, 7]) == [5, 7]


def test_quoted_operator_text_unchanged_in_python():
    source = """@module quoted
[p]
PURPOSE: p
LOGIC:
  1. x = "True and False"
RETURNS: x
"""
    namespace = _exec(source)
    assert namespace["p"]() == "True and False"


def test_emitter_error_no_longer_raised_for_nested_calls():
    # Before the IR path, this raised EmitterError (unclosed paren).
    code = emit_python(parse_nl_file(NESTED_CALL))
    compile(code, "probe.py", "exec")
