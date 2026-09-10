"""Conservative effect-set inference over the IR (Issue #197).

Populates each operation's reserved ``effects`` contract slot.  With no
effect surface syntax yet the contract is deliberately coarse:

- purely structural code (literals, refs, operators, structural calls to
  other analyzed operations) yields an analyzed **empty** set;
- anything that could touch the world — foreign function calls, method
  calls, ``@literal`` implementations, foreign statements/expressions —
  contributes an ``unknown`` effect marker;
- markers propagate to callers transitively (deterministic fixpoint).

``None`` remains *not analyzed*; it is never an implicit proof of
purity.  ``kind`` and ``resource`` fields are reserved for the
read/write resource-identity syntax specified in the full #197 slice.
"""

from __future__ import annotations

from .ir import (
    IRCall,
    IRExpr,
    IRMethodCall,
    IRModule,
    IROperation,
    IREffectSpec,
    ForeignExpr,
    ForeignStmt,
    iter_expr_nodes,
    iter_stmt_nodes,
)

UNKNOWN_EFFECT = IREffectSpec(kind="unknown", origin="call")


def _expr_needs_unknown(expr: IRExpr) -> bool:
    for node in iter_expr_nodes(expr):
        if isinstance(node, (ForeignExpr, IRMethodCall)):
            return True
        if isinstance(node, IRCall) and not node.anlu:
            return True
    return False


def _own_effects(operation: IROperation) -> list[IREffectSpec]:
    own: list[IREffectSpec] = []
    if operation.literal is not None:
        own.append(IREffectSpec(kind="unknown", origin="literal"))

    for stmt in operation.body:
        if isinstance(stmt, ForeignStmt):
            own.append(UNKNOWN_EFFECT)
            continue
        for expr in (
            getattr(stmt, "value", None),
            getattr(stmt, "condition", None),
        ):
            if expr is not None and _expr_needs_unknown(expr):
                own.append(UNKNOWN_EFFECT)

    for guard in operation.guards:
        if _expr_needs_unknown(guard.condition):
            own.append(UNKNOWN_EFFECT)

    if operation.result is not None and operation.result.value is not None:
        if _expr_needs_unknown(operation.result.value):
            own.append(UNKNOWN_EFFECT)

    return own


def _called_operations(operation: IROperation) -> list[str]:
    called: list[str] = []
    for stmt in iter_stmt_nodes(operation.body):
        for expr in (
            getattr(stmt, "value", None),
            getattr(stmt, "condition", None),
        ):
            if expr is None:
                continue
            for node in iter_expr_nodes(expr):
                if isinstance(node, IRCall) and node.anlu:
                    called.append(node.target)
    if operation.result is not None and operation.result.value is not None:
        for node in iter_expr_nodes(operation.result.value):
            if isinstance(node, IRCall) and node.anlu:
                called.append(node.target)
    return called


def _dedupe_sorted(effects: list[IREffectSpec]) -> tuple[IREffectSpec, ...]:
    seen: dict[tuple[str, str, str], IREffectSpec] = {}
    for effect in effects:
        seen.setdefault(effect.sort_key(), effect)
    return tuple(seen[key] for key in sorted(seen))


def populate_effect_sets(module: IRModule) -> None:
    """Fill every operation's effects slot, propagating callee markers."""
    ops = {op.name: op for op in module.operations}
    calls: dict[str, list[str]] = {}

    for operation in module.operations:
        calls[operation.name] = _called_operations(operation)
        operation.effects = _dedupe_sorted(_own_effects(operation))

    for _ in range(len(module.operations) + 1):
        changed = False
        for operation in module.operations:
            current = operation.effects or ()
            merged = list(current)
            for target in calls.get(operation.name, ()):
                if target == operation.name:
                    continue
                callee = ops.get(target)
                if callee is None or callee.effects is None:
                    continue
                for effect in callee.effects:
                    propagated = IREffectSpec(
                        kind=effect.kind,
                        resource=effect.resource,
                        origin="callee",
                    )
                    if propagated.sort_key() not in {e.sort_key() for e in merged}:
                        merged.append(propagated)
                        changed = True
            new_set = _dedupe_sorted(merged)
            if new_set != current:
                operation.effects = new_set
                changed = True
        if not changed:
            break
