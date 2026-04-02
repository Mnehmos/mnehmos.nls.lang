"""Shared CLI diagnostics for stable structured error output."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .parser import ParseError
from .resolver import ResolutionError
from .schema import NLFile
from .stdlib_resolver import StdlibUseError
from .error_catalog import (
    EATOM001,
    EATOM002,
    ECONTRACT001,
    EFILE001,
    EGRAPH001,
    EGRAPH002,
    ELOCK001,
    ELOCK002,
    EPARSE001,
    EPARSE002,
    EWATCH001,
    E_RESOLUTION,
    ETEST001,
)


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


def missing_file_diagnostic(path: Path, *, subject: str = "File") -> Diagnostic:
    return Diagnostic(
        code=EFILE001,
        file=str(path),
        line=None,
        col=None,
        message=f"{subject} not found: {path}",
        hint="Check that the path exists and try again.",
    )


def watch_not_directory_diagnostic(path: Path) -> Diagnostic:
    return Diagnostic(
        code=EWATCH001,
        file=str(path),
        line=None,
        col=None,
        message=f"Watch path is not a directory: {path}",
        hint="Pass a directory path to `nlsc watch` and try again.",
    )


def atomize_syntax_error_diagnostic(path: Path, error: SyntaxError) -> Diagnostic:
    return Diagnostic(
        code=EATOM001,
        file=str(path),
        line=error.lineno or None,
        col=error.offset or None,
        message=f"Python syntax error: {error.msg}",
        hint="Fix the Python syntax and rerun `nlsc atomize`.",
    )


def atomize_failure_diagnostic(
    path: Path, exc: Exception, *, output_path: Path
) -> Diagnostic:
    return Diagnostic(
        code=EATOM002,
        file=str(path),
        line=None,
        col=None,
        message=f"Atomize failed while writing {output_path}: {exc}",
        hint="Check the output path and local filesystem permissions, then rerun `nlsc atomize`.",
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
        code=EPARSE001,
        file=str(path),
        line=line,
        col=None,
        message=message,
        hint=hint,
    )


def parser_backend_unavailable_diagnostic(backend: str, detail: str) -> Diagnostic:
    return Diagnostic(
        code=EPARSE002,
        file="<cli>",
        line=None,
        col=None,
        message=f"Parser backend '{backend}' is unavailable: {detail}",
        hint="Install with: pip install nlsc[treesitter], or rerun with --parser auto or --parser regex.",
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
                    code=E_RESOLUTION,
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
                code=E_RESOLUTION,
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
            code=ECONTRACT001,
            file=str(path),
            line=None,
            col=None,
            message=error,
            hint="Add the required contract field and verify again.",
        )
        for error in errors
    ]


def graph_anlu_not_found_diagnostic(
    path: Path, nl_file: NLFile, anlu_id: str
) -> Diagnostic:
    available = ", ".join(anlu.identifier for anlu in nl_file.anlus) or "none"
    return Diagnostic(
        code=EGRAPH001,
        file=str(path),
        line=None,
        col=None,
        message=f"ANLU '{anlu_id}' not found",
        hint=f"Choose one of the defined ANLUs: {available}.",
    )


def graph_format_diagnostic(path: Path, anlu: object, output_format: str) -> Diagnostic:
    line = getattr(anlu, "line_number", 0) or None
    return Diagnostic(
        code=EGRAPH002,
        file=str(path),
        line=line,
        col=1 if line is not None else None,
        message=f"Format '{output_format}' is not supported for ANLU dataflow graphs",
        hint="Use --format mermaid or --format ascii when selecting --anlu.",
    )


def test_execution_diagnostic(path: Path, pytest_exit_code: int | None) -> Diagnostic:
    if pytest_exit_code is None:
        message = "Generated tests could not be executed."
    else:
        message = f"Generated tests failed with pytest exit code {pytest_exit_code}."

    return Diagnostic(
        code=ETEST001,
        file=str(path),
        line=None,
        col=None,
        message=message,
        hint="Inspect pytest_stdout and pytest_stderr for failing assertions or setup errors.",
    )


def lockfile_unavailable_diagnostic(
    path: Path, *, unreadable: bool = False
) -> Diagnostic:
    message = f"Could not read lockfile: {path}"
    hint = "Run `nlsc compile <file>` or `nlsc lock:update <file>` to regenerate the lockfile."
    if not unreadable:
        message = f"Lockfile not found: {path}"
        hint = "Run `nlsc compile <file>` or `nlsc lock:update <file>` to generate a lockfile."

    return Diagnostic(
        code=ELOCK001,
        file=str(path),
        line=None,
        col=None,
        message=message,
        hint=hint,
    )


def lockfile_outdated_diagnostics(
    path: Path, nl_file: NLFile, errors: Sequence[str]
) -> list[Diagnostic]:
    anlu_lines = {anlu.identifier: anlu.line_number or None for anlu in nl_file.anlus}
    diagnostics: list[Diagnostic] = []
    for error in errors:
        anlu_id = _parse_lockfile_error_anlu(error)
        line = anlu_lines.get(anlu_id) if anlu_id is not None else None
        diagnostics.append(
            Diagnostic(
                code=ELOCK002,
                file=str(path),
                line=line,
                col=1 if line is not None else None,
                message=error,
                hint="Run `nlsc compile <file>` or `nlsc lock:update <file>` to regenerate the lockfile.",
            )
        )
    return diagnostics


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


def _parse_lockfile_error_anlu(error: str) -> str | None:
    if not error.startswith("ANLU "):
        return None
    parts = error.split()
    if len(parts) < 2:
        return None
    return parts[1]
