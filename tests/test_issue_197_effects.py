"""Issue #197 (conservative slice): infer operation effect contracts.

With no effect surface syntax yet, the contract is deliberately coarse
but honest: every operation carries an *analyzed* effect set where pure
structural code is empty, and anything that could touch the world —
foreign calls, method calls, literal implementations — contributes an
``unknown`` effect marker that propagates to callers.  No unfilled slot
ever silently means "pure".
"""

from __future__ import annotations

from nlsc.lockfile import hash_anlu
from nlsc.lowering import lower_module
from nlsc.parser import parse_nl_file

PURE = """@module pure_ops
[add]
PURPOSE: add
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
"""

FOREIGN_EFFECT = """@module foreign_effect
[probe]
PURPOSE: log something
LOGIC:
  1. log_event("hello")
RETURNS: 0
"""

METHOD_EFFECT = """@module method_effect
[probe]
PURPOSE: append to a list
INPUTS:
  - items: list of number
LOGIC:
  1. items.append(1)
RETURNS: 0
"""

PROPAGATION = """@module effect_propagation
[log]
PURPOSE: call foreign code
LOGIC:
  1. log_event("hello")
RETURNS: 0

[caller]
PURPOSE: call the logger
LOGIC:
  1. [log]()
DEPENDS: [log]
RETURNS: 0
"""


def _op(module, name):
    matches = [op for op in module.operations if op.name == name]
    assert matches, f"operation {name} not found"
    return matches[0]


def test_pure_operation_has_analyzed_empty_effects():
    effects = _op(lower_module(parse_nl_file(PURE)), "add").effects
    assert effects == (), "analyzed-pure, not None (never-analyzed)"


def test_foreign_call_carries_unknown_effect():
    effects = _op(lower_module(parse_nl_file(FOREIGN_EFFECT)), "probe").effects or ()
    assert any(e.kind == "unknown" for e in effects)


def test_method_call_carries_unknown_effect():
    effects = _op(lower_module(parse_nl_file(METHOD_EFFECT)), "probe").effects or ()
    assert any(e.kind == "unknown" for e in effects)


def test_effects_propagate_to_callers():
    effects = _op(lower_module(parse_nl_file(PROPAGATION)), "caller").effects or ()
    assert any(e.kind == "unknown" for e in effects)


def test_pure_callers_of_pure_ops_stay_pure():
    source = """@module pure_chain
[add-one]
PURPOSE: add one
INPUTS:
  - value: number
RETURNS: value + 1

[chain]
PURPOSE: call pure op
INPUTS:
  - value: number
LOGIC:
  1. y = [add-one](value)
RETURNS: y
DEPENDS: [add-one]
"""
    effects = _op(lower_module(parse_nl_file(source)), "chain").effects
    assert effects == ()


def test_effects_are_deterministic():
    m1 = lower_module(parse_nl_file(PROPAGATION))
    m2 = lower_module(parse_nl_file(PROPAGATION))
    assert _op(m1, "caller").effects == _op(m2, "caller").effects


def test_caller_hash_changes_when_callee_gains_effects():
    base = parse_nl_file(PROPAGATION)
    pure_callee = parse_nl_file(
        PROPAGATION.replace('  1. log_event("hello")\n', "  1. x = 1\n")
    )
    caller_base = [a for a in base.anlus if a.identifier == "caller"][0]
    caller_pure = [a for a in pure_callee.anlus if a.identifier == "caller"][0]
    assert hash_anlu(caller_base, base) != hash_anlu(caller_pure, pure_callee)


def test_canonical_ir_renders_effect_contract():
    from nlsc.ir import module_to_canonical

    canonical = module_to_canonical(lower_module(parse_nl_file(FOREIGN_EFFECT)))
    assert "(effect unknown" in canonical
    pure = module_to_canonical(lower_module(parse_nl_file(PURE)))
    assert "(effects)" in pure
