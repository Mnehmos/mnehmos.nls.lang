"""Shared parsing, validation, and workspace helpers for CLI commands."""

from __future__ import annotations

import os
import re
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path

from .localization import ANLU_IDENTIFIER_PATTERN, normalize_localized_source
from .parser import parse_nl_file, ParseError
from .resolver import ResolutionError, resolve_dependencies
from .schema import ANLU, NLFile
from .diagnostics import Diagnostic
from .error_catalog import EIR002, EIR004
from .ir import ForeignExpr, operation_unchecked_nodes
from .stdlib_resolver import (
    ResolvedUse,
    bundled_default_major,
    bundled_stdlib_root,
    resolve_use,
    stdlib_search_roots,
)


def detect_treesitter() -> bool:
    """Check if tree-sitter parser is available."""
    try:
        from . import parser_treesitter

        return parser_treesitter.is_available()
    except ImportError:
        return False


def _source_contains_anlu_header(source: str) -> bool:
    """Return True when the source appears to define at least one ANLU."""
    normalized = normalize_localized_source(source)
    return bool(
        re.search(rf"^\s*\[({ANLU_IDENTIFIER_PATTERN})\]\s*$", normalized, re.MULTILINE)
    )


def _source_contains_test_blocks(source: str) -> bool:
    normalized = normalize_localized_source(source)
    return bool(re.search(r"^\s*@test\b", normalized, re.MULTILINE))


def _source_contains_logic_output_bindings(source: str) -> bool:
    normalized = normalize_localized_source(source)
    return bool(re.search(r"^\s*\d+\.\s+.+(?:->|→)\s+.+$", normalized, re.MULTILINE))


def _tree_sitter_parse_needs_fallback(source: str, nl_file: NLFile) -> bool:
    if not nl_file.anlus and _source_contains_anlu_header(source):
        return True
    if _source_contains_test_blocks(source) and not nl_file.tests:
        return True
    if _source_contains_logic_output_bindings(source):
        has_output_binding = any(
            step.output_binding or step.assigns
            for anlu in nl_file.anlus
            for step in anlu.logic_steps
        )
        if not has_output_binding:
            return True
    return False


def parse_nl_path_auto(
    source_path: Path, *, use_treesitter: bool | None = None
) -> NLFile:
    """Parse an .nl file using tree-sitter when available, with safe fallback."""
    if not source_path.exists():
        raise ParseError(f"File not found: {source_path}")
    if source_path.suffix != ".nl":
        raise ParseError(f"Expected .nl file, got: {source_path.suffix}")

    source = source_path.read_text(encoding="utf-8")
    source_path_str = str(source_path)
    should_use_treesitter = (
        detect_treesitter() if use_treesitter is None else use_treesitter
    )

    if not should_use_treesitter:
        return parse_nl_file(source, source_path=source_path_str)

    from .parser_treesitter import parse_nl_file_treesitter

    nl_file = parse_nl_file_treesitter(source, source_path=source_path_str)
    if _tree_sitter_parse_needs_fallback(source, nl_file):
        return parse_nl_file(source, source_path=source_path_str)
    return nl_file


def resolve_stdlib_uses(
    nl_file: NLFile,
    source_path: Path,
    cli_stdlib_paths: list[str] | None = None,
) -> list[ResolvedUse]:
    """Resolve all @use directives and return their resolved file metadata."""
    if not getattr(nl_file.module, "uses", None):
        return []

    bundled_root = bundled_stdlib_root()
    default_major = bundled_default_major(root=bundled_root)
    cli_roots = [Path(p) for p in (cli_stdlib_paths or [])]
    roots = stdlib_search_roots(
        cwd=source_path.parent,
        cli_roots=cli_roots,
        bundled_root=bundled_root,
    )

    return [
        resolve_use(domain_spec=spec, roots=roots, default_major=default_major)
        for spec in nl_file.module.uses
    ]


@dataclass
class SemanticValidationResult:
    """Shared semantic validation result for CLI commands."""

    resolved_uses: list[ResolvedUse]
    dependency_errors: list[ResolutionError]
    contract_errors: list[str]

    @property
    def success(self) -> bool:
        return not self.dependency_errors and not self.contract_errors


def validate_contract_fields(nl_file: NLFile) -> list[str]:
    """Validate required ANLU contract fields."""
    errors = []
    for anlu in nl_file.anlus:
        if not anlu.purpose:
            errors.append(f"{anlu.identifier}: Missing PURPOSE")
        if not anlu.returns:
            errors.append(f"{anlu.identifier}: Missing RETURNS")
    return errors


# --------------------------------------------------------------------------
# Executable contract (Issue #190)
# --------------------------------------------------------------------------
#
# One shared boundary for strict verify/compile/run/test/watch: executable
# content must lower to recognized constructs. In default (scaffold) mode the
# same diagnostics are surfaced as warnings and the artifact is marked
# incomplete; in strict mode they fail the command before any runnable
# artifact or successful lockfile is produced.


@dataclass
class ExecutableContractResult:
    """Result of the shared executable-contract evaluation."""

    diagnostics: list[Diagnostic]
    scaffold_anlus: set[str]

    @property
    def success(self) -> bool:
        return not self.diagnostics


def _edge_case_diagnostics(anlu: ANLU, file_token: str) -> list[Diagnostic]:
    """Reject edge cases that mix executable conditions with prose behavior."""
    from .lowering import lower_expression
    from .ir import SourceSpan

    diagnostics: list[Diagnostic] = []
    for ec in anlu.edge_cases:
        span = SourceSpan(anlu=anlu.identifier, line=anlu.line_number or None)
        condition = lower_expression(ec.condition.strip(), span)
        behavior_text = ec.behavior.strip()
        behavior_candidate = behavior_text
        if behavior_candidate.lower().startswith("return "):
            behavior_candidate = behavior_candidate[7:]
        behavior = lower_expression(behavior_candidate, span)
        condition_ok = not isinstance(condition, ForeignExpr)
        behavior_ok = not isinstance(behavior, ForeignExpr)
        if condition_ok != behavior_ok:
            diagnostics.append(
                Diagnostic(
                    code=EIR002,
                    file=file_token,
                    line=span.line,
                    col=None,
                    message=(
                        f"{anlu.identifier}: edge case mixes executable and narrative "
                        f"content: '{ec.condition.strip()}' -> '{behavior_text}'"
                    ),
                    hint="Make both sides executable (e.g. 'score > 100 -> 100') or keep both descriptive.",
                )
            )
    return diagnostics


def evaluate_executable_contract(
    nl_file: NLFile, *, file_token: str = "<source>"
) -> ExecutableContractResult:
    """Evaluate the strict executable contract for every ANLU.

    Returns the source-level diagnostics plus the set of ANLU identifiers
    whose implementation still contains unresolved (scaffold) content.
    """
    from dataclasses import replace as _dc_replace

    from .lowering import lower_anlu

    diagnostics: list[Diagnostic] = []
    scaffold: set[str] = set()
    declared_types = {t.name for t in nl_file.module.types}

    for anlu in nl_file.anlus:
        operation, op_diagnostics = lower_anlu(anlu, declared_types)
        diagnostics.extend(
            _dc_replace(d, file=file_token) for d in op_diagnostics
        )
        if operation_unchecked_nodes(operation):
            scaffold.add(anlu.identifier)

        if (
            operation.result is not None
            and operation.result.declared_type is not None
            and operation.result.value is None
            and operation.result.declared_type.name not in ("void",)
            and not operation.literal
        ):
            diagnostics.append(
                Diagnostic(
                    code=EIR004,
                    file=file_token,
                    line=anlu.line_number or None,
                    col=None,
                    message=(
                        f"{anlu.identifier}: declared result type "
                        f"'{operation.result.raw}' has no implementation expression; "
                        "a default value would be invented"
                    ),
                    hint="Return the computed value (e.g. 'RETURNS: total') or declare 'RETURNS: none'.",
                )
            )
            scaffold.add(anlu.identifier)

        diagnostics.extend(_edge_case_diagnostics(anlu, file_token))

    return ExecutableContractResult(diagnostics=diagnostics, scaffold_anlus=scaffold)


def executable_contract_diagnostics(
    nl_file: NLFile, *, file_token: str = "<source>"
) -> list[Diagnostic]:
    """Convenience wrapper returning just the contract diagnostics."""
    return evaluate_executable_contract(nl_file, file_token=file_token).diagnostics


def scaffold_anlus(nl_file: NLFile) -> set[str]:
    """ANLU identifiers whose implementation contains unresolved content."""
    return evaluate_executable_contract(nl_file).scaffold_anlus


def validate_semantics(
    nl_file: NLFile,
    source_path: Path,
    *,
    cli_stdlib_paths: list[str] | None = None,
    require_contract_fields: bool = False,
) -> SemanticValidationResult:
    """Run shared semantic validation used by compile/verify/run/watch."""
    resolved_uses = resolve_stdlib_uses(nl_file, source_path, cli_stdlib_paths)
    dependency_result = resolve_dependencies(nl_file)
    dependency_errors = dependency_result.errors
    contract_errors = (
        validate_contract_fields(nl_file) if require_contract_fields else []
    )

    return SemanticValidationResult(
        resolved_uses=resolved_uses,
        dependency_errors=dependency_errors,
        contract_errors=contract_errors,
    )


def create_temp_workdir(prefix: str, *, preferred_root: Path | None = None) -> Path:
    """Create a temporary work directory, preferring a writable local root."""
    env_root = os.environ.get("NLSC_TMPDIR")
    candidates: list[Path] = []

    if env_root:
        candidates.append(Path(env_root))
    if preferred_root is not None:
        preferred_root = Path(preferred_root)
        candidates.extend(
            [
                preferred_root / "build" / "nlsc_tmp",
                preferred_root / "_nlsc_tmp",
                preferred_root,
            ]
        )
    candidates.extend(
        [
            Path.cwd() / "build" / "nlsc_tmp",
            Path.cwd() / "_nlsc_tmp",
        ]
    )

    def _create_unique_dir(root: Path) -> Path:
        root.mkdir(parents=True, exist_ok=True)
        for _ in range(32):
            temp_dir = root / f"{prefix}{uuid.uuid4().hex[:8]}"
            try:
                temp_dir.mkdir()
                probe_path = temp_dir / ".write-probe"
                probe_path.write_text("ok", encoding="utf-8")
                probe_path.unlink()
                return temp_dir
            except FileExistsError:
                continue
            except OSError:
                shutil.rmtree(temp_dir, ignore_errors=True)
                continue
        raise OSError(f"Unable to create writable temp workdir under {root}")

    for root in candidates:
        try:
            return _create_unique_dir(root)
        except OSError:
            continue

    return _create_unique_dir(Path(os.environ.get("TMP", os.getcwd())))
