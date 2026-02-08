"""Regression tests for Issue #121: NL guards must not emit invalid Python."""

import pytest

from nlsc.emitter import emit_python
from nlsc.parser import parse_nl_file


def test_should_require_explicit_python_guard_expression_when_guard_is_natural_language():
    """Natural-language guard text should be rejected with a clear validation contract."""
    source = """\
@module guards_issue_121
@target python

[safe-divide]
PURPOSE: divide numbers safely
INPUTS:
  - dividend: number
  - divisor: number
GUARDS:
  • divisor must not be zero → ValueError(Division by zero)
RETURNS: dividend / divisor
"""

    parsed = parse_nl_file(source)

    with pytest.raises(Exception, match="explicit Python guard expression|invalid guard expression|natural language"):
        emit_python(parsed)
