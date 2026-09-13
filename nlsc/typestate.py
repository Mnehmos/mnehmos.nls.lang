"""Resource state protocols (Issue #200).

A module declares a protocol's states with ``@states``:

```nl
@states Order: Pending, Validated, Charged, Shipped
```

ANLUs then carry state tokens on protocol parameters and results
(``order: Order<Pending>`` / ``RETURNS: Order<Validated>``).  Tokens are
unforgeable in checked code: the checker tracks which state each token is
in and validates every transition.

Rules (all fatal):

- ``ESEM014`` — a token in the wrong state is passed to a transition.
- ``ESEM015`` — a consumed token (or an alias of it) is used again.
- ``ESEM016`` — a token is fabricated: an undeclared protocol/state, a
  protocol parameter without a state token, or a transition that returns
  a protocol value without declaring its result state.
- ``ESEM017`` — a branch join leaves a token's state ambiguous and a later
  transition needs a definite state.

Files without ``@states`` are unaffected: the checks are opt-in.  The
checker is static only — it says nothing about whether an external system
honored the transition (see the language spec's guarantee disclaimer).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .diagnostics import Diagnostic
from .error_catalog import ESEM014, ESEM015, ESEM016, ESEM017
from typing import TYPE_CHECKING

from .ir import (
    IRBind,
    IRBranch,
    IRCall,
    IROperation,
    IRRef,
    TypeRef,
)

if TYPE_CHECKING:
    from .ir import IRExpr, IRModule
from .schema import NLFile


@dataclass
class _Token:
    """A protocol value in flight.

    Aliases (``copy = order``, and copies taken for branch analysis) share
    one ``group`` id, so consuming any alias consumes them all even after
    the branch machinery has copied the tokens.
    """

    protocol: str
    state: str | None  # None = ambiguous (branch join)
    group: str
    source_line: int | None = None


@dataclass
class _CheckState:
    tokens: dict[str, _Token] = field(default_factory=dict)
    consumed_groups: set[str] = field(default_factory=set)
    diagnostics: list[Diagnostic] = field(default_factory=list)
    _next_group: int = 0

    def new_token(
        self, protocol: str, state: str | None, line: int | None, group: str | None = None
    ) -> _Token:
        if group is None:
            self._next_group += 1
            group = f"g{self._next_group}"
        return _Token(protocol=protocol, state=state, group=group, source_line=line)

    def is_consumed(self, token: _Token) -> bool:
        return token.group in self.consumed_groups

    def consume(self, token: _Token) -> None:
        self.consumed_groups.add(token.group)


def _protocol_of(type_ref: TypeRef, protocols: dict[str, tuple[str, ...]]) -> str | None:
    """Protocol name when a type reference names a declared protocol."""
    if type_ref.name in protocols:
        return type_ref.name
    # `list of Order` / optional spellings keep the base type reachable.
    if type_ref.args and type_ref.name == "list":
        return _protocol_of(type_ref.args[0], protocols)
    return None


def _state_of(type_ref: TypeRef) -> str | None:
    if type_ref.name == "list" and type_ref.args:
        return _state_of(type_ref.args[0])
    if type_ref.args and type_ref.args[0].name:
        return type_ref.args[0].name
    return None


def _has_angle_token(raw: str) -> bool:
    return "<" in raw and raw.endswith(">")


def _diag(
    code: str, file_token: str, line: int | None, message: str, hint: str
) -> Diagnostic:
    return Diagnostic(
        code=code, file=file_token, line=line, col=None, message=message, hint=hint
    )


def check_typestate(
    nl_file: NLFile, module: "IRModule", *, file_token: str = "<source>"
) -> list[Diagnostic]:
    """Validate resource-state transitions across the module (#200)."""
    protocols = {name: tuple(states) for name, states in nl_file.module.states.items()}
    if not protocols:
        return []

    diagnostics = _check_declarations(nl_file, protocols, file_token)

    operations = {operation.name: operation for operation in module.operations}
    for operation in module.operations:
        diagnostics.extend(
            _check_operation(operation, operations, protocols, file_token)
        )
    return diagnostics


def _check_declarations(
    nl_file: NLFile, protocols: dict[str, tuple[str, ...]], file_token: str
) -> list[Diagnostic]:
    """Undeclared protocols/states and unlabeled protocol parameters."""
    diagnostics: list[Diagnostic] = []
    for anlu in nl_file.anlus:
        for input_ in anlu.inputs:
            from .ir import type_ref_from_text

            type_ref = type_ref_from_text(input_.type)
            protocol = _protocol_of(type_ref, protocols)
            if protocol is None:
                # A state token on a non-protocol base (including an empty
                # or malformed token, which lowers without arguments) is
                # fabricated: it would bypass the protocol entirely.
                if _has_angle_token(input_.type.strip()):
                    diagnostics.append(
                        _diag(
                            ESEM016,
                            file_token,
                            anlu.line_number or None,
                            f"{anlu.identifier}: '{input_.name}' uses an undeclared "
                            f"or malformed protocol token '{input_.type.strip()}'",
                            "Declare the protocol with @states and spell the token "
                            "with a declared state, e.g. 'Order<Pending>'.",
                        )
                    )
                continue
            state = _state_of(type_ref)
            if state is None:
                detail = (
                    f"malformed state token in '{input_.type.strip()}'"
                    if _has_angle_token(input_.type.strip())
                    else f"protocol parameter '{input_.name}' has no state token"
                )
                diagnostics.append(
                    _diag(
                        ESEM016,
                        file_token,
                        anlu.line_number or None,
                        f"{anlu.identifier}: {detail}",
                        f"Spell the parameter as '{protocol}<State>' with a declared state.",
                    )
                )
                continue
            if state not in protocols[protocol]:
                diagnostics.append(
                    _diag(
                        ESEM016,
                        file_token,
                        anlu.line_number or None,
                        f"{anlu.identifier}: state '{state}' is not declared for "
                        f"protocol '{protocol}'",
                        f"Declared states: {', '.join(protocols[protocol])}.",
                    )
                )
    return diagnostics


def _check_operation(
    operation: IROperation,
    operations: dict[str, IROperation],
    protocols: dict[str, tuple[str, ...]],
    file_token: str,
) -> list[Diagnostic]:
    state = _CheckState()
    line = operation.span.line if operation.span else None

    for param in operation.params:
        protocol = _protocol_of(param.type_ref, protocols)
        if protocol is None:
            continue
        token_state = _state_of(param.type_ref)
        if token_state is not None and token_state in protocols[protocol]:
            state.tokens[param.name] = state.new_token(
                protocol=protocol, state=token_state, line=line
            )

    # A result that names a protocol must declare a valid state, whether or
    # not the operation takes a protocol input (factories fabricate too).
    if operation.result is not None:
        raw_result = operation.result.raw or ""
        result_type = operation.result.declared_type
        if result_type is not None:
            protocol = _protocol_of(result_type, protocols)
            result_state = _state_of(result_type)
            if protocol is not None and result_state is None:
                if _has_angle_token(raw_result):
                    # An empty or malformed token such as `Order<>`.
                    state.diagnostics.append(
                        _diag(
                            ESEM016,
                            file_token,
                            line,
                            f"{operation.name}: malformed state token in "
                            f"'{raw_result}'",
                            f"Spell the state, e.g. 'RETURNS: {protocol}<Succeeded>'.",
                        )
                    )
                else:
                    state.diagnostics.append(
                        _diag(
                            ESEM016,
                            file_token,
                            line,
                            f"{operation.name}: returns protocol '{protocol}' without "
                            "a state token",
                            f"Declare the result state, e.g. "
                            f"'RETURNS: {protocol}<Succeeded>'.",
                        )
                    )
            elif (
                protocol is not None
                and result_state is not None
                and result_state not in protocols[protocol]
            ):
                state.diagnostics.append(
                    _diag(
                        ESEM016,
                        file_token,
                        line,
                        f"{operation.name}: state '{result_state}' is not declared "
                        f"for protocol '{protocol}'",
                        f"Declared states: {', '.join(protocols[protocol])}.",
                    )
                )
            elif protocol is None and _has_angle_token(raw_result):
                state.diagnostics.append(
                    _diag(
                        ESEM016,
                        file_token,
                        line,
                        f"{operation.name}: result '{raw_result}' names an undeclared "
                        f"protocol '{result_type.name}'",
                        "Declare the protocol with @states before using its tokens.",
                    )
                )
        elif _has_angle_token(raw_result):
            state.diagnostics.append(
                _diag(
                    ESEM016,
                    file_token,
                    line,
                    f"{operation.name}: result '{raw_result}' uses an undeclared "
                    "protocol token",
                    "Declare the protocol with @states before using its tokens.",
                )
            )

    for guard in operation.guards:
        _handle_call(
            guard.condition, operation, operations, protocols, state, file_token
        )
    _walk_statements(operation.body, operation, operations, protocols, state, file_token)
    if operation.result is not None and operation.result.value is not None:
        _handle_call(
            operation.result.value,
            operation,
            operations,
            protocols,
            state,
            file_token,
        )
    return state.diagnostics


def _walk_statements(
    statements: tuple,
    operation: IROperation,
    operations: dict[str, IROperation],
    protocols: dict[str, tuple[str, ...]],
    state: _CheckState,
    file_token: str,
) -> None:
    for stmt in statements:
        if isinstance(stmt, IRBranch):
            _check_branch(stmt, operation, operations, protocols, state, file_token)
            continue
        value = getattr(stmt, "value", None)
        if isinstance(stmt, IRBind):
            _handle_call(
                value,
                operation,
                operations,
                protocols,
                state,
                file_token,
                binding_name=stmt.name,
            )
            _handle_alias(stmt, value, state)
        elif value is not None:
            _handle_call(value, operation, operations, protocols, state, file_token)
        condition = getattr(stmt, "condition", None)
        if condition is not None:
            _handle_call(
                condition, operation, operations, protocols, state, file_token
            )


def _check_branch(
    branch: IRBranch,
    operation: IROperation,
    operations: dict[str, IROperation],
    protocols: dict[str, tuple[str, ...]],
    state: _CheckState,
    file_token: str,
) -> None:
    from copy import copy

    # Calls in the branch condition itself are real calls too.
    _handle_call(branch.condition, operation, operations, protocols, state, file_token)

    then_tokens = {name: copy(token) for name, token in state.tokens.items()}
    else_tokens = {name: copy(token) for name, token in state.tokens.items()}

    then_state = _CheckState(
        tokens=then_tokens,
        consumed_groups=set(state.consumed_groups),
        _next_group=state._next_group,
    )
    _walk_statements(
        branch.then_body, operation, operations, protocols, then_state, file_token
    )
    # The else arm continues the group counter so tokens created in the two
    # arms can never share an alias-group id.
    else_state = _CheckState(
        tokens=else_tokens,
        consumed_groups=set(state.consumed_groups),
        _next_group=then_state._next_group,
    )
    if branch.otherwise:
        _walk_statements(
            branch.otherwise, operation, operations, protocols, else_state, file_token
        )

    # Diagnostics raised inside the arms are real: merge them back.
    state.diagnostics.extend(then_state.diagnostics)
    state.diagnostics.extend(else_state.diagnostics)
    state._next_group = max(then_state._next_group, else_state._next_group)

    # Merge arm states: agreement keeps the state, disagreement is ambiguous,
    # and consumption in either arm sticks (conservative). Tokens keep their
    # alias group, so a consumed alias stays consumed across the join.
    merged: dict[str, _Token] = {}
    names = set(then_tokens) | set(else_tokens)
    for name in names:
        then_token = then_tokens.get(name)
        else_token = else_tokens.get(name)
        if then_token is None or else_token is None:
            survivor = then_token or else_token
            assert survivor is not None
            # Bound in one arm only: its state is not definite afterwards.
            merged[name] = _Token(
                protocol=survivor.protocol,
                state=None,
                group=survivor.group,
                source_line=survivor.source_line,
            )
            continue
        merged_state = (
            then_token.state if then_token.state == else_token.state else None
        )
        merged[name] = _Token(
            protocol=then_token.protocol,
            state=merged_state,
            group=then_token.group,
            source_line=then_token.source_line,
        )
    state.tokens = merged
    state.consumed_groups |= then_state.consumed_groups | else_state.consumed_groups


def _handle_alias(stmt: IRBind, value: "IRExpr | None", state: _CheckState) -> None:
    """``copy = order`` shares the token group, so consumption is shared too."""
    if isinstance(value, IRRef) and value.name in state.tokens:
        state.tokens[stmt.name] = state.tokens[value.name]
        return
    if isinstance(value, IRCall) and value.anlu:
        # The result token is created by _handle_call when the callee
        # declares a result state.
        return


def _handle_call(
    value: "IRExpr | None",
    operation: IROperation,
    operations: dict[str, IROperation],
    protocols: dict[str, tuple[str, ...]],
    state: _CheckState,
    file_token: str,
    *,
    binding_name: str | None = None,
) -> None:
    """Check one call's protocol arguments and record its result token."""
    from .ir import iter_expr_nodes

    if value is None:
        return
    for node in iter_expr_nodes(value):
        if not isinstance(node, IRCall) or not node.anlu:
            continue
        callee = operations.get(node.target)
        if callee is None:
            continue
        line = node.span.line if node.span else (
            operation.span.line if operation.span else None
        )
        for index, param in enumerate(callee.params):
            protocol = _protocol_of(param.type_ref, protocols)
            if protocol is None:
                continue
            required_state = _state_of(param.type_ref)
            argument = node.args[index] if index < len(node.args) else None
            if argument is None:
                for kwarg_name, kwarg_value in node.kwargs:
                    if kwarg_name == param.name:
                        argument = kwarg_value
                        break
            if not isinstance(argument, IRRef) or argument.name not in state.tokens:
                # A non-token argument (literal, nested call, untyped name)
                # cannot be validated; fabrication is caught at declarations.
                continue
            token = state.tokens[argument.name]
            if token.protocol != protocol:
                state.diagnostics.append(
                    _diag(
                        ESEM014,
                        file_token,
                        line,
                        f"{operation.name}: token '{argument.name}' is a "
                        f"'{token.protocol}' resource but [{node.target}] requires "
                        f"a '{protocol}' token",
                        "Pass the right resource to the transition.",
                    )
                )
                continue
            if state.is_consumed(token):
                state.diagnostics.append(
                    _diag(
                        ESEM015,
                        file_token,
                        line,
                        f"{operation.name}: token '{argument.name}' was already "
                        f"consumed and cannot be passed to [{node.target}] again",
                        "A protocol token may be consumed once; obtain a new token "
                        "from a transition instead of reusing a spent one.",
                    )
                )
                continue
            if token.state is None:
                state.diagnostics.append(
                    _diag(
                        ESEM017,
                        file_token,
                        line,
                        f"{operation.name}: token '{argument.name}' has an ambiguous "
                        f"state at the branch join before [{node.target}]",
                        "Make both branch arms leave the token in the same state, or "
                        "restructure so the transition happens inside an arm.",
                    )
                )
                continue
            if required_state is not None and token.state != required_state:
                state.diagnostics.append(
                    _diag(
                        ESEM014,
                        file_token,
                        line,
                        f"{operation.name}: token '{argument.name}' is in state "
                        f"'{token.state}' but [{node.target}] requires "
                        f"'{required_state}'",
                        f"Run the transition that produces '{required_state}' first.",
                    )
                )
                continue
            state.consume(token)

        # Record the result token under the binding name when the callee
        # declares a result state. Only the root call of the expression owns
        # the binding; inner calls must not overwrite it.
        if binding_name is not None and node is value and callee.result is not None:
            result_type = callee.result.declared_type
            if result_type is not None:
                protocol = _protocol_of(result_type, protocols)
                result_state = _state_of(result_type)
                if protocol is not None and result_state is not None:
                    state.tokens[binding_name] = state.new_token(
                        protocol=protocol, state=result_state, line=line
                    )


