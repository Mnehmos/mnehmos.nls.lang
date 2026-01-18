"""Hypothesis-based property tests for NLS compiler - Issue #77

These tests verify compiler invariants using property-based testing.
"""

import keyword
import pytest
from hypothesis import given, strategies as st, assume, settings

from nlsc.parser import parse_nl_file, ParseError
from nlsc.emitter import emit_python
from nlsc.schema import Input, TypeField

# Python keywords and builtins to avoid in generated identifiers
PYTHON_RESERVED = set(keyword.kwlist) | {"True", "False", "None"}


# --- Strategies for NLS constructs ---

# Valid NLS identifiers: start with letter, contain alphanumeric + hyphen
nls_identifier = st.from_regex(r"[a-z][a-z0-9-]{0,20}", fullmatch=True)

# Valid type names: PascalCase
type_name = st.from_regex(r"[A-Z][a-zA-Z0-9]{0,15}", fullmatch=True)

# Safe numbers for testing
safe_numbers = st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False)


class TestParserProperties:
    """Property-based tests for the parser"""

    @given(name=nls_identifier)
    @settings(max_examples=50)
    def test_valid_identifier_always_parses(self, name):
        """Any valid NLS identifier should parse successfully"""
        source = f"""\
@module test
@target python

[{name}]
PURPOSE: Test function
RETURNS: void
"""
        nl_file = parse_nl_file(source)
        assert len(nl_file.anlus) == 1
        assert nl_file.anlus[0].identifier == name

    @given(name=type_name)
    @settings(max_examples=50)
    def test_valid_type_name_always_parses(self, name):
        """Any valid PascalCase type name should parse"""
        source = f"""\
@module test
@target python

@type {name} {{
  value: number
}}
"""
        nl_file = parse_nl_file(source)
        assert len(nl_file.module.types) == 1
        assert nl_file.module.types[0].name == name


class TestTypeConversionProperties:
    """Property-based tests for type conversions"""

    @given(st.sampled_from([
        "number", "string", "boolean", "void", "any",
        "list of number", "list of string",
        "number or null", "string or none"
    ]))
    def test_all_types_produce_valid_python(self, nls_type):
        """Every NLS type should convert to valid Python type"""
        inp = Input(name="x", type=nls_type)
        py_type = inp.to_python_type()

        # Should be a valid Python type annotation (can be parsed)
        assert py_type is not None
        assert len(py_type) > 0
        # Should not contain NLS-specific syntax
        assert "or null" not in py_type.lower()
        assert "or none" not in py_type.lower() or py_type == "None"


class TestEmitterProperties:
    """Property-based tests for the emitter"""

    @given(
        func_name=nls_identifier,
        param_name=st.from_regex(r"[a-z][a-z0-9_]{0,10}", fullmatch=True)
    )
    @settings(max_examples=50)
    def test_emitted_code_compiles(self, func_name, param_name):
        """Generated Python should always be syntactically valid"""
        # Avoid Python keywords and reserved names
        assume(param_name not in PYTHON_RESERVED)
        assume(func_name not in PYTHON_RESERVED)

        source = f"""\
@module test
@target python

[{func_name}]
PURPOSE: Test function
INPUTS:
  - {param_name}: number
RETURNS: {param_name}
"""
        try:
            nl_file = parse_nl_file(source)
            code = emit_python(nl_file)
            # Should compile without syntax errors
            compile(code, "<string>", "exec")
        except ParseError:
            # Parser rejection is acceptable for edge cases
            pass

    @given(purpose=st.text(min_size=1, max_size=100, alphabet=st.characters(blacklist_categories=('Cs',), blacklist_characters='\x00\n\r')))
    @settings(max_examples=30)
    def test_purpose_preserved_in_docstring(self, purpose):
        """Purpose text should appear in generated docstring"""
        # Escape any characters that would break string parsing
        safe_purpose = purpose.replace('"', "'").replace("\\", "")
        assume(len(safe_purpose.strip()) > 0)

        source = f"""\
@module test
@target python

[test-func]
PURPOSE: {safe_purpose}
RETURNS: void
"""
        try:
            nl_file = parse_nl_file(source)
            code = emit_python(nl_file)
            # Purpose should be in the docstring
            assert safe_purpose in code or safe_purpose.strip() in code
        except (ParseError, ValueError):
            # Some edge cases may not parse
            pass


class TestRoundtripProperties:
    """Property-based tests for parse-emit roundtrip"""

    @given(
        module_name=st.from_regex(r"[a-z][a-z0-9_]{0,10}", fullmatch=True),
        func_name=nls_identifier
    )
    @settings(max_examples=30)
    def test_parsed_metadata_preserved(self, module_name, func_name):
        """Module metadata should be preserved through parsing"""
        source = f"""\
@module {module_name}
@version 1.0.0
@target python

[{func_name}]
PURPOSE: Test
RETURNS: void
"""
        nl_file = parse_nl_file(source)

        assert nl_file.module.name == module_name
        assert nl_file.module.version == "1.0.0"
        assert nl_file.module.target == "python"
        assert len(nl_file.anlus) == 1
        assert nl_file.anlus[0].identifier == func_name


class TestInvariantProperties:
    """Property-based tests for invariant validation"""

    @given(
        field_name=st.from_regex(r"[a-z][a-z_]{0,10}", fullmatch=True),
        constraint_value=st.integers(min_value=0, max_value=1000)
    )
    @settings(max_examples=30)
    def test_numeric_constraints_generate_valid_checks(self, field_name, constraint_value):
        """Numeric constraints should generate valid Python comparisons"""
        assume(field_name not in PYTHON_RESERVED)

        source = f"""\
@module test
@target python

@type TestType {{
  {field_name}: number, min: {constraint_value}
}}
"""
        nl_file = parse_nl_file(source)
        code = emit_python(nl_file)

        # Should compile
        compile(code, "<string>", "exec")
        # Should contain the constraint check
        assert f"self.{field_name} < {constraint_value}" in code or f"if self.{field_name}" in code
