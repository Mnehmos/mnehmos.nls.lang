"""
Semantic tests for LOGIC step dataflow.

Validates Invariant #2 from core-semantics.md:
"Variables assigned in earlier LOGIC steps are available in later steps.
Emitters must preserve this dependency order."

These tests verify BEHAVIOR, not syntax.
"""
import pytest

from .runners import PythonRunner


class TestDataflowSemantics:
    """Variables must flow correctly through LOGIC steps."""

    def test_sequential_dataflow(self, runner: PythonRunner):
        """Variables assigned in step N are available in step N+1."""
        source = """\
@module test
@target python

[pipeline]
PURPOSE: Sequential pipeline
INPUTS:
  - x: number
LOGIC:
  1. a = x + 1
  2. b = a + 1
  3. c = b + 1
RETURNS: c
"""
        code = runner.compile(source)

        # If dataflow works: c = ((x + 1) + 1) + 1 = x + 3
        result = runner.execute(code, "pipeline", (10,))
        assert result.success
        assert result.return_value == 13

        result = runner.execute(code, "pipeline", (0,))
        assert result.success
        assert result.return_value == 3

    def test_dependency_chain(self, runner: PythonRunner):
        """Long dependency chains work correctly (a→b→c→d→e)."""
        source = """\
@module test
@target python

[chain]
PURPOSE: Long dependency chain
INPUTS:
  - x: number
LOGIC:
  1. a = x * 2
  2. b = a * 2
  3. c = b * 2
  4. d = c * 2
  5. e = d * 2
RETURNS: e
"""
        code = runner.compile(source)

        # e = x * 2^5 = x * 32
        result = runner.execute(code, "chain", (1,))
        assert result.success
        assert result.return_value == 32

        result = runner.execute(code, "chain", (3,))
        assert result.success
        assert result.return_value == 96  # 3 * 32

    def test_parallel_independent_steps(self, runner: PythonRunner):
        """Independent steps produce correct results."""
        source = """\
@module test
@target python

[independent]
PURPOSE: Two independent computations
INPUTS:
  - x: number
  - y: number
LOGIC:
  1. a = x * 2
  2. b = y * 3
  3. result = a + b
RETURNS: result
"""
        code = runner.compile(source)

        # a=4, b=9, result=13
        result = runner.execute(code, "independent", (2, 3))
        assert result.success
        assert result.return_value == 13

        # a=10, b=15, result=25
        result = runner.execute(code, "independent", (5, 5))
        assert result.success
        assert result.return_value == 25

    def test_variable_reuse_from_earlier_step(self, runner: PythonRunner):
        """Variables from step 1 can be used in step 3 (skip step 2)."""
        source = """\
@module test
@target python

[skip-use]
PURPOSE: Use variable from non-adjacent step
INPUTS:
  - x: number
LOGIC:
  1. first = x + 10
  2. second = x * 2
  3. result = first + second
RETURNS: result
"""
        code = runner.compile(source)

        # first=15, second=10, result=25
        result = runner.execute(code, "skip_use", (5,))
        assert result.success
        assert result.return_value == 25

    def test_input_available_in_all_steps(self, runner: PythonRunner):
        """Function inputs are available in all LOGIC steps."""
        source = """\
@module test
@target python

[use-input-everywhere]
PURPOSE: Use input in multiple steps
INPUTS:
  - base: number
LOGIC:
  1. step1 = base + 1
  2. step2 = base + 2
  3. step3 = base + 3
  4. total = step1 + step2 + step3
RETURNS: total
"""
        code = runner.compile(source)

        # base=10: step1=11, step2=12, step3=13, total=36
        result = runner.execute(code, "use_input_everywhere", (10,))
        assert result.success
        assert result.return_value == 36

    def test_complex_dataflow_graph(self, runner: PythonRunner):
        """Complex dataflow with multiple dependencies works correctly."""
        source = """\
@module test
@target python

[complex]
PURPOSE: Complex dataflow
INPUTS:
  - a: number
  - b: number
LOGIC:
  1. sum = a + b
  2. diff = a - b
  3. product = a * b
  4. combined = sum + diff + product
RETURNS: combined
"""
        code = runner.compile(source)

        # a=5, b=3: sum=8, diff=2, product=15, combined=25
        result = runner.execute(code, "complex", (5, 3))
        assert result.success
        assert result.return_value == 25

    def test_dataflow_with_conditional(self, runner: PythonRunner):
        """Dataflow works with conditional logic steps."""
        source = """\
@module test
@target python

[conditional-flow]
PURPOSE: Conditional dataflow
INPUTS:
  - x: number
LOGIC:
  1. base = x * 10
  2. IF x > 0 THEN result = base + 1
  3. IF x <= 0 THEN result = base - 1
RETURNS: result
"""
        code = runner.compile(source)

        # x=5: base=50, result=51 (positive branch)
        result = runner.execute(code, "conditional_flow", (5,))
        assert result.success
        assert result.return_value == 51

        # x=-2: base=-20, result=-21 (negative branch)
        result = runner.execute(code, "conditional_flow", (-2,))
        assert result.success
        assert result.return_value == -21
