"""Issue #202 slice: reject silently incomplete ANLU content.

Two defects of the same class — "the artifact looks complete but the
contract was never implemented":

1. The tree-sitter frontend recovered from grammar errors by parking the
   text in an ``ERROR`` node the section walkers never visit, so an
   unrecognized INPUTS line silently dropped the ANLU's INPUTS, LOGIC, and
   RETURNS and the emitter wrote an empty function.
2. An ANLU with no RETURNS section had no result contract at all, yet
   ``compile`` (and ``ci``) reported success and emitted ``return None``.

Both now produce diagnostics: the parser refuses truncated ANLU blocks,
and the shared executable contract reports ``EIR005`` (fatal under
``--strict`` and in CI, an INCOMPLETE SCAFFOLD marker otherwise).
"""

from __future__ import annotations

import json

import pytest

from nlsc import SPEC_VERSION
from nlsc.cli import main

try:
    from nlsc.parser_treesitter import is_available as treesitter_available

    TREESITTER_AVAILABLE = treesitter_available()
except ImportError:  # pragma: no cover - optional dependency
    TREESITTER_AVAILABLE = False

treesitter_only = pytest.mark.skipif(
    not TREESITTER_AVAILABLE, reason="tree-sitter not available"
)

# Bracket-indexed type spelling: not part of the documented type vocabulary
# (`list of number` is).  The tree-sitter grammar cannot parse it and used to
# drop everything after it in the ANLU.
BRACKETED_TYPE = """@module bracket_type
[total-all]
PURPOSE: sum every value
INPUTS:
  - items: list[number]
LOGIC:
  1. total = 0
RETURNS: total
"""

DIRECTIVE_BETWEEN_ANLUS = f"""@module mid_directive
[first]
PURPOSE: first
RETURNS: 1

@nls {SPEC_VERSION}

[second]
PURPOSE: second
INPUTS:
  - a: number
LOGIC:
  1. out = a + 1
RETURNS: out
"""

NO_RETURNS = """@module no_returns
[checkout]
PURPOSE: process a payment
LOGIC:
  1. status = 0
"""

RETURNS_NONE = """@module returns_none
[record]
PURPOSE: record a payment without a result
LOGIC:
  1. status = 0
RETURNS: none
"""

LITERAL_IMPL = """@module literal_impl
[noop]
PURPOSE: implemented by a literal block

@literal python {
def noop():
    return 0
}
"""

# `@nls` is parsed by the shared regex directive path: the grammar has no
# rule for it, so the whole file arrives as one recovered error before any
# ANLU is recognized and the documented fallback takes over.
LEADING_DIRECTIVE = f"""@module leading_directive
@nls {SPEC_VERSION}

[answer]
PURPOSE: the answer
LOGIC:
  1. value = 42
RETURNS: value
"""


def _write(tmp_path, source: str, name: str = "probe.nl"):
    path = tmp_path / name
    path.write_text(source, encoding="utf-8")
    return path


# --------------------------------------------------------------------------
# 1. tree-sitter must not drop truncated ANLU blocks
# --------------------------------------------------------------------------


@treesitter_only
def test_bracketed_type_is_rejected_not_dropped(tmp_path, capsys):
    path = _write(tmp_path, BRACKETED_TYPE)
    assert main(["compile", str(path)]) == 1
    err = capsys.readouterr().err
    assert "Unparsed content" in err
    assert "list[number]" in err
    # No artifact may be written from a partial parse.
    assert not path.with_suffix(".py").exists()


@treesitter_only
def test_bracketed_type_parse_error_payload(tmp_path, capsys):
    path = _write(tmp_path, BRACKETED_TYPE)
    assert main(["compile", "--json", str(path)]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is False
    diagnostic = payload["diagnostics"][0]
    assert diagnostic["code"] == "EPARSE001"
    assert diagnostic["line"] == 4
    assert "list of number" in diagnostic["hint"]


@treesitter_only
def test_directive_between_anlus_does_not_drop_the_second(tmp_path, capsys):
    path = _write(tmp_path, DIRECTIVE_BETWEEN_ANLUS)
    assert main(["compile", str(path)]) == 1
    err = capsys.readouterr().err
    assert "Unparsed content" in err
    assert "[second]" in err


@treesitter_only
def test_leading_directive_still_uses_regex_fallback(tmp_path, capsys):
    """A grammar gap before every ANLU keeps the documented regex fallback."""
    path = _write(tmp_path, LEADING_DIRECTIVE)
    assert main(["compile", str(path)]) == 0
    assert "def answer()" in path.with_suffix(".py").read_text(encoding="utf-8")


# --------------------------------------------------------------------------
# 2. an ANLU without RETURNS is unresolved executable content
# --------------------------------------------------------------------------


def test_compile_strict_rejects_missing_returns(tmp_path, capsys):
    path = _write(tmp_path, NO_RETURNS)
    assert main(["compile", "--strict", str(path)]) == 1
    err = capsys.readouterr().err
    assert "EIR005" in err
    assert "no RETURNS contract" in err


def test_compile_strict_missing_returns_json(tmp_path, capsys):
    path = _write(tmp_path, NO_RETURNS)
    assert main(["compile", "--strict", "--json", str(path)]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is False
    assert [d["code"] for d in payload["diagnostics"]] == ["EIR005"]


def test_default_compile_marks_incomplete_scaffold(tmp_path, capsys):
    path = _write(tmp_path, NO_RETURNS)
    assert main(["compile", "--json", str(path)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["scaffold"] == ["checkout"]
    assert [d["code"] for d in payload["warnings"]] == ["EIR005"]

    artifact = path.with_suffix(".py").read_text(encoding="utf-8")
    assert "INCOMPLETE SCAFFOLD" in artifact
    assert "checkout" in artifact


def test_ci_rejects_missing_returns(tmp_path, capsys):
    path = _write(tmp_path, NO_RETURNS)
    assert main(["ci", str(path)]) == 1
    err = capsys.readouterr().err
    assert "gate stage failed" in err
    assert "EIR005" in err


def test_returns_none_is_a_complete_contract(tmp_path, capsys):
    path = _write(tmp_path, RETURNS_NONE)
    assert main(["compile", "--strict", str(path)]) == 0


def test_literal_implementation_satisfies_the_contract(tmp_path, capsys):
    path = _write(tmp_path, LITERAL_IMPL)
    assert main(["compile", "--strict", str(path)]) == 0


def test_missing_returns_gate_diagnostic_shape(tmp_path):
    from nlsc.parser import parse_nl_file
    from nlsc.pipeline import evaluate_executable_contract

    nl_file = parse_nl_file(NO_RETURNS, source_path="no_returns.nl")
    result = evaluate_executable_contract(nl_file, file_token="no_returns.nl")
    assert [d.code for d in result.diagnostics] == ["EIR005"]
    assert result.scaffold_anlus == {"checkout"}
