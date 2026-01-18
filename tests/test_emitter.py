"""Tests for the NLS emitter"""

import pytest

from nlsc.parser import parse_nl_file
from nlsc.emitter import emit_python, emit_anlu, _is_safe_numeric


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
        # @imports uses relative imports for cross-module NL imports
        assert "from .datetime import *" in code
        assert "from .json import *" in code


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
