"""
Semantic tests for property-based specifications.

Validates Invariant #5 from core-semantics.md:
"@property assertions hold for all valid inputs. Emitters should generate
property-based tests (using Hypothesis, fast-check, etc.)."

These tests verify BEHAVIOR, not syntax.
"""
import pytest
from hypothesis import given, strategies as st, settings

from .runners import PythonRunner


class TestPropertySemantics:
    """@property assertions must hold universally.

    Note: Hypothesis tests create their own PythonRunner instances
    because @given parametrizes the test arguments.
    """

    @given(
        a=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6),
        b=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6),
    )
    @settings(max_examples=100)
    def test_addition_commutativity(self, a: float, b: float):
        """Commutativity property: add(a, b) == add(b, a)"""
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
        runner = PythonRunner()
        code = runner.compile(source)

        result1 = runner.execute(code, "add", (a, b))
        result2 = runner.execute(code, "add", (b, a))

        assert result1.success and result2.success
        assert result1.return_value == result2.return_value

    @given(x=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6))
    @settings(max_examples=100)
    def test_addition_identity(self, x: float):
        """Identity property: add(x, 0) == x"""
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
        runner = PythonRunner()
        code = runner.compile(source)

        result = runner.execute(code, "add", (x, 0))
        assert result.success
        assert result.return_value == x

    @given(x=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6))
    @settings(max_examples=100)
    def test_multiplication_identity(self, x: float):
        """Identity property: multiply(x, 1) == x"""
        source = """\
@module test
@target python

[multiply]
PURPOSE: Multiply two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a * b
"""
        runner = PythonRunner()
        code = runner.compile(source)

        result = runner.execute(code, "multiply", (x, 1))
        assert result.success
        assert result.return_value == x

    @given(x=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6))
    @settings(max_examples=100)
    def test_multiplication_zero(self, x: float):
        """Zero property: multiply(x, 0) == 0"""
        source = """\
@module test
@target python

[multiply]
PURPOSE: Multiply two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a * b
"""
        runner = PythonRunner()
        code = runner.compile(source)

        result = runner.execute(code, "multiply", (x, 0))
        assert result.success
        assert result.return_value == 0

    @given(x=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6))
    @settings(max_examples=100)
    def test_double_inverse(self, x: float):
        """Inverse property: negate(negate(x)) == x"""
        source = """\
@module test
@target python

[negate]
PURPOSE: Negate a number
INPUTS:
  - x: number
RETURNS: -x
"""
        runner = PythonRunner()
        code = runner.compile(source)

        # First negation
        result1 = runner.execute(code, "negate", (x,))
        assert result1.success

        # Second negation (should return to original)
        result2 = runner.execute(code, "negate", (result1.return_value,))
        assert result2.success
        assert result2.return_value == x

    @given(
        x=st.floats(allow_nan=False, allow_infinity=False, min_value=0.01, max_value=1e6),
    )
    @settings(max_examples=100)
    def test_guard_preserves_property(self, x: float):
        """Guarded functions preserve properties for valid inputs."""
        source = """\
@module test
@target python

[safe-sqrt]
PURPOSE: Square root with guard
INPUTS:
  - x: number
GUARDS:
  - x >= 0 -> ValueError("Cannot sqrt negative")
RETURNS: x ** 0.5
"""
        runner = PythonRunner()
        code = runner.compile(source)

        result = runner.execute(code, "safe_sqrt", (x,))
        assert result.success

        # Property: sqrt(x) * sqrt(x) ≈ x
        sqrt_x = result.return_value
        assert abs(sqrt_x * sqrt_x - x) < 1e-9 or abs((sqrt_x * sqrt_x - x) / x) < 1e-9

    @given(
        discount=st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
    )
    @settings(max_examples=100)
    def test_discount_property(self, discount: float):
        """Property: 0% discount returns original, 100% returns 0."""
        source = """\
@module test
@target python

[apply-discount]
PURPOSE: Apply discount percentage
INPUTS:
  - amount: number
  - discount_percent: number
GUARDS:
  - discount_percent >= 0 -> ValueError("Discount cannot be negative")
  - discount_percent <= 100 -> ValueError("Discount cannot exceed 100")
LOGIC:
  1. reduction = amount * (discount_percent / 100)
  2. result = amount - reduction
RETURNS: result
"""
        runner = PythonRunner()
        code = runner.compile(source)

        # Test with fixed amount
        amount = 100.0
        result = runner.execute(code, "apply_discount", (amount, discount))
        assert result.success

        # Property: result should be between 0 and amount
        assert 0 <= result.return_value <= amount

        # Property: 0% discount returns original
        if discount == 0:
            assert result.return_value == amount

        # Property: 100% discount returns 0
        if discount == 100:
            assert result.return_value == 0
