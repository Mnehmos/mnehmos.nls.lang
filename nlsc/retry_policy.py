"""Checked RETRY:/TIMEOUT: policies (Issue #201).

Static guarantees only: a bounded attempt budget, retryable identities the
operation can actually raise, an idempotency key for effectful replay, and
an explicit timeout outcome.  The checker says nothing about the provider
actually honoring the key, and a timeout never proves the operation
stopped — the external contracts are documented in the language spec.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .diagnostics import Diagnostic
from .error_catalog import ESEM018, ESEM019, ESEM020, ESEM021

if TYPE_CHECKING:
    from .ir import IRModule, IROperation


def check_retry_policies(module: "IRModule", file_token: str) -> list[Diagnostic]:
    """Validate every operation's retry/timeout policy shape."""
    diagnostics: list[Diagnostic] = []
    for operation in module.operations:
        line = operation.span.line if operation.span else None
        param_names = {param.name for param in operation.params}

        if operation.retry is not None:
            diagnostics.extend(
                _check_retry(operation, param_names, line, file_token)
            )
        if operation.timeout is not None:
            diagnostics.extend(_check_timeout(operation, line, file_token))
    return diagnostics


def _check_retry(
    operation: "IROperation", param_names: set[str], line: int | None, file_token: str
) -> list[Diagnostic]:
    retry = operation.retry
    assert retry is not None
    diagnostics: list[Diagnostic] = []
    if retry.attempts is None or retry.attempts <= 0:
        diagnostics.append(
            Diagnostic(
                code=ESEM018,
                file=file_token,
                line=line,
                col=None,
                message=f"{operation.name}: RETRY has no finite attempt budget",
                hint="Declare 'up to N attempts on <Errors>' with N > 0.",
            )
        )

    failures = operation.failures or ()
    unknown_failures = any(failure.origin == "unknown" for failure in failures)
    known_identities = {
        identity
        for failure in failures
        for identity in (failure.error_type, failure.code)
        if identity
    }
    # Retry acts only on the listed identities, so a declaration is
    # rejected when it provably cannot occur (the failure set is fully
    # known and lacks it).  When the set contains unknown markers the
    # author's classification is the only one available; unlisted unknown
    # failures are not retried.
    for error_type in retry.error_types:
        if not unknown_failures and error_type not in known_identities:
            diagnostics.append(
                Diagnostic(
                    code=ESEM019,
                    file=file_token,
                    line=line,
                    col=None,
                    message=(
                        f"{operation.name}: RETRY lists '{error_type}', which is not "
                        "a proven failure identity of this operation"
                    ),
                    hint=(
                        "Retry only errors from the inferred failure set; unknown "
                        "failures cannot be proven retryable."
                    ),
                )
            )

    effects = operation.effects
    if effects and retry.idempotency_key is None:
        diagnostics.append(
            Diagnostic(
                code=ESEM020,
                file=file_token,
                line=line,
                col=None,
                message=(
                    f"{operation.name}: retrying an operation with effects "
                    "requires an idempotency key"
                ),
                hint=(
                    "Add 'idempotency key: <param>' naming the input that "
                    "identifies the request."
                ),
            )
        )
    if (
        retry.idempotency_key is not None
        and retry.idempotency_key not in param_names
    ):
        diagnostics.append(
            Diagnostic(
                code=ESEM020,
                file=file_token,
                line=line,
                col=None,
                message=(
                    f"{operation.name}: idempotency key "
                    f"'{retry.idempotency_key}' is not a parameter"
                ),
                hint=(
                    "Key on an input so the same request value is used on every "
                    "attempt."
                ),
            )
        )
    return diagnostics


def _check_timeout(
    operation: "IROperation", line: int | None, file_token: str
) -> list[Diagnostic]:
    timeout = operation.timeout
    assert timeout is not None
    if timeout.after_ms is None or timeout.after_ms <= 0:
        return [
            Diagnostic(
                code=ESEM021,
                file=file_token,
                line=line,
                col=None,
                message=f"{operation.name}: TIMEOUT has no positive deadline",
                hint="Declare 'after Nms -> outcome' with N > 0.",
            )
        ]
    if not timeout.outcome:
        return [
            Diagnostic(
                code=ESEM021,
                file=file_token,
                line=line,
                col=None,
                message=(
                    f"{operation.name}: TIMEOUT declares no outcome for the deadline"
                ),
                hint=(
                    "State what happens when the deadline passes, e.g. "
                    "'after 5000ms -> cancel-and-reconcile'."
                ),
            )
        ]
    return []
