"""
Semantic tests for guard evaluation ordering.

Validates Invariant #1 from core-semantics.md:
"Guards are evaluated in specification order. This is observable
when guards have side effects (e.g., logging)."

These tests verify BEHAVIOR, not syntax.
"""
import pytest

from .runners import PythonRunner


class TestGuardOrderingSemantics:
    """Guards must be evaluated in specification order."""

    def test_first_failing_guard_wins(self, runner: PythonRunner):
        """When multiple guards fail, the first one raises its error."""
        source = """\
@module test
@target python

[validate]
PURPOSE: Multiple guards test
INPUTS:
  - x: number
GUARDS:
  - x > 0 -> ValueError("Guard 1: must be positive")
  - x > 10 -> ValueError("Guard 2: must be > 10")
  - x != 5 -> ValueError("Guard 3: must not be 5")
RETURNS: x
"""
        code = runner.compile(source)

        # x = -5 fails guards 1 and 2, should get Guard 1 error
        result = runner.execute(code, "validate", (-5,))
        assert not result.success
        assert result.exception_type == "ValueError"
        assert "Guard 1" in result.exception_message

        # x = 5 passes Guard 1, fails Guards 2 and 3, should get Guard 2
        result = runner.execute(code, "validate", (5,))
        assert not result.success
        assert "Guard 2" in result.exception_message

        # x = 15 passes all guards
        result = runner.execute(code, "validate", (15,))
        assert result.success
        assert result.return_value == 15

    def test_guard_short_circuit(self, runner: PythonRunner):
        """When first guard fails, later guards are not evaluated.

        This is verified by testing that errors from later guards
        are never seen when earlier guards fail.
        """
        source = """\
@module test
@target python

[check]
PURPOSE: Guards short-circuit
INPUTS:
  - x: number
GUARDS:
  - x >= 0 -> ValueError("First: negative")
  - x != 999 -> ValueError("Second: is 999")
RETURNS: x
"""
        code = runner.compile(source)

        # x = -999 fails first guard, should NOT see second guard's error
        result = runner.execute(code, "check", (-999,))
        assert not result.success
        assert "First" in result.exception_message
        assert "Second" not in result.exception_message

    def test_all_guards_pass(self, runner: PythonRunner):
        """When all guards pass, function executes normally."""
        source = """\
@module test
@target python

[validated]
PURPOSE: All guards pass
INPUTS:
  - x: number
GUARDS:
  - x > 0 -> ValueError("must be positive")
  - x < 100 -> ValueError("must be < 100")
  - x != 50 -> ValueError("must not be 50")
RETURNS: x * 2
"""
        code = runner.compile(source)

        # 25 passes all guards
        result = runner.execute(code, "validated", (25,))
        assert result.success
        assert result.return_value == 50

    def test_guard_order_matches_specification(self, runner: PythonRunner):
        """Guard evaluation order must match the order in the .nl file."""
        source = """\
@module test
@target python

[ordered]
PURPOSE: Test guard ordering
INPUTS:
  - value: number
GUARDS:
  - value != 1 -> ValueError("Error A")
  - value != 2 -> ValueError("Error B")
  - value != 3 -> ValueError("Error C")
RETURNS: value
"""
        code = runner.compile(source)

        # value=1 fails first guard
        result = runner.execute(code, "ordered", (1,))
        assert not result.success
        assert "Error A" in result.exception_message

        # value=2 fails second guard (first passes)
        result = runner.execute(code, "ordered", (2,))
        assert not result.success
        assert "Error B" in result.exception_message

        # value=3 fails third guard (first two pass)
        result = runner.execute(code, "ordered", (3,))
        assert not result.success
        assert "Error C" in result.exception_message

        # value=4 passes all
        result = runner.execute(code, "ordered", (4,))
        assert result.success

    def test_different_error_types(self, runner: PythonRunner):
        """Different error types are preserved and raised correctly."""
        source = """\
@module test
@target python

[typed-guards]
PURPOSE: Different error types
INPUTS:
  - x: number
  - name: string
GUARDS:
  - x > 0 -> ValueError("x must be positive")
  - name -> TypeError("name required")
RETURNS: name
"""
        code = runner.compile(source)

        # First guard fails with ValueError
        result = runner.execute(code, "typed_guards", (-1, "test"))
        assert not result.success
        assert result.exception_type == "ValueError"

        # Second guard fails with TypeError (when first passes)
        result = runner.execute(code, "typed_guards", (1, ""))
        assert not result.success
        assert result.exception_type == "TypeError"
