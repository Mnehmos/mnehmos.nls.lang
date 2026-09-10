"""Issue #149: automation-native CI gate.

``nlsc ci`` runs strict semantics plus a frozen lockfile (never rewritten),
optionally compiling with reproducibility verification and running tests.
``nlsc compile --frozen-lockfile`` gives plain compiles the same guarantee.
"""

from __future__ import annotations

import json

from nlsc.cli import main

VALID = """@module ci_probe
[add]
PURPOSE: add
INPUTS:
  - a: number
  - b: number
LOGIC:
  1. total = a + b
RETURNS: total

[double]
PURPOSE: double via add
INPUTS:
  - value: number
LOGIC:
  1. out = [add](value, value)
RETURNS: out
DEPENDS: [add]

@test [add] {
  add(1, 2) == 3
}
"""

SCAFFOLD = """@module ci_scaffold
[probe]
PURPOSE: scaffold content
LOGIC:
  1. Process customer payment -> payment
RETURNS: payment
"""


def _write(tmp_path, source: str, name: str = "probe.nl"):
    path = tmp_path / name
    path.write_text(source, encoding="utf-8")
    return path


def _compile(tmp_path, source: str):
    path = _write(tmp_path, source)
    assert main(["compile", str(path)]) == 0
    return path


# --------------------------------------------------------------------------
# nlsc ci
# --------------------------------------------------------------------------


def test_ci_passes_on_valid_current_project(tmp_path, capsys):
    path = _compile(tmp_path, VALID)
    assert main(["ci", str(path)]) == 0
    assert "ci passed" in capsys.readouterr().out


def test_ci_fails_without_lockfile(tmp_path, capsys):
    path = _write(tmp_path, VALID)
    assert main(["ci", str(path)]) == 1
    assert "lockfile stage failed" in capsys.readouterr().err


def test_ci_fails_on_stale_lockfile(tmp_path, capsys):
    path = _compile(tmp_path, VALID)
    edited = VALID.replace("total = a + b", "total = a + b + 1")
    path.write_text(edited, encoding="utf-8")
    assert main(["ci", str(path)]) == 1
    assert "ELOCK002" in capsys.readouterr().err


def test_ci_fails_on_scaffold_content(tmp_path, capsys):
    path = _compile(tmp_path, SCAFFOLD)
    assert main(["ci", str(path)]) == 1
    err = capsys.readouterr().err
    assert "gate stage failed" in err
    assert "EIR002" in err


def test_ci_compile_verifies_reproducibility(tmp_path, capsys):
    path = _compile(tmp_path, VALID)
    assert main(["ci", "--compile", str(path)]) == 0
    captured = capsys.readouterr()
    assert "compile: reproducible" in captured.out.split("ci passed")[-1]


def test_ci_compile_detects_tampered_target_hash(tmp_path, capsys):
    path = _compile(tmp_path, VALID)
    capsys.readouterr()  # discard the setup compile's output

    lock_path = path.with_suffix(".nl.lock")
    content = lock_path.read_text(encoding="utf-8")
    # Tamper the recorded target hash so regeneration cannot match.
    import re

    tampered = re.sub(
        r"(file: .*\.py\n\s+hash: sha256:)[0-9a-f]+",
        r"\1deadbeefdead",
        content,
        count=1,
    )
    lock_path.write_text(tampered, encoding="utf-8")

    assert main(["ci", "--compile", str(path)]) == 1
    assert "does not reproduce the locked target hash" in capsys.readouterr().err


def test_ci_runs_tests_when_requested(tmp_path, capsys):
    path = _compile(tmp_path, VALID)
    capsys.readouterr()  # discard the setup compile's output
    assert main(["ci", "--test", str(path)]) == 0
    assert "test: passed" in capsys.readouterr().out


def test_ci_json_reports_stages(tmp_path, capsys):
    path = _compile(tmp_path, VALID)
    capsys.readouterr()  # discard the setup compile's output
    assert main(["ci", "--json", str(path)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert payload["command"] == "ci"
    assert payload["stages"] == {
        "parse": "passed",
        "gate": "passed",
        "lockfile": "current",
    }


def test_ci_json_reports_failure_diagnostics(tmp_path, capsys):
    path = _write(tmp_path, SCAFFOLD)
    assert main(["ci", "--json", str(path)]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is False
    assert payload["stages"]["gate"] == "failed"
    codes = [d["code"] for d in payload["diagnostics"]]
    assert "EIR002" in codes


# --------------------------------------------------------------------------
# compile --frozen-lockfile
# --------------------------------------------------------------------------


def test_frozen_compile_passes_and_preserves_lock(tmp_path, capsys):
    path = _compile(tmp_path, VALID)
    capsys.readouterr()  # discard the setup compile's output
    lock_path = path.with_suffix(".nl.lock")
    before = lock_path.read_text(encoding="utf-8")

    assert main(["compile", "--frozen-lockfile", str(path)]) == 0
    captured = capsys.readouterr()
    assert "frozen; not rewritten" in captured.out
    assert "Updated" not in captured.out
    assert lock_path.read_text(encoding="utf-8") == before


def test_frozen_compile_fails_on_stale_lock(tmp_path, capsys):
    path = _compile(tmp_path, VALID)
    capsys.readouterr()  # discard the setup compile's output
    lock_path = path.with_suffix(".nl.lock")
    before = lock_path.read_text(encoding="utf-8")

    edited = VALID.replace("out = [add](value, value)", "out = [add](value, value) + 1")
    path.write_text(edited, encoding="utf-8")

    assert main(["compile", "--frozen-lockfile", str(path)]) == 1
    assert "not current" in capsys.readouterr().err
    assert lock_path.read_text(encoding="utf-8") == before


def test_frozen_compile_fails_without_lock(tmp_path, capsys):
    path = _write(tmp_path, VALID)
    assert main(["compile", "--frozen-lockfile", str(path)]) == 1
    err = capsys.readouterr().err
    assert "Lockfile not found" in err
