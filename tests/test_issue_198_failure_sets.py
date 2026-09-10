"""Issue #198: checked failure sets and a portable typed exception contract.

Scope of this slice: failure-set inference over the IR (guards, callee
propagation, conservative unknown markers), a portable TypeScript error
runtime so guard failures preserve type/code/message without undefined
constructors, and dependency-sensitive hashes.
"""

from __future__ import annotations

import pytest

from nlsc.emitter import emit_python
from nlsc.emitter_typescript import emit_typescript
from nlsc.lockfile import hash_anlu
from nlsc.lowering import lower_module
from nlsc.parser import parse_nl_file
from nlsc.typecheck import check_module

GUARDED = """@module guarded_call
[divide]
PURPOSE: safe divide
INPUTS:
  - numerator: number
  - divisor: number
GUARDS:
  - divisor != 0 -> ValueError("Cannot divide by zero")
RETURNS: numerator / divisor
"""

CODED_GUARD = """@module coded
[auth]
PURPOSE: authenticate
INPUTS:
  - token: string
GUARDS:
  - len(token) > 0 -> AuthError(MISSING, "Token required")
RETURNS: True
"""

PROPAGATION = """@module propagation
[reject]
PURPOSE: Always raise when called
GUARDS:
  - False -> ValueError("called")
RETURNS: 0

[probe]
PURPOSE: Call reject
LOGIC:
  1. [reject]()
DEPENDS: [reject]
RETURNS: 0
"""

FOREIGN_FAILURE = """@module foreign_failure
[probe]
PURPOSE: call foreign code
LOGIC:
  1. parse_payload(payload) -> result
RETURNS: result
"""

PURE = """@module pure
[add]
PURPOSE: add
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
"""


def _op(module, name):
    matches = [op for op in module.operations if op.name == name]
    assert matches, f"operation {name} not found"
    return matches[0]


# --------------------------------------------------------------------------
# Failure-set inference over the IR
# --------------------------------------------------------------------------


def test_guard_failure_is_in_the_operation_failure_set():
    module = lower_module(parse_nl_file(GUARDED))
    failures = _op(module, "divide").failures
    assert failures is not None, "analyzed operations carry a failure set"
    entries = [(f.error_type, f.code, f.message) for f in failures]
    assert ("ValueError", None, "Cannot divide by zero") in entries


def test_coded_guard_failure_preserves_code_and_message():
    module = lower_module(parse_nl_file(CODED_GUARD))
    failures = _op(module, "auth").failures or ()
    entries = [(f.error_type, f.code, f.message) for f in failures]
    assert ("AuthError", "MISSING", "Token required") in entries


def test_callee_failures_propagate_into_caller_summary():
    module = lower_module(parse_nl_file(PROPAGATION))
    probe_failures = _op(module, "probe").failures or ()
    entries = [(f.error_type, f.code, f.message) for f in probe_failures]
    assert ("ValueError", None, "called") in entries, entries


def test_foreign_calls_carry_a_conservative_unknown_marker():
    module = lower_module(parse_nl_file(FOREIGN_FAILURE))
    failures = _op(module, "probe").failures or ()
    assert any(f.origin == "unknown" for f in failures), [
        (f.error_type, f.origin) for f in failures
    ]


def test_pure_operations_have_analyzed_empty_failure_sets():
    module = lower_module(parse_nl_file(PURE))
    failures = _op(module, "add").failures
    # Analyzed-empty, not None (never-analyzed); unknown-free.
    assert failures == ()
    assert not any(f.origin == "unknown" for f in failures)


def test_failure_sets_are_deterministic():
    m1 = lower_module(parse_nl_file(PROPAGATION))
    m2 = lower_module(parse_nl_file(PROPAGATION))
    assert _op(m1, "probe").failures == _op(m2, "probe").failures


# --------------------------------------------------------------------------
# Portable TypeScript error runtime
# --------------------------------------------------------------------------


def test_typescript_defines_guard_error_classes():
    code = emit_typescript(parse_nl_file(GUARDED))
    assert "class ValueError extends Error" in code
    assert 'throw new ValueError("Cannot divide by zero"' in code


def test_typescript_preserves_error_code_and_message():
    code = emit_typescript(parse_nl_file(CODED_GUARD))
    assert "class AuthError extends Error" in code
    assert 'new AuthError("Token required", "MISSING")' in code


def test_typescript_defines_each_error_class_once():
    source = PROPAGATION + "\n[other]\nPURPOSE: also reject\nGUARDS:\n  - False -> ValueError(\"nope\")\nRETURNS: 0\n"
    code = emit_typescript(parse_nl_file(source))
    assert code.count("class ValueError extends Error") == 1


def test_python_guard_behavior_is_unchanged():
    namespace: dict = {}
    exec(emit_python(parse_nl_file(GUARDED)), namespace)  # noqa: S102
    assert namespace["divide"](6, 3) == 2.0
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        namespace["divide"](1, 0)


def test_python_coded_guard_raises_with_code():
    namespace: dict = {}
    exec(emit_python(parse_nl_file(CODED_GUARD)), namespace)  # noqa: S102
    with pytest.raises(Exception) as excinfo:
        namespace["auth"]("")
    assert "Token required" in str(excinfo.value)


# --------------------------------------------------------------------------
# Checked surface: undeclared error constructors
# --------------------------------------------------------------------------


def test_undeclared_error_type_warns_strict_only():
    # AuthError is not a known builtin and not a declared @type.
    result = check_module(parse_nl_file(CODED_GUARD))
    assert "ESEM012" in [d.code for d in result.warnings]
    assert not any(d.code == "ESEM012" for d in result.errors)


def test_declared_error_type_does_not_warn():
    source = """@module declared_error
@type AuthError {
  message: string
}

[auth]
PURPOSE: authenticate
INPUTS:
  - token: string
GUARDS:
  - len(token) > 0 -> AuthError("Token required")
RETURNS: True
"""
    result = check_module(parse_nl_file(source))
    assert not any(d.code == "ESEM012" for d in result.warnings)


def test_builtin_error_types_do_not_warn():
    result = check_module(parse_nl_file(GUARDED))
    assert not any(d.code == "ESEM012" for d in result.warnings)


# --------------------------------------------------------------------------
# Lockfile identity is sensitive to callee failure contracts
# --------------------------------------------------------------------------


def test_caller_hash_changes_when_callee_guard_payload_changes():
    before = parse_nl_file(PROPAGATION)
    after = parse_nl_file(PROPAGATION.replace('ValueError("called")', 'ValueError("changed")'))
    caller_before = [a for a in before.anlus if a.identifier == "probe"][0]
    caller_after = [a for a in after.anlus if a.identifier == "probe"][0]
    assert hash_anlu(caller_before, before) != hash_anlu(caller_after, after)
