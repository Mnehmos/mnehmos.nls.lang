"""Checked parallel-eligibility analysis over the IR (Issue #199).

``ANLU.parallel_groups()`` only checked declared data dependencies, which
makes it a *data-dependency layering*, not a proof of safe concurrency.
This module computes conservative eligibility on top: two data-independent
steps may be certified independent only when effect, alias, failure, and
control constraints permit — and every decision carries its reasons.

Rules (all conservative):

- write/write and write/read overlap on the same resource blocks a pair;
- a resource whose provenance is external (an input, a parameter, an
  unresolved value) can alias another external resource, so two effectful
  steps touching distinct-but-external roots are blocked;
- steps with unresolved (unknown) effects are never certified;
- a step that may fail before a later step's effects blocks the pair:
  reordering could perform a write the sequential program never does;
- pure, total arithmetic on fresh local bindings is eligible.

This slice delivers analysis only: emitters stay sequential, and the
report is what ``nlsc graph`` presents.  No thread pool, no reordering.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .ir import (
    IRBind,
    IRBinary,
    IRBranch,
    IRCall,
    IRExpr,
    IRIndexAccess,
    IRMethodCall,
    IROperation,
    IRRef,
    ForeignExpr,
    SourceSpan,
    iter_expr_nodes,
)
from .lowering import lower_anlu
from .schema import ANLU


@dataclass(frozen=True)
class StepProfile:
    """Resource and failure profile of one LOGIC step."""

    number: int
    writes: frozenset[str]
    reads: frozenset[str]
    unknown_effects: bool
    can_fail: bool
    has_control: bool  # conditional execution (IF)
    notes: tuple[str, ...]


@dataclass(frozen=True)
class PairDecision:
    """Eligibility decision for one ordered pair of steps."""

    left: int
    right: int
    allowed: bool
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class LayerReport:
    """One data-dependency layer and its pairwise eligibility."""

    steps: tuple[int, ...]
    eligible: bool
    pairs: tuple[PairDecision, ...]
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class EligibilityReport:
    """Full eligibility analysis for one operation."""

    anlu: str
    layers: tuple[LayerReport, ...] = ()
    premises: tuple[str, ...] = field(default=())

    @property
    def all_steps(self) -> tuple[int, ...]:
        return tuple(step for layer in self.layers for step in layer.steps)


def _expr_refs(expr: IRExpr) -> set[str]:
    return {
        node.name for node in iter_expr_nodes(expr) if isinstance(node, IRRef)
    }


def _expr_can_fail(expr: IRExpr) -> bool:
    for node in iter_expr_nodes(expr):
        if isinstance(node, IRBinary) and node.op in ("div", "mod", "floor_div"):
            return True
        if isinstance(node, IRCall) and node.anlu:
            return True  # callee failures propagate into the caller
        if isinstance(node, (ForeignExpr, IRMethodCall)):
            return True
        if isinstance(node, IRCall) and not node.anlu:
            return True  # foreign function
    return False


def _method_roots(expr: IRExpr) -> tuple[set[str], bool]:
    """Identifiers whose objects method calls mutate; and unknown-flag."""
    roots: set[str] = set()
    unknown = False
    for node in iter_expr_nodes(expr):
        if isinstance(node, IRMethodCall):
            base: Optional[IRExpr] = node.base
            # Chained bases (a.b.append) have unresolved identity.
            while isinstance(base, (IRMethodCall, IRIndexAccess)):
                base = getattr(base, "base", None)
            if isinstance(base, IRRef):
                roots.add(base.name)
            else:
                unknown = True
            unknown = unknown or True  # method bodies are unresolved
    return roots, unknown


def _profile_expr(expr: IRExpr) -> tuple[set[str], set[str], bool, bool]:
    """(writes, reads, unknown_effects, can_fail) for one expression."""
    reads = _expr_refs(expr)
    writes: set[str] = set()
    unknown = False
    for node in iter_expr_nodes(expr):
        if isinstance(node, ForeignExpr):
            unknown = True
        elif isinstance(node, IRCall) and not node.anlu:
            unknown = True
        elif isinstance(node, IRMethodCall):
            roots, method_unknown = _method_roots(node)
            writes |= roots
            unknown = unknown or method_unknown
    return writes, reads, unknown, _expr_can_fail(expr)


def _step_profiles(operation: IROperation) -> dict[int, StepProfile]:
    profiles: dict[int, StepProfile] = {}

    for stmt in operation.body:
        span: Optional[SourceSpan] = getattr(stmt, "span", None)
        step = span.step if span else None
        if step is None:
            continue
        writes: set[str] = set()
        reads: set[str] = set()
        unknown = False
        can_fail = False
        notes: list[str] = []

        if isinstance(stmt, IRBranch):
            reads |= _expr_refs(stmt.condition)
            unknown = unknown or any(
                isinstance(node, (ForeignExpr, IRMethodCall))
                or (isinstance(node, IRCall) and not node.anlu)
                for node in iter_expr_nodes(stmt.condition)
            )
            for inner in (*stmt.then_body, *stmt.otherwise):
                value = getattr(inner, "value", None)
                if value is not None:
                    w, r, u, f = _profile_expr(value)
                    writes |= w
                    reads |= r
                    unknown = unknown or u
                    can_fail = can_fail or f
                if isinstance(inner, IRBind):
                    writes |= {inner.name}
            notes.append("conditional step")
        elif isinstance(stmt, IRBind):
            w, r, u, f = _profile_expr(stmt.value)
            writes |= w | {stmt.name}
            reads |= r
            unknown = unknown or u
            can_fail = can_fail or f
        else:
            value = getattr(stmt, "value", None)
            if value is not None:
                w, r, u, f = _profile_expr(value)
                writes |= w
                reads |= r
                unknown = unknown or u
                can_fail = can_fail or f

        profiles[step] = StepProfile(
            number=step,
            writes=frozenset(writes),
            reads=frozenset(reads),
            unknown_effects=unknown,
            can_fail=can_fail,
            has_control=isinstance(stmt, IRBranch),
            notes=tuple(notes),
        )
    return profiles


def _external_roots(names: set[str], params: set[str], fresh: set[str]) -> set[str]:
    return {name for name in names if name not in fresh} | (names & params)


def analyze_parallel_eligibility(anlu: ANLU) -> EligibilityReport:
    """Compute dependency layers with conservative pairwise eligibility."""
    operation, _diagnostics = lower_anlu(anlu, set())
    profiles = _step_profiles(operation)
    params = {param.name for param in operation.params}
    # Fresh locals: names bound by pure, total steps.  They are provably
    # disjoint from every other resource in the operation, so writes to
    # distinct fresh locals cannot alias.
    fresh: set[str] = set()
    for number in sorted(profiles):
        profile = profiles[number]
        if not profile.unknown_effects and not profile.can_fail:
            fresh |= profile.writes - params

    layers = anlu.dependency_layers()
    reports: list[LayerReport] = []
    premises: list[str] = []
    if anlu.guards:
        premises.append(
            "guards execute first in declaration order; layers never "
            "reorder across them"
        )

    for layer in layers:
        steps = tuple(sorted(layer))
        pairs: list[PairDecision] = []
        for i in range(len(steps)):
            for j in range(i + 1, len(steps)):
                pairs.append(
                    _decide_pair(
                        profiles.get(steps[i]),
                        profiles.get(steps[j]),
                        params,
                        fresh,
                    )
                )
        eligible = all(pair.allowed for pair in pairs) if pairs else True
        notes: list[str] = []
        if not eligible:
            blocked: list[str] = []
            for pair in pairs:
                if not pair.allowed:
                    for reason in pair.reasons:
                        if reason not in blocked:
                            blocked.append(reason)
            notes.extend(blocked)
        reports.append(
            LayerReport(steps=steps, eligible=eligible, pairs=tuple(pairs), notes=tuple(notes))
        )

    return EligibilityReport(
        anlu=anlu.identifier,
        layers=tuple(reports),
        premises=tuple(premises),
    )


def _decide_pair(
    left: Optional[StepProfile],
    right: Optional[StepProfile],
    params: set[str],
    fresh: set[str],
) -> PairDecision:
    if left is None or right is None:
        return PairDecision(
            left=left.number if left else -1,
            right=right.number if right else -1,
            allowed=False,
            reasons=("step could not be analyzed",),
        )

    reasons: list[str] = []

    if left.unknown_effects or right.unknown_effects:
        reasons.append("unresolved (unknown) effects; cannot certify independence")

    overlap_ww = left.writes & right.writes
    if overlap_ww:
        reasons.append(
            "write/write overlap on " + ", ".join(sorted(overlap_ww))
        )
    overlap_wr = (left.writes & right.reads) | (right.writes & left.reads)
    if overlap_wr:
        reasons.append(
            "write/read overlap on " + ", ".join(sorted(overlap_wr))
        )

    # Aliasing: two effectful steps touching distinct external resources
    # could receive the same underlying object.
    left_external = _external_roots(set(left.writes), params, fresh)
    right_external = _external_roots(set(right.writes), params, fresh)
    if left.writes and right.writes and not overlap_ww:
        if left_external and right_external:
            reasons.append(
                "possible aliasing between external resources "
                f"({', '.join(sorted(left_external))} vs {', '.join(sorted(right_external))})"
            )

    # Failure ordering: a failing step before an effectful later step must
    # not be reordered — the sequential program may never perform the
    # later effect.
    if left.can_fail and (right.writes or right.unknown_effects):
        reasons.append(
            f"step {left.number} may fail before step {right.number}'s effects; "
            "reordering could perform effects the sequential program never does"
        )

    if reasons:
        return PairDecision(
            left=left.number, right=right.number, allowed=False, reasons=tuple(reasons)
        )

    if not left.writes and not right.writes:
        premise = "both steps are pure and total"
    else:
        premise = "disjoint fresh bindings"
    return PairDecision(
        left=left.number,
        right=right.number,
        allowed=True,
        reasons=(premise,),
    )
