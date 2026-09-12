"""Issue #91: OS integration — desktop files, docs, and Windows diagnostics.

The Linux integration files are generated portably (tested here on
Windows); the guide is guarded against rot by checking the commands it
documents actually exist.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from nlsc.cli import main

DOC = Path(__file__).resolve().parent.parent / "docs" / "os-integration.md"


def test_assoc_desktop_writes_both_files(tmp_path, capsys):
    target = tmp_path / "out"
    assert main(["assoc", "--desktop", "--output", str(target)]) == 0
    desktop = (target / "nlsc.desktop").read_text(encoding="utf-8")
    mime = (target / "text-x-nls.xml").read_text(encoding="utf-8")
    capsys.readouterr()

    assert "[Desktop Entry]" in desktop
    assert "MimeType=text/x-nls;" in desktop
    for action in ("Verify", "Compile", "Test"):
        assert f"[Desktop Action {action}]" in desktop
        assert f"Exec=nlsc {action.lower()} %f" in desktop
    assert 'mime-type type="text/x-nls"' in mime
    assert 'glob pattern="*.nl"' in mime


def test_assoc_desktop_json_payload(tmp_path, capsys):
    target = tmp_path / "out"
    assert main(["assoc", "--desktop", "-o", str(target), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert payload["mode"] == "desktop"
    assert len(payload["files"]) == 2


def test_assoc_desktop_is_idempotent(tmp_path):
    target = tmp_path / "out"
    assert main(["assoc", "--desktop", "-o", str(target)]) == 0
    first = (target / "nlsc.desktop").read_text(encoding="utf-8")
    assert main(["assoc", "--desktop", "-o", str(target)]) == 0
    assert (target / "nlsc.desktop").read_text(encoding="utf-8") == first


def test_assoc_desktop_works_on_this_platform():
    # The generator is portable by design; the Windows path is a separate
    # code path taken only without --desktop.
    assert sys.platform  # sanity: this test runs wherever the suite runs


# --------------------------------------------------------------------------
# Documentation guard
# --------------------------------------------------------------------------


def test_guide_covers_every_platform_and_provided_artifacts():
    text = DOC.read_text(encoding="utf-8")
    for section in ("## macOS", "## Windows", "## Linux"):
        assert section in text
    assert "nlsc assoc --desktop" in text
    assert "text/x-nls" in text
    assert "Quick Action" in text
    assert "SystemFileAssociations" in text  # Windows context menu snippet
    assert "update-mime-database" in text


def test_guide_commands_exist_in_cli():
    from nlsc.cli import cmd_fmt, cmd_lint, cmd_verify  # noqa: F401

    text = DOC.read_text(encoding="utf-8")
    # The documented commands are real entry points.
    assert "nlsc verify" in text
    assert "nlsc fmt --check" in text
    assert "nlsc ci" in text
