"""Issue #93: edit provenance — format, CLI, and the CI trust gate.

The workflow under test: an LLM proposal is recorded as pending, CI
refuses to pass it, a human accepts it, CI passes.  Specs without a
sidecar are unaffected.
"""

from __future__ import annotations

import json
from pathlib import Path

from nlsc.cli import main

SPEC = """@module prov_probe
@version 1.0.0

[work]
PURPOSE: do the work
INPUTS:
  - x: number
GUARDS:
  - x >= 0 -> ValueError("x must be non-negative")
RETURNS: x
"""


def _write(tmp_path, name="probe.nl"):
    path = tmp_path / name
    path.write_text(SPEC, encoding="utf-8")
    return path


def _sidecar(path: Path) -> Path:
    return Path(str(path) + ".provenance.json")


def _compile(path, capsys=None):
    assert main(["compile", str(path)]) == 0
    if capsys is not None:
        capsys.readouterr()


# --------------------------------------------------------------------------
# Read/write
# --------------------------------------------------------------------------


def test_record_and_show_round_trip(tmp_path, capsys):
    path = _write(tmp_path)
    assert (
        main(
            [
                "provenance",
                str(path),
                "--source",
                "llm",
                "--model",
                "claude-3-opus",
                "--conversation",
                "abc123",
                "--status",
                "pending",
            ]
        )
        == 0
    )
    capsys.readouterr()

    data = json.loads(_sidecar(path).read_text(encoding="utf-8"))
    assert data["file"] == "probe.nl"
    assert data["source"] == {
        "type": "llm",
        "model": "claude-3-opus",
        "conversation_id": "abc123",
    }
    assert data["status"] == "pending"
    assert data["timestamp"]
    assert data["changes"] and data["changes"][0]["name"] == "work"

    assert main(["provenance", str(path)]) == 0
    out = capsys.readouterr().out
    assert '"status": "pending"' in out


def test_show_without_sidecar_is_explicit(tmp_path, capsys):
    path = _write(tmp_path)
    assert main(["provenance", str(path)]) == 0
    assert "No provenance recorded" in capsys.readouterr().out

    assert main(["provenance", "--json", str(path)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["recorded"] is False


def test_accept_sets_review_marker(tmp_path, capsys):
    path = _write(tmp_path)
    assert main(["provenance", str(path), "--source", "llm", "--status", "pending"]) == 0
    assert main(["provenance", str(path), "--status", "accepted"]) == 0
    capsys.readouterr()
    data = json.loads(_sidecar(path).read_text(encoding="utf-8"))
    assert data["status"] == "accepted"
    assert data["human_review"] == "accepted"
    assert data["source"]["type"] == "llm"  # source survives the status update


def test_clear_removes_sidecar(tmp_path, capsys):
    path = _write(tmp_path)
    assert main(["provenance", str(path), "--source", "tool"]) == 0
    assert _sidecar(path).exists()
    assert main(["provenance", str(path), "--clear"]) == 0
    assert not _sidecar(path).exists()
    capsys.readouterr()


def test_malformed_sidecar_reports_eprov002(tmp_path, capsys):
    path = _write(tmp_path)
    _sidecar(path).write_text("{ not json", encoding="utf-8")
    assert main(["provenance", str(path), "--status", "accepted"]) == 1
    assert "EPROV002" in capsys.readouterr().err


def test_unknown_source_or_status_rejected_by_cli(tmp_path, capsys):
    import pytest

    path = _write(tmp_path)
    with pytest.raises(SystemExit) as source_exit:
        main(["provenance", str(path), "--source", "robot"])
    assert source_exit.value.code == 2  # argparse choice rejection
    with pytest.raises(SystemExit) as status_exit:
        main(["provenance", str(path), "--status", "maybe"])
    assert status_exit.value.code == 2
    capsys.readouterr()


# --------------------------------------------------------------------------
# The CI trust gate
# --------------------------------------------------------------------------


def test_ci_blocks_pending_provenance(tmp_path, capsys):
    path = _write(tmp_path)
    _compile(path, capsys)
    assert main(["provenance", str(path), "--source", "llm", "--status", "pending"]) == 0
    capsys.readouterr()

    assert main(["ci", str(path)]) == 1
    err = capsys.readouterr().err
    assert "EPROV001" in err
    assert "review required" in err


def test_ci_passes_after_acceptance(tmp_path, capsys):
    path = _write(tmp_path)
    _compile(path, capsys)
    assert main(["provenance", str(path), "--source", "llm", "--status", "pending"]) == 0
    assert main(["provenance", str(path), "--status", "accepted"]) == 0
    capsys.readouterr()

    assert main(["ci", str(path)]) == 0
    out = capsys.readouterr().out
    assert "provenance: accepted" in out


def test_ci_unaffected_without_provenance(tmp_path, capsys):
    path = _write(tmp_path)
    _compile(path, capsys)
    assert main(["ci", str(path)]) == 0
    assert "provenance: unrecorded" in capsys.readouterr().out


def test_ci_fails_on_malformed_sidecar(tmp_path, capsys):
    path = _write(tmp_path)
    _compile(path, capsys)
    _sidecar(path).write_text("[]", encoding="utf-8")
    assert main(["ci", str(path)]) == 1
    assert "EPROV002" in capsys.readouterr().err


def test_ci_json_reports_provenance_stage(tmp_path, capsys):
    path = _write(tmp_path)
    _compile(path, capsys)
    assert main(["provenance", str(path), "--source", "llm", "--status", "pending"]) == 0
    capsys.readouterr()
    assert main(["ci", "--json", str(path)]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["stages"]["provenance"] == "failed"
    assert "EPROV001" in [d["code"] for d in payload["diagnostics"]]
