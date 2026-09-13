"""Issue #264: an incomplete scaffold must never be runnable or importable.

Default (permissive) compilation stays available — #190 made it visible, this
contract makes it *inert*:

- ``nlsc run`` and ``nlsc test`` refuse to execute a module whose LOGIC is
  unresolved, instead of executing it and reporting success.
- ``nlsc compile`` writes the scaffold to ``<stem>.draft.<ext>``, a name that
  cannot be imported as the module, so it can never be substituted into a
  build or picked up by a test run.

The reproducer is the ``calculate-tax`` example from PRD.md, which before this
contract compiled to a tax function returning ``None``, ran clean, and exited 0.
"""

from __future__ import annotations

import json

from nlsc.cli import main

SCAFFOLD = """@module tax_probe
@target python

[calculate-tax]
PURPOSE: Compute tax owed based on income and filing status
INPUTS:
  - income: number
GUARDS:
  - income >= 0 -> ValueError("Income cannot be negative")
LOGIC:
  1. Look up tax brackets for the income -> brackets
  2. Sum bracket amounts to get total_tax -> total_tax
RETURNS: total_tax

@test [calculate-tax] {
  calculate_tax(100) == 0
}

@main {
  print(calculate_tax(50000))
}
"""

COMPLETE = """@module complete_probe
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
LOGIC:
  1. total = a + b
RETURNS: total

@test [add] {
  add(2, 3) == 5
}

@main {
  print(add(2, 3))
}
"""


def _write(tmp_path, source: str, name: str):
    path = tmp_path / name
    path.write_text(source, encoding="utf-8")
    return path


# --------------------------------------------------------------------------
# run / test refuse to execute a scaffold
# --------------------------------------------------------------------------


def test_run_refuses_to_execute_a_scaffold(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, SCAFFOLD, "tax_probe.nl")

    code = main(["run", str(path)])
    captured = capsys.readouterr()

    assert code == 1, "running an unimplemented module must not report success"
    assert "ESCAF001" in captured.err
    assert "calculate-tax" in captured.err
    # The scaffold body must not have executed.
    assert "None" not in captured.out


def test_run_names_every_unresolved_anlu(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = SCAFFOLD.replace(
        "@main {",
        """[estimate-penalty]
PURPOSE: Estimate the late penalty
INPUTS:
  - owed: number
LOGIC:
  1. Apply the published penalty schedule -> penalty
RETURNS: penalty

@main {""",
    )
    path = _write(tmp_path, source, "tax_probe.nl")

    code = main(["run", str(path)])
    captured = capsys.readouterr()

    assert code == 1
    assert "calculate-tax" in captured.err
    assert "estimate-penalty" in captured.err


def test_test_refuses_scaffold_instead_of_reporting_assertion_failure(
    tmp_path, capsys, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, SCAFFOLD, "tax_probe.nl")

    code = main(["test", str(path)])
    captured = capsys.readouterr()

    assert code == 1
    assert "ESCAF001" in captured.err
    # The failure must name the cause, not surface as a mysterious
    # "assert None == 0" from a test run that should never have started.
    assert "assert None" not in captured.out


def test_run_still_executes_a_complete_module(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, COMPLETE, "complete_probe.nl")

    code = main(["run", str(path)])
    captured = capsys.readouterr()

    assert code == 0, captured.err
    assert "5" in captured.out


def test_test_still_runs_for_a_complete_module(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, COMPLETE, "complete_probe.nl")

    code = main(["test", str(path)])
    captured = capsys.readouterr()

    assert code == 0, captured.err + captured.out


def test_run_refusal_is_reported_in_json_mode(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, SCAFFOLD, "tax_probe.nl")

    code = main(["run", "--json", str(path)])
    captured = capsys.readouterr()

    assert code == 1
    payload = json.loads(captured.out)
    assert any(d["code"] == "ESCAF001" for d in payload["diagnostics"])


# --------------------------------------------------------------------------
# compile quarantines the artifact
# --------------------------------------------------------------------------


def test_compile_writes_scaffold_to_draft_artifact(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, SCAFFOLD, "tax_probe.nl")

    code = main(["compile", str(path)])
    captured = capsys.readouterr()

    assert code == 0, captured.err
    assert (tmp_path / "tax_probe.draft.py").exists()
    assert not (tmp_path / "tax_probe.py").exists(), (
        "a scaffold must never claim the module's importable filename"
    )
    assert "draft" in captured.out.lower()


def test_compile_writes_normal_artifact_for_complete_module(
    tmp_path, capsys, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, COMPLETE, "complete_probe.nl")

    code = main(["compile", str(path)])
    captured = capsys.readouterr()

    assert code == 0, captured.err
    assert (tmp_path / "complete_probe.py").exists()
    assert not (tmp_path / "complete_probe.draft.py").exists()


def test_draft_artifact_is_not_importable_under_the_module_name(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, SCAFFOLD, "tax_probe.nl")
    assert main(["compile", str(path)]) == 0

    import importlib.util

    assert importlib.util.find_spec is not None
    # There is no tax_probe.py for an importer to resolve.
    assert not (tmp_path / "tax_probe.py").exists()


def test_stale_artifact_is_replaced_by_the_draft(tmp_path, capsys, monkeypatch):
    """A module that regresses into a scaffold must not leave the old .py behind."""
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, COMPLETE, "drift_probe.nl")
    assert main(["compile", str(path)]) == 0
    assert (tmp_path / "drift_probe.py").exists()

    # Same module, now with unresolved LOGIC.
    regressed = COMPLETE.replace("1. total = a + b", "1. Add the two numbers -> total")
    path.write_text(regressed, encoding="utf-8")
    code = main(["compile", str(path)])
    captured = capsys.readouterr()

    assert code == 0, captured.err
    assert (tmp_path / "drift_probe.draft.py").exists()
    assert not (tmp_path / "drift_probe.py").exists(), (
        "the previously valid artifact must not survive as an importable stale build"
    )


def test_scaffold_emits_no_collectible_test_artifact(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, SCAFFOLD, "tax_probe.nl")

    assert main(["compile", str(path)]) == 0
    capsys.readouterr()

    assert not (tmp_path / "test_tax_probe.py").exists(), (
        "pytest would collect this and report a placeholder body as a logic bug"
    )


def test_complete_module_still_emits_its_test_artifact(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, COMPLETE, "complete_probe.nl")

    assert main(["compile", str(path)]) == 0
    capsys.readouterr()

    assert (tmp_path / "test_complete_probe.py").exists()


def test_resolved_scaffold_removes_its_superseded_draft(tmp_path, capsys, monkeypatch):
    """The inverse of the stale-artifact case: a draft must not outlive its fix."""
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, SCAFFOLD, "fix_probe.nl")
    assert main(["compile", str(path)]) == 0
    assert (tmp_path / "fix_probe.draft.py").exists()

    # Same module, LOGIC now executable.
    resolved = SCAFFOLD.replace(
        "  1. Look up tax brackets for the income -> brackets\n"
        "  2. Sum bracket amounts to get total_tax -> total_tax\n",
        "  1. income * 0.2 -> total_tax\n",
    )
    path.write_text(resolved, encoding="utf-8")
    code = main(["compile", str(path)])
    captured = capsys.readouterr()

    assert code == 0, captured.err
    assert (tmp_path / "fix_probe.py").exists()
    assert not (tmp_path / "fix_probe.draft.py").exists(), (
        "a superseded draft must not linger next to the real artifact"
    )


def test_explicit_output_path_is_honoured_but_warned(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, SCAFFOLD, "tax_probe.nl")

    code = main(["compile", str(path), "-o", "chosen.py"])
    captured = capsys.readouterr()

    assert code == 0, captured.err
    assert (tmp_path / "chosen.py").exists()
    assert "scaffold" in (captured.out + captured.err).lower()


def test_strict_compile_still_refuses_outright(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, SCAFFOLD, "tax_probe.nl")

    code = main(["compile", "--strict", str(path)])
    captured = capsys.readouterr()

    assert code == 1
    assert "EIR002" in captured.err
    assert not (tmp_path / "tax_probe.draft.py").exists()
    assert not (tmp_path / "tax_probe.py").exists()
