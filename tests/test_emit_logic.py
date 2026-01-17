"""Tests for deterministic code generation from LOGIC steps - Issue #9"""

import pytest
from nlsc.parser import parse_nl_file
from nlsc.emitter import emit_python, emit_body_from_logic


class TestSimpleAssignments:
    """Tests for basic LOGIC step code generation"""

    def test_emit_single_assignment(self):
        """Generate code from single assignment step"""
        source = """\
@module test
@target python

[calculate-tax]
PURPOSE: Calculate tax
INPUTS:
  - income: number
  - rate: number
LOGIC:
  1. tax = income * rate
RETURNS: tax
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        body = emit_body_from_logic(anlu)

        assert "tax = income * rate" in body
        assert "return tax" in body

    def test_emit_multiple_assignments(self):
        """Generate code from multiple assignment steps"""
        source = """\
@module test
@target python

[calculate-final-tax]
PURPOSE: Calculate final tax
INPUTS:
  - income: number
  - deductions: list of number
LOGIC:
  1. base_tax = income * 0.25
  2. total_deductions = sum(deductions)
  3. final_tax = base_tax - total_deductions
RETURNS: final_tax
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        body = emit_body_from_logic(anlu)

        assert "base_tax = income * 0.25" in body
        assert "total_deductions = sum(deductions)" in body
        assert "final_tax = base_tax - total_deductions" in body
        assert "return final_tax" in body


class TestConditionals:
    """Tests for IF/THEN conditional generation"""

    def test_emit_simple_conditional(self):
        """Generate if statement from IF condition THEN"""
        source = """\
@module test
@target python

[check-positive]
PURPOSE: Check if positive
INPUTS:
  - value: number
LOGIC:
  1. IF value > 0 THEN result = True
  2. IF value <= 0 THEN result = False
RETURNS: result
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        body = emit_body_from_logic(anlu)

        assert "if value > 0:" in body
        assert "result = True" in body
        assert "if value <= 0:" in body or "else:" in body

    def test_emit_conditional_with_not(self):
        """Generate if statement with NOT condition"""
        source = """\
@module test
@target python

[validate-payment]
PURPOSE: Validate payment
INPUTS:
  - payment: Payment
LOGIC:
  1. valid = payment.amount > 0
  2. IF NOT valid THEN return Error
RETURNS: Result
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        body = emit_body_from_logic(anlu)

        assert "if not valid:" in body or "if NOT valid:" in body


class TestOutputBindings:
    """Tests for → output binding syntax"""

    def test_emit_output_binding(self):
        """Generate assignment from → binding"""
        source = """\
@module test
@target python

[pipeline]
PURPOSE: Data pipeline
INPUTS:
  - data: string
LOGIC:
  1. Validate input → valid_data
  2. Transform valid_data → result
RETURNS: result
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        body = emit_body_from_logic(anlu)

        # Output bindings should become assignments
        assert "valid_data" in body
        assert "result" in body


class TestReturnGeneration:
    """Tests for RETURNS statement generation"""

    def test_return_variable(self):
        """RETURNS variable generates return statement"""
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
        anlu = result.anlus[0]
        body = emit_body_from_logic(anlu)

        assert "return result" in body

    def test_return_expression(self):
        """RETURNS expression generates return statement"""
        source = """\
@module test
@target python

[add]
PURPOSE: Add numbers
INPUTS:
  - a: number
  - b: number
LOGIC:
  1. Calculate sum
RETURNS: a + b
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        body = emit_body_from_logic(anlu)

        assert "return a + b" in body


class TestFullEmission:
    """Tests for complete function emission"""

    def test_emit_complete_function(self):
        """Generate complete Python function"""
        source = """\
@module math_ops
@target python

[calculate-area]
PURPOSE: Calculate rectangle area
INPUTS:
  - width: number
  - height: number
LOGIC:
  1. area = width * height
RETURNS: area
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        # Should have valid Python syntax
        assert "def calculate_area(width: float, height: float) -> float:" in python
        assert "area = width * height" in python
        assert "return area" in python
        # Should NOT have NotImplementedError
        assert "NotImplementedError" not in python

    def test_emit_preserves_order(self):
        """Steps are emitted in correct order"""
        source = """\
@module test
@target python

[pipeline]
PURPOSE: Multi-step pipeline
INPUTS:
  - x: number
LOGIC:
  1. a = x + 1
  2. b = a * 2
  3. c = b - 3
RETURNS: c
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        body = emit_body_from_logic(anlu)

        # Find positions
        pos_a = body.find("a = x + 1")
        pos_b = body.find("b = a * 2")
        pos_c = body.find("c = b - 3")

        # Verify order
        assert pos_a < pos_b < pos_c


class TestEdgeCases:
    """Tests for edge cases and error handling"""

    def test_no_logic_steps(self):
        """Handle ANLU with no LOGIC steps"""
        source = """\
@module test
@target python

[simple]
PURPOSE: Simple operation
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        body = emit_body_from_logic(anlu)

        # Should still generate return
        assert "return a + b" in body

    def test_descriptive_step_without_assignment(self):
        """Handle descriptive steps (no =)"""
        source = """\
@module test
@target python

[validate]
PURPOSE: Validate input
INPUTS:
  - data: string
LOGIC:
  1. Check data is not empty
  2. result = len(data) > 0
RETURNS: result
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        body = emit_body_from_logic(anlu)

        # Descriptive step becomes comment
        assert "# Check data is not empty" in body or "Check data is not empty" in body
        # Assignment step is preserved
        assert "result = len(data) > 0" in body


class TestCodeValidity:
    """Tests that generated code is valid Python"""

    def test_generated_code_compiles(self):
        """Generated code should be valid Python"""
        source = """\
@module test
@target python

[calculate]
PURPOSE: Calculate value
INPUTS:
  - x: number
  - y: number
LOGIC:
  1. temp = x * 2
  2. result = temp + y
RETURNS: result
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        # Should compile without errors
        compile(python, "<test>", "exec")

    def test_generated_code_executes(self):
        """Generated code should execute correctly"""
        source = """\
@module test
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
LOGIC:
  1. result = a + b
RETURNS: result
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        # Execute and test
        namespace = {}
        exec(python, namespace)
        assert namespace["add"](2, 3) == 5
        assert namespace["add"](10, -5) == 5
