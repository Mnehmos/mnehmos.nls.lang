"""
NLS CLI - Command-line interface for nlsc

Commands:
    nlsc init              Initialize a new NLS project
    nlsc compile <file>    Compile .nl file to target language
    nlsc run <file>        Compile and execute in one step
    nlsc verify <file>     Verify .nl file without generating
    nlsc explain <code>    Explain a stable CLI error code
    nlsc graph <file>      Visualize dependencies and dataflow
    nlsc test <file>       Run @test specifications
    nlsc atomize <file>    Extract ANLUs from Python code
    nlsc diff <file>       Show changes since last compile
    nlsc watch <dir>       Watch directory for .nl changes
    nlsc lsp               Start the NLS language server
    nlsc assoc             Install Windows Explorer file association
"""

import argparse
import json
import os
import py_compile
import subprocess
import sys
from pathlib import Path
from typing import Any, NoReturn

from . import __version__
from .parser import ParseError
from .schema import NLFile
from .emitter import emit_python, emit_tests
from .emitter_typescript import emit_tests_typescript, emit_typescript
from .lockfile import generate_lockfile, write_lockfile, verify_lockfile
from .sourcemap import generate_source_map
from .graph import (
    emit_mermaid,
    emit_dot,
    emit_ascii,
    emit_dataflow_mermaid,
    emit_dataflow_ascii,
    emit_fsm_mermaid,
)
from .atomize import atomize_file
from .diff import (
    ANLUChange,
    get_anlu_changes,
    format_changes_output,
    format_stat_output,
    generate_full_diff,
)
from .diagnostics import (
    assoc_icon_missing_diagnostic,
    assoc_permission_diagnostic,
    assoc_platform_diagnostic,
    assoc_runtime_failure_diagnostic,
    atomize_failure_diagnostic,
    atomize_syntax_error_diagnostic,
    cli_parse_error_diagnostic,
    Diagnostic,
    contract_error_diagnostics,
    dependency_error_diagnostics,
    explain_unknown_code_diagnostic,
    graph_anlu_not_found_diagnostic,
    graph_format_diagnostic,
    init_directory_creation_diagnostic,
    init_file_write_diagnostic,
    init_target_path_diagnostic,
    lockfile_outdated_diagnostics,
    lockfile_unavailable_diagnostic,
    lsp_dependencies_unavailable_diagnostic,
    lsp_startup_failure_diagnostic,
    missing_file_diagnostic,
    parse_error_diagnostic,
    parser_backend_unavailable_diagnostic,
    run_execution_failure_diagnostic,
    stdlib_use_diagnostic,
    test_execution_diagnostic,
    watch_not_directory_diagnostic,
)
from .error_catalog import (
    ECLI001,
    EEXPLAIN001,
    EEXEC001,
    ETARGET001,
    EVALIDATE001,
    E_RUN,
    format_error_explanation,
    get_error_definition,
    known_error_codes,
)
from .lockfile import read_lockfile
from .watch import NLWatcher, format_timestamp
import platform
import shutil

from .pipeline import (
    create_temp_workdir,
    detect_treesitter,
    parse_nl_path_auto,
    validate_semantics,
)
from .stdlib_resolver import (
    StdlibUseError,
)


# Unicode symbols with ASCII fallbacks for Windows console
def _check() -> str:
    """Return checkmark, falling back to ASCII if needed."""
    try:
        "\u2713".encode(sys.stdout.encoding or "utf-8")
        return "\u2713"
    except (UnicodeEncodeError, LookupError):
        return "[OK]"


def _cross() -> str:
    """Return cross mark, falling back to ASCII if needed."""
    try:
        "\u2717".encode(sys.stdout.encoding or "utf-8")
        return "\u2717"
    except (UnicodeEncodeError, LookupError):
        return "[X]"


# Parser selection - default to tree-sitter if available
_use_treesitter = detect_treesitter()
_JSON_PARSER_BOOTSTRAP_COMMANDS = {
    "compile",
    "verify",
    "run",
    "explain",
    "test",
    "graph",
    "diff",
    "lsp",
    "watch",
    "lock:check",
    "lock:update",
}


class CLIParseError(RuntimeError):
    """Raised when argparse fails after a JSON request is detected."""

    def __init__(self, command: str, message: str, usage: str) -> None:
        super().__init__(message)
        self.command = command
        self.message = message
        self.usage = usage


def _normalize_command_name(command: str | None) -> str:
    if command == "dif":
        return "diff"
    return command or "nlsc"


def _infer_cli_context(argv: list[str]) -> tuple[str, bool]:
    command: str | None = None
    json_requested = False
    skip_next = False

    for token in argv:
        if skip_next:
            skip_next = False
            continue

        if token == "--parser":
            skip_next = True
            continue

        if token.startswith("--parser="):
            continue

        if token == "--json":
            json_requested = True
            continue

        if token.startswith("-"):
            continue

        if command is None:
            command = token

    return _normalize_command_name(command), json_requested


class NLSArgumentParser(argparse.ArgumentParser):
    """ArgumentParser that can switch parse failures to JSON diagnostics."""

    def __init__(self, *, argv: list[str] | None = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._argv = list(sys.argv[1:] if argv is None else argv)

    def error(self, message: str) -> NoReturn:
        command, json_requested = _infer_cli_context(self._argv)
        if json_requested:
            raise CLIParseError(command, message, self.format_usage().strip())
        super().error(message)


class ParserBootstrapError(RuntimeError):
    """Raised when the requested parser backend cannot be initialized."""

    def __init__(self, backend: str, detail: str) -> None:
        super().__init__(detail)
        self.backend = backend
        self.detail = detail


def _resolve_target(nl_file: NLFile, requested_target: str | None) -> str:
    """Resolve target from CLI override or module metadata."""
    return requested_target or nl_file.module.target or "python"


def _emit_target_code(
    nl_file: NLFile, target: str
) -> tuple[str, str, str | None, str | None]:
    """Emit module and optional tests for the selected target."""
    if target == "python":
        return emit_python(nl_file, mode="mock"), ".py", emit_tests(nl_file), ".py"
    if target == "typescript":
        return emit_typescript(nl_file), ".ts", emit_tests_typescript(nl_file), ".ts"
    raise ValueError(f"Target '{target}' not yet supported")


def _validate_target_output(target: str, output_path: Path) -> tuple[bool, str | None]:
    """Validate emitted output when a validator is available."""
    if target == "python":
        try:
            py_compile.compile(str(output_path), doraise=True)
        except py_compile.PyCompileError as exc:
            return False, str(exc)
    return True, None


def set_parser_backend(backend: str) -> None:
    """Set the parser backend to use: 'regex', 'treesitter', or 'auto'."""
    global _use_treesitter
    if backend == "auto":
        _use_treesitter = detect_treesitter()
    elif backend == "treesitter":
        # Check if tree-sitter is available
        try:
            from . import parser_treesitter

            if not parser_treesitter.is_available():
                raise ImportError("tree-sitter is not installed")
        except ImportError as e:
            raise ParserBootstrapError("treesitter", str(e)) from e
        _use_treesitter = True
    else:
        _use_treesitter = False


def _emit_parser_bootstrap_failure(
    args: argparse.Namespace, error: ParserBootstrapError
) -> int:
    command = getattr(args, "command", None) or "nlsc"
    json_output = command in _JSON_PARSER_BOOTSTRAP_COMMANDS and getattr(
        args, "json", False
    )
    diagnostic = parser_backend_unavailable_diagnostic(error.backend, error.detail)

    if json_output:
        return _emit_json(
            command, [diagnostic], file=diagnostic.file, parser=error.backend
        )

    print(f"Error: {diagnostic.message}", file=sys.stderr)
    if diagnostic.hint:
        print(diagnostic.hint, file=sys.stderr)
    return 1


def parse_nl_file_auto(source_path: Path) -> NLFile:
    """Parse a .nl file using the selected parser backend."""
    return parse_nl_path_auto(source_path, use_treesitter=_use_treesitter)


def _print_stdlib_use_error(error: StdlibUseError) -> None:
    """Emit a stable stdlib resolution diagnostic."""
    attempted = [str(p) for p in error.attempted_roots]
    print(
        f"Error: {error.code} domain={error.domain} major={error.major} "
        f"candidate_relpath={error.candidate_relpath} attempted_roots={attempted}",
        file=sys.stderr,
    )


def _emit_json(
    command: str,
    diagnostics: list[Diagnostic],
    *,
    status_code: int | None = None,
    **extra: object,
) -> int:
    payload: dict[str, object] = {
        "ok": not diagnostics,
        "command": command,
        "diagnostics": [diagnostic.to_dict() for diagnostic in diagnostics],
    }
    payload.update(extra)
    print(json.dumps(payload, indent=2))
    if status_code is not None:
        return status_code
    return 0 if not diagnostics else 1


def _emit_watch_runtime_json(path: Path, diagnostics: list[Diagnostic]) -> None:
    payload: dict[str, object] = {
        "ok": False,
        "command": "watch",
        "event": "compile",
        "phase": "runtime",
        "file": str(path),
        "diagnostics": [diagnostic.to_dict() for diagnostic in diagnostics],
    }
    print(json.dumps(payload, indent=2))


def _emit_cli_parse_failure(error: CLIParseError) -> int:
    diagnostic = cli_parse_error_diagnostic(error.message)
    return _emit_json(
        error.command,
        [diagnostic],
        usage=error.usage,
        error_type=ECLI001,
    )


def _emit_explain_definition_json(code: str) -> int:
    definition = get_error_definition(code)
    if definition is None:
        diagnostic = explain_unknown_code_diagnostic(code)
        return _emit_json(
            "explain",
            [diagnostic],
            requested_code=code,
            known_codes=list(known_error_codes()),
            error_type=EEXPLAIN001,
        )

    payload: dict[str, object] = {
        "ok": True,
        "command": "explain",
        "code": definition.code,
        "title": definition.title,
        "summary": definition.summary,
        "emitted_by": list(definition.emitted_by),
        "common_causes": list(definition.common_causes),
        "next_steps": list(definition.next_steps),
        "diagnostics": [],
    }
    print(json.dumps(payload, indent=2))
    return 0


def _anlu_change_to_dict(change: ANLUChange) -> dict[str, str]:
    return {
        "identifier": change.identifier,
        "status": change.status,
        "details": change.details,
    }


def _diff_summary(changes: list[ANLUChange]) -> dict[str, int]:
    summary = {
        "unchanged": 0,
        "modified": 0,
        "new": 0,
        "removed": 0,
    }
    for change in changes:
        summary[change.status] = summary.get(change.status, 0) + 1
    return summary


def _emit_lsp_startup_failure(args: argparse.Namespace, diagnostic: Diagnostic) -> int:
    transport = getattr(args, "transport", "stdio")
    host = getattr(args, "host", "127.0.0.1")
    port = getattr(args, "port", 2087)

    if getattr(args, "json", False):
        return _emit_json(
            "lsp",
            [diagnostic],
            transport=transport,
            host=host,
            port=port,
        )

    print(f"Error [{diagnostic.code}]: {diagnostic.message}", file=sys.stderr)
    if diagnostic.hint:
        print(diagnostic.hint, file=sys.stderr)
    return 1


def _format_dependency_error(error: object) -> str:
    if hasattr(error, "anlu_id") and hasattr(error, "message"):
        anlu_id = getattr(error, "anlu_id")
        message = getattr(error, "message")
        return f"{anlu_id}: {message}"
    return str(error)


def cmd_explain(args: argparse.Namespace) -> int:
    """Explain a stable CLI error code."""
    if getattr(args, "json", False):
        return _emit_explain_definition_json(args.code)

    definition = get_error_definition(args.code)
    if definition is None:
        diagnostic = explain_unknown_code_diagnostic(args.code)
        print(f"Error [{diagnostic.code}]: {diagnostic.message}", file=sys.stderr)
        print(f"Known codes: {', '.join(known_error_codes())}", file=sys.stderr)
        return 1

    print(format_error_explanation(definition))
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    """Initialize a new NLS project"""
    json_output = getattr(args, "json", False)
    raw_path = getattr(args, "path", ".")

    if raw_path is None or not str(raw_path).strip():
        diagnostic = init_target_path_diagnostic(raw_path)
        if json_output:
            return _emit_json(
                "init", [diagnostic], path="" if raw_path is None else str(raw_path)
            )
        print(f"Error [{diagnostic.code}]: {diagnostic.message}", file=sys.stderr)
        if diagnostic.hint:
            print(diagnostic.hint, file=sys.stderr)
        return 1

    project_dir = Path(str(raw_path))

    if project_dir.exists() and not project_dir.is_dir():
        diagnostic = init_target_path_diagnostic(str(project_dir), exists_as_file=True)
        if json_output:
            return _emit_json("init", [diagnostic], path=str(project_dir))
        print(f"Error [{diagnostic.code}]: {diagnostic.message}", file=sys.stderr)
        if diagnostic.hint:
            print(diagnostic.hint, file=sys.stderr)
        return 1

    # Create project directory if it doesn't exist
    try:
        project_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        diagnostic = init_directory_creation_diagnostic(project_dir, exc)
        if json_output:
            return _emit_json("init", [diagnostic], path=str(project_dir))
        print(f"Error [{diagnostic.code}]: {diagnostic.message}", file=sys.stderr)
        if diagnostic.hint:
            print(diagnostic.hint, file=sys.stderr)
        return 1

    if not json_output:
        print(f"Initializing NLS project in {project_dir.absolute()}...")

    created_entries: list[str] = []
    existing_entries: list[str] = []

    # Create config file
    config_path = project_dir / "nl.config.yaml"
    if not config_path.exists():
        config_content = """\
# NLS Project Configuration
# Generated by nlsc init

project:
  name: my-project
  version: 0.1.0

compiler:
  default_target: python
  llm_backend: mock  # mock, claude, openai, ollama
  cache_strategy: aggressive

targets:
  python:
    version: ">=3.11"
    style: black
    type_hints: strict

validation:
  require_purpose: true
  require_guards: false
  max_anlu_complexity: 10
"""
        try:
            config_path.write_text(config_content, encoding="utf-8")
        except OSError as exc:
            diagnostic = init_file_write_diagnostic(config_path, exc)
            if json_output:
                return _emit_json("init", [diagnostic], path=str(project_dir))
            print(f"Error [{diagnostic.code}]: {diagnostic.message}", file=sys.stderr)
            if diagnostic.hint:
                print(diagnostic.hint, file=sys.stderr)
            return 1
        created_entries.append(config_path.name)
        if not json_output:
            print(f"  {_check()} Created {config_path.name}")
    else:
        existing_entries.append(config_path.name)
        if not json_output:
            print(f"  • {config_path.name} already exists")

    # Create directories
    src_dir = project_dir / "src"
    tests_dir = project_dir / "tests"

    for dir_path in [src_dir, tests_dir]:
        if not dir_path.exists():
            try:
                dir_path.mkdir(parents=True)
            except OSError as exc:
                diagnostic = init_directory_creation_diagnostic(dir_path, exc)
                if json_output:
                    return _emit_json("init", [diagnostic], path=str(project_dir))
                print(
                    f"Error [{diagnostic.code}]: {diagnostic.message}", file=sys.stderr
                )
                if diagnostic.hint:
                    print(diagnostic.hint, file=sys.stderr)
                return 1
            created_entries.append(f"{dir_path.name}/")
            if not json_output:
                print(f"  {_check()} Created {dir_path.name}/")
        else:
            existing_entries.append(f"{dir_path.name}/")
            if not json_output:
                print(f"  • {dir_path.name}/ already exists")

    # Create __init__.py files
    for init_path in [src_dir / "__init__.py", tests_dir / "__init__.py"]:
        if not init_path.exists():
            try:
                init_path.write_text("", encoding="utf-8")
            except OSError as exc:
                diagnostic = init_file_write_diagnostic(init_path, exc)
                if json_output:
                    return _emit_json("init", [diagnostic], path=str(project_dir))
                print(
                    f"Error [{diagnostic.code}]: {diagnostic.message}", file=sys.stderr
                )
                if diagnostic.hint:
                    print(diagnostic.hint, file=sys.stderr)
                return 1
            created_entries.append(str(init_path.relative_to(project_dir)))
        else:
            existing_entries.append(str(init_path.relative_to(project_dir)))

    if json_output:
        return _emit_json(
            "init",
            [],
            path=str(project_dir),
            created=created_entries,
            existing=existing_entries,
        )

    print("\nNLS project initialized! Next steps:")
    print("  1. Create a .nl file in src/")
    print("  2. Run: nlsc compile src/your-file.nl")

    return 0


def cmd_compile(args: argparse.Namespace) -> int:
    """Compile a .nl file to target language"""
    source_path = Path(args.file)
    json_output = getattr(args, "json", False)

    if not source_path.exists():
        diagnostic = missing_file_diagnostic(source_path)
        if json_output:
            return _emit_json("compile", [diagnostic], file=str(source_path))
        print(f"Error: {diagnostic.message}", file=sys.stderr)
        print(f"Error: {diagnostic.hint}", file=sys.stderr)
        return 1

    parser_name = "tree-sitter" if _use_treesitter else "regex"
    if not json_output:
        print(f"Compiling {source_path} (parser: {parser_name})...")

    # Parse
    try:
        nl_file = parse_nl_file_auto(source_path)
        if not json_output:
            print(f"  {_check()} Parsed {len(nl_file.anlus)} ANLUs")
    except ParseError as e:
        diagnostic = parse_error_diagnostic(source_path, e)
        if json_output:
            return _emit_json("compile", [diagnostic], file=str(source_path))
        print(f"  {_cross()} Parse error: {e}", file=sys.stderr)
        return 1

    try:
        validation = validate_semantics(
            nl_file,
            source_path,
            cli_stdlib_paths=getattr(args, "stdlib_path", None),
        )
    except StdlibUseError as e:
        if json_output:
            return _emit_json(
                "compile",
                [stdlib_use_diagnostic(source_path, e)],
                file=str(source_path),
            )
        _print_stdlib_use_error(e)
        return 1

    if not json_output:
        for resolved in validation.resolved_uses:
            print(f"  {_check()} @use {resolved.domain} -> {resolved.path}")

    if validation.dependency_errors:
        diagnostics = dependency_error_diagnostics(
            source_path, nl_file, validation.dependency_errors
        )
        if json_output:
            return _emit_json("compile", diagnostics, file=str(source_path))
        print(f"  {_cross()} Resolution errors:", file=sys.stderr)
        for err in validation.dependency_errors:
            print(f"    - {_format_dependency_error(err)}", file=sys.stderr)
        return 1
    if not json_output:
        print(f"  {_check()} Resolved dependencies")

    target = _resolve_target(nl_file, getattr(args, "target", None))
    try:
        generated_code, output_suffix, test_code, test_suffix = _emit_target_code(
            nl_file, target
        )
    except ValueError as exc:
        if json_output:
            diagnostic = Diagnostic(
                code=ETARGET001,
                file=str(source_path),
                line=None,
                col=None,
                message=str(exc),
                hint="Select a supported target and try again.",
            )
            return _emit_json("compile", [diagnostic], file=str(source_path))
        print(f"  {_cross()} {exc}", file=sys.stderr)
        return 1

    # Determine output path
    output_path = source_path.with_suffix(output_suffix)
    if args.output:
        output_path = Path(args.output)

    output_path.write_text(generated_code, encoding="utf-8")
    line_count = generated_code.count("\n") + 1
    if not json_output:
        print(f"  {_check()} Generated {output_path.name} ({line_count} lines)")

    is_valid, validation_error = _validate_target_output(target, output_path)
    if not is_valid:
        if json_output:
            diagnostic = Diagnostic(
                code=EVALIDATE001,
                file=str(output_path),
                line=None,
                col=None,
                message=f"py_compile validation failed for {output_path}: {validation_error}",
                hint="Inspect the generated output and compiler logic.",
            )
            return _emit_json("compile", [diagnostic], file=str(source_path))
        print(
            f"  {_cross()} py_compile validation failed for {output_path}: {validation_error}",
            file=sys.stderr,
        )
        return 1

    if test_code and nl_file.tests:
        test_path = source_path.parent / f"test_{source_path.stem}{test_suffix}"
        test_path.write_text(test_code, encoding="utf-8")
        if not json_output:
            print(f"  {_check()} Generated {test_path.name}")

    # Generate lockfile
    lock_path = source_path.with_suffix(".nl.lock")
    lockfile = generate_lockfile(
        nl_file,
        generated_code,
        str(output_path),
        llm_backend="mock",
        target=target,
    )
    write_lockfile(lockfile, lock_path)
    if json_output:
        return _emit_json(
            "compile",
            [],
            file=str(source_path),
            output=str(output_path),
            lockfile=str(lock_path),
            target=target,
            line_count=line_count,
        )
    print(f"  {_check()} Updated {lock_path.name}")

    print("\nCompilation complete!")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    """Verify a .nl file without generating code"""
    source_path = Path(args.file)
    json_output = getattr(args, "json", False)

    if not source_path.exists():
        diagnostic = missing_file_diagnostic(source_path)
        if json_output:
            return _emit_json("verify", [diagnostic], file=str(source_path))
        print(f"Error: {diagnostic.message}", file=sys.stderr)
        return 1

    parser_name = "tree-sitter" if _use_treesitter else "regex"
    if not json_output:
        print(f"Verifying {source_path} (parser: {parser_name})...")

    # Parse
    try:
        nl_file = parse_nl_file_auto(source_path)
        if not json_output:
            print(f"  {_check()} Syntax valid: {len(nl_file.anlus)} ANLUs")
    except ParseError as e:
        diagnostic = parse_error_diagnostic(source_path, e)
        if json_output:
            return _emit_json("verify", [diagnostic], file=str(source_path))
        print(f"  {_cross()} Parse error: {e}", file=sys.stderr)
        return 1

    try:
        validation = validate_semantics(
            nl_file,
            source_path,
            require_contract_fields=True,
        )
    except StdlibUseError as e:
        if json_output:
            return _emit_json(
                "verify", [stdlib_use_diagnostic(source_path, e)], file=str(source_path)
            )
        _print_stdlib_use_error(e)
        return 1
    if validation.resolved_uses:
        if not json_output:
            print(
                f"  {_check()} Resolved {len(validation.resolved_uses)} @use directive(s)"
            )

    if validation.dependency_errors:
        diagnostics = dependency_error_diagnostics(
            source_path, nl_file, validation.dependency_errors
        )
        if json_output:
            return _emit_json("verify", diagnostics, file=str(source_path))
        print(f"  {_cross()} Resolution errors:")
        for err in validation.dependency_errors:
            print(f"    - {_format_dependency_error(err)}")
        return 1
    if not json_output:
        print(f"  {_check()} Dependencies valid")

    if validation.contract_errors:
        diagnostics = contract_error_diagnostics(
            source_path, validation.contract_errors
        )
        if json_output:
            return _emit_json("verify", diagnostics, file=str(source_path))
        print(f"  {_cross()} Validation errors:")
        for validation_err in validation.contract_errors:
            print(f"    - {validation_err}")
        return 1

    if json_output:
        return _emit_json(
            "verify", [], file=str(source_path), anlu_count=len(nl_file.anlus)
        )
    print(f"  {_check()} All ANLUs valid")
    print("\nVerification passed!")
    return 0


def cmd_graph(args: argparse.Namespace) -> int:
    """Generate dependency graph visualization"""
    source_path = Path(args.file)
    json_output = getattr(args, "json", False)

    if not source_path.exists():
        diagnostic = missing_file_diagnostic(source_path)
        if json_output:
            return _emit_json("graph", [diagnostic], file=str(source_path))
        print(f"Error: {diagnostic.message}", file=sys.stderr)
        print(f"Error: {diagnostic.hint}", file=sys.stderr)
        return 1

    # Parse
    try:
        nl_file = parse_nl_file_auto(source_path)
    except ParseError as e:
        diagnostic = parse_error_diagnostic(source_path, e)
        if json_output:
            return _emit_json("graph", [diagnostic], file=str(source_path))
        print(f"Parse error: {e}", file=sys.stderr)
        return 1

    output_format = args.format or "mermaid"
    anlu_id = args.anlu
    dataflow = args.dataflow
    graph_kind = "dependency"

    # If specific ANLU requested
    if anlu_id:
        anlu = nl_file.get_anlu(anlu_id)
        if not anlu:
            diagnostic = graph_anlu_not_found_diagnostic(source_path, nl_file, anlu_id)
            if json_output:
                return _emit_json("graph", [diagnostic], file=str(source_path))
            print(f"Error: {diagnostic.message}", file=sys.stderr)
            print(f"Error: {diagnostic.hint}", file=sys.stderr)
            return 1

        # Check if ANLU has FSM states
        has_fsm = bool(anlu.fsm_states())

        if output_format == "mermaid":
            if has_fsm and not dataflow:
                graph_kind = "fsm"
                output = emit_fsm_mermaid(anlu)
            else:
                graph_kind = "dataflow"
                output = emit_dataflow_mermaid(anlu)
        elif output_format == "ascii":
            graph_kind = "dataflow"
            output = emit_dataflow_ascii(anlu)
        else:
            diagnostic = graph_format_diagnostic(source_path, anlu, output_format)
            if json_output:
                return _emit_json("graph", [diagnostic], file=str(source_path))
            print(f"Error: {diagnostic.message}", file=sys.stderr)
            print(f"Error: {diagnostic.hint}", file=sys.stderr)
            return 1
    else:
        # Full file dependency graph
        if output_format == "mermaid":
            output = emit_mermaid(nl_file)
        elif output_format == "dot":
            output = emit_dot(nl_file)
        elif output_format == "ascii":
            output = emit_ascii(nl_file)
        else:
            print(f"Error: Unknown format '{output_format}'", file=sys.stderr)
            return 1

    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output, encoding="utf-8")
        if json_output:
            return _emit_json(
                "graph",
                [],
                file=str(source_path),
                format=output_format,
                anlu=anlu_id,
                dataflow=graph_kind == "dataflow",
                graph_kind=graph_kind,
                output_file=str(output_path),
                graph=output,
            )
        print(f"Graph written to {output_path}")
    else:
        if json_output:
            return _emit_json(
                "graph",
                [],
                file=str(source_path),
                format=output_format,
                anlu=anlu_id,
                dataflow=graph_kind == "dataflow",
                graph_kind=graph_kind,
                output_file=None,
                graph=output,
            )
        print(output)

    return 0


def cmd_test(args: argparse.Namespace) -> int:
    """Run @test specifications from a .nl file"""
    source_path = Path(args.file)
    json_output = getattr(args, "json", False)

    if not source_path.exists():
        diagnostic = missing_file_diagnostic(source_path)
        if json_output:
            return _emit_json("test", [diagnostic], file=str(source_path))
        print(f"Error: {diagnostic.message}", file=sys.stderr)
        return 1

    # Parse
    try:
        nl_file = parse_nl_file_auto(source_path)
    except ParseError as e:
        diagnostic = parse_error_diagnostic(source_path, e)
        if json_output:
            return _emit_json("test", [diagnostic], file=str(source_path))
        print(f"Parse error: {e}", file=sys.stderr)
        return 1

    try:
        validation = validate_semantics(nl_file, source_path)
    except StdlibUseError as e:
        diagnostic = stdlib_use_diagnostic(source_path, e)
        if json_output:
            return _emit_json("test", [diagnostic], file=str(source_path))
        _print_stdlib_use_error(e)
        return 1

    if validation.dependency_errors:
        diagnostics = dependency_error_diagnostics(
            source_path, nl_file, validation.dependency_errors
        )
        if json_output:
            return _emit_json("test", diagnostics, file=str(source_path))
        print(f"{_cross()} Resolution errors:", file=sys.stderr)
        for err in validation.dependency_errors:
            print(f"  - {_format_dependency_error(err)}", file=sys.stderr)
        return 1

    # Check for tests
    if not nl_file.tests:
        if json_output:
            return _emit_json(
                "test",
                [],
                file=str(source_path),
                total_cases=0,
                pytest_exit_code=None,
                pytest_stdout="",
                pytest_stderr="",
            )
        print(f"No @test blocks found in {source_path}")
        return 0

    temp_path = create_temp_workdir("nlsc_test_", preferred_root=source_path.parent)
    try:
        # Generate the module code
        python_code = emit_python(nl_file, mode="mock")
        module_name = nl_file.module.name.replace("-", "_")
        module_path = temp_path / f"{module_name}.py"
        module_path.write_text(python_code, encoding="utf-8")

        # Generate the test code
        test_code = emit_tests(nl_file)
        if not test_code:
            print(f"No tests generated from {source_path}")
            return 0

        # Fix import to be direct (not relative)
        test_code = test_code.replace(
            f"from .{module_name} import *", f"from {module_name} import *"
        )
        test_path = temp_path / f"test_{module_name}.py"
        test_path.write_text(test_code, encoding="utf-8")

        # Create __init__.py
        init_path = temp_path / "__init__.py"
        init_path.write_text("", encoding="utf-8")

        # Print summary
        total_cases = sum(len(ts.cases) for ts in nl_file.tests)
        if not json_output:
            print(f"Running {total_cases} test cases from {source_path}...")
            for ts in nl_file.tests:
                print(f"  • [{ts.anlu_id}]: {len(ts.cases)} cases")
            print()

        # Run pytest
        verbose_flag = "-v" if getattr(args, "verbose", False) else "-q"
        pytest_args = [
            sys.executable,
            "-m",
            "pytest",
            str(test_path),
            verbose_flag,
            "--tb=short",
        ]

        if getattr(args, "case", None):
            pytest_args.extend(["-k", args.case])

        env = os.environ.copy()
        existing_pythonpath = env.get("PYTHONPATH", "")
        pythonpath_parts = [str(temp_path), str(source_path.parent.resolve())]
        if existing_pythonpath:
            pythonpath_parts.append(existing_pythonpath)
        env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

        result = subprocess.run(
            pytest_args,
            cwd=str(temp_path),
            capture_output=json_output or not getattr(args, "verbose", False),
            text=True,
            env=env,
        )

        # Report results
        if result.returncode == 0:
            if json_output:
                return _emit_json(
                    "test",
                    [],
                    file=str(source_path),
                    total_cases=total_cases,
                    pytest_exit_code=result.returncode,
                    pytest_stdout=result.stdout or "",
                    pytest_stderr=result.stderr or "",
                )
            print(f"{_check()} All {total_cases} tests passed!")
            return 0

        if json_output:
            return _emit_json(
                "test",
                [test_execution_diagnostic(source_path, result.returncode)],
                file=str(source_path),
                total_cases=total_cases,
                pytest_exit_code=result.returncode,
                pytest_stdout=result.stdout or "",
                pytest_stderr=result.stderr or "",
            )

        print(f"{_cross()} Tests failed")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return 1
    except OSError as exc:
        diagnostic = test_execution_diagnostic(source_path, None)
        if json_output:
            return _emit_json(
                "test",
                [diagnostic],
                file=str(source_path),
                total_cases=0,
                pytest_exit_code=None,
                pytest_stdout="",
                pytest_stderr=str(exc),
            )
        print(f"{_cross()} {diagnostic.message}", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1
    finally:
        shutil.rmtree(temp_path, ignore_errors=True)


def cmd_atomize(args: argparse.Namespace) -> int:
    """Extract ANLUs from Python source code"""
    source_path = Path(args.file)
    json_output = getattr(args, "json", False)

    if not source_path.exists():
        diagnostic = missing_file_diagnostic(source_path)
        if json_output:
            return _emit_json("atomize", [diagnostic], file=str(source_path))
        print(f"Error: {diagnostic.message}", file=sys.stderr)
        return 1

    # Determine output path
    output_path = Path(args.output) if args.output else source_path.with_suffix(".nl")

    # Determine module name
    module_name = args.module

    if not json_output:
        print(f"Atomizing {source_path}...")

    try:
        nl_content = atomize_file(source_path, output_path, module_name)

        # Count ANLUs
        anlu_count = nl_content.count("[") - nl_content.count("[[")
        final_output = output_path

        if json_output:
            return _emit_json(
                "atomize",
                [],
                file=str(source_path),
                output=str(final_output),
                anlu_count=anlu_count,
                module=module_name or source_path.stem.replace("_", "-"),
            )

        print(f"  {_check()} Extracted {anlu_count} ANLUs")
        print(f"  {_check()} Wrote {final_output}")
        return 0
    except SyntaxError as e:
        diagnostic = atomize_syntax_error_diagnostic(source_path, e)
        if json_output:
            return _emit_json("atomize", [diagnostic], file=str(source_path))
        print(f"  {_cross()} {diagnostic.message}", file=sys.stderr)
        return 1
    except Exception as e:
        diagnostic = atomize_failure_diagnostic(source_path, e, output_path=output_path)
        if json_output:
            return _emit_json("atomize", [diagnostic], file=str(source_path))
        print(f"  {_cross()} {diagnostic.message}", file=sys.stderr)
        return 1


def cmd_diff(args: argparse.Namespace) -> int:
    """Show changes since last compile"""
    source_path = Path(args.file)
    json_output = getattr(args, "json", False)

    if not source_path.exists():
        diagnostic = missing_file_diagnostic(source_path)
        if json_output:
            return _emit_json("diff", [diagnostic], file=str(source_path))
        print(f"Error: {diagnostic.message}", file=sys.stderr)
        print(f"Error: {diagnostic.hint}", file=sys.stderr)
        return 1

    # Parse current NL file
    try:
        nl_file = parse_nl_file_auto(source_path)
    except ParseError as e:
        diagnostic = parse_error_diagnostic(source_path, e)
        if json_output:
            return _emit_json("diff", [diagnostic], file=str(source_path))
        print(f"Parse error: {e}", file=sys.stderr)
        return 1

    # Load lockfile if exists
    lock_path = source_path.with_suffix(".nl.lock")
    lockfile = None
    lockfile_present = lock_path.exists()
    lockfile_error = None
    if lockfile_present:
        if not lock_path.is_file():
            lockfile_error = f"Lockfile path is not a regular file: {lock_path}"
        else:
            try:
                lockfile = read_lockfile(lock_path)
            except Exception as e:
                lockfile_error = str(e)
                if not json_output:
                    print(f"Warning: Could not read lockfile: {e}", file=sys.stderr)

            if lockfile is None and lockfile_error is None:
                lockfile_error = f"Could not load lockfile: {lock_path}"

    # Get changes
    changes = get_anlu_changes(nl_file, lockfile)

    mode = "changes"
    text_output = ""

    # Output based on flags
    if args.stat:
        mode = "stat"
        text_output = format_stat_output(changes)
    elif args.full:
        mode = "full"
        target = _resolve_target(nl_file, None)
        generated_code, output_suffix, _, _ = _emit_target_code(nl_file, target)
        output_path = source_path.with_suffix(output_suffix)
        if output_path.exists():
            previous_code = output_path.read_text(encoding="utf-8")
            text_output = generate_full_diff(
                previous_code,
                generated_code,
                output_path.name,
            )
        else:
            text_output = (
                f"No existing compiled output to diff against: {output_path.name}.\n"
                f"{format_changes_output(changes)}"
            )
    else:
        text_output = format_changes_output(changes)

    if json_output:
        return _emit_json(
            "diff",
            [],
            file=str(source_path),
            lockfile=str(lock_path),
            lockfile_present=lockfile_present,
            lockfile_loaded=lockfile is not None,
            lockfile_error=lockfile_error,
            mode=mode,
            summary=_diff_summary(changes),
            changes=[_anlu_change_to_dict(change) for change in changes],
            text=text_output,
        )

    if lockfile is None:
        print("No lockfile found. All ANLUs shown as new.\n")

    print(text_output)

    return 0


def cmd_watch(args: argparse.Namespace) -> int:
    """Watch directory for .nl file changes and recompile"""
    watch_path = Path(args.dir)
    json_output = getattr(args, "json", False)

    if not watch_path.exists():
        diagnostic = missing_file_diagnostic(watch_path, subject="Directory")
        if json_output:
            return _emit_json("watch", [diagnostic], file=str(watch_path))
        print(f"Error: {diagnostic.message}", file=sys.stderr)
        return 1

    if not watch_path.is_dir():
        diagnostic = watch_not_directory_diagnostic(watch_path)
        if json_output:
            return _emit_json("watch", [diagnostic], file=str(watch_path))
        print(f"Error: {diagnostic.message}", file=sys.stderr)
        return 1

    quiet = args.quiet
    run_tests = args.test
    debounce_ms = args.debounce

    def on_compile(
        path: Path,
        success: bool,
        error: str | None,
        diagnostics: list[Diagnostic] | None = None,
    ) -> None:
        """Callback for compile events"""
        if json_output and not success and diagnostics:
            _emit_watch_runtime_json(path, diagnostics)
            return

        timestamp = format_timestamp()
        if success:
            if not quiet:
                print(f"{timestamp} " + _check() + "  Compiled {path.name}")
        else:
            print(
                f"{timestamp} " + _cross() + "  {path.name}: {error}", file=sys.stderr
            )

    print(f"Watching {watch_path.absolute()} for .nl changes...")
    print("Press Ctrl+C to stop.\n")

    watcher = NLWatcher(
        watch_path=watch_path,
        debounce_ms=debounce_ms,
        quiet=quiet,
        run_tests=run_tests,
        on_compile=on_compile,
    )

    try:
        watcher.start()
    except KeyboardInterrupt:
        watcher.stop()
        print("\nStopped watching.")

    return 0


def cmd_lock_check(args: argparse.Namespace) -> int:
    """Verify that lockfile is current with source"""
    source_path = Path(args.file)
    json_output = getattr(args, "json", False)

    if not source_path.exists():
        diagnostic = missing_file_diagnostic(source_path)
        if json_output:
            return _emit_json("lock:check", [diagnostic], file=str(source_path))
        print(f"Error: {diagnostic.message}", file=sys.stderr)
        return 1

    lock_path = source_path.with_suffix(".nl.lock")
    if not lock_path.exists():
        diagnostic = lockfile_unavailable_diagnostic(lock_path)
        if json_output:
            return _emit_json(
                "lock:check",
                [diagnostic],
                file=str(source_path),
                lockfile=str(lock_path),
            )
        print(f"Error: {diagnostic.message}", file=sys.stderr)
        return 1

    # Parse current NL file
    try:
        nl_file = parse_nl_file_auto(source_path)
    except ParseError as e:
        diagnostic = parse_error_diagnostic(source_path, e)
        if json_output:
            return _emit_json(
                "lock:check",
                [diagnostic],
                file=str(source_path),
                lockfile=str(lock_path),
            )
        print(f"Parse error: {e}", file=sys.stderr)
        return 1

    # Read lockfile
    lockfile = read_lockfile(lock_path)
    if not lockfile:
        diagnostic = lockfile_unavailable_diagnostic(lock_path, unreadable=True)
        if json_output:
            return _emit_json(
                "lock:check",
                [diagnostic],
                file=str(source_path),
                lockfile=str(lock_path),
            )
        print(f"Error: {diagnostic.message}", file=sys.stderr)
        return 1

    # Verify
    errors = verify_lockfile(lockfile, nl_file)

    if errors:
        diagnostics = lockfile_outdated_diagnostics(source_path, nl_file, errors)
        if json_output:
            return _emit_json(
                "lock:check",
                diagnostics,
                file=str(source_path),
                lockfile=str(lock_path),
            )
        print("Lockfile out of date:")
        for err in errors:
            print(f"  • {err}")
        return 1

    if json_output:
        return _emit_json(
            "lock:check",
            [],
            file=str(source_path),
            lockfile=str(lock_path),
            anlu_count=len(nl_file.anlus),
        )
    print(f"{_check()} Lockfile is current")
    return 0


def cmd_lock_update(args: argparse.Namespace) -> int:
    """Regenerate lockfile from current source and compiled output"""
    source_path = Path(args.file)
    json_output = getattr(args, "json", False)

    if not source_path.exists():
        diagnostic = missing_file_diagnostic(source_path)
        if json_output:
            return _emit_json("lock:update", [diagnostic], file=str(source_path))
        print(f"Error: {diagnostic.message}", file=sys.stderr)
        return 1

    # Parse current NL file
    try:
        nl_file = parse_nl_file_auto(source_path)
    except ParseError as e:
        diagnostic = parse_error_diagnostic(source_path, e)
        if json_output:
            return _emit_json("lock:update", [diagnostic], file=str(source_path))
        print(f"Parse error: {e}", file=sys.stderr)
        return 1

    target = _resolve_target(nl_file, None)
    output_suffix = ".py" if target == "python" else ".ts"
    output_path = source_path.with_suffix(output_suffix)
    if not output_path.exists():
        if not json_output:
            print(f"Warning: Compiled file not found, generating fresh: {output_path}")
        try:
            generated_code, _, _, _ = _emit_target_code(nl_file, target)
        except ValueError as exc:
            if json_output:
                diagnostic = Diagnostic(
                    code=ETARGET001,
                    file=str(source_path),
                    line=None,
                    col=None,
                    message=str(exc),
                    hint="Select a supported target and try again.",
                )
                return _emit_json("lock:update", [diagnostic], file=str(source_path))
            print(str(exc), file=sys.stderr)
            return 1
    else:
        generated_code = output_path.read_text(encoding="utf-8")

    # Generate lockfile
    lock_path = source_path.with_suffix(".nl.lock")
    lockfile = generate_lockfile(
        nl_file,
        generated_code,
        str(output_path),
        llm_backend="mock",
        target=target,
    )
    write_lockfile(lockfile, lock_path)

    if json_output:
        return _emit_json(
            "lock:update",
            [],
            file=str(source_path),
            lockfile=str(lock_path),
            output=str(output_path),
            target=target,
            anlu_count=len(nl_file.anlus),
        )
    print(f"{_check()} Updated {lock_path.name}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    """Compile and execute a .nl file in one step"""
    source_path = Path(args.file)
    source_root = source_path.parent.resolve()
    verbose = getattr(args, "verbose", False)
    json_output = getattr(args, "json", False)

    if not source_path.exists():
        diagnostic = missing_file_diagnostic(source_path)
        if json_output:
            return _emit_json("run", [diagnostic], file=str(source_path))
        print(f"Error: {diagnostic.message}", file=sys.stderr)
        print(f"Error: {diagnostic.hint}", file=sys.stderr)
        return 1

    # Parse
    try:
        nl_file = parse_nl_file_auto(source_path)
    except ParseError as e:
        if json_output:
            return _emit_json(
                "run", [parse_error_diagnostic(source_path, e)], file=str(source_path)
            )
        print(f"Error: Parse error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        if json_output:
            diagnostic = Diagnostic(
                code=E_RUN,
                file=str(source_path),
                line=None,
                col=None,
                message=f"Unexpected run error: {e}",
                hint="Retry with --verbose and inspect the parser backend.",
            )
            return _emit_json("run", [diagnostic], file=str(source_path))
        print(f"Error: Unexpected run error [E_RUN]: {e}", file=sys.stderr)
        return 1

    try:
        validation = validate_semantics(nl_file, source_path)
    except StdlibUseError as e:
        if json_output:
            return _emit_json(
                "run", [stdlib_use_diagnostic(source_path, e)], file=str(source_path)
            )
        _print_stdlib_use_error(e)
        return 1

    if validation.dependency_errors:
        diagnostics = dependency_error_diagnostics(
            source_path, nl_file, validation.dependency_errors
        )
        if json_output:
            return _emit_json("run", diagnostics, file=str(source_path))
        print("Error: [E_RESOLUTION] Resolution errors:", file=sys.stderr)
        for err in validation.dependency_errors:
            print(f"  - {_format_dependency_error(err)}", file=sys.stderr)
        return 1

    # Emit Python (target flag for future multi-target support)
    target = getattr(args, "target", "python")
    if target != "python":
        if json_output:
            diagnostic = Diagnostic(
                code=ETARGET001,
                file=str(source_path),
                line=None,
                col=None,
                message=f"Target '{target}' not yet supported",
                hint="Use the python target for nlsc run.",
            )
            return _emit_json("run", [diagnostic], file=str(source_path))
        print(f"Error: Target '{target}' not yet supported", file=sys.stderr)
        return 1

    python_code = emit_python(nl_file, mode="mock")
    proc: subprocess.CompletedProcess[str] | None = None
    translated_stderr = ""

    # Create temp directory or use --keep location
    if args.keep:
        temp_dir = Path(args.keep).resolve()
        temp_dir.mkdir(parents=True, exist_ok=True)
        cleanup = False
    else:
        temp_dir = create_temp_workdir("nlsc_run_", preferred_root=source_path.parent)
        cleanup = True

    # Write generated Python
    # Normalize module name to valid Python identifier (replace hyphens with underscores)
    raw_name = nl_file.module.name or source_path.stem
    module_name = raw_name.replace("-", "_")
    py_path = temp_dir / f"{module_name}.py"
    py_path.write_text(python_code, encoding="utf-8")

    # Generate source map for error translation
    source_map = generate_source_map(nl_file, python_code)
    source_map.py_path = str(py_path)

    if verbose:
        print(f"Compiled {source_path} -> {py_path}")
        print(f"Source mappings: {len(source_map.mappings)} entries")

    # Build run command - look for main-like functions
    run_args = [sys.executable, str(py_path)]

    # Check for common main patterns
    main_candidates = ["main", "run", "start"]
    for candidate in main_candidates:
        # Also check with underscores since we normalize hyphens
        candidate_normalized = candidate.replace("-", "_")
        for anlu in nl_file.anlus:
            if anlu.identifier == candidate or anlu.identifier == candidate_normalized:
                # Add -c to call the function - use repr() for safe path escaping on all platforms
                safe_path = repr(str(temp_dir))
                safe_source_root = repr(str(source_root))
                run_args = [
                    sys.executable,
                    "-c",
                    f"import sys; sys.path.insert(0, {safe_source_root}); "
                    f"sys.path.insert(0, {safe_path}); "
                    f"from {module_name} import {candidate_normalized}; {candidate_normalized}()",
                ]
                if verbose:
                    print(f"Found entry point: {candidate}")
                break
        else:
            continue
        break

    # Execute
    try:
        # Preserve existing PYTHONPATH if present
        env = os.environ.copy()
        existing_pythonpath = env.get("PYTHONPATH", "")
        pythonpath_parts = [str(temp_dir), str(source_root)]
        if existing_pythonpath:
            pythonpath_parts.append(existing_pythonpath)
        env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

        proc = subprocess.run(
            run_args,
            cwd=str(temp_dir),
            env=env,
            capture_output=True,
            text=True,
        )

        # Output stdout
        if proc.stdout and not json_output:
            print(proc.stdout, end="")

        # Translate and output stderr with source mapping
        translated_stderr = ""
        if proc.stderr:
            translated_stderr = source_map.translate_error(proc.stderr)
            if not json_output:
                print(translated_stderr, end="", file=sys.stderr)

        exit_code = proc.returncode
    except Exception as e:
        if json_output:
            diagnostic = Diagnostic(
                code=EEXEC001,
                file=str(source_path),
                line=None,
                col=None,
                message=f"Execution error: {e}",
                hint="Inspect the generated module and runtime environment.",
            )
            return _emit_json("run", [diagnostic], file=str(source_path))
        print(f"Execution error: {e}", file=sys.stderr)
        exit_code = 1
    finally:
        # Cleanup temp directory unless --keep
        if cleanup:
            import shutil

            shutil.rmtree(temp_dir, ignore_errors=True)

    if json_output:
        diagnostics: list[Diagnostic] = []
        if exit_code != 0:
            diagnostics.append(run_execution_failure_diagnostic(source_path, exit_code))
        return _emit_json(
            "run",
            diagnostics,
            status_code=exit_code,
            file=str(source_path),
            exit_code=exit_code,
            stdout=proc.stdout if proc is not None else "",
            stderr=translated_stderr,
        )
    return exit_code


def cmd_assoc(args: argparse.Namespace) -> int:
    """Install Windows file association for .nl files"""
    json_output = getattr(args, "json", False)

    if platform.system() != "Windows":
        if json_output:
            return _emit_json("assoc", [assoc_platform_diagnostic()])
        print(
            "Error: File association command is only available on Windows",
            file=sys.stderr,
        )
        return 1

    import winreg

    uninstall = getattr(args, "uninstall", False)
    current_user = getattr(args, "user", False)
    action = "uninstall" if uninstall else "install"
    scope = "user" if current_user else "system"

    # Determine icon location
    icon_path = None

    # First, check for bundled icon in package resources
    package_dir = Path(__file__).parent
    bundled_icon = package_dir / "resources" / "nls-file.ico"
    if bundled_icon.exists():
        # Copy to user's app data for persistence
        app_data = Path(os.environ.get("LOCALAPPDATA", "")) / "nlsc"
        app_data.mkdir(parents=True, exist_ok=True)
        dest_icon = app_data / "nls-file.ico"
        shutil.copy2(bundled_icon, dest_icon)
        icon_path = dest_icon

    if not icon_path:
        if json_output:
            return _emit_json("assoc", [assoc_icon_missing_diagnostic()])
        print(
            "Error: Could not find nls-file.ico in package resources", file=sys.stderr
        )
        print(
            "Run 'python windows/generate_ico.py' from the project root first",
            file=sys.stderr,
        )
        return 1

    # Choose registry root
    if current_user:
        root_key = winreg.HKEY_CURRENT_USER
        base_path = r"SOFTWARE\Classes"
        if not json_output:
            print("Installing for current user...")
    else:
        root_key = winreg.HKEY_CLASSES_ROOT
        base_path = ""
        if not json_output:
            print("Installing system-wide (requires admin)...")

    ext_path = f"{base_path}\\.nl" if base_path else ".nl"
    progid_path = f"{base_path}\\NLSFile" if base_path else "NLSFile"

    try:
        if uninstall:
            if not json_output:
                print("Uninstalling NLS file association...")
            # Delete keys
            try:
                winreg.DeleteKey(root_key, f"{progid_path}\\DefaultIcon")
            except FileNotFoundError:
                pass
            try:
                winreg.DeleteKey(root_key, progid_path)
            except FileNotFoundError:
                pass
            try:
                winreg.DeleteKey(root_key, ext_path)
            except FileNotFoundError:
                pass
            if not json_output:
                print(f"  {_check()} Uninstalled file association")
        else:
            if not json_output:
                print("Installing NLS file association...")
                print(f"  Icon: {icon_path}")

            # Create .nl extension key
            with winreg.CreateKey(root_key, ext_path) as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "NLSFile")
                winreg.SetValueEx(key, "Content Type", 0, winreg.REG_SZ, "text/plain")
                winreg.SetValueEx(key, "PerceivedType", 0, winreg.REG_SZ, "text")
            if not json_output:
                print(f"  {_check()} Registered .nl extension")

            # Create NLSFile ProgID
            with winreg.CreateKey(root_key, progid_path) as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "NLS Specification File")
            if not json_output:
                print(f"  {_check()} Created NLSFile ProgID")

            # Create DefaultIcon
            with winreg.CreateKey(root_key, f"{progid_path}\\DefaultIcon") as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{icon_path}"')
            if not json_output:
                print(f"  {_check()} Set default icon")

        # Notify shell of changes
        try:
            import ctypes

            SHCNE_ASSOCCHANGED = 0x08000000
            SHCNF_IDLIST = 0
            ctypes.windll.shell32.SHChangeNotify(
                SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None
            )
            if not json_output:
                print(f"  {_check()} Notified shell of changes")
        except Exception:
            pass

        if json_output:
            return _emit_json(
                "assoc",
                [],
                action=action,
                scope=scope,
                icon=str(icon_path),
            )

        print("\nDone! If icons don't appear immediately:")
        print("  1. Restart Windows Explorer")
        print("  2. Or log out and back in")

        return 0

    except PermissionError:
        if json_output:
            return _emit_json("assoc", [assoc_permission_diagnostic()])
        print(
            "Error: Permission denied. Run as administrator or use --user flag.",
            file=sys.stderr,
        )
        return 1
    except Exception as e:
        if json_output:
            return _emit_json("assoc", [assoc_runtime_failure_diagnostic(str(e))])
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_lsp(args: argparse.Namespace) -> int:
    """Start the NLS language server"""
    try:
        from nlsc.lsp import start_server
    except ImportError as e:
        diagnostic = lsp_dependencies_unavailable_diagnostic(str(e))
        return _emit_lsp_startup_failure(args, diagnostic)
    except Exception as e:
        diagnostic = lsp_startup_failure_diagnostic(str(e))
        return _emit_lsp_startup_failure(args, diagnostic)

    transport = getattr(args, "transport", "stdio")
    host = getattr(args, "host", "127.0.0.1")
    port = getattr(args, "port", 2087)

    if not getattr(args, "json", False):
        if transport == "stdio":
            print("Starting NLS Language Server (stdio)...", file=sys.stderr)
        else:
            print(
                f"Starting NLS Language Server (tcp://{host}:{port})...",
                file=sys.stderr,
            )

    try:
        start_server(transport=transport, host=host, port=port)
    except Exception as e:
        diagnostic = lsp_startup_failure_diagnostic(str(e))
        return _emit_lsp_startup_failure(args, diagnostic)
    return 0


def main(argv: list[str] | None = None) -> int:
    """Main entry point for nlsc CLI"""
    raw_argv = list(sys.argv[1:] if argv is None else argv)

    class CLICommandParser(NLSArgumentParser):
        def __init__(self, **kwargs: Any) -> None:
            super().__init__(argv=raw_argv, **kwargs)

    parser = NLSArgumentParser(
        prog="nlsc",
        argv=raw_argv,
        description="Natural Language Source Compiler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  nlsc init                     Initialize new NLS project
  nlsc compile src/math.nl      Compile to Python
  nlsc verify src/auth.nl       Validate without generating
  nlsc graph src/order.nl       Generate Mermaid dependency diagram
  nlsc graph src/order.nl -a process-order  Visualize ANLU dataflow

The conversation is the programming. The .nl file is the receipt.
""",
    )
    parser.add_argument("--version", action="version", version=f"nlsc {__version__}")
    parser.add_argument(
        "--parser",
        choices=["auto", "regex", "treesitter"],
        default="auto",
        help="Parser backend: 'auto' (default, uses tree-sitter if available), 'regex', or 'treesitter'",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        parser_class=CLICommandParser,
    )

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize NLS project")
    init_parser.add_argument(
        "path", nargs="?", default=".", help="Project directory (default: current)"
    )
    init_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON diagnostics and init metadata.",
    )

    # compile command
    compile_parser = subparsers.add_parser("compile", help="Compile .nl file")
    compile_parser.add_argument("file", help="Path to .nl file")
    compile_parser.add_argument(
        "-t",
        "--target",
        choices=["python", "typescript"],
        default=None,
        help="Target language (defaults to @target in source, or python if omitted)",
    )
    compile_parser.add_argument("-o", "--output", help="Output file path")
    compile_parser.add_argument(
        "--stdlib-path",
        action="append",
        default=[],
        help="Additional stdlib root directory (repeatable; highest precedence).",
    )
    compile_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON output.",
    )

    # run command
    run_parser = subparsers.add_parser("run", help="Compile and execute .nl file")
    run_parser.add_argument("file", help="Path to .nl file")
    run_parser.add_argument(
        "-k",
        "--keep",
        metavar="DIR",
        help="Keep generated files in specified directory",
    )
    run_parser.add_argument(
        "-t",
        "--target",
        choices=["python"],
        default="python",
        help="Target language for code generation (default: python)",
    )
    run_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed output including source mapping",
    )
    run_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON output.",
    )

    # verify command
    verify_parser = subparsers.add_parser("verify", help="Verify .nl file")
    verify_parser.add_argument("file", help="Path to .nl file")
    verify_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON output.",
    )

    # explain command
    explain_parser = subparsers.add_parser(
        "explain", help="Explain a stable CLI error code"
    )
    explain_parser.add_argument("code", help="Stable CLI error code to explain")
    explain_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON output.",
    )

    # graph command
    graph_parser = subparsers.add_parser(
        "graph", help="Visualize dependencies and dataflow"
    )
    graph_parser.add_argument("file", help="Path to .nl file")
    graph_parser.add_argument(
        "-f",
        "--format",
        choices=["mermaid", "dot", "ascii"],
        default="mermaid",
        help="Output format (default: mermaid)",
    )
    graph_parser.add_argument(
        "-a", "--anlu", help="Specific ANLU for dataflow visualization"
    )
    graph_parser.add_argument(
        "--dataflow", action="store_true", help="Show dataflow instead of FSM states"
    )
    graph_parser.add_argument(
        "-o", "--output", help="Output file path (default: stdout)"
    )
    graph_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON output.",
    )

    # test command
    test_parser = subparsers.add_parser("test", help="Run @test specifications")
    test_parser.add_argument("file", help="Path to .nl file")
    test_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose output"
    )
    test_parser.add_argument(
        "-k", "--case", help="Run specific test case (regex pattern)"
    )
    test_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON output.",
    )

    # atomize command
    atomize_parser = subparsers.add_parser(
        "atomize", help="Extract ANLUs from Python code"
    )
    atomize_parser.add_argument("file", help="Path to Python file")
    atomize_parser.add_argument("-o", "--output", help="Output .nl file path")
    atomize_parser.add_argument("-m", "--module", help="Module name for generated .nl")
    atomize_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON diagnostics.",
    )

    # diff command
    diff_parser = subparsers.add_parser(
        "diff", aliases=["dif"], help="Show changes since last compile"
    )
    diff_parser.add_argument("file", help="Path to .nl file")
    diff_parser.add_argument("--stat", action="store_true", help="Show summary only")
    diff_parser.add_argument(
        "--full", action="store_true", help="Show full unified dif"
    )
    diff_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON output.",
    )

    # watch command
    watch_parser = subparsers.add_parser(
        "watch", help="Watch directory for .nl changes"
    )
    watch_parser.add_argument(
        "dir", nargs="?", default=".", help="Directory to watch (default: current)"
    )
    watch_parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress success messages"
    )
    watch_parser.add_argument(
        "-t", "--test", action="store_true", help="Run tests after successful compile"
    )
    watch_parser.add_argument(
        "-d",
        "--debounce",
        type=int,
        default=100,
        help="Debounce interval in ms (default: 100)",
    )
    watch_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON diagnostics for startup errors.",
    )

    # lock:check command
    lock_check_parser = subparsers.add_parser(
        "lock:check", help="Verify lockfile is current"
    )
    lock_check_parser.add_argument("file", help="Path to .nl file")
    lock_check_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON diagnostics.",
    )

    # lock:update command
    lock_update_parser = subparsers.add_parser(
        "lock:update", help="Regenerate lockfile"
    )
    lock_update_parser.add_argument("file", help="Path to .nl file")
    lock_update_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON diagnostics.",
    )

    # lsp command
    lsp_parser = subparsers.add_parser("lsp", help="Start NLS language server")
    lsp_parser.add_argument(
        "--transport",
        choices=["stdio", "tcp"],
        default="stdio",
        help="Transport protocol (default: stdio)",
    )
    lsp_parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host address for tcp transport (default: 127.0.0.1)",
    )
    lsp_parser.add_argument(
        "--port",
        type=int,
        default=2087,
        help="TCP port for tcp transport (default: 2087)",
    )
    lsp_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON diagnostics for startup failures.",
    )

    # assoc command (Windows only)
    assoc_parser = subparsers.add_parser(
        "assoc", help="Install Windows file association for .nl files"
    )
    assoc_parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove file association instead of installing",
    )
    assoc_parser.add_argument(
        "--user",
        action="store_true",
        help="Install for current user only (no admin required)",
    )
    assoc_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON diagnostics for assoc failures.",
    )

    try:
        args = parser.parse_args(raw_argv)
    except CLIParseError as error:
        return _emit_cli_parse_failure(error)

    if args.command is None:
        parser.print_help()
        return 0

    # Set parser backend before any parsing commands
    if hasattr(args, "parser") and args.parser:
        try:
            set_parser_backend(args.parser)
        except ParserBootstrapError as error:
            return _emit_parser_bootstrap_failure(args, error)

    if args.command == "init":
        return cmd_init(args)
    elif args.command == "compile":
        return cmd_compile(args)
    elif args.command == "run":
        return cmd_run(args)
    elif args.command == "verify":
        return cmd_verify(args)
    elif args.command == "explain":
        return cmd_explain(args)
    elif args.command == "graph":
        return cmd_graph(args)
    elif args.command == "test":
        return cmd_test(args)
    elif args.command == "atomize":
        return cmd_atomize(args)
    elif args.command in {"diff", "dif"}:
        return cmd_diff(args)
    elif args.command == "watch":
        return cmd_watch(args)
    elif args.command == "lock:check":
        return cmd_lock_check(args)
    elif args.command == "lock:update":
        return cmd_lock_update(args)
    elif args.command == "lsp":
        return cmd_lsp(args)
    elif args.command == "assoc":
        return cmd_assoc(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
