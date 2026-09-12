"""Issue #202 slice: FOR-each loop steps are a Python-only capability.

The TypeScript backend has no loop representation, but it used to emit the
LOGIC step verbatim — ``FOR each item IN items: total = total + item;``
inside the function body, which ``tsc`` rejects — while ``nlsc compile
--target typescript`` exited 0.  An unsupported construct must be refused
before output instead of producing an invalid artifact.
"""

from __future__ import annotations

import json

from nlsc.capabilities import emitter_semantics_version
from nlsc.cli import main
from nlsc.parser import parse_nl_file
from nlsc.schema import FOR_EACH_STEP_RE

LOOP_FILE = """@module loop_probe
[total-all]
PURPOSE: sum every value
INPUTS:
  - items: list of number
LOGIC:
  1. total = 0
  2. FOR each item IN items: total = total + item
RETURNS: total
"""

NO_LOOP_FILE = """@module no_loop
[add]
PURPOSE: add
INPUTS:
  - a: number
  - b: number
LOGIC:
  1. total = a + b
RETURNS: total
"""

PROSE_FOR_FILE = """@module prose_for
[describe]
PURPOSE: narrate
LOGIC:
  1. FOR each customer, apply the discount policy
RETURNS: 0
"""


def _write(tmp_path, source: str, name: str = "probe.nl"):
    path = tmp_path / name
    path.write_text(source, encoding="utf-8")
    return path


# --------------------------------------------------------------------------
# Detection
# --------------------------------------------------------------------------


def test_loop_step_detection():
    assert FOR_EACH_STEP_RE.match("FOR each item IN items: total = total + item")
    assert FOR_EACH_STEP_RE.match("for each x IN values: acc = acc + x")
    assert not FOR_EACH_STEP_RE.match("FOR each customer, apply the policy")


def test_nl_file_reports_loop_usage():
    assert parse_nl_file(LOOP_FILE, source_path="loop.nl").uses_for_each_loops()
    assert not parse_nl_file(
        NO_LOOP_FILE, source_path="add.nl"
    ).uses_for_each_loops()
    assert not parse_nl_file(
        PROSE_FOR_FILE, source_path="prose.nl"
    ).uses_for_each_loops()


# --------------------------------------------------------------------------
# Capability gate
# --------------------------------------------------------------------------


def test_typescript_compile_refuses_loops_and_writes_nothing(tmp_path, capsys):
    path = _write(tmp_path, LOOP_FILE)
    assert main(["compile", str(path), "-t", "typescript"]) == 1
    err = capsys.readouterr().err
    assert "ETARGET002" in err
    assert "FOR each LOGIC loop steps" in err
    assert not (tmp_path / "probe.ts").exists()


def test_typescript_loop_refusal_json(tmp_path, capsys):
    path = _write(tmp_path, LOOP_FILE)
    assert main(["compile", "--json", str(path), "-t", "typescript"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is False
    assert [d["code"] for d in payload["diagnostics"]] == ["ETARGET002"]


def test_python_compile_still_emits_the_loop(tmp_path, capsys):
    path = _write(tmp_path, LOOP_FILE)
    assert main(["compile", str(path), "-t", "python"]) == 0
    code = (tmp_path / "probe.py").read_text(encoding="utf-8")
    assert "for item in items:" in code
    assert "total = total + item" in code


def test_typescript_compile_of_loop_free_file_is_unaffected(tmp_path, capsys):
    path = _write(tmp_path, NO_LOOP_FILE)
    assert main(["compile", str(path), "-t", "typescript"]) == 0
    assert "export function add" in (tmp_path / "probe.ts").read_text(
        encoding="utf-8"
    )


def test_prose_for_step_is_not_a_loop(tmp_path, capsys):
    path = _write(tmp_path, PROSE_FOR_FILE)
    # No colon-delimited action: narrative, not a loop, so no capability gap.
    assert main(["compile", str(path), "-t", "typescript", "--strict"]) == 0


def test_ci_refuses_loops_on_typescript(tmp_path, capsys):
    path = _write(tmp_path, LOOP_FILE)
    assert main(["compile", str(path), "-t", "python"]) == 0
    capsys.readouterr()
    assert main(["ci", str(path), "--compile", "-t", "typescript"]) == 1
    assert "ETARGET002" in capsys.readouterr().err


def test_capability_listing_includes_loop_steps():
    from nlsc.capabilities import TARGET_CAPABILITIES

    assert TARGET_CAPABILITIES["python"]["loop_steps"] is True
    assert TARGET_CAPABILITIES["typescript"]["loop_steps"] is False


# --------------------------------------------------------------------------
# The capability flip is part of the TypeScript semantics marker
# --------------------------------------------------------------------------


def test_typescript_semantics_marker_reflects_the_capability_change():
    assert emitter_semantics_version("typescript") == "ts-2"


def test_fresh_typescript_lock_records_the_marker(tmp_path, capsys):
    path = _write(tmp_path, NO_LOOP_FILE)
    assert main(["compile", str(path), "-t", "typescript"]) == 0
    capsys.readouterr()
    lock = path.with_suffix(".nl.lock").read_text(encoding="utf-8")
    assert "semantics_version: ts-2" in lock


def test_stale_typescript_marker_requires_regeneration(tmp_path, capsys):
    path = _write(tmp_path, NO_LOOP_FILE)
    assert main(["compile", str(path), "-t", "typescript"]) == 0
    lock_path = path.with_suffix(".nl.lock")
    lock_path.write_text(
        lock_path.read_text(encoding="utf-8").replace(
            "semantics_version: ts-2", "semantics_version: ts-1"
        ),
        encoding="utf-8",
    )
    capsys.readouterr()

    assert main(["ci", "--compile", str(path), "-t", "typescript"]) == 1
    assert "ELOCK004" in capsys.readouterr().err
