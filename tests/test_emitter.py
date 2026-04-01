"""Tests for the NLS emitter"""

import pytest

from nlsc.parser import parse_nl_file
from nlsc.emitter import emit_python, emit_anlu, _is_safe_numeric, _is_valid_return_expr


class TestEmitMath:
    """Tests for emitting the math example"""
    
    @pytest.fixture
    def math_nl(self):
        source = """\
@module math
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  • a: number
  • b: number
RETURNS: a + b

[multiply]
PURPOSE: Multiply two numbers
INPUTS:
  • a: number
  • b: number
RETURNS: a × b
"""
        return parse_nl_file(source, source_path="math.nl")
    
    def test_emit_generates_valid_python(self, math_nl):
        code = emit_python(math_nl)
        # Should be valid Python - try to compile it
        compile(code, "<string>", "exec")
    
    def test_emit_add_function(self, math_nl):
        code = emit_python(math_nl)
        assert "def add(a: float, b: float) -> float:" in code
    
    def test_emit_multiply_function(self, math_nl):
        code = emit_python(math_nl)
        assert "def multiply(a: float, b: float) -> float:" in code
    
    def test_emit_return_statements(self, math_nl):
        code = emit_python(math_nl)
        assert "return a + b" in code
        assert "return a * b" in code  # × should be converted to *
    
    def test_emit_docstrings(self, math_nl):
        code = emit_python(math_nl)
        assert "Add two numbers" in code
        assert "Multiply two numbers" in code
    
    def test_emitted_code_executes(self, math_nl):
        code = emit_python(math_nl)
        
        # Execute the generated code
        namespace = {}
        exec(code, namespace)
        
        # Test the functions work
        assert namespace["add"](2, 3) == 5
        assert namespace["add"](-1, 1) == 0
        assert namespace["multiply"](4, 5) == 20


class TestEmitSignatures:
    """Tests for function signature generation"""
    
    def test_number_to_float(self):
        source = """\
@module test
@target python

[func]
PURPOSE: Test
INPUTS:
  • x: number
RETURNS: number
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        assert "x: float" in code
        assert "-> float:" in code
    
    def test_string_type(self):
        source = """\
@module test
@target python

[func]
PURPOSE: Test
INPUTS:
  • name: string
RETURNS: string
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        assert "name: str" in code
    
    def test_list_type(self):
        source = """\
@module test
@target python

[func]
PURPOSE: Test
INPUTS:
  • items: list of number
RETURNS: number
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        assert "items: list[float]" in code


class TestEmitModule:
    """Tests for module-level emission"""
    
    def test_module_docstring(self):
        source = """\
@module mymodule
@target python

[func]
PURPOSE: Test
RETURNS: void
"""
        nl_file = parse_nl_file(source, source_path="mymodule.nl")
        code = emit_python(nl_file)
        assert "Module: mymodule" in code
    
    def test_imports(self):
        source = """\
@module test
@target python
@imports datetime, json

[func]
PURPOSE: Test
RETURNS: void
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        # @imports uses regular imports for stdlib modules
        assert "import datetime" in code
        assert "import json" in code

    def test_custom_imports_support_module_and_symbol_access(self):
        source = """\
@module test
@target python
@imports helper

[func]
PURPOSE: Test
RETURNS: helper.value()
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        assert "import helper" in code
        assert "from helper import *" in code


class TestSecurityValidation:
    """Tests for security validation in code generation"""

    def test_is_safe_numeric_integers(self):
        assert _is_safe_numeric("0") is True
        assert _is_safe_numeric("42") is True
        assert _is_safe_numeric("-1") is True
        assert _is_safe_numeric("999999") is True

    def test_is_safe_numeric_floats(self):
        assert _is_safe_numeric("3.14") is True
        assert _is_safe_numeric("-0.5") is True
        assert _is_safe_numeric("1e10") is True

    def test_is_safe_numeric_rejects_code(self):
        assert _is_safe_numeric("0; import os") is False
        assert _is_safe_numeric("__import__('os')") is False
        assert _is_safe_numeric("exec('bad')") is False
        assert _is_safe_numeric("1 + 1") is False

    def test_is_safe_numeric_rejects_special_values(self):
        """Reject infinity and NaN which could cause unexpected behavior"""
        assert _is_safe_numeric("inf") is False
        assert _is_safe_numeric("-inf") is False
        assert _is_safe_numeric("nan") is False
        assert _is_safe_numeric("Infinity") is False

    def test_malicious_constraint_not_emitted(self):
        """Ensure malicious min/max constraints are silently skipped"""
        source = """\
@module test
@target python

@type BadType {
    value: number, min: 0; import os
}
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        # The malicious constraint should NOT appear in output
        assert "import os" not in code
        assert "__import__" not in code


class TestValidReturnExpr:
    """Tests for _is_valid_return_expr - validates return expressions"""

    @pytest.mark.parametrize("expr", [
        "a + b",
        "(a + b) / 2",
        "x",
        "result",
        "123",
        "3.14",
        "task.status.value",
        "len(items)",
        'task.status.value in ["pending", "in_progress"]',
        "1 if x > 0 else 0",
        "(estimate.optimistic + 4 * estimate.realistic + estimate.pessimistic) / 6",
        "TimeEstimate(opt, real, pess)",
        "{}",
        "[]",
        "[x for x in items]",
        "sum(values)",
        "a == b",
        "x > 0 and y < 10",
    ])
    def test_valid_expressions(self, expr):
        assert _is_valid_return_expr(expr), f"Should be valid: {expr}"

    @pytest.mark.parametrize("expr", [
        "weight based on priority value",
        "highest priority",
        "count of matching tasks",
        "TimeEstimate with summed values",
        "user with lowest workload",
        "updated task with no assignee",
        "tasks with matching tag",
        "",
    ])
    def test_invalid_descriptive_text(self, expr):
        assert not _is_valid_return_expr(expr), f"Should be invalid: {expr}"


class TestDescriptiveReturnsEmitNotImplemented:
    """Tests that descriptive RETURNS generate NotImplementedError"""

    def test_descriptive_returns_emits_not_implemented(self):
        source = """\
@module test
@target python

[func]
PURPOSE: Test function with descriptive return
INPUTS:
  - x: number
RETURNS: calculated result based on input
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        assert "NotImplementedError" in code
        assert "TODO:" in code

    def test_valid_returns_emits_return_statement(self):
        source = """\
@module test
@target python

[func]
PURPOSE: Test function with valid return expression
INPUTS:
  - x: number
RETURNS: x * 2
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        assert "return x * 2" in code
        assert "NotImplementedError" not in code

    def test_descriptive_returns_has_any_return_type(self):
        source = """\
@module test
@target python

[func]
PURPOSE: Test function
INPUTS:
  - x: number
RETURNS: weight based on priority value
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        # Should use Any as return type, not the descriptive text
        assert "-> Any:" in code
        assert "-> weight based on priority value:" not in code


class TestRegressionFixes:
    """Regression tests for Phase 1 emitter fixes."""

    def test_guard_messages_with_apostrophes_are_escaped(self):
        source = """\
@module test
@target python

[check]
PURPOSE: Test quoted guard messages
INPUTS:
  - x: number
GUARDS:
  - x > 0 -> ValueError("can't be zero")
RETURNS: x
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        compile(code, "<string>", "exec")
        assert "raise ValueError(\"can't be zero\")" in code or 'raise ValueError("can\\\'t be zero")' in code

    def test_edge_cases_emit_early_returns(self):
        """Edge cases with Python conditions should emit as early returns."""
        source = """\
@module test
@target python

[safe-divide]
PURPOSE: Divide safely
INPUTS:
  - a: number
  - b: number
EDGE CASES:
  - b == 0 -> return 0
RETURNS: a / b
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        assert "if b == 0:" in code
        assert "return 0" in code
        # Should produce valid, runnable Python
        ns = {}
        exec(code, ns)
        assert ns["safe_divide"](10, 0) == 0
        assert ns["safe_divide"](10, 2) == 5.0

    def test_edge_cases_with_logic_steps(self):
        """Edge cases should emit before LOGIC steps."""
        source = """\
@module test
@target python

[func]
PURPOSE: Test edge cases with logic
INPUTS:
  - items: list of number
EDGE CASES:
  - len(items) < 2 -> return items
LOGIC:
  1. items[0] -> pivot
RETURNS: pivot
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        # Edge case should appear before logic
        edge_pos = code.index("if len(items) < 2:")
        pivot_pos = code.index("pivot = items[0]")
        assert edge_pos < pivot_pos

    def test_python_expr_in_logic_binding(self):
        """LOGIC steps with Python expressions and -> binding should compile."""
        source = """\
@module test
@target python

[func]
PURPOSE: Test expression bindings
INPUTS:
  - items: list of number
LOGIC:
  1. items[0] -> first
  2. len(items) -> count
RETURNS: first + count
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        assert "first = items[0]" in code
        assert "count = len(items)" in code
        # Should be runnable
        ns = {}
        exec(code, ns)
        assert ns["func"]([10, 20, 30]) == 13.0  # 10 + 3

    def test_list_comprehension_in_logic_binding(self):
        """List comprehensions in LOGIC -> binding should not be mangled."""
        source = """\
@module test
@target python

[func]
PURPOSE: Filter a list
INPUTS:
  - items: list of number
LOGIC:
  1. [x for x in items if x > 0] -> positive
RETURNS: positive
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        assert "positive = [x for x in items if x > 0]" in code
        ns = {}
        exec(code, ns)
        assert ns["func"]([-1, 2, -3, 4]) == [2, 4]

    def test_return_type_list_concatenation(self):
        """RETURNS with list-typed variable concatenation should infer list type."""
        source = """\
@module test
@target python

[func]
PURPOSE: Partition items
INPUTS:
  - items: list of number
LOGIC:
  1. [x for x in items if x < 0] -> negatives
  2. [x for x in items if x >= 0] -> positives
RETURNS: negatives + positives
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        assert "-> list[float]:" in code

    def test_quicksort_compiles_to_working_code(self):
        """Full quicksort spec should compile to executable Python."""
        source = """\
@module sorting
@target python

[quick-sort]
PURPOSE: Sort a list of numbers using the quicksort algorithm
INPUTS:
  - items: list of number
EDGE CASES:
  - len(items) < 2 -> return items
LOGIC:
  1. items[0] -> pivot
  2. [x for x in items if x < pivot] -> lesser
  3. [x for x in items if x == pivot] -> equal
  4. [x for x in items if x > pivot] -> greater
  5. [quick-sort](lesser) -> sorted_lesser
  6. [quick-sort](greater) -> sorted_greater
RETURNS: sorted_lesser + equal + sorted_greater
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        ns = {}
        exec(code, ns)
        assert ns["quick_sort"]([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]
        assert ns["quick_sort"]([]) == []
        assert ns["quick_sort"]([1]) == [1]
        assert ns["quick_sort"]([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_main_block_preserves_subtraction(self):
        source = """\
@module test
@target python

[noop]
PURPOSE: No-op
RETURNS: void

@main {
  print(a-b)
}
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)
        assert "print(a-b)" in code
        assert "print(a_b)" not in code
