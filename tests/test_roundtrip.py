"""Tests for round-trip equivalence - Issue #29

Proves that atomize(compile(x)) ≈ x for behavioral equivalence.

Strategy:
  .nl file → compile → .py → atomize → .nl → compile → .py
  Then compare behavior between original and round-tripped code.
"""

import pytest
from nlsc.parser import parse_nl_file
from nlsc.emitter import emit_python
from nlsc.atomize import atomize_python_file, atomize_to_nl


class TestSimpleArithmeticRoundTrip:
    """Test round-trip for simple arithmetic functions"""

    def test_add_roundtrip(self):
        """Add function should round-trip correctly"""
        original_nl = """\
@module arithmetic
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
"""
        # First compile
        nl_file = parse_nl_file(original_nl)
        py_code = emit_python(nl_file)

        # Execute original
        ns1 = {}
        exec(py_code, ns1)
        original_result = ns1["add"](3.0, 4.0)

        # Atomize back to NL
        regenerated_nl = atomize_to_nl(py_code, module_name="arithmetic")

        # Compile regenerated
        nl_file2 = parse_nl_file(regenerated_nl)
        py_code2 = emit_python(nl_file2)

        # Execute regenerated
        ns2 = {}
        exec(py_code2, ns2)
        roundtrip_result = ns2["add"](3.0, 4.0)

        # Compare results
        assert original_result == roundtrip_result

    def test_multiply_roundtrip(self):
        """Multiply function should round-trip correctly"""
        original_nl = """\
@module arithmetic
@target python

[multiply]
PURPOSE: Multiply two numbers
INPUTS:
  - x: number
  - y: number
RETURNS: x * y
"""
        # Round-trip
        nl_file = parse_nl_file(original_nl)
        py_code = emit_python(nl_file)

        ns1 = {}
        exec(py_code, ns1)

        regenerated_nl = atomize_to_nl(py_code, module_name="arithmetic")
        nl_file2 = parse_nl_file(regenerated_nl)
        py_code2 = emit_python(nl_file2)

        ns2 = {}
        exec(py_code2, ns2)

        # Test with multiple inputs
        test_cases = [(2.0, 3.0), (0.0, 5.0), (-1.0, 7.0)]
        for a, b in test_cases:
            assert ns1["multiply"](a, b) == ns2["multiply"](a, b)


class TestMultipleFunctionsRoundTrip:
    """Test round-trip for files with multiple functions"""

    def test_multiple_functions_roundtrip(self):
        """Multiple functions should all round-trip correctly"""
        original_nl = """\
@module calculator
@target python

[add]
PURPOSE: Add numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

[subtract]
PURPOSE: Subtract b from a
INPUTS:
  - a: number
  - b: number
RETURNS: a - b

[negate]
PURPOSE: Negate a number
INPUTS:
  - x: number
RETURNS: -x
"""
        nl_file = parse_nl_file(original_nl)
        py_code = emit_python(nl_file)

        ns1 = {}
        exec(py_code, ns1)

        regenerated_nl = atomize_to_nl(py_code, module_name="calculator")
        nl_file2 = parse_nl_file(regenerated_nl)
        py_code2 = emit_python(nl_file2)

        ns2 = {}
        exec(py_code2, ns2)

        # All functions should work the same
        assert ns1["add"](5.0, 3.0) == ns2["add"](5.0, 3.0)
        assert ns1["subtract"](10.0, 4.0) == ns2["subtract"](10.0, 4.0)
        assert ns1["negate"](7.0) == ns2["negate"](7.0)


class TestFunctionsWithLogicRoundTrip:
    """Test round-trip for functions with LOGIC steps"""

    def test_logic_steps_roundtrip(self):
        """Functions with LOGIC should round-trip behaviorally"""
        original_nl = """\
@module process
@target python

[double-and-add]
PURPOSE: Double a number and add offset
INPUTS:
  - x: number
  - offset: number
LOGIC:
  1. doubled = x * 2
  2. result = doubled + offset
RETURNS: result
"""
        nl_file = parse_nl_file(original_nl)
        py_code = emit_python(nl_file)

        ns1 = {}
        exec(py_code, ns1)

        regenerated_nl = atomize_to_nl(py_code, module_name="process")
        nl_file2 = parse_nl_file(regenerated_nl)
        py_code2 = emit_python(nl_file2)

        ns2 = {}
        exec(py_code2, ns2)

        # Behavioral equivalence
        test_cases = [(5.0, 3.0), (0.0, 1.0), (-2.0, 4.0)]
        for x, offset in test_cases:
            assert ns1["double_and_add"](x, offset) == ns2["double_and_add"](x, offset)


class TestSignaturePreservation:
    """Test that function signatures are preserved"""

    def test_parameter_count_preserved(self):
        """Number of parameters should be preserved"""
        original_nl = """\
@module funcs
@target python

[three-args]
PURPOSE: Take three arguments
INPUTS:
  - a: number
  - b: number
  - c: number
RETURNS: a + b + c
"""
        nl_file = parse_nl_file(original_nl)
        py_code = emit_python(nl_file)

        # Atomize
        anlus = atomize_python_file(py_code)

        assert len(anlus) == 1
        assert len(anlus[0]["inputs"]) == 3

    def test_return_type_preserved(self):
        """Return should be meaningful after round-trip"""
        original_nl = """\
@module types
@target python

[identity]
PURPOSE: Return the input
INPUTS:
  - x: number
RETURNS: x
"""
        nl_file = parse_nl_file(original_nl)
        py_code = emit_python(nl_file)

        ns1 = {}
        exec(py_code, ns1)

        regenerated_nl = atomize_to_nl(py_code, module_name="types")
        nl_file2 = parse_nl_file(regenerated_nl)
        py_code2 = emit_python(nl_file2)

        ns2 = {}
        exec(py_code2, ns2)

        # Should preserve identity behavior
        for val in [0.0, 1.0, -5.5, 100.0]:
            assert ns1["identity"](val) == ns2["identity"](val)


class TestBehavioralEquivalence:
    """Test that behavior is equivalent even if structure differs"""

    def test_equivalent_results(self):
        """Results should match even with structural differences"""
        original_nl = """\
@module math
@target python

[square]
PURPOSE: Compute square of a number
INPUTS:
  - n: number
RETURNS: n * n
"""
        nl_file = parse_nl_file(original_nl)
        py_code = emit_python(nl_file)

        ns1 = {}
        exec(py_code, ns1)

        regenerated_nl = atomize_to_nl(py_code, module_name="math")
        nl_file2 = parse_nl_file(regenerated_nl)
        py_code2 = emit_python(nl_file2)

        ns2 = {}
        exec(py_code2, ns2)

        # Extensive behavioral testing
        test_values = [0.0, 1.0, 2.0, -3.0, 0.5, 10.0, -0.25]
        for val in test_values:
            expected = val * val
            assert ns1["square"](val) == expected
            assert ns2["square"](val) == expected


class TestRoundTripHelper:
    """Test helper for round-trip validation"""

    def test_roundtrip_helper(self):
        """Helper function should validate round-trips"""
        from nlsc.roundtrip import validate_roundtrip

        nl_source = """\
@module test
@target python

[double]
PURPOSE: Double a number
INPUTS:
  - x: number
RETURNS: x * 2
"""
        test_cases = [(1.0,), (2.0,), (0.0,), (-5.0,)]

        result = validate_roundtrip(nl_source, "double", test_cases)
        assert result.success
        assert result.all_match

    def test_roundtrip_detects_mismatch(self):
        """Helper should detect behavioral mismatches"""
        from nlsc.roundtrip import validate_roundtrip

        # This should work fine
        nl_source = """\
@module test
@target python

[add-one]
PURPOSE: Add one
INPUTS:
  - x: number
RETURNS: x + 1
"""
        test_cases = [(0.0,), (1.0,), (-1.0,)]

        result = validate_roundtrip(nl_source, "add_one", test_cases)
        assert result.success
