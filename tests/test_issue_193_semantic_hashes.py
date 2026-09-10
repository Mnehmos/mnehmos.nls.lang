"""Issue #193: lockfile hashes must cover executable semantics.

Regression fixtures run against the public APIs the issue reproducer
uses: get_anlu_changes, verify_lockfile, rebuild_from_lockfile.
"""

from __future__ import annotations

from nlsc.diff import get_anlu_changes
from nlsc.emitter import emit_python
from nlsc.lockfile import (
    generate_lockfile,
    hash_anlu,
    rebuild_from_lockfile,
    verify_lockfile,
)
from nlsc.parser import parse_nl_file

BASE_SOURCE = """@module hash_audit
[probe]
PURPOSE: Hash fixture
LOGIC:
  1. x = 1 + 0
RETURNS: x
"""


def _lock_for(source: str):
    nl_file = parse_nl_file(source)
    return nl_file, generate_lockfile(nl_file, emit_python(nl_file), "hash_audit.py")


def test_reproducer_logic_edit_invalidates_every_consumer():
    nl_file, lock = _lock_for(BASE_SOURCE)
    edited = parse_nl_file(BASE_SOURCE.replace("x = 1 + 0", "x = 2 + 0"))

    changes = get_anlu_changes(edited, lock)
    assert [c.status for c in changes] == ["modified"]

    assert verify_lockfile(lock, edited) != []

    rebuilt = rebuild_from_lockfile(edited, lock)
    assert rebuilt.used_cache is False


def test_reproducer_rebuild_never_reuses_stale_body():
    nl_file, lock = _lock_for(BASE_SOURCE)
    edited = parse_nl_file(BASE_SOURCE.replace("x = 1 + 0", "x = 2 + 0"))
    rebuilt = rebuild_from_lockfile(edited, lock)
    if rebuilt.code:
        namespace: dict = {}
        exec(rebuilt.code, namespace)  # noqa: S102
        assert namespace["probe"]() != 1


def test_guard_and_error_payload_changes_invalidate():
    guarded = """@module guard_audit
[divide]
PURPOSE: safe divide
INPUTS:
  - numerator: number
  - divisor: number
GUARDS:
  - divisor != 0 -> ValueError("Cannot divide by zero")
RETURNS: numerator / divisor
"""
    nl_file, lock = _lock_for(guarded)

    payload_edit = parse_nl_file(guarded.replace("Cannot divide by zero", "nope"))
    assert verify_lockfile(lock, payload_edit) != []

    condition_edit = parse_nl_file(guarded.replace("divisor != 0", "divisor > 0"))
    assert verify_lockfile(lock, condition_edit) != []

    # The unchanged case must still verify.
    assert verify_lockfile(lock, nl_file) == []


def test_input_constraint_changes_invalidate():
    constrained = """@module constraint_audit
[f]
PURPOSE: p
INPUTS:
  - age: number, > 0
LOGIC:
  1. x = age
RETURNS: x
"""
    nl_file, lock = _lock_for(constrained)
    edited = parse_nl_file(constrained.replace("> 0", ">= 1"))
    assert verify_lockfile(lock, edited) != []


def test_edge_case_changes_invalidate():
    edged = """@module edge_audit
[grade]
PURPOSE: p
INPUTS:
  - score: number
EDGE CASES:
  - score > 100 -> return 100
RETURNS: score
"""
    nl_file, lock = _lock_for(edged)
    edited = parse_nl_file(edged.replace("return 100", "return 99"))
    assert verify_lockfile(lock, edited) != []
    assert verify_lockfile(lock, parse_nl_file(edged)) == []


def test_insignificant_formatting_and_docs_do_not_invalidate():
    nl_file, lock = _lock_for(BASE_SOURCE)

    spaced = parse_nl_file(BASE_SOURCE.replace("x = 1 + 0", "x =  1+0"))
    assert verify_lockfile(lock, spaced) == []

    reworded = parse_nl_file(BASE_SOURCE.replace("Hash fixture", "Another wording"))
    assert verify_lockfile(lock, reworded) == []

    commented = parse_nl_file("# a leading comment\n" + BASE_SOURCE)
    assert verify_lockfile(lock, commented) == []


def test_line_moves_do_not_change_semantic_hash():
    # Line numbers are spans, not semantics: adding lines above shifts
    # spans but must not alter the semantic identity.
    a = hash_anlu(parse_nl_file(BASE_SOURCE).anlus[0])
    shifted = hash_anlu(parse_nl_file("\n\n\n" + BASE_SOURCE).anlus[0])
    assert a == shifted


def test_semantic_hashes_are_deterministic():
    nl_file = parse_nl_file(BASE_SOURCE)
    assert hash_anlu(nl_file.anlus[0]) == hash_anlu(parse_nl_file(BASE_SOURCE).anlus[0])


def test_dependency_signature_change_invalidates_caller():
    pair = """@module dep_audit
[increment]
PURPOSE: add one
INPUTS:
  - value: number
RETURNS: value + 1

[caller]
PURPOSE: use increment
LOGIC:
  1. y = [increment](1)
RETURNS: y
DEPENDS: [increment]
"""
    nl_file, lock = _lock_for(pair)

    # Changing the dependency's signature must invalidate the caller too.
    edited = parse_nl_file(pair.replace("  - value: number", "  - value: integer"))
    errors = verify_lockfile(lock, edited)
    assert any("caller" in e for e in errors)


def test_legacy_lock_entries_are_conservatively_invalidated():
    # Old-format lock entries (pre-semver scheme) must never compare equal
    # to a new semantic hash; they are treated as stale and rebuilt.
    from nlsc.lockfile import ANLULock, Lockfile, ModuleLock

    nl_file = parse_nl_file(BASE_SOURCE)
    lock = Lockfile()
    module_lock = ModuleLock(source_hash="sha256:legacy")
    module_lock.anlus["probe"] = ANLULock(
        source_hash="sha256:000000000000legacy",
        output_hash="sha256:0",
        output_lines=1,
        generated_code="def probe():\n    return 999\n",
    )
    lock.modules[nl_file.module.name] = module_lock

    assert verify_lockfile(lock, nl_file) != []
    rebuilt = rebuild_from_lockfile(nl_file, lock)
    assert rebuilt.used_cache is False
