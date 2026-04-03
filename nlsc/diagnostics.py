"""Shared CLI diagnostics for stable structured error output."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Sequence

from .parser import ParseError
from .resolver import ResolutionError
from .schema import NLFile
from .stdlib_resolver import StdlibUseError
from .error_catalog import (
    ECLI001,
    EEXPLAIN001,
    EINIT001,
    EINIT002,
    EINIT003,
    EATOM001,
    EATOM002,
    EARTIFACT001,
    ECONTRACT001,
    EFILE001,
    EGRAPH001,
    EGRAPH002,
    ELOCK001,
    ELOCK002,
    ELOCK003,
    ELSP001,
    ELSP002,
    EASSOC001,
    EASSOC002,
    EASSOC003,
    EASSOC004,
    EPARSE001,
    EPARSE002,
    EWATCH001,
    E_RESOLUTION,
    ETEST001,
    EEXEC001,
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


def cli_parse_error_diagnostic(message: str) -> Diagnostic:
    message = _normalize_cli_parse_message(message)
    return Diagnostic(
        code=ECLI001,
        file="<cli>",
        line=None,
        col=None,
        message=message,
        hint="Rerun the command with --help to inspect the required arguments and valid options.",
    )


def explain_unknown_code_diagnostic(code: str) -> Diagnostic:
    return Diagnostic(
        code=EEXPLAIN001,
        file="<cli>",
        line=None,
        col=None,
        message=f"Unknown error code: {code}",
        hint="Run `nlsc explain --json ECLI001` or inspect `known_codes` to choose a cataloged error code.",
    )


def init_target_path_diagnostic(
    path: str | None, *, exists_as_file: bool = False
) -> Diagnostic:
    if exists_as_file:
        rendered_path = path or "<cli>"
        return Diagnostic(
            code=EINIT001,
            file=rendered_path,
            line=None,
            col=None,
            message=f"Init target path is not a directory: {rendered_path}",
            hint="Choose a directory path for `nlsc init`, or remove the conflicting file and rerun.",
        )

    return Diagnostic(
        code=EINIT001,
        file="<cli>",
        line=None,
        col=None,
        message="Init target path is missing or blank.",
        hint="Pass a directory path to `nlsc init`, or omit the argument to use the current directory.",
    )


def init_directory_creation_diagnostic(path: Path, exc: OSError) -> Diagnostic:
    return Diagnostic(
        code=EINIT002,
        file=str(path),
        line=None,
        col=None,
        message=f"Failed to create project directory: {path} ({exc})",
        hint="Check that the parent path exists and that you can create directories there, then rerun `nlsc init`.",
    )


def init_file_write_diagnostic(path: Path, exc: OSError) -> Diagnostic:
    return Diagnostic(
        code=EINIT003,
        file=str(path),
        line=None,
        col=None,
        message=f"Failed to write project file: {path} ({exc})",
        hint="Check the destination path and filesystem permissions, then rerun `nlsc init`.",
    )


def _normalize_cli_parse_message(message: str) -> str:
    return re.sub(
        r"\(choose from (?P<choices>[^)]*)\)",
        _strip_argparse_choice_quotes,
        message,
    )


def _strip_argparse_choice_quotes(match: re.Match[str]) -> str:
    choices = match.group("choices").replace("'", "")
    return f"(choose from {choices})"


def watch_not_directory_diagnostic(path: Path) -> Diagnostic:
    return Diagnostic(
        code=EWATCH001,
        file=str(path),
        line=None,
        col=None,
        message=f"Watch path is not a directory: {path}",
        hint="Pass a directory path to `nlsc watch` and try again.",
    )


def lsp_dependencies_unavailable_diagnostic(detail: str) -> Diagnostic:
    return Diagnostic(
        code=ELSP001,
        file="<cli>",
        line=None,
        col=None,
        message=f"LSP optional dependencies are unavailable: {detail}",
        hint="Install with: pip install nlsc[lsp] and rerun `nlsc lsp`.",
    )


def lsp_startup_failure_diagnostic(detail: str) -> Diagnostic:
    return Diagnostic(
        code=ELSP002,
        file="<cli>",
        line=None,
        col=None,
        message=f"LSP server failed to start: {detail}",
        hint="Check the selected transport, host, and port, then rerun `nlsc lsp`.",
    )


def assoc_platform_diagnostic() -> Diagnostic:
    return Diagnostic(
        code=EASSOC001,
        file="<cli>",
        line=None,
        col=None,
        message="File association command is only available on Windows.",
        hint="Run `nlsc assoc` on Windows, or manage `.nl` file associations with your OS tooling.",
    )


def assoc_icon_missing_diagnostic() -> Diagnostic:
    return Diagnostic(
        code=EASSOC002,
        file="<cli>",
        line=None,
        col=None,
        message="Could not find `nls-file.ico` in package resources.",
        hint="Run `python windows/generate_ico.py` from the project root to regenerate the icon asset.",
    )


def assoc_permission_diagnostic() -> Diagnostic:
    return Diagnostic(
        code=EASSOC003,
        file="<cli>",
        line=None,
        col=None,
        message="Permission denied while updating file associations.",
        hint="Rerun with elevated permissions or use `nlsc assoc --user` for a per-user association.",
    )


def assoc_runtime_failure_diagnostic(detail: str) -> Diagnostic:
    return Diagnostic(
        code=EASSOC004,
        file="<cli>",
        line=None,
        col=None,
        message=f"File association update failed: {detail}",
        hint="Inspect the Windows registry state and the reported runtime failure, then rerun `nlsc assoc`.",
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
    path: Path, exc: Exception, *, output_path: Path | None
) -> Diagnostic:
    if output_path is None:
        message = f"Atomize failed for {path}: {exc}"
    else:
        message = f"Atomize failed while writing {output_path}: {exc}"

    return Diagnostic(
        code=EATOM002,
        file=str(path),
        line=None,
        col=None,
        message=message,
        hint="Check the output path and local filesystem permissions, then rerun `nlsc atomize`.",
    )


def artifact_io_diagnostic(
    path: Path, exc: Exception, *, action: str, command: str
) -> Diagnostic:
    hint = f"Check the output path and filesystem permissions, then rerun `nlsc {command}`."
    if command == "lock:update" and action == "read":
        hint = "Check that the compiled artifact exists and is readable, or remove it so `nlsc lock:update` can regenerate it."

    return Diagnostic(
        code=EARTIFACT001,
        file=str(path),
        line=None,
        col=None,
        message=f"Failed to {action} artifact: {path} ({exc})",
        hint=hint,
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


def run_execution_failure_diagnostic(path: Path, exit_code: int) -> Diagnostic:
    return Diagnostic(
        code=EEXEC001,
        file=str(path),
        line=None,
        col=None,
        message=f"Generated program exited with code {exit_code}.",
        hint="Inspect stdout/stderr for the runtime failure and rerun `nlsc run` after fixing the generated behavior or inputs.",
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


def lockfile_write_diagnostic(path: Path, exc: OSError, *, command: str) -> Diagnostic:
    return Diagnostic(
        code=ELOCK003,
        file=str(path),
        line=None,
        col=None,
        message=f"Failed to write lockfile: {path} ({exc})",
        hint=f"Check the destination path and filesystem permissions, then rerun `nlsc {command}`.",
    )


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
