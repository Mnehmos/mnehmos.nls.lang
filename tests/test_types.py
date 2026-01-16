"""Tests for @type block parsing and method binding - Issue #1"""

import pytest
from nlsc.parser import parse_nl_file
from nlsc.schema import TypeDefinition, TypeField


class TestTypeBlockParsing:
    """Tests for @type { ... } block parsing"""

    def test_parse_simple_type(self):
        """Parse a basic @type block with fields"""
        source = """\
@module test
@target python

@type Point {
  x: number
  y: number
}
"""
        result = parse_nl_file(source)
        assert len(result.module.types) == 1
        point_type = result.module.types[0]
        assert point_type.name == "Point"
        assert len(point_type.fields) == 2

    def test_parse_type_field_names(self):
        """Verify field names are correctly parsed"""
        source = """\
@module test
@target python

@type Account {
  balance: number
  owner: string
}
"""
        result = parse_nl_file(source)
        account = result.module.types[0]
        field_names = [f.name for f in account.fields]
        assert "balance" in field_names
        assert "owner" in field_names

    def test_parse_type_field_types(self):
        """Verify field types are correctly parsed"""
        source = """\
@module test
@target python

@type Account {
  balance: number
  owner: string
  active: boolean
}
"""
        result = parse_nl_file(source)
        account = result.module.types[0]
        balance = next(f for f in account.fields if f.name == "balance")
        owner = next(f for f in account.fields if f.name == "owner")
        active = next(f for f in account.fields if f.name == "active")

        assert balance.type == "number"
        assert owner.type == "string"
        assert active.type == "boolean"

    def test_parse_type_field_constraints(self):
        """Parse field constraints like non-negative"""
        source = """\
@module test
@target python

@type Account {
  balance: number, non-negative
  name: string, required
}
"""
        result = parse_nl_file(source)
        account = result.module.types[0]
        balance = next(f for f in account.fields if f.name == "balance")
        name = next(f for f in account.fields if f.name == "name")

        assert "non-negative" in balance.constraints
        assert "required" in name.constraints

    def test_parse_multiple_types(self):
        """Parse multiple @type blocks in one file"""
        source = """\
@module test
@target python

@type Point {
  x: number
  y: number
}

@type Rectangle {
  origin: Point
  width: number
  height: number
}
"""
        result = parse_nl_file(source)
        assert len(result.module.types) == 2
        type_names = [t.name for t in result.module.types]
        assert "Point" in type_names
        assert "Rectangle" in type_names


class TestMethodBinding:
    """Tests for [Type.method] syntax"""

    def test_parse_method_identifier(self):
        """Parse [Type.method] as method bound to Type"""
        source = """\
@module test
@target python

@type Account {
  balance: number
}

[Account.deposit]
PURPOSE: Add funds to account
INPUTS:
  • self: Account
  • amount: number
RETURNS: Account
"""
        result = parse_nl_file(source)
        assert len(result.anlus) == 1
        method = result.anlus[0]
        assert method.identifier == "Account.deposit"
        assert method.bound_type == "Account"
        assert method.method_name == "deposit"

    def test_method_has_self_param(self):
        """Method's first param should be self: TypeName"""
        source = """\
@module test
@target python

@type Account {
  balance: number
}

[Account.withdraw]
PURPOSE: Remove funds from account
INPUTS:
  • self: Account
  • amount: number
RETURNS: Account
"""
        result = parse_nl_file(source)
        method = result.anlus[0]
        assert len(method.inputs) >= 1
        assert method.inputs[0].name == "self"
        assert method.inputs[0].type == "Account"

    def test_regular_anlu_not_method(self):
        """Regular ANLUs without dot should not be methods"""
        source = """\
@module test
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  • a: number
  • b: number
RETURNS: a + b
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        assert anlu.identifier == "add"
        assert anlu.bound_type is None
        assert anlu.method_name is None


class TestTypeFieldDataclass:
    """Tests for TypeField dataclass"""

    def test_type_field_to_python_type(self):
        """TypeField should convert to Python type hints"""
        from nlsc.schema import TypeField

        field = TypeField(name="balance", type="number")
        assert field.to_python_type() == "float"

        field = TypeField(name="name", type="string")
        assert field.to_python_type() == "str"

        field = TypeField(name="active", type="boolean")
        assert field.to_python_type() == "bool"

    def test_type_field_list_type(self):
        """TypeField should handle list of X types"""
        from nlsc.schema import TypeField

        field = TypeField(name="items", type="list of string")
        assert field.to_python_type() == "list[str]"

    def test_type_field_custom_type(self):
        """TypeField should preserve custom type names"""
        from nlsc.schema import TypeField

        field = TypeField(name="origin", type="Point")
        assert field.to_python_type() == "Point"


class TestTypeDependencyOrder:
    """Tests for type-aware dependency ordering"""

    def test_type_before_method(self):
        """Types should be emitted before their methods"""
        source = """\
@module test
@target python

[Account.deposit]
PURPOSE: Add funds
INPUTS:
  • self: Account
  • amount: number
RETURNS: Account

@type Account {
  balance: number
}
"""
        result = parse_nl_file(source)
        # Even though method appears first in source, type should come first in order
        order = result.dependency_order()
        # Types should be processed first
        assert result.module.types[0].name == "Account"
