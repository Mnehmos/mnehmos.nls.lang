"""Red-phase regression tests for Issue #83 edge-case matrix.

These tests intentionally codify expected edge behavior that is currently
missing, so they should fail until Green phase implementation lands.
"""

from pathlib import Path

import pytest

from nlsc.atomize import atomize_python_file
from nlsc.lockfile import read_lockfile
from nlsc.parser import ParseError, parse_nl_file

try:
    from nlsc.parser_treesitter import is_available as treesitter_available
    from nlsc.parser_treesitter import parse_nl_file_treesitter

    TREESITTER_AVAILABLE = treesitter_available()
except ImportError:
    TREESITTER_AVAILABLE = False
    parse_nl_file_treesitter = None


@pytest.mark.skipif(not TREESITTER_AVAILABLE, reason="tree-sitter not available")
def test_should_raise_parse_error_in_both_parsers_when_inputs_bullet_marker_is_invalid():
    """Parser parity: malformed INPUTS bullets must fail consistently in both parsers."""
    source = """\
@module issue83
@target python

[strict-inputs]
PURPOSE: Ensure malformed section markers are rejected consistently
INPUTS:
  => bad: number
RETURNS: bad
"""

    with pytest.raises(ParseError, match="Invalid INPUTS bullet marker"):
        parse_nl_file(source)

    with pytest.raises(ParseError, match="Invalid INPUTS bullet marker"):
        parse_nl_file_treesitter(source)


def test_should_include_keyword_only_arguments_when_atomizing_function_signature():
    """Atomizer parity: keyword-only args are part of callable contract and must be preserved."""
    code = """\
def configure(host: str, *, port: int, secure: bool = True) -> str:
    return f"{host}:{port}:{secure}"
"""

    anlus, _ = atomize_python_file(code)

    assert len(anlus) == 1, "Expected one ANLU from a single public function."
    input_names = [inp["name"] for inp in anlus[0]["inputs"]]

    assert "port" in input_names, (
        "Keyword-only argument 'port' must be included in atomized INPUTS for signature fidelity."
    )
    assert "secure" in input_names, (
        "Keyword-only argument 'secure' must be included in atomized INPUTS even when it has a default."
    )


def test_should_include_varargs_and_varkwargs_when_atomizing_function_signature():
    """Atomizer edge behavior: variadic parameters must not be dropped from extracted INPUTS."""
    code = """\
def forward(prefix: str, *values: int, **labels: str) -> tuple:
    return (prefix, values, labels)
"""

    anlus, _ = atomize_python_file(code)

    assert len(anlus) == 1, "Expected one ANLU from a single public function."
    input_names = [inp["name"] for inp in anlus[0]["inputs"]]

    assert "values" in input_names, (
        "Variadic positional parameter '*values' must be represented in atomized INPUTS."
    )
    assert "labels" in input_names, (
        "Variadic keyword parameter '**labels' must be represented in atomized INPUTS."
    )


def test_should_return_none_when_generated_code_literal_block_is_unterminated_at_eof(tmp_path: Path):
    """Lockfile hardening: unterminated multiline generated_code must be rejected deterministically."""
    malformed_lock = """\
schema_version: 1
generated_at: 2026-02-08T00:00:00+00:00
compiler_version: 0.0.0
llm_backend: mock
modules:
  sample:
    source_hash: sha256:abc
    anlus:
      add:
        source_hash: sha256:def
        output_hash: sha256:ghi
        output_lines: 2
        generated_code: |
"""
    lock_path = tmp_path / "unterminated_generated_code.nl.lock"
    lock_path.write_text(malformed_lock, encoding="utf-8")

    parsed = read_lockfile(lock_path)

    assert parsed is None, (
        "Lockfile parser must return None when generated_code literal block is opened but not terminated."
    )

