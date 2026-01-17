"""Tests for generating dataclasses from @type blocks - Issue #10"""

import pytest
from nlsc.parser import parse_nl_file
from nlsc.emitter import emit_python, emit_type_definition


class TestSimpleTypeEmission:
    """Tests for basic @type to dataclass generation"""

    def test_emit_simple_type(self):
        """Generate dataclass from simple @type block"""
        source = """\
@module test
@target python

@type Account {
  balance: number
  owner: string
}
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        assert "@dataclass" in python
        assert "class Account:" in python
        assert "balance: float" in python
        assert "owner: str" in python

    def test_emit_type_definition_function(self):
        """emit_type_definition generates a single dataclass"""
        source = """\
@module test
@target python

@type User {
  name: string
  age: number
}
"""
        result = parse_nl_file(source)
        type_def = result.module.types[0]
        code = emit_type_definition(type_def)

        assert "@dataclass" in code
        assert "class User:" in code
        assert "name: str" in code
        assert "age: float" in code


class TestTypeConstraints:
    """Tests for constraint validation in __post_init__"""

    def test_emit_non_negative_constraint(self):
        """Generate validation for non-negative constraint"""
        source = """\
@module test
@target python

@type Account {
  balance: number, non-negative
}
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        assert "__post_init__" in python
        assert "balance" in python
        # Should check for negative
        assert "< 0" in python or ">= 0" in python

    def test_emit_required_constraint(self):
        """Generate validation for required constraint"""
        source = """\
@module test
@target python

@type User {
  name: string, required
}
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        assert "__post_init__" in python
        # Should check for empty/None
        assert "not self.name" in python or "self.name is None" in python

    def test_emit_multiple_constraints(self):
        """Generate validation for multiple constraints"""
        source = """\
@module test
@target python

@type Account {
  balance: number, non-negative
  owner: string, required
}
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        assert "__post_init__" in python
        assert "balance" in python
        assert "owner" in python


class TestListTypes:
    """Tests for list type handling"""

    def test_emit_list_of_number(self):
        """Handle list of number type"""
        source = """\
@module test
@target python

@type DataSet {
  values: list of number
}
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        assert "values: list[float]" in python

    def test_emit_list_of_string(self):
        """Handle list of string type"""
        source = """\
@module test
@target python

@type Tags {
  items: list of string
}
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        assert "items: list[str]" in python


class TestTypeInheritance:
    """Tests for type inheritance (extends)"""

    def test_emit_type_extends(self):
        """Handle type inheritance with extends"""
        source = """\
@module test
@target python

@type Entity {
  id: string
}

@type User extends Entity {
  name: string
}
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        assert "class Entity:" in python
        assert "class User(Entity):" in python


class TestTypeOrdering:
    """Tests for correct type ordering in output"""

    def test_types_before_functions(self):
        """Types should be emitted before ANLUs"""
        source = """\
@module test
@target python

@type User {
  name: string
}

[create-user]
PURPOSE: Create a user
INPUTS:
  - name: string
RETURNS: User
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        # Type should come before function
        class_pos = python.find("class User:")
        def_pos = python.find("def create_user")
        assert class_pos < def_pos


class TestDataclassImport:
    """Tests for dataclass import handling"""

    def test_dataclass_import_added(self):
        """Add dataclass import when types exist"""
        source = """\
@module test
@target python

@type User {
  name: string
}
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        assert "from dataclasses import dataclass" in python


class TestCodeValidity:
    """Tests that generated code is valid Python"""

    def test_generated_type_compiles(self):
        """Generated dataclass should compile"""
        source = """\
@module test
@target python

@type Account {
  balance: number
  owner: string
}
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        # Should compile without errors
        compile(python, "<test>", "exec")

    def test_generated_type_instantiates(self):
        """Generated dataclass should be instantiable"""
        source = """\
@module test
@target python

@type Point {
  x: number
  y: number
}
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        # Execute and test
        namespace = {}
        exec(python, namespace)
        point = namespace["Point"](x=3.0, y=4.0)
        assert point.x == 3.0
        assert point.y == 4.0

    def test_constraint_validation_works(self):
        """Constraint validation should raise on invalid data"""
        source = """\
@module test
@target python

@type Account {
  balance: number, non-negative
}
"""
        result = parse_nl_file(source)
        python = emit_python(result)

        namespace = {}
        exec(python, namespace)

        # Valid balance should work
        account = namespace["Account"](balance=100.0)
        assert account.balance == 100.0

        # Negative balance should raise
        with pytest.raises(ValueError):
            namespace["Account"](balance=-50.0)
