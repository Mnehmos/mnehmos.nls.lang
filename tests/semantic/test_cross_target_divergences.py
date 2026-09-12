"""Cross-target semantic conformance (Issue #202).

The divergence table from the audit, now pinned as behavior on BOTH
targets: values, normalized failures, and error identities must match.
"""

from __future__ import annotations

import pytest

from .runners import require_typescript_runner


def test_quoted_operator_text_survives_both_targets(runner):
    """The audit's `"True and False"` case: the literal is returned verbatim."""
    source = """@module literal_probe
[answer]
PURPOSE: Return quoted text
LOGIC:
  1. x = "True and False"
RETURNS: x
"""
    code = runner.compile(source)
    result = runner.execute(code, "answer", ())
    assert result.success
    assert result.return_value == "True and False"


def test_list_equality_is_structural_on_both_targets(runner):
    """Distinct lists with equal contents compare equal."""
    source = """@module list_eq
[compare]
PURPOSE: structural equality
LOGIC:
  1. a = [1]
  2. b = [1]
RETURNS: a == b
"""
    code = runner.compile(source)
    result = runner.execute(code, "compare", ())
    assert result.success
    assert result.return_value is True


def test_division_by_zero_is_a_typed_failure_on_both_targets(runner):
    source = """@module div_zero
[ratio]
PURPOSE: divide
INPUTS:
  - a: number
  - b: number
RETURNS: a / b
"""
    code = runner.compile(source)
    result = runner.execute(code, "ratio", (1, 0))
    assert not result.success
    assert result.exception_type == "ZeroDivisionError"
    assert "division by zero" in (result.exception_message or "")


def test_empty_list_truthiness_matches_on_both_targets(runner):
    """`1 if items else 0` with items=[] is 0 — empty lists are falsy."""
    source = """@module truthy
[has-items]
PURPOSE: NLS truthiness for lists
INPUTS:
  - items: list of number
RETURNS: 1 if items else 0
"""
    code = runner.compile(source)
    result = runner.execute(code, "has_items", ([],))
    assert result.success
    assert result.return_value == 0
    result = runner.execute(code, "has_items", ([7],))
    assert result.success
    assert result.return_value == 1


def test_guard_failure_identity_matches_on_both_targets(runner):
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
    code = runner.compile(source)
    ok = runner.execute(code, "divide", (6, 3))
    assert ok.success
    assert ok.return_value == 2

    failure = runner.execute(code, "divide", (1, 0))
    assert not failure.success
    assert failure.exception_type == "ValueError"
    assert failure.exception_message == "Cannot divide by zero"


def test_modulo_by_zero_matches_on_both_targets(runner):
    source = """@module mod_zero
[rem]
PURPOSE: modulo
INPUTS:
  - a: number
  - b: number
RETURNS: a % b
"""
    code = runner.compile(source)
    result = runner.execute(code, "rem", (1, 0))
    assert not result.success
    assert result.exception_type == "ZeroDivisionError"


def test_negative_modulo_sign_matches(runner):
    source = """@module mod_sign
[rem]
PURPOSE: python-sign modulo
INPUTS:
  - a: number
  - b: number
RETURNS: a % b
"""
    code = runner.compile(source)
    result = runner.execute(code, "rem", (-1, 3))
    assert result.success
    assert result.return_value == 2


def test_len_sum_max_builtins_match(runner):
    source = """@module builtins_probe
[stats]
PURPOSE: builtin parity
INPUTS:
  - items: list of number
RETURNS: len(items) + sum(items) + max(items)
"""
    code = runner.compile(source)
    result = runner.execute(code, "stats", ([1, 2, 3],))
    assert result.success
    assert result.return_value == 12  # len(3) + sum(6) + max(3)


def test_string_methods_match(runner):
    source = """@module strings_probe
[shout]
PURPOSE: uppercase and trim
INPUTS:
  - text: string
RETURNS: text.strip().upper()
"""
    code = runner.compile(source)
    result = runner.execute(code, "shout", ("  hello  ",))
    assert result.success
    assert result.return_value == "HELLO"


def test_typescript_output_passes_strict_compilation():
    ts_runner = require_typescript_runner()
    code = ts_runner.compile(
        """@module strict_probe
[compare]
PURPOSE: structural equality
LOGIC:
  1. a = [1]
  2. b = [1]
RETURNS: a == b
"""
    )
    ok, diagnostics = ts_runner.strict_check(code)
    assert ok, diagnostics


# --------------------------------------------------------------------------
# Harness gating: the cross-target table must not vanish from CI
# --------------------------------------------------------------------------


def test_missing_node_skips_locally(monkeypatch):
    from . import runners

    monkeypatch.setattr(runners, "node_available", lambda: False)
    monkeypatch.delenv("NLSC_REQUIRE_TS", raising=False)
    with pytest.raises(pytest.skip.Exception):
        runners.require_typescript_runner()


def test_missing_node_fails_when_required(monkeypatch):
    from . import runners

    monkeypatch.setattr(runners, "node_available", lambda: False)
    monkeypatch.setenv("NLSC_REQUIRE_TS", "1")
    with pytest.raises(pytest.fail.Exception):
        runners.require_typescript_runner()
