"""Regression tests for Issue #124: parser must not silently drop unrecognized section lines."""

import pytest

from nlsc.parser import ParseError, parse_nl_file


def test_should_raise_parse_error_when_unrecognized_non_empty_line_appears_in_inputs_section():
    """INPUTS section must reject non-bullet content with explicit ParseError context."""
    source = """\
@module issue124
@target python

[validate-inputs]
PURPOSE: Ensure inputs are parsed strictly
INPUTS:
  unexpected free-form line that should not be ignored
RETURNS: ok
"""

    with pytest.raises(ParseError) as exc_info:
        parse_nl_file(source)

    err = exc_info.value
    err_text = str(err)

    assert err.line_number == 7, (
        "ParseError must report the exact source line for unrecognized INPUTS content."
    )
    assert "unexpected free-form line" in err.line_content or "unexpected free-form line" in err_text, (
        "ParseError must include the offending INPUTS content to avoid silent line loss."
    )


def test_should_raise_parse_error_when_unrecognized_non_empty_line_appears_in_guards_section():
    """GUARDS section must reject non-bullet content instead of silently dropping it."""
    source = """\
@module issue124
@target python

[validate-guards]
PURPOSE: Ensure guards are parsed strictly
INPUTS:
  • x: number
GUARDS:
  this line is not a bullet guard and must not be ignored
RETURNS: x
"""

    with pytest.raises(ParseError) as exc_info:
        parse_nl_file(source)

    err = exc_info.value
    err_text = str(err)

    assert err.line_number == 9, (
        "ParseError must report the exact source line for unrecognized GUARDS content."
    )
    assert "not a bullet guard" in err.line_content or "not a bullet guard" in err_text, (
        "ParseError must include offending GUARDS text to prevent silent parser drops."
    )


def test_should_raise_parse_error_when_unrecognized_non_empty_line_appears_in_logic_section():
    """LOGIC section must reject non-numbered content instead of silently dropping it."""
    source = """\
@module issue124
@target python

[validate-logic]
PURPOSE: Ensure logic is parsed strictly
INPUTS:
  • x: number
LOGIC:
  this line is not a numbered logic step and must not be ignored
RETURNS: x
"""

    with pytest.raises(ParseError) as exc_info:
        parse_nl_file(source)

    err = exc_info.value
    err_text = str(err)

    assert err.line_number == 9, (
        "ParseError must report the exact source line for unrecognized LOGIC content."
    )
    assert "not a numbered logic step" in err.line_content or "not a numbered logic step" in err_text, (
        "ParseError must include offending LOGIC text to prevent silent parser drops."
    )


def test_should_preserve_existing_behavior_when_nearby_inputs_guards_and_logic_syntax_is_valid():
    """Valid nearby section syntax should still parse, preserving established behavior."""
    source = """\
@module issue124
@target python

[valid-nearby-syntax]
PURPOSE: Ensure existing valid syntax remains accepted
INPUTS:
  • x: number
GUARDS:
  • x > 0 -> ValueError(x must be positive)
LOGIC:
  1. y = x + 1
RETURNS: y
"""

    parsed = parse_nl_file(source)
    anlu = parsed.anlus[0]

    assert anlu.identifier == "valid-nearby-syntax", (
        "Valid ANLU should still parse after strict unrecognized-line handling is introduced."
    )
    assert len(anlu.inputs) == 1, "Valid INPUTS bullet syntax should continue to parse unchanged."
    assert len(anlu.guards) == 1, "Valid GUARDS bullet syntax should continue to parse unchanged."
    assert len(anlu.logic_steps) == 1, "Valid numbered LOGIC syntax should continue to parse unchanged."

