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
        # @imports uses regular imports for stdlib, relative for custom modules
        assert "import datetime" in code
        assert "import json" in code


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
