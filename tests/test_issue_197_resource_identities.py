"""Issue #197 slice: resource identities in inferred effects + EFFECTS contracts.

Method calls now name the resource they may mutate (``write(items)``)
instead of collapsing to a blanket ``unknown``, callee effects substitute
the caller's argument names, and an optional ``EFFECTS:`` line declares an
upper bound checked as ``EFX001`` (malformed declarations are ``EFX002``).
"""

from __future__ import annotations

import json

import pytest

from nlsc.cli import main
from nlsc.effects import (
    EffectDeclarationError,
    declaration_covers,
    parse_effect_declaration,
    uncovered_effects,
)
from nlsc.ir import IREffectSpec
from nlsc.lowering import lower_module
from nlsc.parser import parse_nl_file

METHOD_ON_PARAM = """@module method_param
[append-one]
PURPOSE: append to a list
INPUTS:
  - items: list of number
LOGIC:
  1. items.append(1)
RETURNS: 0
"""

METHOD_ON_LOCAL = """@module method_local
[build]
PURPOSE: build a list locally
LOGIC:
  1. result = []
  2. result.append(1)
RETURNS: result
"""

FOREIGN_CALL = """@module foreign_call
[log]
PURPOSE: log something
LOGIC:
  1. log_event("hello")
RETURNS: 0
"""

SUBSTITUTION = """@module substitution
[mutate]
PURPOSE: append to a list
INPUTS:
  - items: list of number
LOGIC:
  1. items.append(1)
RETURNS: 0

[caller]
PURPOSE: pass rows through
INPUTS:
  - rows: list of number
LOGIC:
  1. [mutate](rows)
RETURNS: 0
DEPENDS: [mutate]
"""

INTERNAL_ONLY = """@module internal_only
[helper]
PURPOSE: mutate a local list
LOGIC:
  1. scratch = []
  2. scratch.append(1)
RETURNS: 0

[caller]
PURPOSE: call the helper
LOGIC:
  1. [helper]()
RETURNS: 0
DEPENDS: [helper]
"""

PURE = """@module pure_ops
[add]
PURPOSE: add
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
"""

DECLARED_PURE_VIOLATED = """@module claimed_pure
[sweep]
PURPOSE: claims purity but mutates
INPUTS:
  - items: list of number
EFFECTS: pure
LOGIC:
  1. items.append(1)
RETURNS: 0
"""

DECLARED_WRITE_OK = """@module declared_write
[sweep]
PURPOSE: declares its write
INPUTS:
  - items: list of number
EFFECTS: write(items)
LOGIC:
  1. items.append(1)
RETURNS: 0
"""

DECLARED_UNKNOWN_OK = """@module declared_unknown
[log]
PURPOSE: declares unknown
EFFECTS: unknown
LOGIC:
  1. log_event("hello")
RETURNS: 0
"""

DECLARED_READ_MISMATCH = """@module declared_read
[sweep]
PURPOSE: reads but is declared to read
INPUTS:
  - items: list of number
EFFECTS: read(items)
LOGIC:
  1. items.append(1)
RETURNS: 0
"""

MALFORMED = """@module malformed
[sweep]
PURPOSE: bad declaration
INPUTS:
  - items: list of number
EFFECTS: writes(items)
LOGIC:
  1. items.append(1)
RETURNS: 0
"""


def _op(source: str, name: str):
    module = lower_module(parse_nl_file(source, source_path="probe.nl"))
    return {operation.name: operation for operation in module.operations}[name]


def _write(tmp_path, source: str):
    path = tmp_path / "probe.nl"
    path.write_text(source, encoding="utf-8")
    return path


# --------------------------------------------------------------------------
# Inferred resource identities
# --------------------------------------------------------------------------


def test_method_call_on_param_is_a_named_write():
    effects = _op(METHOD_ON_PARAM, "append-one").effects or ()
    assert ("write", "items") in {(e.kind, e.resource) for e in effects}
    assert any(e.origin == "call" for e in effects)


def test_method_call_on_local_binding_is_a_named_write():
    effects = _op(METHOD_ON_LOCAL, "build").effects or ()
    assert ("write", "result") in {(e.kind, e.resource) for e in effects}


def test_foreign_call_stays_unknown():
    effects = _op(FOREIGN_CALL, "log").effects or ()
    assert any(e.kind == "unknown" for e in effects)


def test_pure_structural_code_has_empty_effects():
    assert _op(PURE, "add").effects == ()


def test_callee_effects_substitute_caller_argument_names():
    effects = _op(SUBSTITUTION, "caller").effects or ()
    assert ("write", "rows") in {(e.kind, e.resource) for e in effects}
    assert all(e.origin == "callee" for e in effects)


def test_callee_internal_resource_propagates_as_unknown():
    effects = _op(INTERNAL_ONLY, "caller").effects or ()
    assert any(e.kind == "unknown" for e in effects)


def test_effect_inference_is_deterministic():
    first = _op(METHOD_ON_PARAM, "append-one").effects
    second = _op(METHOD_ON_PARAM, "append-one").effects
    assert first == second


# --------------------------------------------------------------------------
# EFFECTS declarations
# --------------------------------------------------------------------------


def test_declaration_parsing_forms():
    assert parse_effect_declaration("pure") == ()
    assert parse_effect_declaration("unknown")[0].kind == "unknown"
    assert parse_effect_declaration("write(items)")[0].resource == "items"
    assert parse_effect_declaration("read(log), write(items)")[1].kind == "write"
    assert parse_effect_declaration("read")[0].resource is None


def test_declaration_rejects_malformed_forms():
    for bad in ("", "writes(items)", "pure, write(x)", "read()", "write(items"):
        with pytest.raises(EffectDeclarationError):
            parse_effect_declaration(bad)


def test_declaration_coverage_rules():
    declared = parse_effect_declaration("write(items)")
    assert declaration_covers(declared, IREffectSpec(kind="write", resource="items"))
    assert not declaration_covers(
        declared, IREffectSpec(kind="write", resource="other")
    )
    assert not declaration_covers(
        declared, IREffectSpec(kind="read", resource="items")
    )
    unknown_declared = parse_effect_declaration("unknown")
    assert declaration_covers(
        unknown_declared, IREffectSpec(kind="write", resource="anything")
    )
    assert uncovered_effects(parse_effect_declaration("pure"), (IREffectSpec(),)) != []


def test_verify_rejects_exceeded_pure_declaration(tmp_path, capsys):
    path = _write(tmp_path, DECLARED_PURE_VIOLATED)
    assert main(["verify", str(path)]) == 1
    err = capsys.readouterr().err
    assert "EFX001" in err
    assert "write(items)" in err


def test_verify_accepts_satisfied_declarations(tmp_path):
    for source in (DECLARED_WRITE_OK, DECLARED_UNKNOWN_OK):
        path = _write(tmp_path, source)
        assert main(["verify", str(path)]) == 0


def test_verify_rejects_read_declaration_covering_a_write(tmp_path, capsys):
    path = _write(tmp_path, DECLARED_READ_MISMATCH)
    assert main(["verify", str(path)]) == 1
    assert "EFX001" in capsys.readouterr().err


def test_malformed_declaration_is_efx002(tmp_path, capsys):
    path = _write(tmp_path, MALFORMED)
    assert main(["verify", str(path)]) == 1
    assert "EFX002" in capsys.readouterr().err


def test_compile_rejects_exceeded_declaration(tmp_path, capsys):
    path = _write(tmp_path, DECLARED_PURE_VIOLATED)
    assert main(["compile", str(path)]) == 1
    assert "EFX001" in capsys.readouterr().err


def test_declared_effects_json_payload(tmp_path, capsys):
    path = _write(tmp_path, DECLARED_WRITE_OK)
    assert main(["ir", "--json", str(path)]) == 0
    payload = json.loads(capsys.readouterr().out)
    declared = payload["ir"]["operations"][0]["declared_effects"]
    assert declared == [{"kind": "write", "resource": "items", "origin": "declared"}]


def test_effects_line_parses_on_both_backends(tmp_path):
    from nlsc.parser_treesitter import is_available, parse_nl_file_treesitter

    source = DECLARED_WRITE_OK
    regex_parse = parse_nl_file(source, source_path="probe.nl")
    assert regex_parse.anlus[0].declared_effects == "write(items)"

    if is_available():
        ts_parse = parse_nl_file_treesitter(source, source_path="probe.nl")
        assert ts_parse.anlus[0].declared_effects == "write(items)"


def test_files_without_declarations_are_unaffected(tmp_path):
    path = _write(tmp_path, METHOD_ON_PARAM)
    assert main(["verify", str(path)]) == 0


def test_semantic_hash_scheme_is_sem3():
    from nlsc.lockfile import SEMANTIC_HASH_SCHEME

    assert SEMANTIC_HASH_SCHEME == "sem3"


def test_resource_identity_changes_the_semantic_hash(tmp_path):
    from nlsc.lockfile import hash_anlu

    anlu = parse_nl_file(METHOD_ON_PARAM, source_path="probe.nl").anlus[0]
    method_hash = hash_anlu(anlu)
    foreign_anlu = parse_nl_file(FOREIGN_CALL, source_path="probe.nl").anlus[0]
    assert method_hash != hash_anlu(foreign_anlu)


# --------------------------------------------------------------------------
# Review follow-ups: parity, soundness, and coverage gaps
# --------------------------------------------------------------------------


def test_effects_header_is_case_insensitive_on_both_backends(tmp_path):
    """Section headers are case-insensitive; the tree-sitter escape must match."""
    source = DECLARED_WRITE_OK.replace("EFFECTS:", "effects:")
    regex_parse = parse_nl_file(source, source_path="probe.nl")
    assert regex_parse.anlus[0].declared_effects == "write(items)"

    from nlsc.pipeline import parse_nl_path_auto

    path = _write(tmp_path, source)
    parsed = parse_nl_path_auto(path)
    assert parsed.anlus[0].declared_effects == "write(items)"


def test_blank_declaration_is_efx002(tmp_path, capsys):
    source = DECLARED_WRITE_OK.replace("EFFECTS: write(items)", "EFFECTS:")
    path = _write(tmp_path, source)
    assert main(["compile", str(path)]) == 1
    assert "EFX002" in capsys.readouterr().err


def test_kwargs_substitution_uses_the_named_parameter():
    source = """@module kwargs_sub
[mutate]
PURPOSE: append
INPUTS:
  - items: list of number
LOGIC:
  1. items.append(1)
RETURNS: 0

[caller]
PURPOSE: call with a kwarg
INPUTS:
  - rows: list of number
LOGIC:
  1. [mutate](items=rows)
RETURNS: 0
DEPENDS: [mutate]
"""
    effects = _op(source, "caller").effects or ()
    assert ("write", "rows") in {(e.kind, e.resource) for e in effects}


def test_method_call_on_field_root_is_a_named_write():
    source = """@module field_root
[sweep]
PURPOSE: mutate through a field
INPUTS:
  - order: Order
LOGIC:
  1. order.items.append(1)
RETURNS: 0
"""
    effects = _op(source, "sweep").effects or ()
    assert any(e.kind == "unknown" for e in effects) or (
        "write",
        "order",
    ) in {(e.kind, e.resource) for e in effects}
    assert ("write", "order") in {(e.kind, e.resource) for e in effects}


def test_unattributable_method_base_stays_unknown():
    source = """@module unnamed_base
[probe]
PURPOSE: method on a call result
LOGIC:
  1. make-list().append(1)
RETURNS: 0
"""
    effects = _op(source, "probe").effects or ()
    assert any(e.kind == "unknown" for e in effects)


def test_guard_calls_propagate_effects():
    """A call in a GUARD is still a call: pure must not be certified."""
    source = """@module guard_call
[impure]
PURPOSE: mutate
INPUTS:
  - items: list of number
LOGIC:
  1. items.append(1)
RETURNS: 0

[caller]
PURPOSE: calls in a guard condition
INPUTS:
  - rows: list of number
GUARDS:
  - [impure](rows) == 0 -> ValueError("impure call failed")
RETURNS: 0
DEPENDS: [impure]
"""
    effects = _op(source, "caller").effects or ()
    assert ("write", "rows") in {(e.kind, e.resource) for e in effects}, effects


def test_declared_pure_caller_with_impure_guard_call_is_rejected(tmp_path, capsys):
    """The guard-call propagation is load-bearing for EFX001 soundness."""
    source = """@module guard_pure
[impure]
PURPOSE: mutate
INPUTS:
  - items: list of number
LOGIC:
  1. items.append(1)
RETURNS: 0

[caller]
PURPOSE: claims pure but calls impure in a guard
INPUTS:
  - rows: list of number
EFFECTS: pure
GUARDS:
  - [impure](rows) == 0 -> ValueError("impure call failed")
RETURNS: 0
DEPENDS: [impure]
"""
    path = _write(tmp_path, source)
    assert main(["verify", str(path)]) == 1
    assert "EFX001" in capsys.readouterr().err


def test_declaration_only_change_changes_the_semantic_hash():
    from nlsc.lockfile import hash_anlu

    declared = parse_nl_file(DECLARED_WRITE_OK, source_path="probe.nl").anlus[0]
    undeclared = parse_nl_file(
        DECLARED_WRITE_OK.replace("EFFECTS: write(items)\n", ""),
        source_path="probe.nl",
    ).anlus[0]
    assert hash_anlu(declared) != hash_anlu(undeclared)


def test_declaration_renders_in_canonical_ir(tmp_path, capsys):
    path = _write(tmp_path, DECLARED_WRITE_OK)
    assert main(["ir", str(path)]) == 0
    assert "(declares (effect write items origin=declared))" in capsys.readouterr().out


def test_efx002_is_fatal_in_every_executable_path(tmp_path, capsys):
    path = _write(tmp_path, MALFORMED)
    for command in (["compile", str(path)], ["run", str(path)], ["ci", str(path)]):
        assert main(command) == 1, command
        assert "EFX002" in capsys.readouterr().err


def test_bare_read_and_write_cover_any_resource():
    assert declaration_covers(
        parse_effect_declaration("write"),
        IREffectSpec(kind="write", resource="anything"),
    )
    assert not declaration_covers(
        parse_effect_declaration("read"),
        IREffectSpec(kind="write", resource="anything"),
    )


def test_pure_declaration_on_empty_inference_passes(tmp_path):
    source = """@module truly_pure
[add]
PURPOSE: add
INPUTS:
  - a: number
  - b: number
EFFECTS: pure
RETURNS: a + b
"""
    path = _write(tmp_path, source)
    assert main(["verify", str(path)]) == 0


# --------------------------------------------------------------------------
# Pure builtins and declared-type constructors (review + showcase finding)
# --------------------------------------------------------------------------

BUILTIN_CALL = """@module builtin_pure
[clamp-percent]
PURPOSE: clamp a percentage
INPUTS:
  - value: number
EFFECTS: pure
RETURNS: min(100, max(0, value))
"""

TYPE_CONSTRUCTOR = """@module type_ctor
@type Waypoint
  - label: string

[base]
PURPOSE: the base waypoint
EFFECTS: pure
RETURNS: Waypoint("base")
"""

GUARD_BUILTIN = """@module guard_builtin
[authorize]
PURPOSE: refuse empty routes
INPUTS:
  - route: list of number
EFFECTS: pure
GUARDS:
  - len(route) > 0 -> ValueError("empty route")
RETURNS: 0
"""


def test_documented_builtins_are_pure():
    effects = _op(BUILTIN_CALL, "clamp-percent").effects
    assert effects == ()


def test_declared_type_constructors_are_pure():
    effects = _op(TYPE_CONSTRUCTOR, "base").effects
    assert effects == ()


def test_builtins_in_guards_are_pure():
    effects = _op(GUARD_BUILTIN, "authorize").effects
    assert effects == ()


def test_declared_pure_with_builtins_passes_the_gate(tmp_path, capsys):
    for source in (BUILTIN_CALL, TYPE_CONSTRUCTOR, GUARD_BUILTIN):
        path = _write(tmp_path, source)
        assert main(["verify", str(path)]) == 0, source


def test_unknown_foreign_calls_still_infer_unknown():
    effects = _op(FOREIGN_CALL, "log").effects or ()
    assert any(e.kind == "unknown" for e in effects)
