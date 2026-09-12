"""Issue #224: distribution contract — manifest, workspace script, health.

The dashboard contract is executable: `.mnehmos/tool.json` declares the
workspace actions, and `scripts/nls_workspace.py` implements exactly
those actions. These tests keep the two in sync and prove the whole
workflow runs end to end with the current interpreter.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO / ".mnehmos" / "tool.json"


def _manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _run_action(action: str, *extra: str) -> dict:
    result = subprocess.run(
        [sys.executable, "scripts/nls_workspace.py", action, *extra],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    text = result.stdout
    payload = json.loads(text[text.find("{") :])
    return payload


# --------------------------------------------------------------------------
# Manifest structure
# --------------------------------------------------------------------------


def test_manifest_has_required_contract_sections():
    manifest = _manifest()
    assert manifest["schema"] == "mnehmos.tool/1"
    assert manifest["name"] == "nlsc"
    assert manifest["distribution"]["channel"] == "pypi"
    assert manifest["distribution"]["install"]["python"] == ">=3.11"
    assert manifest["distribution"]["provenance"]["publishing"].startswith(
        "PyPI Trusted Publishing"
    )
    assert manifest["distribution"]["npm_bridge"]["status"] == "not-provided"


def test_manifest_workspace_actions_reference_the_script():
    manifest = _manifest()
    script = manifest["workspace"]["script"]
    assert (REPO / script).exists()
    for name, argv in manifest["workspace"]["actions"].items():
        assert argv[1] == script, name
        assert argv[-1] == "--json", name


def test_manifest_actions_match_script_actions(tmp_path):
    manifest = _manifest()
    declared = set(manifest["workspace"]["actions"])
    help_result = subprocess.run(
        [sys.executable, manifest["workspace"]["script"], "--help"],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    for action in declared:
        assert action in help_result.stdout


def test_manifest_capabilities_match_the_toolchain():
    manifest = _manifest()
    capabilities = manifest["capabilities"]
    assert set(capabilities["targets"]) == {"python", "typescript"}
    assert capabilities["language_server"]["command"] == ["nlsc", "lsp"]
    for feature in ("diagnostics", "lint", "formatting", "hover"):
        assert feature in capabilities["language_server"]["features"]
    for gate in ("verify", "compile", "test", "ci", "lint", "fmt"):
        assert gate in capabilities["quality_gates"]


# --------------------------------------------------------------------------
# The workspace workflow runs end to end
# --------------------------------------------------------------------------


def test_workspace_workflow_with_current_interpreter(tmp_path):
    root = str(tmp_path / "ws")

    bootstrap = _run_action("bootstrap", "--root", root, "--no-venv")
    assert bootstrap["ok"] is True
    assert bootstrap["nlsc_version"].startswith("nlsc ")

    health = _run_action("health", "--root", root)
    assert health["ok"] is True
    assert health["sample_exists"] is True
    assert health["current_python_ok"] is True

    verify = _run_action("verify", "--root", root)
    assert verify["ok"] is True

    tests = _run_action("test", "--root", root)
    assert tests["ok"] is True
    assert tests["nlsc"]["stages"]["test"] == "passed"

    compiled = _run_action("compile-sample", "--root", root)
    assert compiled["ok"] is True
    assert compiled["produced"] is True
