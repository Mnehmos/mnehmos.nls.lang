"""Failure-set inference over the IR (Issue #198).

Populates each operation's reserved ``failures`` contract slot:

- **guard** entries come from the operation's own guards (typed error,
  optional code, message);
- **callee** entries propagate from called operations transitively (to a
  fixpoint, cycle-safe);
- an **unknown** marker is appended conservatively for foreign calls,
  method calls, division/modulo and index access, and literal
  implementations — an unknown external failure is never treated as an
  empty set.

The pass is deterministic and target-neutral; the same source always
produces the same sorted failure set.  ``None`` still means *not
analyzed* — after this pass runs, an analyzed operation always carries a
tuple (possibly empty for pure operations).
"""

from __future__ import annotations

from .ir import (
    IRBinary,
    IRCall,
    IRExpr,
    IRIndexAccess,
    IRMethodCall,
    IRModule,
    IROperation,
    IRFailureSpec,
    ForeignExpr,
    ForeignStmt,
    iter_expr_nodes,
    iter_stmt_nodes,
)

UNKNOWN_FAILURE = IRFailureSpec(origin="unknown")


def _expr_needs_unknown(expr: IRExpr) -> bool:
    for node in iter_expr_nodes(expr):
        if isinstance(node, ForeignExpr):
            return True
        if isinstance(node, IRMethodCall):
            return True
        if isinstance(node, IRCall) and not node.anlu:
            return True
        if isinstance(node, IRIndexAccess):
            return True
        if isinstance(node, IRBinary) and node.op in ("div", "mod", "floor_div"):
            return True
    return False


def _own_failures(operation: IROperation) -> list[IRFailureSpec]:
    own: list[IRFailureSpec] = []
    for guard in operation.guards:
        if guard.error is not None:
            own.append(
                IRFailureSpec(
                    error_type=guard.error.error_type,
                    code=guard.error.code,
                    message=guard.error.message,
                    origin="guard",
                )
            )
        else:
            # A guard without an error spec still fails when violated;
            # what it raises is unspecified, so it is unknown.
            own.append(UNKNOWN_FAILURE)

    if operation.literal is not None:
        own.append(UNKNOWN_FAILURE)

    for stmt in operation.body:
        if isinstance(stmt, ForeignStmt):
            own.append(UNKNOWN_FAILURE)
            continue
        value: IRExpr | None = getattr(stmt, "value", None)
        condition: IRExpr | None = getattr(stmt, "condition", None)
        if value is not None and _expr_needs_unknown(value):
            own.append(UNKNOWN_FAILURE)
        if condition is not None and _expr_needs_unknown(condition):
            own.append(UNKNOWN_FAILURE)

    if operation.result is not None and operation.result.value is not None:
        if _expr_needs_unknown(operation.result.value):
            own.append(UNKNOWN_FAILURE)

    return own


def _called_operations(operation: IROperation, ops: dict[str, IROperation]) -> list[str]:
    """ANLU call targets inside the operation body and result."""
    called: list[str] = []
    for stmt in iter_stmt_nodes(operation.body):
        for expr in (
            getattr(stmt, "value", None),
            getattr(stmt, "condition", None),
        ):
            if expr is None:
                continue
            for node in iter_expr_nodes(expr):
                if isinstance(node, IRCall) and node.anlu and node.target in ops:
                    called.append(node.target)
    if operation.result is not None and operation.result.value is not None:
        for node in iter_expr_nodes(operation.result.value):
            if isinstance(node, IRCall) and node.anlu and node.target in ops:
                called.append(node.target)
    return called


def _dedupe_sorted(failures: list[IRFailureSpec]) -> tuple[IRFailureSpec, ...]:
    seen: dict[tuple[str, str, str, str], IRFailureSpec] = {}
    for failure in failures:
        seen.setdefault(failure.sort_key(), failure)
    return tuple(seen[key] for key in sorted(seen))


def populate_failure_sets(module: IRModule) -> None:
    """Fill every operation's failures slot, propagating callee failures."""
    ops = {op.name: op for op in module.operations}
    calls: dict[str, list[str]] = {}

    for operation in module.operations:
        own = _own_failures(operation)
        calls[operation.name] = _called_operations(operation, ops)
        operation.failures = _dedupe_sorted(own)

    # Propagate callee failures to a fixpoint.  Self-calls do not feed
    # themselves (a recursive operation's set already includes its own).
    for _ in range(len(module.operations) + 1):
        changed = False
        for operation in module.operations:
            current = operation.failures or ()
            merged = list(current)
            for target in calls.get(operation.name, ()):
                if target == operation.name:
                    continue
                callee = ops.get(target)
                if callee is None or callee.failures is None:
                    continue
                for failure in callee.failures:
                    propagated = IRFailureSpec(
                        error_type=failure.error_type,
                        code=failure.code,
                        message=failure.message,
                        origin="callee" if failure.origin != "unknown" else "unknown",
                    )
                    if propagated.sort_key() not in {f.sort_key() for f in merged}:
                        merged.append(propagated)
                        changed = True
            if changed or len(merged) != len(current):
                new_set = _dedupe_sorted(merged)
                if new_set != current:
                    operation.failures = new_set
                    changed = True
        if not changed:
            break
