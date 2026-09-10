"""Issue #196: branch outputs, binding mutation, and joined values.

Behavior contract:

- A value bound on only one branch path and used afterwards is rejected
  before either emitter runs (fatal, both modes, same diagnostic per target).
- Explicit ``IF ... THEN ... ELSE ...`` makes a branch total: both paths
  bind, and the program executes identically under Python (and emits
  valid block-scoped TypeScript).
- Plain rebinding is an immutable-binding violation: strict-only.
- Augmented assignment on an undefined value is fatal.
"""

from __future__ import annotations

import json

from nlsc.cli import main
from nlsc.emitter import emit_python
from nlsc.emitter_typescript import emit_typescript
from nlsc.lowering import lower_module
from nlsc.parser import parse_nl_file
from nlsc.typecheck import check_module

PARTIAL_BRANCH = """@module branch_probe
[probe]
PURPOSE: Conditional output
INPUTS:
  - flag: boolean
LOGIC:
  1. IF flag THEN 1 -> x
RETURNS: x
"""

TOTAL_BRANCH = """@module branch_total
[probe]
PURPOSE: Conditional output on both paths
INPUTS:
  - flag: boolean
LOGIC:
  1. IF flag THEN 1 -> x ELSE 0 -> x
RETURNS: x
"""

REBINDING = """@module rebind
[probe]
PURPOSE: rebind a value
LOGIC:
  1. x = 1
  2. x = 2
RETURNS: x
"""

AUG_UNDEFINED = """@module aug_undef
[probe]
PURPOSE: accumulate onto nothing
LOGIC:
  1. acc += 1
RETURNS: acc
"""

NESTED_JOINS = """@module nested_joins
[probe]
PURPOSE: nested branches
INPUTS:
  - a: boolean
  - b: boolean
LOGIC:
  1. IF a THEN 1 -> x ELSE 0 -> x
  2. IF b THEN x + 1 -> y ELSE x - 1 -> y
RETURNS: y
"""

USE_INSIDE_ARM = """@module arm_scope
[probe]
PURPOSE: bind and use inside one arm
INPUTS:
  - flag: boolean
LOGIC:
  1. IF flag THEN 1 -> x
  2. IF flag THEN [consume](x)
RETURNS: 0

[consume]
PURPOSE: consume
INPUTS:
  - value: number
RETURNS: value
"""


def _write(tmp_path, source: str):
    path = tmp_path / "probe.nl"
    path.write_text(source, encoding="utf-8")
    return path


def _exec(code: str) -> dict:
    namespace: dict = {}
    exec(code, namespace)  # noqa: S102
    return namespace


# --------------------------------------------------------------------------
# IR shape: ELSE lowers to a branch with both regions
# --------------------------------------------------------------------------


def test_else_lowers_to_branch_regions():
    module = lower_module(parse_nl_file(TOTAL_BRANCH))
    (op,) = module.operations
    (branch,) = op.body
    assert branch.__class__.__name__ == "IRBranch"
    assert branch.otherwise, "ELSE arm must lower into the otherwise region"


# --------------------------------------------------------------------------
# Fatal: partial branch output used afterwards
# --------------------------------------------------------------------------


def test_partial_branch_output_is_fatal():
    result = check_module(parse_nl_file(PARTIAL_BRANCH))
    codes = [d.code for d in result.errors]
    assert "ESEM010" in codes
    diag = [d for d in result.errors if d.code == "ESEM010"][0]
    assert diag.line is not None
    assert "'x'" in diag.message


def test_partial_branch_reproducer_fails_verify_and_compile(tmp_path, capsys, monkeypatch):
    path = _write(tmp_path, PARTIAL_BRANCH)
    assert main(["verify", str(path)]) == 1
    assert "ESEM010" in capsys.readouterr().err

    monkeypatch.chdir(tmp_path)
    assert main(["compile", str(path)]) == 1
    assert "ESEM010" in capsys.readouterr().err
    assert not (tmp_path / "probe.py").exists()


def test_partial_branch_fails_identically_for_both_targets(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, PARTIAL_BRANCH)
    messages = []
    for extra in ([], ["-t", "typescript"]):
        assert main(["compile", *extra, str(path)]) == 1
        err = capsys.readouterr().err
        messages.append(
            [line for line in err.splitlines() if "ESEM010" in line][0].strip()
        )
    assert messages[0] == messages[1]


def test_partial_branch_json_diagnostic(tmp_path, capsys):
    path = _write(tmp_path, PARTIAL_BRANCH)
    assert main(["verify", "--json", str(path)]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert "ESEM010" in [d["code"] for d in payload["diagnostics"]]


# --------------------------------------------------------------------------
# Total branches: same value on both paths, valid on both targets
# --------------------------------------------------------------------------


def test_total_branch_passes_checks():
    result = check_module(parse_nl_file(TOTAL_BRANCH))
    assert result.errors == []
    assert result.warnings == []


def test_total_branch_executes_identically_on_both_paths():
    namespace = _exec(emit_python(parse_nl_file(TOTAL_BRANCH)))
    assert namespace["probe"](True) == 1
    assert namespace["probe"](False) == 0


def test_total_branch_typescript_hoists_joined_binding():
    code = emit_typescript(parse_nl_file(TOTAL_BRANCH))
    assert "if (__nls_truthy(flag))" in code
    assert "else" in code
    # The joined binding must escape both block scopes: declared once at
    # function scope, assigned in each arm (no duplicate const).
    assert "let x" in code
    assert code.count("const x") == 0


def test_nested_joins_pass_and_execute():
    result = check_module(parse_nl_file(NESTED_JOINS))
    assert result.errors == []
    namespace = _exec(emit_python(parse_nl_file(NESTED_JOINS)))
    assert namespace["probe"](True, True) == 2
    assert namespace["probe"](True, False) == 0
    assert namespace["probe"](False, True) == 1
    assert namespace["probe"](False, False) == -1


def test_partial_use_inside_a_later_arm_is_also_rejected():
    # Conservative rule: the checker never infers that two IF steps share
    # the same condition, so a value partial after step 1 cannot be used
    # in step 2's arm. Migrate to IF/THEN/ELSE or restructure.
    result = check_module(parse_nl_file(USE_INSIDE_ARM))
    assert "ESEM010" in [d.code for d in result.errors]


# --------------------------------------------------------------------------
# Rebinding: immutable bindings in checked mode
# --------------------------------------------------------------------------


def test_plain_rebinding_is_strict_only():
    result = check_module(parse_nl_file(REBINDING))
    assert result.errors == []
    assert [d.code for d in result.warnings] == ["ESEM011"]


def test_augmented_binding_on_undefined_is_fatal():
    result = check_module(parse_nl_file(AUG_UNDEFINED))
    codes = [d.code for d in result.errors]
    assert "ESEM004" in codes


def test_rebinding_fails_strict_verify(tmp_path, capsys):
    path = _write(tmp_path, REBINDING)
    assert main(["verify", "--strict", str(path)]) == 1
    assert "ESEM011" in capsys.readouterr().err
    # Default mode still compiles (legacy behavior) with a warning.
    assert main(["verify", str(path)]) == 0
    assert "ESEM011" in capsys.readouterr().err


def test_rebound_name_typescript_emits_valid_declarations(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, REBINDING)
    assert main(["compile", str(path), "-t", "typescript"]) == 0
    code = (tmp_path / "probe.ts").read_text(encoding="utf-8")
    # One declaration, then reassignment; never duplicate const.
    assert "let x" in code
    assert code.count("const x") == 0
    assert "x = 2" in code
