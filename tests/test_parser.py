"""Tests for the NLS parser"""

import pytest
from pathlib import Path

from nlsc.parser import parse_nl_file, parse_nl_path, ParseError
from nlsc.schema import ANLU, Input


class TestParseBasic:
    """Basic parsing tests"""
    
    def test_parse_module_directive(self):
        source = "@module mymodule\n@target python\n"
        result = parse_nl_file(source)
        assert result.module.name == "mymodule"
        assert result.module.target == "python"
    
    def test_parse_simple_anlu(self):
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
        assert len(result.anlus) == 1
        anlu = result.anlus[0]
        assert anlu.identifier == "add"
        assert anlu.purpose == "Add two numbers"
        assert anlu.returns == "a + b"
        assert len(anlu.inputs) == 2
    
    def test_parse_inputs(self):
        source = """\
@module test
@target python

[greet]
PURPOSE: Greet a user
INPUTS:
  • name: string
  • times: number
RETURNS: string
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        assert anlu.inputs[0].name == "name"
        assert anlu.inputs[0].type == "string"
        assert anlu.inputs[1].name == "times"
        assert anlu.inputs[1].type == "number"


class TestParseMathExample:
    """Tests for the canonical math.nl example"""
    
    @pytest.fixture
    def math_source(self):
        return """\
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

@test [add] {
  add(2, 3) == 5
  add(-1, 1) == 0
  add(0, 0) == 0
}
"""
    
    def test_parse_two_anlus(self, math_source):
        result = parse_nl_file(math_source)
        assert len(result.anlus) == 2
        
        identifiers = [a.identifier for a in result.anlus]
        assert "add" in identifiers
        assert "multiply" in identifiers
    
    def test_parse_multiply_returns(self, math_source):
        result = parse_nl_file(math_source)
        multiply = next(a for a in result.anlus if a.identifier == "multiply")
        assert multiply.returns == "a × b"
    
    def test_parse_tests(self, math_source):
        result = parse_nl_file(math_source)
        assert len(result.tests) == 1
        test_suite = result.tests[0]
        assert test_suite.anlu_id == "add"
        assert len(test_suite.cases) == 3


class TestInputParsing:
    """Tests for input parameter parsing"""
    
    def test_input_with_type(self):
        source = """\
@module test
@target python

[func]
PURPOSE: Test
INPUTS:
  • x: number
RETURNS: void
"""
        result = parse_nl_file(source)
        inp = result.anlus[0].inputs[0]
        assert inp.name == "x"
        assert inp.type == "number"
    
    def test_input_with_constraints(self):
        source = """\
@module test
@target python

[func]
PURPOSE: Test
INPUTS:
  • income: number, non-negative
RETURNS: void
"""
        result = parse_nl_file(source)
        inp = result.anlus[0].inputs[0]
        assert inp.name == "income"
        assert inp.type == "number"
        assert "non-negative" in inp.constraints
    
    def test_input_with_description(self):
        source = """\
@module test
@target python

[func]
PURPOSE: Test
INPUTS:
  • token: string, required, "The JWT to validate"
RETURNS: void
"""
        result = parse_nl_file(source)
        inp = result.anlus[0].inputs[0]
        assert inp.name == "token"
        assert inp.type == "string"
        assert inp.description == "The JWT to validate"


class TestDependencies:
    """Tests for DEPENDS parsing"""
    
    def test_parse_depends(self):
        source = """\
@module test
@target python

[base]
PURPOSE: Base function
RETURNS: void

[derived]
PURPOSE: Derived function
DEPENDS: [base]
RETURNS: void
"""
        result = parse_nl_file(source)
        derived = next(a for a in result.anlus if a.identifier == "derived")
        assert "[base]" in derived.depends


class TestParseErrors:
    """Parser error handling tests."""

    def test_unknown_anlu_section_raises(self):
        source = """\
@module test
@target python

[add]
PURPOSE: Add two numbers
PRECONDITIONS:
  - a > 0
RETURNS: a
"""
        with pytest.raises(ParseError) as exc:
            parse_nl_file(source)
        assert "Expected INPUTS, GUARDS, LOGIC, RETURNS, EDGE CASES, or DEPENDS section" in str(exc.value)
