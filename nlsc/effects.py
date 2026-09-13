"""Conservative effect-set inference over the IR (Issue #197).

Populates each operation's ``effects`` contract slot plus, when declared,
its ``declared_effects`` upper bound.

Inference rules:

- purely structural code (literals, refs, operators, structural calls to
  other analyzed operations) yields an analyzed **empty** set — reads of
  local bindings are world-free and are tracked per-step by
  ``nlsc/parallel.py``, not here;
- a **method call** conservatively writes its base resource when the base
  resolves to a parameter or a binding (``items.append(x)`` ->
  ``write(items)``); a method call whose base cannot be named stays
  ``unknown``;
- foreign function calls, foreign expressions/statements, and ``@literal``
  implementations stay ``unknown`` markers;
- markers propagate to callers transitively (deterministic fixpoint), and
  a callee's effects are **substituted** through the call arguments so the
  caller sees its own resource names.  A callee-internal resource that
  cannot be attributed to a caller name propagates as ``unknown``.

``None`` remains *not analyzed*; it is never an implicit proof of purity.
"""

from __future__ import annotations

from .ir import (
    IRBind,
    IRCall,
    IRExpr,
    IRMethodCall,
    IRModule,
    IROperation,
    IRRef,
    IREffectSpec,
    ForeignExpr,
    ForeignStmt,
    iter_expr_nodes,
    iter_stmt_nodes,
)

UNKNOWN_EFFECT = IREffectSpec(kind="unknown", origin="call")


def _named_resources(operation: IROperation) -> set[str]:
    """Names a method call can be attributed to: params and bindings."""
    names = {param.name for param in operation.params}
    for stmt in iter_stmt_nodes(operation.body):
        if isinstance(stmt, IRBind):
            names.add(stmt.name)
    return names


def _root_ref(expr: IRExpr) -> str | None:
    """Root identifier of a reference chain (``a.b[0]`` -> ``a``)."""
    from .ir import IRFieldAccess, IRIndexAccess

    node = expr
    while True:
        if isinstance(node, IRRef):
            return node.name
        if isinstance(node, IRFieldAccess):
            node = node.base
            continue
        if isinstance(node, IRIndexAccess):
            node = node.base
            continue
        return None


def _expr_needs_unknown(expr: IRExpr, named: set[str]) -> bool:
    for node in iter_expr_nodes(expr):
        if isinstance(node, ForeignExpr):
            return True
        if isinstance(node, IRCall) and not node.anlu:
            return True
        if isinstance(node, IRMethodCall):
            base = _root_ref(node.base)
            if base is None or base not in named:
                return True
    return False


def _method_write_effects(expr: IRExpr, named: set[str]) -> list[IREffectSpec]:
    """``write(<resource>)`` for each method call whose base we can name."""
    effects: list[IREffectSpec] = []
    for node in iter_expr_nodes(expr):
        if isinstance(node, IRMethodCall):
            base = _root_ref(node.base)
            if base is not None and base in named:
                effects.append(
                    IREffectSpec(kind="write", resource=base, origin="call")
                )
    return effects


def _statement_expressions(statement: object) -> list[IRExpr]:
    return [
        expr
        for expr in (
            getattr(statement, "value", None),
            getattr(statement, "condition", None),
        )
        if expr is not None
    ]


def _own_effects(operation: IROperation) -> list[IREffectSpec]:
    own: list[IREffectSpec] = []
    if operation.literal is not None:
        own.append(IREffectSpec(kind="unknown", origin="literal"))

    named = _named_resources(operation)

    for stmt in iter_stmt_nodes(operation.body):
        if isinstance(stmt, ForeignStmt):
            own.append(UNKNOWN_EFFECT)
            continue
        for expr in _statement_expressions(stmt):
            own.extend(_method_write_effects(expr, named))
            if _expr_needs_unknown(expr, named):
                own.append(UNKNOWN_EFFECT)

    for guard in operation.guards:
        own.extend(_method_write_effects(guard.condition, named))
        if _expr_needs_unknown(guard.condition, named):
            own.append(UNKNOWN_EFFECT)

    if operation.result is not None and operation.result.value is not None:
        own.extend(_method_write_effects(operation.result.value, named))
        if _expr_needs_unknown(operation.result.value, named):
            own.append(UNKNOWN_EFFECT)

    return own


def _anlu_calls(operation: IROperation) -> list[IRCall]:
    calls: list[IRCall] = []
    expressions: list[IRExpr] = []
    for stmt in iter_stmt_nodes(operation.body):
        if isinstance(stmt, IRBind):
            expressions.append(stmt.value)
        else:
            expressions.extend(_statement_expressions(stmt))
    for guard in operation.guards:
        expressions.append(guard.condition)
    if operation.result is not None and operation.result.value is not None:
        expressions.append(operation.result.value)
    for expression in expressions:
        for node in iter_expr_nodes(expression):
            if isinstance(node, IRCall) and node.anlu:
                calls.append(node)
    return calls


def _call_argument_map(call: IRCall) -> dict[str, str | None]:
    """Map callee parameter names to caller resource names for one call.

    ``None`` marks an argument that cannot be named (a literal, a nested
    call, ...): effects attributed to it become ``unknown`` at the caller.
    """
    mapping: dict[str, str | None] = {}
    for index, argument in enumerate(call.args):
        mapping[f"#{index}"] = _root_ref(argument)
    for name, value in call.kwargs:
        mapping[name] = _root_ref(value)
    return mapping


def _substitute(
    effect: IREffectSpec,
    callee: IROperation,
    argument_map: dict[str, str | None],
) -> IREffectSpec:
    """Rewrite a callee effect into the caller's resource names."""
    if effect.kind == "unknown" or effect.resource is None:
        return IREffectSpec(kind=effect.kind, origin="callee")

    param_names = [param.name for param in callee.params]
    if effect.resource in param_names:
        position = param_names.index(effect.resource)
        caller_resource = argument_map.get(effect.resource)
        if caller_resource is None:
            caller_resource = argument_map.get(f"#{position}")
        if caller_resource is None:
            return IREffectSpec(kind="unknown", origin="callee")
        return IREffectSpec(
            kind=effect.kind, resource=caller_resource, origin="callee"
        )

    # A callee-internal resource cannot be attributed to a caller name.
    return IREffectSpec(kind="unknown", origin="callee")


def _dedupe_sorted(effects: list[IREffectSpec]) -> tuple[IREffectSpec, ...]:
    seen: dict[tuple[str, str, str], IREffectSpec] = {}
    for effect in effects:
        seen.setdefault(effect.sort_key(), effect)
    return tuple(seen[key] for key in sorted(seen))


def populate_effect_sets(module: IRModule) -> None:
    """Fill every operation's effects slot, propagating callee effects."""
    ops = {op.name: op for op in module.operations}
    calls: dict[str, list[IRCall]] = {}

    for operation in module.operations:
        calls[operation.name] = _anlu_calls(operation)
        operation.effects = _dedupe_sorted(_own_effects(operation))

    for _ in range(len(module.operations) + 1):
        changed = False
        for operation in module.operations:
            current = operation.effects or ()
            merged = list(current)
            seen = {effect.sort_key() for effect in merged}
            for call in calls.get(operation.name, ()):
                target = call.target
                if target == operation.name:
                    continue
                callee = ops.get(target)
                if callee is None or callee.effects is None:
                    continue
                argument_map = _call_argument_map(call)
                for effect in callee.effects:
                    propagated = _substitute(effect, callee, argument_map)
                    if propagated.sort_key() not in seen:
                        merged.append(propagated)
                        seen.add(propagated.sort_key())
                        changed = True
            new_set = _dedupe_sorted(merged)
            if new_set != current:
                operation.effects = new_set
                changed = True
        if not changed:
            break


# --------------------------------------------------------------------------
# Declared effect contracts (EFFECTS: ...)
# --------------------------------------------------------------------------


class EffectDeclarationError(ValueError):
    """A malformed ``EFFECTS:`` declaration."""


def parse_effect_declaration(text: str) -> tuple[IREffectSpec, ...]:
    """Parse an ``EFFECTS:`` contract line into an upper bound.

    Accepted forms (comma- or space-separated):

    - ``pure`` — the empty set; any inferred effect violates it;
    - ``unknown`` — the top; covers every inferred effect;
    - ``read`` / ``write`` — any resource of that kind;
    - ``read(name)`` / ``write(name)`` — one named resource.
    """
    raw = (text or "").strip()
    if not raw:
        raise EffectDeclarationError("empty EFFECTS declaration")

    items = [item.strip() for item in raw.replace(",", " ").split()]
    if not items:
        raise EffectDeclarationError("empty EFFECTS declaration")

    if len(items) == 1 and items[0].lower() == "pure":
        return ()
    if any(item.lower() == "pure" for item in items):
        raise EffectDeclarationError("'pure' cannot be combined with other effects")

    effects: list[IREffectSpec] = []
    for item in items:
        lowered = item.lower()
        if lowered == "unknown":
            effects.append(IREffectSpec(kind="unknown", origin="declared"))
            continue
        if lowered in ("read", "write"):
            effects.append(IREffectSpec(kind=lowered, origin="declared"))
            continue
        parts = item.split("(", 1)
        if len(parts) != 2 or not parts[1].endswith(")"):
            raise EffectDeclarationError(
                f"unsupported effect {item!r}; use pure, unknown, read, write, "
                "read(name), or write(name)"
            )
        kind = parts[0].strip().lower()
        resource = parts[1][:-1].strip()
        if (
            kind not in ("read", "write")
            or not resource
            or "(" in resource
            or ")" in resource
        ):
            raise EffectDeclarationError(
                f"unsupported effect {item!r}; use pure, unknown, read, write, "
                "read(name), or write(name)"
            )
        effects.append(IREffectSpec(kind=kind, resource=resource, origin="declared"))
    return tuple(effects)


def declaration_covers(
    declaration: tuple[IREffectSpec, ...], inferred: IREffectSpec
) -> bool:
    """True when a declared upper bound allows one inferred effect."""
    for declared in declaration:
        if declared.kind == "unknown":
            return True
        if declared.kind != inferred.kind:
            continue
        if declared.resource is None:
            return True
        if declared.resource == inferred.resource:
            return True
    return False


def uncovered_effects(
    declaration: tuple[IREffectSpec, ...], inferred: tuple[IREffectSpec, ...]
) -> list[IREffectSpec]:
    """Inferred effects the declaration does not allow."""
    return [
        effect
        for effect in inferred
        if not declaration_covers(declaration, effect)
    ]
