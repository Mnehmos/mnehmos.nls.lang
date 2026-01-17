"""Tests for generating guard validation code - Issue #11"""

import pytest
from nlsc.parser import parse_nl_file
from nlsc.emitter import emit_python, emit_guards


class TestSimpleGuards:
    """Tests for basic guard emission"""

    def test_emit_simple_guard(self):
        """Generate validation for simple guard"""
        source = """\
@module test
@target python

[withdraw]
PURPOSE: Withdraw money
INPUTS:
  - amount: number
GUARDS:
  • amount > 0 → ValueError(Amount must be positive)
RETURNS: void
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        assert "if not (amount > 0):" in python
        assert "raise ValueError" in python
        assert "Amount must be positive" in python

    def test_emit_guard_with_error_code(self):
        """Generate validation with error code"""
        source = """\
@module test
@target python

[withdraw]
PURPOSE: Withdraw money
INPUTS:
  - balance: number
  - amount: number
GUARDS:
  • balance >= amount → InsufficientFunds(E002, Insufficient balance)
RETURNS: number
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        assert "if not (balance >= amount):" in python
        assert "InsufficientFunds" in python


class TestGuardFunction:
    """Tests for emit_guards function"""

    def test_emit_guards_returns_list(self):
        """emit_guards returns list of validation lines"""
        source = """\
@module test
@target python

[validate]
PURPOSE: Validate input
INPUTS:
  - x: number
GUARDS:
  • x > 0 → ValueError(Must be positive)
RETURNS: boolean
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        guard_lines = emit_guards(anlu)

        assert isinstance(guard_lines, list)
        assert len(guard_lines) > 0


class TestMultipleGuards:
    """Tests for multiple guard conditions"""

    def test_emit_multiple_guards(self):
        """Generate validation for multiple guards"""
        source = """\
@module test
@target python

[transfer]
PURPOSE: Transfer money
INPUTS:
  - from_balance: number
  - to_balance: number
  - amount: number
GUARDS:
  • amount > 0 → ValueError(Amount must be positive)
  • from_balance >= amount → ValueError(Insufficient balance)
RETURNS: number
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        # Both guards should be present
        assert "amount > 0" in python
        assert "from_balance >= amount" in python


class TestGuardOrdering:
    """Tests for guard placement in output"""

    def test_guards_before_logic(self):
        """Guards should appear before LOGIC code"""
        source = """\
@module test
@target python

[process]
PURPOSE: Process value
INPUTS:
  - x: number
GUARDS:
  • x > 0 → ValueError(Must be positive)
LOGIC:
  1. result = x * 2
RETURNS: result
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        # Guard check should come before logic
        guard_pos = python.find("if not (x > 0):")
        logic_pos = python.find("result = x * 2")
        assert guard_pos < logic_pos


class TestCustomErrorTypes:
    """Tests for custom error type handling"""

    def test_emit_value_error(self):
        """Standard ValueError emission"""
        source = """\
@module test
@target python

[validate]
PURPOSE: Validate
INPUTS:
  - x: number
GUARDS:
  • x > 0 → ValueError(Must be positive)
RETURNS: boolean
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        assert "raise ValueError('Must be positive')" in python

    def test_emit_type_error(self):
        """Standard TypeError emission"""
        source = """\
@module test
@target python

[check]
PURPOSE: Check type
INPUTS:
  - x: any
GUARDS:
  • isinstance(x, int) → TypeError(Expected integer)
RETURNS: boolean
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        assert "TypeError" in python

    def test_emit_custom_error_type(self):
        """Custom error type emission"""
        source = """\
@module test
@target python

[withdraw]
PURPOSE: Withdraw
INPUTS:
  - amount: number
GUARDS:
  • amount > 0 → InvalidAmountError(Amount invalid)
RETURNS: void
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        assert "InvalidAmountError" in python


class TestCodeValidity:
    """Tests that generated code is valid Python"""

    def test_generated_guard_compiles(self):
        """Generated guard code should compile"""
        source = """\
@module test
@target python

[validate]
PURPOSE: Validate positive
INPUTS:
  - x: number
GUARDS:
  • x > 0 → ValueError(Must be positive)
LOGIC:
  1. result = x * 2
RETURNS: result
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        # Should compile without errors
        compile(python, "<test>", "exec")

    def test_guard_raises_on_invalid(self):
        """Guard should raise exception on invalid input"""
        source = """\
@module test
@target python

[validate]
PURPOSE: Validate positive
INPUTS:
  - x: number
GUARDS:
  • x > 0 → ValueError(Must be positive)
LOGIC:
  1. result = x * 2
RETURNS: result
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        namespace = {}
        exec(python, namespace)

        # Valid input should work
        assert namespace["validate"](5.0) == 10.0

        # Invalid input should raise
        with pytest.raises(ValueError) as exc_info:
            namespace["validate"](-1.0)
        assert "Must be positive" in str(exc_info.value)

    def test_guard_allows_valid_input(self):
        """Guard should allow valid input through"""
        source = """\
@module test
@target python

[add-positive]
PURPOSE: Add positive numbers
INPUTS:
  - a: number
  - b: number
GUARDS:
  • a > 0 → ValueError(a must be positive)
  • b > 0 → ValueError(b must be positive)
LOGIC:
  1. result = a + b
RETURNS: result
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        namespace = {}
        exec(python, namespace)

        # Both positive should work
        assert namespace["add_positive"](3.0, 4.0) == 7.0

        # First negative should raise
        with pytest.raises(ValueError):
            namespace["add_positive"](-1.0, 4.0)

        # Second negative should raise
        with pytest.raises(ValueError):
            namespace["add_positive"](3.0, -1.0)


class TestEdgeCases:
    """Tests for edge cases"""

    def test_no_guards(self):
        """Function without guards should work"""
        source = """\
@module test
@target python

[add]
PURPOSE: Add numbers
INPUTS:
  - a: number
  - b: number
LOGIC:
  1. result = a + b
RETURNS: result
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        # Should not have guard checks
        assert "if not (" not in python

        # Should still work
        namespace = {}
        exec(python, namespace)
        assert namespace["add"](2.0, 3.0) == 5.0

    def test_guard_with_complex_expression(self):
        """Guard with complex boolean expression"""
        source = """\
@module test
@target python

[validate-range]
PURPOSE: Validate in range
INPUTS:
  - x: number
GUARDS:
  • x >= 0 and x <= 100 → ValueError(Must be 0-100)
RETURNS: boolean
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        assert "x >= 0 and x <= 100" in python
