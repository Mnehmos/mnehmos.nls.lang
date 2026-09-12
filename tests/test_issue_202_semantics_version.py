"""Issue #202 slice: emitter semantics version in lock identity.

A lockfile records which backend semantics revision produced each target
artifact.  When the recorded marker disagrees with the current emitter,
frozen compiles and `nlsc ci` refuse with ELOCK004 instead of silently
accepting output the emitter no longer promises.
"""

from __future__ import annotations

import json

from nlsc.capabilities import emitter_semantics_version
from nlsc.cli import main
from nlsc.lockfile import target_semantics_mismatch

VALID = """@module semantics_probe
[add]
PURPOSE: add two numbers
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
"""


def _compile(tmp_path, source: str = VALID):
    path = tmp_path / "probe.nl"
    path.write_text(source, encoding="utf-8")
    assert main(["compile", str(path)]) == 0
    return path


def _rewrite_marker(lock_path, marker: str) -> None:
    content = lock_path.read_text(encoding="utf-8")
    assert "semantics_version:" in content
    updated = []
    for line in content.splitlines():
        if line.strip().startswith("semantics_version:"):
            line = f"    semantics_version: {marker}"
        updated.append(line)
    lock_path.write_text("\n".join(updated) + "\n", encoding="utf-8")


def test_compile_records_emitter_semantics_marker(tmp_path, capsys):
    path = _compile(tmp_path)
    capsys.readouterr()
    content = path.with_suffix(".nl.lock").read_text(encoding="utf-8")
    assert f"semantics_version: {emitter_semantics_version('python')}" in content


def test_lockfile_round_trip_preserves_marker(tmp_path):
    from nlsc.lockfile import read_lockfile

    path = _compile(tmp_path)
    lock_path = path.with_suffix(".nl.lock")
    lock = read_lockfile(lock_path)
    assert lock is not None
    assert lock.targets["python"].semantics_version == emitter_semantics_version("python")
    assert target_semantics_mismatch(lock, "python") is None


def test_lock_without_marker_stays_compatible(tmp_path, capsys):
    path = _compile(tmp_path)
    lock_path = path.with_suffix(".nl.lock")
    stripped = "\n".join(
        line
        for line in lock_path.read_text(encoding="utf-8").splitlines()
        if not line.strip().startswith("semantics_version:")
    )
    lock_path.write_text(stripped + "\n", encoding="utf-8")
    capsys.readouterr()

    assert main(["compile", "--frozen-lockfile", str(path)]) == 0
    assert "frozen; not rewritten" in capsys.readouterr().out


def test_frozen_compile_rejects_changed_marker(tmp_path, capsys):
    path = _compile(tmp_path)
    lock_path = path.with_suffix(".nl.lock")
    _rewrite_marker(lock_path, "py-0")
    tampered = lock_path.read_text(encoding="utf-8")
    capsys.readouterr()

    assert main(["compile", "--frozen-lockfile", str(path)]) == 1
    captured = capsys.readouterr()
    assert "ELOCK004" in captured.err
    assert "py-0" in captured.err
    assert emitter_semantics_version("python") in captured.err
    # Frozen compiles never rewrite the lockfile, even when they refuse it.
    assert lock_path.read_text(encoding="utf-8") == tampered


def test_frozen_compile_marker_mismatch_json(tmp_path, capsys):
    path = _compile(tmp_path)
    _rewrite_marker(path.with_suffix(".nl.lock"), "py-0")
    capsys.readouterr()

    assert main(["compile", "--frozen-lockfile", "--json", str(path)]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is False
    assert [d["code"] for d in payload["diagnostics"]] == ["ELOCK004"]


def test_ci_rejects_changed_marker(tmp_path, capsys):
    path = _compile(tmp_path)
    _rewrite_marker(path.with_suffix(".nl.lock"), "py-0")
    capsys.readouterr()

    assert main(["ci", "--compile", str(path)]) == 1
    captured = capsys.readouterr()
    assert "lockfile stage failed" in captured.err
    assert "ELOCK004" in captured.err


def test_ci_rejects_changed_marker_without_compile(tmp_path, capsys):
    path = _compile(tmp_path)
    _rewrite_marker(path.with_suffix(".nl.lock"), "py-0")
    capsys.readouterr()

    assert main(["ci", str(path)]) == 1
    assert "ELOCK004" in capsys.readouterr().err


def test_ci_json_reports_marker_mismatch_stage(tmp_path, capsys):
    path = _compile(tmp_path)
    _rewrite_marker(path.with_suffix(".nl.lock"), "py-0")
    capsys.readouterr()

    assert main(["ci", "--json", str(path)]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["stages"]["lockfile"] == "failed"
    assert [d["code"] for d in payload["diagnostics"]] == ["ELOCK004"]


def test_ci_accepts_matching_marker(tmp_path, capsys):
    path = _compile(tmp_path)
    capsys.readouterr()
    assert main(["ci", "--compile", str(path)]) == 0
    assert "compile: reproducible" in capsys.readouterr().out


def test_regenerate_clears_marker_mismatch(tmp_path, capsys):
    path = _compile(tmp_path)
    lock_path = path.with_suffix(".nl.lock")
    _rewrite_marker(lock_path, "py-0")
    capsys.readouterr()

    # The documented remedy: regenerate and commit the lockfile.
    assert main(["compile", str(path)]) == 0
    capsys.readouterr()
    assert main(["compile", "--frozen-lockfile", str(path)]) == 0
