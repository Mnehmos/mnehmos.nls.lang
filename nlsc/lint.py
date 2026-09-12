"""Semantic linter for NLS intent quality (Issue #94).

Linting in NLS is not about code style — it is about **intent quality**:
is the specification complete, consistent, and safe before it becomes
code?  Rules operate on the surface AST plus the target-neutral IR, so
they report on meaning, not formatting.

Rules are warnings by default (``nlsc lint`` exits 0 unless ``--strict``)
and configurable: rules listed in a ``.nlslintrc`` (JSON) or
``nls.toml`` (``[lint] disable = [...]``) file, searched upward from the
linted file, are skipped.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterator, Optional

from .diagnostics import Diagnostic
from .ir import (
    IRBind,
    IRExpr,
    IROperation,
    IRBinary,
    IRIndexAccess,
    IRRef,
    iter_expr_nodes,
    iter_stmt_nodes,
)
from .lowering import lower_anlu
from .schema import ANLU, NLFile

MAX_LOGIC_STEPS = 10


@dataclass(frozen=True)
class LintRule:
    code: str
    name: str
    description: str


RULES: dict[str, LintRule] = {
    "ELINT001": LintRule(
        "ELINT001", "guards-for-inputs", "ANLU declares INPUTS but no GUARDS"
    ),
    "ELINT002": LintRule(
        "ELINT002", "tests-for-inputs", "ANLU declares INPUTS but has no @test/@property coverage"
    ),
    "ELINT003": LintRule(
        "ELINT003", "invariants-for-types", "@type has no @invariant"
    ),
    "ELINT004": LintRule(
        "ELINT004", "zero-guard-for-division", "division/modulo without a divisor guard"
    ),
    "ELINT005": LintRule(
        "ELINT005", "bounds-guard-for-indexing", "list indexing without a length guard"
    ),
    "ELINT006": LintRule(
        "ELINT006", "nil-check-for-optionals", "optional input used in arithmetic without a nil check"
    ),
    "ELINT007": LintRule(
        "ELINT007", "no-implicit-mutation", "augmented assignment (mutation is not modeled explicitly)"
    ),
    "ELINT008": LintRule(
        "ELINT008", "declare-module-version", "module does not declare @version"
    ),
    "ELINT009": LintRule(
        "ELINT009", "decompose-long-logic", f"LOGIC exceeds {MAX_LOGIC_STEPS} steps"
    ),
    "ELINT010": LintRule(
        "ELINT010",
        "limit-conditional-nesting",
        "nested IF/THEN inside a step action (not supported; split instead)",
    ),
    "ELINT011": LintRule(
        "ELINT011", "tests-cover-inputs", "an input is never referenced by the ANLU's test cases"
    ),
    "ELINT012": LintRule(
        "ELINT012", "typed-guard-errors", "guard has no typed error (type, message)"
    ),
}


@dataclass
class LintConfig:
    """Per-project lint configuration."""

    disabled: set[str] = field(default_factory=set)

    @classmethod
    def discover(cls, source_path: Optional[Path]) -> "LintConfig":
        """Search upward for .nlslintrc (JSON) or nls.toml ([lint])."""
        if source_path is None:
            return cls()
        directory = source_path.resolve().parent
        for candidate_dir in [directory, *directory.parents]:
            rc_path = candidate_dir / ".nlslintrc"
            if rc_path.exists():
                try:
                    data = json.loads(rc_path.read_text(encoding="utf-8"))
                    return cls(disabled=set(data.get("disable", [])))
                except (OSError, ValueError):
                    return cls()
            toml_path = candidate_dir / "nls.toml"
            if toml_path.exists():
                try:
                    import tomllib

                    data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
                    return cls(disabled=set(data.get("lint", {}).get("disable", [])))
                except (OSError, ValueError):
                    return cls()
        return cls()


def _warn(
    diagnostics: list[Diagnostic],
    code: str,
    file_token: str,
    line: Optional[int],
    message: str,
    hint: str,
) -> None:
    diagnostics.append(
        Diagnostic(code=code, file=file_token, line=line, col=None, message=message, hint=hint)
    )


def _guard_text(anlu: ANLU) -> str:
    return " ".join(guard.condition for guard in anlu.guards)


def _test_text(nl_file: NLFile, anlu_id: str) -> str:
    chunks: list[str] = []
    for suite in nl_file.tests:
        if suite.anlu_id == anlu_id:
            for case in suite.cases:
                chunks.append(f"{case.expression} {case.expected}")
    for prop in nl_file.properties:
        if prop.anlu_id == anlu_id:
            for assertion in prop.assertions:
                chunks.append(assertion.expression)
    return " ".join(chunks)


def _test_coverage(
    nl_file: NLFile, anlu_id: str, test_text: str
) -> tuple[set[str], int]:
    """Names referenced by tests plus the largest positional call arity.

    Test calls are written as ``anlu_name(args)``; positional arguments
    cover inputs by declaration order, so an input is covered either when
    its name appears anywhere in the tests or when some call passes at
    least that many positional arguments.
    """
    snake = anlu_id.replace("-", "_")
    covered = set(re.findall(r"([A-Za-z_]\w*)\s*=(?!=)", test_text))
    max_positional = 0
    for call_start in re.finditer(rf"\b{re.escape(snake)}\s*\(", test_text):
        open_paren = call_start.end() - 1
        depth = 0
        close_paren = -1
        for index in range(open_paren, len(test_text)):
            char = test_text[index]
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    close_paren = index
                    break
        if close_paren == -1:
            continue
        args_text = test_text[open_paren + 1 : close_paren].strip()
        if not args_text:
            continue
        # Split top-level arguments by scanning; an '=' only marks a
        # keyword argument when it appears at parenthesis depth zero (a
        # nested constructor's kwargs must not count).
        positional = 0
        depth = 0
        keyword = False
        in_string: str | None = None
        for char in args_text:
            if in_string:
                if char == in_string:
                    in_string = None
                continue
            if char in "\"'":
                in_string = char
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            elif char == "=" and depth == 0 and not keyword:
                keyword = True
            elif char == "," and depth == 0:
                if not keyword:
                    positional += 1
                keyword = False
        if not keyword:
            positional += 1
        max_positional = max(max_positional, positional)
    covered.update(re.findall(r"([A-Za-z_]\w*)", test_text))
    return covered, max_positional


def lint_module(
    nl_file: NLFile,
    *,
    file_token: Optional[str] = None,
    config: Optional[LintConfig] = None,
) -> list[Diagnostic]:
    """Run all enabled lint rules over one parsed module."""
    token = file_token or (nl_file.source_path or "<source>")
    config = config or LintConfig.discover(
        Path(nl_file.source_path) if nl_file.source_path else None
    )
    diagnostics: list[Diagnostic] = []

    def enabled(code: str) -> bool:
        return code not in config.disabled

    # Module-level: ELINT008 ------------------------------------------------
    if enabled("ELINT008") and nl_file.source_path:
        try:
            source = Path(nl_file.source_path).read_text(encoding="utf-8")
            if not re.search(r"^\s*@version\b", source, re.MULTILINE):
                _warn(
                    diagnostics,
                    "ELINT008",
                    token,
                    1,
                    "module does not declare @version; a default is assumed",
                    "Add `@version 1.0.0` so consumers can track the module's releases.",
                )
        except OSError:
            pass

    # The linter itself must never execute anything: literal search only.

    # Types: ELINT003 -------------------------------------------------------
    if enabled("ELINT003"):
        invariant_types = {inv.type_name for inv in nl_file.invariants}
        for type_def in nl_file.module.types:
            if type_def.name not in invariant_types:
                _warn(
                    diagnostics,
                    "ELINT003",
                    token,
                    type_def.line_number or None,
                    f"@type {type_def.name} has no @invariant",
                    "Add an @invariant block stating what must always hold for this type.",
                )

    for anlu in nl_file.anlus:
        _lint_anlu(nl_file, anlu, token, diagnostics, enabled)

    return diagnostics


def _lint_anlu(
    nl_file: NLFile,
    anlu: ANLU,
    token: str,
    diagnostics: list[Diagnostic],
    enabled: Callable[[str], bool],
) -> None:
    line = anlu.line_number or None
    guard_text = _guard_text(anlu)

    # ELINT001 ---------------------------------------------------------------
    if enabled("ELINT001") and anlu.inputs and not anlu.guards:
        _warn(
            diagnostics,
            "ELINT001",
            token,
            line,
            f"[{anlu.identifier}] has INPUTS but no GUARDS",
            "State what makes each input invalid with a GUARDS bullet and a typed error.",
        )

    # ELINT002 ---------------------------------------------------------------
    if enabled("ELINT002") and anlu.inputs and not _test_text(nl_file, anlu.identifier):
        _warn(
            diagnostics,
            "ELINT002",
            token,
            line,
            f"[{anlu.identifier}] has INPUTS but no test coverage",
            "Add an @test block with at least one case per meaningful input.",
        )

    # ELINT009 ---------------------------------------------------------------
    if enabled("ELINT009") and len(anlu.logic_steps) > MAX_LOGIC_STEPS:
        _warn(
            diagnostics,
            "ELINT009",
            token,
            line,
            f"[{anlu.identifier}] has {len(anlu.logic_steps)} LOGIC steps "
            f"(limit {MAX_LOGIC_STEPS})",
            "Consider decomposing into smaller ANLUs that call each other.",
        )

    # ELINT011 ---------------------------------------------------------------
    if enabled("ELINT011") and anlu.inputs:
        test_text = _test_text(nl_file, anlu.identifier)
        if test_text:
            covered_names, max_positional = _test_coverage(
                nl_file, anlu.identifier, test_text
            )
            for index, input_ in enumerate(anlu.inputs):
                if input_.name in covered_names:
                    continue
                if index < max_positional:
                    continue
                _warn(
                    diagnostics,
                    "ELINT011",
                    token,
                    line,
                    f"[{anlu.identifier}] input '{input_.name}' is never "
                    "referenced by its test cases",
                    f"Add a case that exercises '{input_.name}', or remove it.",
                )

    # ELINT012 ---------------------------------------------------------------
    if enabled("ELINT012"):
        for guard in anlu.guards:
            if not guard.error_type:
                _warn(
                    diagnostics,
                    "ELINT012",
                    token,
                    line,
                    f"[{anlu.identifier}] guard has no typed error: "
                    f"{guard.condition.strip()}",
                    "Write `condition -> ErrorType(\"message\")` so the failure contract is explicit.",
                )

    # IR-based rules (structure, not prose) ---------------------------------
    operation, _diagnostics = lower_anlu(anlu, {t.name for t in nl_file.module.types})
    if operation is None:
        return

    optional_inputs = {
        input_.name
        for input_ in anlu.inputs
        if any(c.lower().strip() == "optional" for c in input_.constraints)
        or input_.type.strip().endswith("?")
    }
    list_inputs = {
        input_.name
        for input_ in anlu.inputs
        if input_.type.strip().lower().startswith("list")
    }

    def mentions(name: str) -> bool:
        return bool(re.search(rf"\b{re.escape(name)}\b", guard_text)) or bool(
            re.search(rf"\blen\s*\(\s*{re.escape(name)}\b", guard_text)
        )

    if enabled("ELINT010"):
        for step in anlu.logic_steps:
            action = step.description.strip()
            if re.match(r"^IF\s+", action, re.IGNORECASE):
                _warn(
                    diagnostics,
                    "ELINT010",
                    token,
                    step.line_number or line,
                    f"[{anlu.identifier}] step {step.number} nests an IF inside "
                    "its action, which is not executable syntax",
                    "Split into separate IF/THEN/ELSE steps or a new ANLU; "
                    "nested conditionals are not supported.",
                )

    for stmt in iter_stmt_nodes(operation.body):
        if enabled("ELINT007") and isinstance(stmt, IRBind) and stmt.aug is not None:
            _warn(
                diagnostics,
                "ELINT007",
                token,
                stmt.span.line if stmt.span else line,
                f"[{anlu.identifier}] '{stmt.name} {stmt.aug}=' mutates a binding",
                "Checked bindings are immutable; bind a fresh name or model the mutation explicitly.",
            )

    for expr in _iter_operation_exprs(operation):
        for node in iter_expr_nodes(expr):
            if enabled("ELINT004") and isinstance(node, IRBinary) and node.op in (
                "div",
                "mod",
                "floor_div",
            ):
                _lint_divisor(anlu, node, guard_text, token, diagnostics, line)
            if enabled("ELINT005") and isinstance(node, IRIndexAccess):
                if isinstance(node.base, IRRef) and node.base.name in list_inputs:
                    if not mentions(node.base.name):
                        _warn(
                            diagnostics,
                            "ELINT005",
                            token,
                            node.span.line if node.span else line,
                            f"[{anlu.identifier}] indexes '{node.base.name}' without "
                            "a length guard",
                            f"Add a GUARDS bullet such as `len({node.base.name}) > 0`.",
                        )
            if enabled("ELINT006") and isinstance(node, IRBinary) and node.op in (
                "add",
                "sub",
                "mul",
                "div",
                "mod",
                "floor_div",
                "pow",
            ):
                for side in (node.left, node.right):
                    if isinstance(side, IRRef) and side.name in optional_inputs:
                        if not mentions(side.name):
                            _warn(
                                diagnostics,
                                "ELINT006",
                                token,
                                node.span.line if node.span else line,
                                f"[{anlu.identifier}] optional input '{side.name}' "
                                "is used in arithmetic without a nil check",
                                f"Guard with `{side.name} is not None` or handle the "
                                "absent case with IF/ELSE.",
                            )


def _lint_divisor(
    anlu: ANLU,
    node: IRBinary,
    guard_text: str,
    token: str,
    diagnostics: list[Diagnostic],
    line: Optional[int],
) -> None:
    divisor = node.right
    if isinstance(divisor, IRRef):
        if not re.search(rf"\b{re.escape(divisor.name)}\b", guard_text):
            _warn(
                diagnostics,
                "ELINT004",
                token,
                node.span.line if node.span else line,
                f"[{anlu.identifier}] divides by '{divisor.name}' without a guard "
                "on it",
                f"Add `{divisor.name} != 0 -> ZeroDivisionError(\"...\")` to GUARDS.",
            )
    elif getattr(divisor, "kind", None) == "number" and getattr(divisor, "value", None) == 0:
        _warn(
            diagnostics,
            "ELINT004",
            token,
            node.span.line if node.span else line,
            f"[{anlu.identifier}] divides by literal zero",
            "Remove the step or replace the divisor with an input.",
        )


def _iter_operation_exprs(operation: IROperation) -> "Iterator[IRExpr]":
    for stmt in iter_stmt_nodes(operation.body):
        for attr in ("value", "condition"):
            expr = getattr(stmt, attr, None)
            if expr is not None:
                yield expr
    if operation.result is not None and operation.result.value is not None:
        yield operation.result.value
