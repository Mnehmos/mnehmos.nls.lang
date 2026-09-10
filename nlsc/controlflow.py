"""Control-flow checks over the IR (Issue #196).

Validates that value availability follows dominating definitions:

* A binding defined only inside one branch arm is *partial*; using it
  after the branch is a fatal error (the emitted code would raise
  UnboundLocalError / ReferenceError on the other path).
* Bindings are immutable in checked code: plain rebinding is a
  strict-only diagnostic.  Augmented assignment on an undefined value is
  a fatal use-before-definition.
* Branch joins: only names defined on **all** reachable arms (or
  unconditionally before the branch) are definitely defined afterwards.
  No complementary conditions or exhaustiveness are inferred from prose;
  an explicit ELSE makes a branch total.

Loop regions are reserved in the IR; there is no ANLU loop surface
syntax to check yet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .diagnostics import Diagnostic
from .error_catalog import ESEM004, ESEM010, ESEM011
from .ir import (
    IRBind,
    IRBranch,
    IRExpr,
    IRModule,
    IROperation,
    IRRef,
    IRStmt,
    SourceSpan,
    iter_expr_nodes,
)


@dataclass
class ControlResult:
    errors: list[Diagnostic] = field(default_factory=list)
    warnings: list[Diagnostic] = field(default_factory=list)


def _diag(
    bucket: list[Diagnostic],
    code: str,
    file_token: str,
    operation: str,
    span: Optional[SourceSpan],
    message: str,
    hint: str,
) -> None:
    bucket.append(
        Diagnostic(
            code=code,
            file=file_token,
            line=span.line if span else None,
            col=None,
            message=f"{operation}: {message}",
            hint=hint,
        )
    )


class _OperationWalk:
    """Tracks definite/partial definitions through one operation body."""

    def __init__(
        self,
        operation: IROperation,
        result: ControlResult,
        file_token: str,
    ):
        self.operation = operation
        self.result = result
        self.file_token = file_token
        # name -> span of first definition
        self.definite: dict[str, Optional[SourceSpan]] = {}
        # name -> span of the branch that defined it partially
        self.partial: dict[str, Optional[SourceSpan]] = {}

    def run(self) -> None:
        params = {param.name: self.operation.span for param in self.operation.params}
        self.definite.update(params)

        for stmt in self.operation.body:
            self.walk_statement(stmt)

        if self.operation.result is not None and self.operation.result.value is not None:
            self.check_expression_uses(
                self.operation.result.value, self.operation.span, "RETURNS"
            )

    # -- statements ----------------------------------------------------------
    def walk_statement(self, stmt: IRStmt) -> None:
        if isinstance(stmt, IRBind):
            self.check_expression_uses(stmt.value, stmt.span, f"step binding '{stmt.name}'")
            if stmt.aug is not None:
                if stmt.name in self.partial:
                    self._partial_use(stmt.name, stmt.span, "augmented assignment")
                elif stmt.name not in self.definite:
                    _diag(
                        self.result.errors,
                        ESEM004,
                        self.file_token,
                        self.operation.name,
                        stmt.span,
                        f"augmented assignment '{stmt.name} {stmt.aug}=' targets a value "
                        "that is not defined yet",
                        f"Define '{stmt.name}' with an initial value first.",
                    )
                else:
                    self._rebind_warning(stmt.name, stmt.span)
                return
            if stmt.name in self.definite or stmt.name in self.partial:
                self._rebind_warning(stmt.name, stmt.span)
            self.definite[stmt.name] = stmt.span
            self.partial.pop(stmt.name, None)
            return
        if isinstance(stmt, IRBranch):
            self.check_expression_uses(
                stmt.condition, stmt.span, "IF condition"
            )
            then_walk = self._arm_walk()
            for inner in stmt.then_body:
                then_walk.walk_statement(inner)
            else_walk = self._arm_walk()
            for inner in stmt.otherwise:
                else_walk.walk_statement(inner)

            joined = set(then_walk.definite) & set(else_walk.definite)
            for name in sorted(joined - set(self.definite)):
                self.definite[name] = stmt.span
                self.partial.pop(name, None)
            for name in sorted(
                (set(then_walk.definite) | set(else_walk.definite))
                - joined
                - set(self.definite)
            ):
                self.partial.setdefault(name, stmt.span)
            return
        # Guards/notes/discards/foreign statements do not bind values.
        value: Optional[IRExpr] = getattr(stmt, "value", None)
        condition: Optional[IRExpr] = getattr(stmt, "condition", None)
        if value is not None:
            self.check_expression_uses(value, stmt.span, "step")
        if condition is not None:
            self.check_expression_uses(condition, stmt.span, "condition")

    def _arm_walk(self) -> "_OperationWalk":
        arm = _OperationWalk(self.operation, self.result, self.file_token)
        arm.definite.update(self.definite)
        arm.partial.update(self.partial)
        return arm

    # -- expressions -----------------------------------------------------------
    def check_expression_uses(
        self, expr: IRExpr, span: Optional[SourceSpan], context: str
    ) -> None:
        for node in iter_expr_nodes(expr):
            if isinstance(node, IRRef):
                if node.name in self.partial:
                    self._partial_use(node.name, span, context)

    def _partial_use(self, name: str, span: Optional[SourceSpan], context: str) -> None:
        _diag(
            self.result.errors,
            ESEM010,
            self.file_token,
            self.operation.name,
            span,
            f"value '{name}' is only defined under a branch condition but is "
            f"used by {context}",
            f"Bind '{name}' on every path (IF ... THEN ... ELSE ... -> {name}) "
            "or keep its use inside the same branch.",
        )

    def _rebind_warning(self, name: str, span: Optional[SourceSpan]) -> None:
        _diag(
            self.result.warnings,
            ESEM011,
            self.file_token,
            self.operation.name,
            span,
            f"binding '{name}' is rebound; checked bindings are immutable",
            "Use a new name for the new value, or model mutation explicitly "
            "once the mutation contract is specified.",
        )


def check_control(module: IRModule, *, file_token: str = "<source>") -> ControlResult:
    """Check every operation's control flow for dominating definitions."""
    result = ControlResult()
    for operation in module.operations:
        _OperationWalk(operation, result, file_token).run()
    return result
