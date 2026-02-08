"""Regression tests for Issue #120: guards must not be dropped for RETURNS-only ANLUs."""

from nlsc.emitter import emit_python
from nlsc.parser import parse_nl_file


def test_should_emit_guards_when_returns_only_function_has_simple_binary_return():
    """Guards must be emitted even when function body is only `RETURNS: a + b`."""
    source = """\
@module issue120
@target python

[safe-add]
PURPOSE: Add two numbers with validation
INPUTS:
  - a: number
  - b: number
GUARDS:
  • a > 0 -> ValueError(a must be positive)
  • b > 0 -> ValueError(b must be positive)
RETURNS: a + b
"""

    nl_file = parse_nl_file(source)
    python = emit_python(nl_file)

    guard_a = "if not (a > 0):"
    guard_b = "if not (b > 0):"
    return_stmt = "return a + b"

    assert guard_a in python, (
        "Contract violated: guards must appear before return for RETURNS-only functions; "
        "missing emitted guard for `a > 0` in generated Python."
    )
    assert guard_b in python, (
        "Contract violated: guards must appear before return for RETURNS-only functions; "
        "missing emitted guard for `b > 0` in generated Python."
    )
    assert return_stmt in python, "Expected binary RETURNS expression to be emitted as `return a + b`."

    assert python.find(guard_a) < python.find(return_stmt), (
        "Contract violated: guard checks must be emitted before return in RETURNS-only functions "
        "(a-guard appears after return)."
    )
    assert python.find(guard_b) < python.find(return_stmt), (
        "Contract violated: guard checks must be emitted before return in RETURNS-only functions "
        "(b-guard appears after return)."
    )


def test_should_emit_guards_when_returns_only_function_has_single_expression_return():
    """Guards must be emitted for RETURNS-only functions with a single-name return expression."""
    source = """\
@module issue120
@target python

[validate-score]
PURPOSE: Validate score and return it
INPUTS:
  - score: number
GUARDS:
  • score >= 0 -> ValueError(score cannot be negative)
RETURNS: score
"""

    nl_file = parse_nl_file(source)
    python = emit_python(nl_file)

    guard = "if not (score >= 0):"
    return_stmt = "return score"

    assert guard in python, (
        "Contract violated: guards must appear before return for RETURNS-only functions; "
        "missing emitted guard for `score >= 0`."
    )
    assert return_stmt in python, "Expected single-expression RETURNS to emit `return score`."
    assert python.find(guard) < python.find(return_stmt), (
        "Contract violated: guard check must be emitted before return in RETURNS-only functions."
    )
