"""Tests for nlsc atomize command - Issue #12"""

import pytest
from pathlib import Path
from argparse import Namespace

from nlsc.atomize import atomize_python_file, extract_anlu_from_function
from nlsc.cli import cmd_atomize


class TestAtomizePythonFunction:
    """Tests for extracting ANLU from Python function"""

    def test_extract_simple_function(self):
        """Extract ANLU from simple typed function"""
        code = '''\
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b
'''
        anlus, _ = atomize_python_file(code)

        assert len(anlus) == 1
        anlu = anlus[0]
        assert anlu["identifier"] == "add"
        assert anlu["purpose"] == "Add two numbers"
        assert len(anlu["inputs"]) == 2
        assert anlu["inputs"][0]["name"] == "a"
        assert anlu["inputs"][0]["type"] == "number"
        assert anlu["returns"] == "a + b"

    def test_extract_function_with_type_hints(self):
        """Extract proper type mapping from Python types"""
        code = '''\
def validate(name: str, count: int, ratio: float, active: bool) -> bool:
    """Validate input data"""
    return True
'''
        anlus, _ = atomize_python_file(code)

        assert len(anlus) == 1
        inputs = anlus[0]["inputs"]
        assert inputs[0]["type"] == "string"  # str -> string
        assert inputs[1]["type"] == "number"  # int -> number
        assert inputs[2]["type"] == "number"  # float -> number
        assert inputs[3]["type"] == "boolean"  # bool -> boolean

    def test_extract_function_no_docstring(self):
        """Handle function without docstring"""
        code = '''\
def multiply(x: float, y: float) -> float:
    return x * y
'''
        anlus, _ = atomize_python_file(code)

        assert len(anlus) == 1
        # Should generate purpose from function name
        assert "multiply" in anlus[0]["purpose"].lower()

    def test_extract_multiple_functions(self):
        """Extract multiple functions from file"""
        code = '''\
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract b from a"""
    return a - b
'''
        anlus, _ = atomize_python_file(code)

        assert len(anlus) == 2
        assert anlus[0]["identifier"] == "add"
        assert anlus[1]["identifier"] == "subtract"


class TestAtomizeToNL:
    """Tests for generating .nl content from Python"""

    def test_generate_nl_content(self):
        """Generate valid .nl content"""
        from nlsc.atomize import atomize_to_nl

        code = '''\
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b
'''
        nl_content = atomize_to_nl(code, module_name="calculator")

        assert "@module calculator" in nl_content
        assert "@target python" in nl_content
        assert "[add]" in nl_content
        assert "PURPOSE: Add two numbers" in nl_content
        assert "- a: number" in nl_content
        assert "- b: number" in nl_content
        assert "RETURNS: a + b" in nl_content


class TestAtomizeCommand:
    """Tests for nlsc atomize CLI command"""

    def test_cmd_atomize_exists(self):
        """cmd_atomize function should exist"""
        assert callable(cmd_atomize)

    def test_cmd_atomize_generates_nl_file(self, tmp_path):
        """nlsc atomize should generate .nl file"""
        py_file = tmp_path / "calculator.py"
        py_file.write_text('''\
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b
''')

        args = Namespace(file=str(py_file), output=None, module=None)
        result = cmd_atomize(args)

        assert result == 0
        nl_file = tmp_path / "calculator.nl"
        assert nl_file.exists()

        content = nl_file.read_text()
        assert "[add]" in content

    def test_cmd_atomize_file_not_found(self):
        """nlsc atomize should error on missing file"""
        args = Namespace(file="nonexistent.py", output=None, module=None)
        result = cmd_atomize(args)

        assert result == 1


class TestEdgeCases:
    """Tests for edge cases in atomization"""

    def test_skip_private_functions(self):
        """Skip functions starting with underscore"""
        code = '''\
def _private(x: int) -> int:
    """Private helper"""
    return x

def public(x: int) -> int:
    """Public function"""
    return x * 2
'''
        anlus, _ = atomize_python_file(code)

        assert len(anlus) == 1
        assert anlus[0]["identifier"] == "public"

    def test_handle_no_return_annotation(self):
        """Handle function without return annotation"""
        code = '''\
def process(data: str):
    """Process some data"""
    return data.upper()
'''
        anlus, _ = atomize_python_file(code)

        assert len(anlus) == 1
        # Should infer or default
        assert "returns" in anlus[0]

    def test_handle_list_type(self):
        """Handle list type annotations"""
        code = '''\
def sum_all(values: list[float]) -> float:
    """Sum all values"""
    return sum(values)
'''
        anlus, _ = atomize_python_file(code)

        assert len(anlus) == 1
        assert anlus[0]["inputs"][0]["type"] == "list of number"

    def test_convert_snake_to_kebab(self):
        """Convert snake_case to kebab-case for identifiers"""
        code = '''\
def process_data(input_value: str) -> str:
    """Process the data"""
    return input_value
'''
        anlus, _ = atomize_python_file(code)

        assert anlus[0]["identifier"] == "process-data"
