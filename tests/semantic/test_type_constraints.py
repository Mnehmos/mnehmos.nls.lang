"""
Semantic tests for type constraint enforcement.

Validates Invariant #3 from core-semantics.md:
"Field constraints (required, min:, max:) are enforced at construction time.
Objects with invariants are always valid after construction."

These tests verify BEHAVIOR, not syntax.
"""
import pytest

from .runners import PythonRunner


class TestTypeConstraintSemantics:
    """Type constraints must be enforced at construction time."""

    def test_min_constraint_enforced(self, runner: PythonRunner):
        """min: constraint rejects values below threshold."""
        source = """\
@module test
@target python

@type Order {
  quantity: number, min: 1
}
"""
        code = runner.compile(source)

        # Valid: quantity >= 1
        result = runner.create_instance(code, "Order", {"quantity": 5})
        assert result.success
        assert result.return_value.quantity == 5

        result = runner.create_instance(code, "Order", {"quantity": 1})
        assert result.success

        # Invalid: quantity < 1
        result = runner.create_instance(code, "Order", {"quantity": 0})
        assert not result.success
        assert result.exception_type == "ValueError"

        result = runner.create_instance(code, "Order", {"quantity": -5})
        assert not result.success

    def test_max_constraint_enforced(self, runner: PythonRunner):
        """max: constraint rejects values above threshold."""
        source = """\
@module test
@target python

@type Percentage {
  value: number, max: 100
}
"""
        code = runner.compile(source)

        # Valid: value <= 100
        result = runner.create_instance(code, "Percentage", {"value": 50})
        assert result.success

        result = runner.create_instance(code, "Percentage", {"value": 100})
        assert result.success

        # Invalid: value > 100
        result = runner.create_instance(code, "Percentage", {"value": 101})
        assert not result.success
        assert result.exception_type == "ValueError"

    def test_required_constraint_enforced(self, runner: PythonRunner):
        """required constraint rejects empty/None values."""
        source = """\
@module test
@target python

@type User {
  name: string, required
}
"""
        code = runner.compile(source)

        # Valid: non-empty string
        result = runner.create_instance(code, "User", {"name": "Alice"})
        assert result.success
        assert result.return_value.name == "Alice"

        # Invalid: empty string
        result = runner.create_instance(code, "User", {"name": ""})
        assert not result.success
        assert result.exception_type == "ValueError"

    def test_positive_constraint_enforced(self, runner: PythonRunner):
        """positive constraint rejects zero and negative values."""
        source = """\
@module test
@target python

@type Price {
  amount: number, positive
}
"""
        code = runner.compile(source)

        # Valid: positive
        result = runner.create_instance(code, "Price", {"amount": 10.50})
        assert result.success

        # Invalid: zero
        result = runner.create_instance(code, "Price", {"amount": 0})
        assert not result.success

        # Invalid: negative
        result = runner.create_instance(code, "Price", {"amount": -5})
        assert not result.success

    def test_non_negative_constraint_enforced(self, runner: PythonRunner):
        """non-negative constraint allows zero but rejects negative."""
        source = """\
@module test
@target python

@type Balance {
  value: number, non-negative
}
"""
        code = runner.compile(source)

        # Valid: positive
        result = runner.create_instance(code, "Balance", {"value": 100})
        assert result.success

        # Valid: zero
        result = runner.create_instance(code, "Balance", {"value": 0})
        assert result.success

        # Invalid: negative
        result = runner.create_instance(code, "Balance", {"value": -1})
        assert not result.success

    def test_multiple_constraints(self, runner: PythonRunner):
        """Multiple constraints on same field are all enforced."""
        source = """\
@module test
@target python

@type Rating {
  score: number, min: 1, max: 5
}
"""
        code = runner.compile(source)

        # Valid: 1 <= score <= 5
        for score in [1, 2, 3, 4, 5]:
            result = runner.create_instance(code, "Rating", {"score": score})
            assert result.success, f"score={score} should be valid"

        # Invalid: below min
        result = runner.create_instance(code, "Rating", {"score": 0})
        assert not result.success

        # Invalid: above max
        result = runner.create_instance(code, "Rating", {"score": 6})
        assert not result.success

    def test_invariant_enforced_at_construction(self, runner: PythonRunner):
        """@invariant conditions are checked when object is created."""
        source = """\
@module test
@target python

@type Account {
  balance: number
}

@invariant Account {
  balance >= 0
}
"""
        code = runner.compile(source)

        # Valid: satisfies invariant
        result = runner.create_instance(code, "Account", {"balance": 100})
        assert result.success
        assert result.return_value.balance == 100

        result = runner.create_instance(code, "Account", {"balance": 0})
        assert result.success

        # Invalid: violates invariant
        result = runner.create_instance(code, "Account", {"balance": -50})
        assert not result.success
        assert "Invariant violated" in result.exception_message

    def test_multiple_invariants(self, runner: PythonRunner):
        """Multiple @invariant conditions are all enforced."""
        source = """\
@module test
@target python

@type Range {
  low: number
  high: number
}

@invariant Range {
  low >= 0
  high >= low
}
"""
        code = runner.compile(source)

        # Valid: both invariants satisfied
        result = runner.create_instance(code, "Range", {"low": 5, "high": 10})
        assert result.success

        # Invalid: low < 0
        result = runner.create_instance(code, "Range", {"low": -1, "high": 10})
        assert not result.success
        assert "Invariant violated" in result.exception_message

        # Invalid: high < low
        result = runner.create_instance(code, "Range", {"low": 10, "high": 5})
        assert not result.success
        assert "Invariant violated" in result.exception_message

    def test_constraints_with_multiple_fields(self, runner: PythonRunner):
        """Types with multiple constrained fields validate all fields."""
        source = """\
@module test
@target python

@type LineItem {
  description: string, required
  quantity: number, min: 1
  unit_price: number, non-negative
}
"""
        code = runner.compile(source)

        # Valid: all constraints satisfied
        result = runner.create_instance(
            code, "LineItem",
            {"description": "Widget", "quantity": 2, "unit_price": 9.99}
        )
        assert result.success

        # Invalid: empty description
        result = runner.create_instance(
            code, "LineItem",
            {"description": "", "quantity": 2, "unit_price": 9.99}
        )
        assert not result.success

        # Invalid: quantity < 1
        result = runner.create_instance(
            code, "LineItem",
            {"description": "Widget", "quantity": 0, "unit_price": 9.99}
        )
        assert not result.success

        # Invalid: negative price
        result = runner.create_instance(
            code, "LineItem",
            {"description": "Widget", "quantity": 2, "unit_price": -1}
        )
        assert not result.success
