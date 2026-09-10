"""Cross-target semantic conformance (Issue #202).

The divergence table from the audit, now pinned as behavior on BOTH
targets: values, normalized failures, and error identities must match.
"""

from __future__ import annotations

import pytest

from .runners import PythonRunner, TypeScriptRunner, node_available


@pytest.fixture(params=["python", "typescript"])
def conformance_runner(request):
    if request.param == "typescript":
        if not node_available():
            pytest.skip("Node.js runtime not available")
        return TypeScriptRunner()
    return PythonRunner()


def test_quoted_operator_text_survives_both_targets(conformance_runner):
    """The audit's `"True and False"` case: the literal is returned verbatim."""
    source = """@module literal_probe
[answer]
PURPOSE: Return quoted text
LOGIC:
  1. x = "True and False"
RETURNS: x
"""
    code = conformance_runner.compile(source)
    result = conformance_runner.execute(code, "answer", ())
    assert result.success
    assert result.return_value == "True and False"


def test_list_equality_is_structural_on_both_targets(conformance_runner):
    """Distinct lists with equal contents compare equal."""
    source = """@module list_eq
[compare]
PURPOSE: structural equality
LOGIC:
  1. a = [1]
  2. b = [1]
RETURNS: a == b
"""
    code = conformance_runner.compile(source)
    result = conformance_runner.execute(code, "compare", ())
    assert result.success
    assert result.return_value is True


def test_division_by_zero_is_a_typed_failure_on_both_targets(conformance_runner):
    source = """@module div_zero
[ratio]
PURPOSE: divide
INPUTS:
  - a: number
  - b: number
RETURNS: a / b
"""
    code = conformance_runner.compile(source)
    result = conformance_runner.execute(code, "ratio", (1, 0))
    assert not result.success
    assert result.exception_type == "ZeroDivisionError"
    assert "division by zero" in (result.exception_message or "")


def test_empty_list_truthiness_matches_on_both_targets(conformance_runner):
    """`1 if items else 0` with items=[] is 0 — empty lists are falsy."""
    source = """@module truthy
[has-items]
PURPOSE: NLS truthiness for lists
INPUTS:
  - items: list of number
RETURNS: 1 if items else 0
"""
    code = conformance_runner.compile(source)
    result = conformance_runner.execute(code, "has_items", ([],))
    assert result.success
    assert result.return_value == 0
    result = conformance_runner.execute(code, "has_items", ([7],))
    assert result.success
    assert result.return_value == 1


def test_guard_failure_identity_matches_on_both_targets(conformance_runner):
    source = """@module guarded
[divide]
PURPOSE: safe divide
INPUTS:
  - numerator: number
  - divisor: number
GUARDS:
  - divisor != 0 -> ValueError("Cannot divide by zero")
RETURNS: numerator / divisor
"""
    code = conformance_runner.compile(source)
    ok = conformance_runner.execute(code, "divide", (6, 3))
    assert ok.success
    assert ok.return_value == 2

    failure = conformance_runner.execute(code, "divide", (1, 0))
    assert not failure.success
    assert failure.exception_type == "ValueError"
    assert failure.exception_message == "Cannot divide by zero"


def test_modulo_by_zero_matches_on_both_targets(conformance_runner):
    source = """@module mod_zero
[rem]
PURPOSE: modulo
INPUTS:
  - a: number
  - b: number
RETURNS: a % b
"""
    code = conformance_runner.compile(source)
    result = conformance_runner.execute(code, "rem", (1, 0))
    assert not result.success
    assert result.exception_type == "ZeroDivisionError"


def test_negative_modulo_sign_matches(conformance_runner):
    source = """@module mod_sign
[rem]
PURPOSE: python-sign modulo
INPUTS:
  - a: number
  - b: number
RETURNS: a % b
"""
    code = conformance_runner.compile(source)
    result = conformance_runner.execute(code, "rem", (-1, 3))
    assert result.success
    assert result.return_value == 2


def test_len_sum_max_builtins_match(conformance_runner):
    source = """@module builtins_probe
[stats]
PURPOSE: builtin parity
INPUTS:
  - items: list of number
RETURNS: len(items) + sum(items) + max(items)
"""
    code = conformance_runner.compile(source)
    result = conformance_runner.execute(code, "stats", ([1, 2, 3],))
    assert result.success
    assert result.return_value == 12  # len(3) + sum(6) + max(3)


def test_string_methods_match(conformance_runner):
    source = """@module strings_probe
[shout]
PURPOSE: uppercase and trim
INPUTS:
  - text: string
RETURNS: text.strip().upper()
"""
    code = conformance_runner.compile(source)
    result = conformance_runner.execute(code, "shout", ("  hello  ",))
    assert result.success
    assert result.return_value == "HELLO"


def test_typescript_output_passes_strict_compilation():
    if not node_available():
        pytest.skip("Node.js runtime not available")
    runner = TypeScriptRunner()
    code = runner.compile(
        """@module strict_probe
[compare]
PURPOSE: structural equality
LOGIC:
  1. a = [1]
  2. b = [1]
RETURNS: a == b
"""
    )
    ok, diagnostics = runner.strict_check(code)
    assert ok, diagnostics
