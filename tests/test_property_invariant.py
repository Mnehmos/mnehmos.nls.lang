"""Tests for @property and @invariant specifications - Issue #30"""

import pytest

from nlsc.parser import parse_nl_file
from nlsc.schema import PropertyTest, Invariant
from nlsc.emitter import emit_python, emit_property_tests


class TestPropertyParsing:
    """Tests for @property block parsing"""

    def test_parse_property_block_basic(self):
        """Should parse basic @property block"""
        source = """\
@module math
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

@property [add] {
  add(a, b) == add(b, a)  # commutativity
  add(a, 0) == a          # identity
}
"""
        nl_file = parse_nl_file(source)
        assert len(nl_file.properties) == 1
        prop = nl_file.properties[0]
        assert prop.anlu_id == "add"
        assert len(prop.assertions) == 2

    def test_parse_property_with_forall(self):
        """Should parse @property with forall quantifier"""
        source = """\
@module math
@target python

[abs]
PURPOSE: Absolute value
INPUTS:
  - x: number
RETURNS: absolute value of x

@property [abs] {
  forall x: number -> abs(x) >= 0
  forall x: number -> abs(-x) == abs(x)
}
"""
        nl_file = parse_nl_file(source)
        prop = nl_file.properties[0]
        assert len(prop.assertions) == 2
        assert prop.assertions[0].quantifier == "forall"
        assert prop.assertions[0].variable == "x"
        assert prop.assertions[0].variable_type == "number"

    def test_parse_multiple_properties(self):
        """Should parse multiple @property blocks"""
        source = """\
@module math
@target python

[add]
PURPOSE: Add
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

[multiply]
PURPOSE: Multiply
INPUTS:
  - a: number
  - b: number
RETURNS: a * b

@property [add] {
  add(0, x) == x
}

@property [multiply] {
  multiply(1, x) == x
  multiply(0, x) == 0
}
"""
        nl_file = parse_nl_file(source)
        assert len(nl_file.properties) == 2
        assert nl_file.properties[0].anlu_id == "add"
        assert nl_file.properties[1].anlu_id == "multiply"


class TestInvariantParsing:
    """Tests for @invariant block parsing"""

    def test_parse_invariant_basic(self):
        """Should parse basic @invariant block"""
        source = """\
@module banking
@target python

@type Account {
  balance: number
  owner: string
}

@invariant Account {
  balance >= 0
  len(owner) > 0
}
"""
        nl_file = parse_nl_file(source)
        assert len(nl_file.invariants) == 1
        inv = nl_file.invariants[0]
        assert inv.type_name == "Account"
        assert len(inv.conditions) == 2
        assert "balance >= 0" in inv.conditions
        assert "len(owner) > 0" in inv.conditions

    def test_parse_invariant_with_self(self):
        """Should parse @invariant using self prefix"""
        source = """\
@module core
@target python

@type Rectangle {
  width: number
  height: number
}

@invariant Rectangle {
  self.width > 0
  self.height > 0
  self.width * self.height > 0
}
"""
        nl_file = parse_nl_file(source)
        inv = nl_file.invariants[0]
        assert len(inv.conditions) == 3


class TestPropertyEmission:
    """Tests for @property block emission to hypothesis tests"""

    def test_emit_property_generates_hypothesis(self):
        """Should generate hypothesis tests from @property"""
        source = """\
@module math
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

@property [add] {
  add(a, b) == add(b, a)
}
"""
        nl_file = parse_nl_file(source)
        test_code = emit_property_tests(nl_file)

        assert "from hypothesis import given, strategies as st" in test_code
        assert "@given" in test_code
        assert "st.floats" in test_code
        assert "def test_property_" in test_code  # Generated test names

    def test_emit_property_handles_forall(self):
        """Should emit forall as hypothesis strategies"""
        source = """\
@module math
@target python

[abs]
PURPOSE: Absolute value
INPUTS:
  - x: number
RETURNS: absolute value of x

@property [abs] {
  forall x: number -> abs(x) >= 0
}
"""
        nl_file = parse_nl_file(source)
        test_code = emit_property_tests(nl_file)

        assert "@given(x=st.floats(" in test_code


class TestInvariantEmission:
    """Tests for @invariant injection into types"""

    def test_emit_invariant_in_post_init(self):
        """Should inject invariant checks into __post_init__"""
        source = """\
@module banking
@target python

@type Account {
  balance: number
  owner: string
}

@invariant Account {
  balance >= 0
  len(owner) > 0
}
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)

        assert "def __post_init__(self):" in code
        assert "if not (self.balance >= 0):" in code
        assert 'raise ValueError("Invariant violated: balance >= 0")' in code

    def test_emit_invariant_validates_at_construction(self):
        """Invariants should be enforced when object is created"""
        source = """\
@module banking
@target python

@type Account {
  balance: number
  owner: string
}

@invariant Account {
  balance >= 0
}

[create-account]
PURPOSE: Create a new account
INPUTS:
  - owner: string
  - initial_balance: number
RETURNS: Account(balance=initial_balance, owner=owner)
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)

        # Execute and verify invariant enforcement
        namespace = {}
        exec(code, namespace)

        # Valid account should work
        account = namespace["Account"](balance=100, owner="Alice")
        assert account.balance == 100

        # Invalid account should raise ValueError
        with pytest.raises(ValueError, match="Invariant violated"):
            namespace["Account"](balance=-50, owner="Bob")


class TestIntegration:
    """Integration tests for properties and invariants together"""

    def test_full_example_banking(self):
        """Full banking example with properties and invariants"""
        source = """\
@module banking
@target python

@type Account {
  balance: number
  owner: string
}

@invariant Account {
  balance >= 0
}

[deposit]
PURPOSE: Add money to account
INPUTS:
  - account: Account
  - amount: number
GUARDS:
  - amount > 0 -> ValueError("Amount must be positive")
RETURNS: Account(balance=account.balance + amount, owner=account.owner)

@property [deposit] {
  deposit(acc, amt).balance == acc.balance + amt  # correct balance
  deposit(acc, amt).balance >= acc.balance        # balance never decreases
}
"""
        nl_file = parse_nl_file(source)

        # Should parse both invariants and properties
        assert len(nl_file.invariants) == 1
        assert len(nl_file.properties) == 1

        # Should generate valid Python
        code = emit_python(nl_file)
        compile(code, "<string>", "exec")
