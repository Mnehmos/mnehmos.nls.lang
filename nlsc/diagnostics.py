"""Shared CLI diagnostics for stable structured error output."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .parser import ParseError
from .resolver import ResolutionError
from .schema import NLFile
from .stdlib_resolver import StdlibUseError


@dataclass(frozen=True)
class Diagnostic:
    code: str
    file: str
    line: int | None
    col: int | None
    message: str
    hint: str | None = None

    def to_dict(self) -> dict[str, object | None]:
        return {
            "code": self.code,
            "file": self.file,
            "line": self.line,
            "col": self.col,
            "message": self.message,
            "hint": self.hint,
        }


def missing_file_diagnostic(path: Path) -> Diagnostic:
    return Diagnostic(
        code="EFILE001",
        file=str(path),
        line=None,
        col=None,
        message=f"File not found: {path}",
        hint="Check that the path exists and try again.",
    )


def parse_error_diagnostic(path: Path, error: ParseError) -> Diagnostic:
    line = error.line_number or None
    prefix = f"Line {error.line_number}: " if error.line_number else ""
    message = str(error)
    if prefix and message.startswith(prefix):
        message = message[len(prefix) :]

    hint = "Fix the reported syntax and try again."
    if "Invalid LOGIC step format" in message:
        hint = "Rewrite the line as a numbered LOGIC step like '1. ...'."
    elif "Invalid INPUTS bullet marker" in message:
        hint = "Rewrite the line as an INPUTS bullet using -, *, or •."
    elif "Invalid GUARDS bullet marker" in message:
        hint = "Rewrite the line as a GUARDS bullet using -, *, or •."

    return Diagnostic(
        code="EPARSE001",
        file=str(path),
        line=line,
        col=None,
        message=message,
        hint=hint,
    )


def stdlib_use_diagnostic(path: Path, error: StdlibUseError) -> Diagnostic:
    line = _find_use_line(path, error.domain_spec)
    return Diagnostic(
        code=error.code,
        file=str(path),
        line=line,
        col=1 if line is not None else None,
        message=str(error),
        hint="Add the module under an stdlib root or pass --stdlib-path.",
    )


def dependency_error_diagnostics(
    path: Path, nl_file: NLFile, errors: Sequence[ResolutionError | str]
) -> list[Diagnostic]:
    anlu_lines = {anlu.identifier: anlu.line_number or None for anlu in nl_file.anlus}
    diagnostics: list[Diagnostic] = []
    for error in errors:
        if isinstance(error, str):
            anlu_id, _ = _split_dependency_error(error)
            line = anlu_lines.get(anlu_id) if anlu_id is not None else None
            diagnostics.append(
                Diagnostic(
                    code="E_RESOLUTION",
                    file=str(path),
                    line=line,
                    col=1 if line is not None else None,
                    message=error,
                    hint="Inspect the dependency graph and fix the unresolved reference.",
                )
            )
            continue

        hint = "Inspect the dependency graph and fix the unresolved reference."
        if error.missing_dep:
            hint = f"Define [{error.missing_dep}] or remove it from DEPENDS."
        elif "Circular dependency" in error.message:
            hint = "Break the cycle in the DEPENDS declarations."

        line = anlu_lines.get(error.anlu_id)
        diagnostics.append(
            Diagnostic(
                code="E_RESOLUTION",
                file=str(path),
                line=line,
                col=1 if line is not None else None,
                message=f"{error.anlu_id}: {error.message}",
                hint=hint,
            )
        )
    return diagnostics


def contract_error_diagnostics(path: Path, errors: list[str]) -> list[Diagnostic]:
    return [
        Diagnostic(
            code="ECONTRACT001",
            file=str(path),
            line=None,
            col=None,
            message=error,
            hint="Add the required contract field and verify again.",
        )
        for error in errors
    ]


def _find_use_line(path: Path, domain_spec: str) -> int | None:
    try:
        for index, raw_line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            line = raw_line.strip()
            if line.startswith("@use ") and line[5:].strip() == domain_spec:
                return index
    except OSError:
        return None
    return None


def _split_dependency_error(error: str) -> tuple[str | None, str]:
    if ":" not in error:
        return None, error
    anlu_id, message = error.split(":", 1)
    return anlu_id.strip() or None, message.strip()
