"""Issue #95: `nlsc fmt` — canonical formatting.

Idempotence, comment preservation, verbatim bodies, CLI contract, and a
corpus-wide guarantee that formatting never changes meaning.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from nlsc.cli import main
from nlsc.formatting import format_source
from nlsc.parser import parse_nl_file
from nlsc.typecheck import check_module

FEATURES_DIR = Path(__file__).resolve().parent.parent / "examples" / "features"

MESSY = """@module fmt_probe
@version 1.0.0


[f]
# doc comment for RETURNS
RETURNS:  a +  b
PURPOSE:  add two numbers
LOGIC:
  1. total = a + b
INPUTS:
  - a: number
  - longer_name: number
GUARDS:
  * a >= 0 -> ValueError("non-negative")
"""


def test_bullets_arrows_headers_and_whitespace_normalized():
    result = format_source(MESSY)
    assert result.safe
    text = result.text
    assert "* a >= 0" not in text
    assert "  - a:" in text
    assert "PURPOSE: add two numbers" in text
    assert "RETURNS: a + b" in text
    assert "\n\n\n" not in text
    assert text.endswith("\n") and not text.endswith("\n\n")


def test_sections_reordered_into_canonical_order():
    result = format_source(MESSY)
    text = result.text
    order = [text.index(name) for name in ("PURPOSE", "INPUTS", "GUARDS", "LOGIC", "RETURNS")]
    assert order == sorted(order)


def test_comments_move_with_their_section():
    result = format_source(MESSY)
    text = result.text
    # The comment attached above RETURNS must move with it, still attached.
    returns_block = text[text.index("# doc comment for RETURNS") :]
    assert returns_block.split("\n")[1].startswith("RETURNS:")


def test_inputs_types_align_after_colon():
    result = format_source(MESSY)
    lines = result.text.split("\n")
    inputs_start = lines.index("INPUTS:")
    entries = []
    for line in lines[inputs_start + 1 :]:
        if not line.startswith("  - "):
            break
        entries.append(line)
    assert len(entries) >= 2
    type_columns = {line.index("number") for line in entries}
    assert len(type_columns) == 1


def test_blank_line_between_anlus_enforced():
    source = """@module m
@version 1.0.0
[a]
PURPOSE: p
RETURNS: 1
[b]
PURPOSE: q
RETURNS: 2
"""
    result = format_source(source)
    assert "\n\n[b]" in result.text


def test_verbatim_literal_and_main_bodies_untouched():
    source = '''@module m
@version 1.0.0
@literal python {
def helper(x):
    return x  #  weird   spacing kept
}

[use]
PURPOSE: p
RETURNS: helper(1)

@main {
  PRINT   helper(1)
}
'''
    result = format_source(source)
    assert "return x  #  weird   spacing kept" in result.text
    assert "  PRINT   helper(1)" in result.text


def test_idempotent_on_messy_fixture():
    first = format_source(MESSY)
    second = format_source(first.text)
    assert second.text == first.text
    assert second.changed is False


def test_already_formatted_source_is_unchanged():
    source = """@module m
@version 1.0.0

[f]
PURPOSE: p
RETURNS: 1
"""
    result = format_source(source)
    assert result.changed is False
    assert result.text == source


def test_formatting_preserves_structure_everywhere():
    for path in sorted(FEATURES_DIR.glob("*.nl")):
        source = path.read_text(encoding="utf-8")
        result = format_source(source)
        assert result.safe, f"{path.name}: {result.reason}"
        reparsed = check_module(
            parse_nl_file(result.text, source_path=str(path)), file_token=str(path)
        )
        assert reparsed.errors == [], f"{path.name}: {[d.code for d in reparsed.errors]}"
        assert parse_nl_file(result.text, source_path=str(path)).anlus


def test_formatting_is_fast_for_a_typical_file():
    source = (FEATURES_DIR / "composition.nl").read_text(encoding="utf-8")
    start = time.perf_counter()
    format_source(source)
    assert time.perf_counter() - start < 1.0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _write(tmp_path, source: str, name="probe.nl"):
    path = tmp_path / name
    path.write_text(source, encoding="utf-8")
    return path


def test_cli_fmt_in_place_and_check(tmp_path, capsys):
    path = _write(tmp_path, MESSY)
    assert main(["fmt", str(path), "--check"]) == 1  # needs formatting
    assert main(["fmt", str(path)]) == 0
    capsys.readouterr()
    assert main(["fmt", str(path), "--check"]) == 0
    assert "RETURNS: a + b" in path.read_text(encoding="utf-8")


def test_cli_fmt_check_writes_nothing(tmp_path):
    path = _write(tmp_path, MESSY)
    before = path.read_text(encoding="utf-8")
    assert main(["fmt", str(path), "--check"]) == 1
    assert path.read_text(encoding="utf-8") == before


def test_cli_fmt_diff_shows_changes_without_writing(tmp_path, capsys):
    path = _write(tmp_path, MESSY)
    before = path.read_text(encoding="utf-8")
    assert main(["fmt", str(path), "--diff"]) == 0
    out = capsys.readouterr().out
    assert "--- " in out and "+++ " in out
    assert path.read_text(encoding="utf-8") == before


def test_cli_fmt_directory_mode(tmp_path, capsys):
    _write(tmp_path, MESSY, "one.nl")
    (tmp_path / "sub").mkdir()
    _write(tmp_path / "sub", MESSY, "two.nl")
    assert main(["fmt", str(tmp_path)]) == 0
    assert "Formatted 2 file(s)" in capsys.readouterr().out


def test_cli_fmt_json_payload(tmp_path, capsys):
    path = _write(tmp_path, MESSY)
    assert main(["fmt", "--json", str(path)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["command"] == "fmt"
    assert payload["changed"] == [str(path)]
    assert payload["formatted"] == 1


def test_cli_fmt_unsafe_file_reports_efmt001(tmp_path, capsys, monkeypatch):
    path = _write(tmp_path, MESSY)

    from nlsc.formatting import FormatResult

    def fake_format_source(source: str) -> FormatResult:
        return FormatResult(text=source, changed=False, safe=False, reason="synthetic")

    monkeypatch.setattr("nlsc.formatting.format_source", fake_format_source)
    assert main(["fmt", str(path)]) == 1
    assert "EFMT001" in capsys.readouterr().err


def test_cli_fmt_missing_file(tmp_path, capsys):
    assert main(["fmt", "--json", str(tmp_path / "nope.nl")]) == 1
