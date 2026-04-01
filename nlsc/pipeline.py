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
from .resolver import resolve_dependencies
from .schema import NLFile
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
    if not nl_file.anlus and _source_contains_anlu_header(source):
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
    dependency_errors: list[str]
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
    dependency_errors = [
        f"{err.anlu_id}: {err.message}" for err in dependency_result.errors
    ]
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
