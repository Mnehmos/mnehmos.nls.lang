"""
Semantic tests for test isolation.

Validates Invariant #4 from core-semantics.md:
"@test blocks execute in isolation. Each test case is independent—no shared state."

These tests verify BEHAVIOR, not syntax.
"""
import pytest

from .runners import PythonRunner


class TestIsolationSemantics:
    """Each @test case must execute in isolation."""

    def test_function_calls_are_independent(self, runner: PythonRunner):
        """Multiple calls to the same function don't share state."""
        source = """\
@module test
@target python

[pure-double]
PURPOSE: Pure function that doubles
INPUTS:
  - x: number
RETURNS: x * 2
"""
        code = runner.compile(source)

        # Each call should be independent
        result1 = runner.execute(code, "pure_double", (5,))
        result2 = runner.execute(code, "pure_double", (5,))
        result3 = runner.execute(code, "pure_double", (10,))

        assert result1.success and result1.return_value == 10
        assert result2.success and result2.return_value == 10
        assert result3.success and result3.return_value == 20

        # Order shouldn't matter
        assert result1.return_value == result2.return_value

    def test_instances_are_independent(self, runner: PythonRunner):
        """Multiple instances of the same type don't share state."""
        source = """\
@module test
@target python

@type Counter {
  value: number
}
"""
        code = runner.compile(source)

        # Create two instances
        result1 = runner.create_instance(code, "Counter", {"value": 10})
        result2 = runner.create_instance(code, "Counter", {"value": 20})

        assert result1.success
        assert result2.success

        # They should be independent
        assert result1.return_value.value == 10
        assert result2.return_value.value == 20

    def test_compiled_code_reusable(self, runner: PythonRunner):
        """Same compiled code can be executed multiple times independently."""
        source = """\
@module test
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
"""
        code = runner.compile(source)

        # Execute multiple times with same and different args
        results = [
            runner.execute(code, "add", (1, 2)),
            runner.execute(code, "add", (3, 4)),
            runner.execute(code, "add", (1, 2)),  # Same as first
            runner.execute(code, "add", (0, 0)),
        ]

        assert all(r.success for r in results)
        assert results[0].return_value == 3
        assert results[1].return_value == 7
        assert results[2].return_value == 3  # Same as first
        assert results[3].return_value == 0

        # First and third should match (same inputs)
        assert results[0].return_value == results[2].return_value

    def test_guard_failures_dont_affect_later_calls(self, runner: PythonRunner):
        """A failed guard in one call doesn't affect subsequent calls."""
        source = """\
@module test
@target python

[safe-divide]
PURPOSE: Divide with guard
INPUTS:
  - a: number
  - b: number
GUARDS:
  - b != 0 -> ValueError("Cannot divide by zero")
RETURNS: a / b
"""
        code = runner.compile(source)

        # First call fails
        result1 = runner.execute(code, "safe_divide", (10, 0))
        assert not result1.success

        # Second call should work fine
        result2 = runner.execute(code, "safe_divide", (10, 2))
        assert result2.success
        assert result2.return_value == 5

        # Third call with same failing input
        result3 = runner.execute(code, "safe_divide", (5, 0))
        assert not result3.success

        # Fourth call should still work
        result4 = runner.execute(code, "safe_divide", (20, 4))
        assert result4.success
        assert result4.return_value == 5

    def test_separate_namespaces(self, runner: PythonRunner):
        """Each execution gets a fresh namespace."""
        source = """\
@module test
@target python

[identity]
PURPOSE: Return input
INPUTS:
  - x: number
RETURNS: x
"""
        code = runner.compile(source)

        # Execute in isolation - each should get fresh namespace
        # This verifies the runner creates new namespace each time
        result1 = runner.execute(code, "identity", (42,))
        result2 = runner.execute(code, "identity", (99,))

        assert result1.success and result1.return_value == 42
        assert result2.success and result2.return_value == 99
