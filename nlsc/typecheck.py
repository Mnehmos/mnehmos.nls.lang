"""Semantic type checking over the target-neutral IR (Issue #195).

Consumes the #194 lowering (so both parser backends share this checker)
and validates operation signatures before any backend generates code:

* A **symbol table** of module ANLUs (kebab id + snake alias), declared
  record types, and a small table of documented builtin functions.
* Calls resolve through that table; an unknown ``[anlu]`` reference is
  always fatal, while undeclared foreign/builtin calls are strict-only.
* Bindings are tracked through the body in source order; undefined value
  uses are always fatal.
* Field access and construction check against declared record types.
* Declared DEPENDS is compared against inferred call dependencies.

Severity tiers:

- ``errors`` — unambiguous NameError/AttributeError-in-waiting; fatal in
  every mode.
- ``warnings`` — contract drift (argument types, DEPENDS mismatches,
  undeclared foreign calls, condition types); fatal under ``--strict``,
  advisory otherwise.

``any``/unknown compatibility is *explicit*: unknown types make a check
pass, but they are never treated as evidence that code is type-safe.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

from .diagnostics import Diagnostic
from .error_catalog import (
    ESEM001,
    ESEM002,
    ESEM003,
    ESEM004,
    ESEM005,
    ESEM006,
    ESEM007,
    ESEM008,
    ESEM009,
    ESEM012,
    ESEM013,
)
from .ir import (
    IRBind,
    IRBinary,
    IRBranch,
    IRCall,
    IRDiscard,
    IRExpr,
    IRFieldAccess,
    IRGuard,
    IRIndexAccess,
    IRList,
    IRLiteral,
    IRMethodCall,
    IRModule,
    IROperation,
    IRParam,
    IRRef,
    IRStmt,
    IRUnary,
    ForeignExpr,
    ForeignStmt,
    SourceSpan,
    TypeRef,
)
from .lowering import lower_module
from .schema import ANLU, NLFile

UNKNOWN = TypeRef(name="any")

# Documented builtin signatures.  Everything here is target-neutral;
# anything outside this table is a foreign call (see ESEM009).
_BUILTIN_SIGNATURES: dict[str, tuple[tuple[str, ...], str]] = {
    "len": (("any",), "integer"),
    "sum": (("list of number",), "number"),
    "max": (("number",), "number"),  # variadic or list
    "min": (("number",), "number"),
    "abs": (("number",), "number"),
    "round": (("number",), "number"),
    "sqrt": (("number",), "number"),
    "str": (("any",), "string"),
    "int": (("any",), "integer"),
    "float": (("any",), "number"),
    "bool": (("any",), "boolean"),
}

_NUMERIC_TYPES = {"number", "integer"}
_PRIMITIVE_TYPES = {"number", "integer", "string", "boolean", "void", "any"}

# Error constructors available without declaration (union of the runtime
# builtins the supported targets provide).
_KNOWN_ERROR_TYPES = {
    "ArithmeticError",
    "AssertionError",
    "AttributeError",
    "Error",
    "EvalError",
    "Exception",
    "IndexError",
    "KeyError",
    "LookupError",
    "NotImplementedError",
    "OverflowError",
    "RangeError",
    "ReferenceError",
    "RuntimeError",
    "SyntaxError",
    "TypeError",
    "URIError",
    "ValueError",
    "ZeroDivisionError",
}


def _snake(name: str) -> str:
    return name.replace("-", "_")


def types_compatible(expected: TypeRef, actual: TypeRef) -> bool:
    """Conservative structural/nominal compatibility.

    ``any`` on either side is an explicit unknown: it is compatible with
    everything but is never evidence of type safety.
    """
    if expected.name == "any" or actual.name == "any":
        return True
    expected_base = expected.name
    actual_base = actual.name
    if expected.args or actual.args:
        if expected_base == "list" and actual_base == "list":
            expected_inner = expected.args[0] if expected.args else UNKNOWN
            actual_inner = actual.args[0] if actual.args else UNKNOWN
            return types_compatible(expected_inner, actual_inner)
        if expected_base != actual_base:
            return False
    # Numeric tower: integer values are numbers.
    if {expected_base, actual_base} <= _NUMERIC_TYPES:
        return True
    return expected_base == actual_base


def _is_booleanish(ref: TypeRef) -> bool:
    return ref.name in ("boolean", "any")


@dataclass
class _SymbolTable:
    """Module-level semantic symbols."""

    operations: dict[str, IROperation] = field(default_factory=dict)
    snake_to_kebab: dict[str, str] = field(default_factory=dict)
    records: dict[str, dict[str, TypeRef]] = field(default_factory=dict)
    # Names brought in via @imports; usable as explicit unknowns (their
    # signatures are not declared in NLS yet).
    imports: set[str] = field(default_factory=set)
    # Top-level functions defined by @literal blocks: they exist in the
    # emitted module, so calls to them are declared escapes rather than
    # undeclared foreign calls (#202).
    literal_functions: set[str] = field(default_factory=set)

    def resolve_operation(self, target: str) -> Optional[IROperation]:
        op = self.operations.get(target)
        if op is not None:
            return op
        kebab = self.snake_to_kebab.get(_snake(target))
        if kebab is not None:
            return self.operations.get(kebab)
        return None


@dataclass
class SemanticCheckResult:
    """Tiered diagnostics from the semantic checker."""

    errors: list[Diagnostic] = field(default_factory=list)      # Tier A
    warnings: list[Diagnostic] = field(default_factory=list)    # Tier B


class _OperationChecker:
    def __init__(
        self,
        operation: IROperation,
        table: _SymbolTable,
        result: SemanticCheckResult,
        file_token: str,
    ):
        self.operation = operation
        self.table = table
        self.result = result
        self.file_token = file_token
        self.env: dict[str, TypeRef] = {}
        self.current_span: Optional[SourceSpan] = None

    # -- diagnostic helpers -------------------------------------------------
    def _resolve_span(self, span: Optional[SourceSpan]) -> Optional[SourceSpan]:
        return span if span is not None else self.current_span

    def _error(self, code: str, span: Optional[SourceSpan], message: str, hint: str) -> None:
        span = self._resolve_span(span)
        self.result.errors.append(
            Diagnostic(
                code=code,
                file=self.file_token,
                line=span.line if span else None,
                col=None,
                message=f"{self.operation.name}: {message}",
                hint=hint,
            )
        )

    def _warn(self, code: str, span: Optional[SourceSpan], message: str, hint: str) -> None:
        span = self._resolve_span(span)
        self.result.warnings.append(
            Diagnostic(
                code=code,
                file=self.file_token,
                line=span.line if span else None,
                col=None,
                message=f"{self.operation.name}: {message}",
                hint=hint,
            )
        )

    # -- entry ---------------------------------------------------------------
    def run(self) -> set[str]:
        for param in self.operation.params:
            self.env[param.name] = param.type_ref
        for imported in sorted(self.table.imports):
            self.env.setdefault(imported, UNKNOWN)

        inferred_deps: set[str] = set()
        for guard in self.operation.guards:
            condition_type = self.infer(guard.condition, inferred_deps)
            if not _is_booleanish(condition_type):
                self._warn(
                    ESEM006,
                    guard.span,
                    f"guard condition has type '{condition_type.render()}'; expected boolean",
                    "Guards must evaluate to boolean conditions.",
                )

        for stmt in self.operation.body:
            self.check_statement(stmt, inferred_deps)

        if self.operation.result is not None and self.operation.result.value is not None:
            previous_span = self.current_span
            if self.operation.span is not None:
                self.current_span = self.operation.span
            self.infer(self.operation.result.value, inferred_deps)
            self.current_span = previous_span

        return inferred_deps

    # -- statements ------------------------------------------------------------
    def check_statement(self, stmt: IRStmt, inferred_deps: set[str]) -> set[str]:
        if isinstance(stmt, ForeignStmt):
            return inferred_deps
        previous_span = self.current_span
        if getattr(stmt, "span", None) is not None:
            self.current_span = stmt.span
        try:
            return self._check_statement_inner(stmt, inferred_deps)
        finally:
            self.current_span = previous_span

    def _check_statement_inner(self, stmt: IRStmt, inferred_deps: set[str]) -> set[str]:
        if isinstance(stmt, ForeignStmt):
            return inferred_deps
        if isinstance(stmt, IRBind):
            value_type = self.infer(stmt.value, inferred_deps)
            if stmt.aug is not None:
                current = self.env.get(stmt.name)
                if current is not None and current.name not in (
                    *_NUMERIC_TYPES,
                    "any",
                    "string",
                    "list",
                ):
                    self._warn(
                        ESEM006,
                        stmt.span,
                        f"augmented binding '{stmt.name} {stmt.aug}=' requires a numeric, string, or list value",
                        "Rewrite the step with an explicit expression.",
                    )
            self.env[stmt.name] = value_type
            return inferred_deps
        if isinstance(stmt, IRDiscard):
            self.infer(stmt.value, inferred_deps)
            return inferred_deps
        if isinstance(stmt, IRGuard):
            condition_type = self.infer(stmt.condition, inferred_deps)
            if not _is_booleanish(condition_type):
                self._warn(
                    ESEM006,
                    stmt.span,
                    f"guard condition has type '{condition_type.render()}'; expected boolean",
                    "Guards must evaluate to boolean conditions.",
                )
            return inferred_deps
        if isinstance(stmt, IRBranch):
            condition_type = self.infer(stmt.condition, inferred_deps)
            if not _is_booleanish(condition_type):
                self._warn(
                    ESEM006,
                    stmt.span,
                    f"IF condition has type '{condition_type.render()}'; expected boolean",
                    "IF conditions must evaluate to boolean values.",
                )
            for inner in stmt.then_body:
                self.check_statement(inner, inferred_deps)
            for inner in stmt.otherwise:
                self.check_statement(inner, inferred_deps)
            return inferred_deps
        return inferred_deps

    # -- expressions ------------------------------------------------------------
    def infer(self, expr: IRExpr, inferred_deps: set[str]) -> TypeRef:
        if isinstance(expr, ForeignExpr):
            return UNKNOWN
        if isinstance(expr, IRLiteral):
            if expr.kind == "number":
                return TypeRef(name="integer" if isinstance(expr.value, int) else "number")
            if expr.kind == "string":
                return TypeRef(name="string")
            if expr.kind == "boolean":
                return TypeRef(name="boolean")
            return TypeRef(name="void")
        if isinstance(expr, IRRef):
            known = self.env.get(expr.name)
            if known is None:
                self._error(
                    ESEM004,
                    expr.span,
                    f"value '{expr.name}' is used before it is defined",
                    f"Define '{expr.name}' in LOGIC or declare it as an input.",
                )
                return UNKNOWN
            return known
        if isinstance(expr, IRFieldAccess):
            base_type = self.infer(expr.base, inferred_deps)
            return self._field_type(base_type, expr.field_name, expr.span)
        if isinstance(expr, IRIndexAccess):
            base_type = self.infer(expr.base, inferred_deps)
            self.infer(expr.index, inferred_deps)
            if base_type.name == "any":
                return UNKNOWN
            if base_type.name == "list":
                inner = base_type.args[0] if base_type.args else UNKNOWN
                return inner
            self._warn(
                ESEM006,
                expr.span,
                f"indexing a value of type '{base_type.render()}'",
                "Index access requires a list.",
            )
            return UNKNOWN
        if isinstance(expr, IRList):
            item_types = [self.infer(item, inferred_deps) for item in expr.items]
            inner = UNKNOWN
            for candidate in item_types:
                if candidate.name != "any":
                    inner = candidate
                    break
            return TypeRef(name="list", args=(inner,))
        if isinstance(expr, IRUnary):
            operand_type = self.infer(expr.operand, inferred_deps)
            if expr.op == "not":
                if not _is_booleanish(operand_type):
                    self._warn(
                        ESEM006,
                        expr.span,
                        f"'not' applied to type '{operand_type.render()}'",
                        "'not' requires a boolean operand.",
                    )
                return TypeRef(name="boolean")
            if operand_type.name not in (*_NUMERIC_TYPES, "any"):
                self._warn(
                    ESEM006,
                    expr.span,
                    f"negating a value of type '{operand_type.render()}'",
                    "Unary minus requires a number.",
                )
            return TypeRef(name="number")
        if isinstance(expr, IRBinary):
            return self._infer_binary(expr, inferred_deps)
        if isinstance(expr, IRCall):
            return self._infer_call(expr, inferred_deps)
        if isinstance(expr, IRMethodCall):
            return self._infer_method_call(expr, inferred_deps)
        return UNKNOWN

    def _field_type(
        self, base_type: TypeRef, field_name: str, span: Optional[SourceSpan]
    ) -> TypeRef:
        if base_type.name == "any":
            return UNKNOWN
        fields = self.table.records.get(base_type.name)
        if fields is None:
            if base_type.name not in _PRIMITIVE_TYPES:
                # A foreign/undeclared type reference: its fields are an
                # explicit unknown in default mode; checked code must
                # declare the contract.
                self._warn(
                    ESEM009,
                    span,
                    f"type '{base_type.render()}' is not declared in this module; "
                    f"field '{field_name}' is unchecked",
                    "Declare the @type (or import its contract) before checked use.",
                )
                return UNKNOWN
            self._error(
                ESEM005,
                span,
                f"field '{field_name}' accessed on non-record type '{base_type.render()}'",
                "Field access requires a declared @type or an explicitly unknown base.",
            )
            return UNKNOWN
        field_type = fields.get(field_name)
        if field_type is None:
            self._error(
                ESEM005,
                span,
                f"type '{base_type.name}' has no field '{field_name}'",
                f"Available fields: {', '.join(sorted(fields)) or 'none'}.",
            )
            return UNKNOWN
        return field_type

    def _infer_binary(self, expr: IRBinary, inferred_deps: set[str]) -> TypeRef:
        left = self.infer(expr.left, inferred_deps)
        right = self.infer(expr.right, inferred_deps)
        op = expr.op
        if op in ("and", "or"):
            for operand, side in ((left, "left"), (right, "right")):
                if not _is_booleanish(operand):
                    self._warn(
                        ESEM006,
                        expr.span,
                        f"'{op}' {side} operand has type '{operand.render()}'; expected boolean",
                        "Logical operators require boolean operands.",
                    )
            return TypeRef(name="boolean")
        if op in ("eq", "ne", "lt", "le", "gt", "ge", "is", "is_not", "in", "not_in"):
            return TypeRef(name="boolean")
        # Arithmetic
        if op == "add" and left.name == "string" and right.name == "string":
            return TypeRef(name="string")
        if op == "add" and left.name == "list" and right.name == "list":
            left_inner = left.args[0] if left.args else UNKNOWN
            right_inner = right.args[0] if right.args else UNKNOWN
            return TypeRef(name="list", args=(left_inner if left_inner.name != "any" else right_inner,))
        if left.name == "any" or right.name == "any":
            return UNKNOWN
        numeric_pair = left.name in _NUMERIC_TYPES and right.name in _NUMERIC_TYPES
        if numeric_pair:
            if {left.name, right.name} == {"integer"}:
                return TypeRef(name="integer") if op != "div" else TypeRef(name="number")
            return TypeRef(name="number")
        self._error(
            ESEM006,
            expr.span,
            f"operator '{op}' applied to '{left.render()}' and '{right.render()}'",
            "Use numbers for arithmetic, or strings/lists with '+' for concatenation.",
        )
        return UNKNOWN

    def _check_arguments(
        self,
        params: tuple[IRParam, ...],
        args: tuple[IRExpr, ...],
        kwargs: tuple[tuple[str, IRExpr], ...],
        span: Optional[SourceSpan],
        target_label: str,
        inferred_deps: set[str],
    ) -> None:
        by_name = {param.name: param for param in params}
        required = sum(1 for param in params if not param.optional)
        positional_names = [param.name for param in params[: len(args)]]

        if len(args) + len(kwargs) < required or len(args) + len(kwargs) > len(params):
            self._error(
                ESEM002,
                span,
                f"'{target_label}' expects "
                f"{required if required == len(params) else f'{required}-{len(params)}'} "
                f"argument(s), got {len(args) + len(kwargs)}",
                f"Parameters: {', '.join(f'{p.name}: {p.type_ref.render()}' for p in params) or 'none'}.",
            )
        for param_name, value in kwargs:
            param = by_name.get(param_name)
            if param is None:
                self._error(
                    ESEM005,
                    span,
                    f"'{target_label}' has no parameter '{param_name}'",
                    f"Parameters: {', '.join(by_name) or 'none'}.",
                )
                continue
            self._check_argument_type(param, value, target_label, inferred_deps)
        for param_name, value in zip(positional_names, args):
            param = by_name[param_name]
            self._check_argument_type(param, value, target_label, inferred_deps)

    def _check_argument_type(
        self,
        param: IRParam,
        value: IRExpr,
        target_label: str,
        inferred_deps: set[str],
    ) -> None:
        actual = self.infer(value, inferred_deps)
        expected = param.type_ref if not param.optional else param.type_ref
        if not types_compatible(expected, actual):
            self._warn(
                ESEM003,
                value.span if hasattr(value, "span") else None,
                f"'{target_label}' parameter '{param.name}' expects "
                f"'{expected.render()}' but got '{actual.render()}'",
                "Pass a matching value or widen the declared parameter type.",
            )

    def _result_of(self, operation: IROperation) -> TypeRef:
        if operation.result is not None and operation.result.declared_type is not None:
            return operation.result.declared_type
        return UNKNOWN

    def _infer_call(self, expr: IRCall, inferred_deps: set[str]) -> TypeRef:
        if expr.anlu:
            operation = self.table.resolve_operation(expr.target)
            if operation is None:
                self._error(
                    ESEM001,
                    expr.span,
                    f"call to unknown operation '[{expr.target}]'",
                    f"Define [{expr.target}] or fix the reference. An omitted DEPENDS entry never makes a call valid.",
                )
                return UNKNOWN
            inferred_deps.add(operation.name)
            self._check_arguments(
                operation.params,
                expr.args,
                expr.kwargs,
                expr.span,
                f"[{operation.name}]",
                inferred_deps,
            )
            return self._result_of(operation)

        target = expr.target
        if target in self.table.literal_functions:
            for arg in expr.args:
                self.infer(arg, inferred_deps)
            for _, value in expr.kwargs:
                self.infer(value, inferred_deps)
            return UNKNOWN

        if target in _BUILTIN_SIGNATURES:
            for arg in expr.args:
                self.infer(arg, inferred_deps)
            for _, value in expr.kwargs:
                self.infer(value, inferred_deps)
            return TypeRef(name=_BUILTIN_SIGNATURES[target][1])

        operation = self.table.resolve_operation(target)
        if operation is not None:
            inferred_deps.add(operation.name)
            self._check_arguments(
                operation.params,
                expr.args,
                expr.kwargs,
                expr.span,
                f"[{operation.name}]",
                inferred_deps,
            )
            return self._result_of(operation)

        if target[:1].isupper():
            # Constructor call: check against the declared record type.
            fields = self.table.records.get(target)
            if fields is None:
                self._warn(
                    ESEM009,
                    expr.span,
                    f"constructor '{target}' is not a declared @type in this module",
                    "Declare the type with @type or import its contract before checked use.",
                )
                return UNKNOWN
            field_types = dict(fields)
            positional = list(expr.args)
            for (field_name, field_type), value in zip(fields.items(), positional):
                actual = self.infer(value, inferred_deps)
                if not types_compatible(field_type, actual):
                    self._warn(
                        ESEM003,
                        expr.span,
                        f"field '{field_name}' of {target} expects "
                        f"'{field_type.render()}' but got '{actual.render()}'",
                        "Pass a matching value for the field.",
                    )
            for kwarg_name, value in expr.kwargs:
                kwarg_type = field_types.get(kwarg_name)
                if kwarg_type is None:
                    self._error(
                        ESEM005,
                        expr.span,
                        f"{target} has no field '{kwarg_name}'",
                        f"Fields: {', '.join(sorted(fields)) or 'none'}.",
                    )
                    continue
                actual = self.infer(value, inferred_deps)
                if not types_compatible(kwarg_type, actual):
                    self._warn(
                        ESEM003,
                        expr.span,
                        f"field '{kwarg_name}' of {target} expects "
                        f"'{kwarg_type.render()}' but got '{actual.render()}'",
                        "Pass a matching value for the field.",
                    )
            return TypeRef(name=target)

        self._warn(
            ESEM009,
            expr.span,
            f"call to undeclared foreign function '{target}'",
            "Checked code requires declared signatures: define the operation, or use a documented builtin.",
        )
        return UNKNOWN

    def _infer_method_call(self, expr: IRMethodCall, inferred_deps: set[str]) -> TypeRef:
        base_type = self.infer(expr.base, inferred_deps)
        for arg in expr.args:
            self.infer(arg, inferred_deps)
        for _, value in expr.kwargs:
            self.infer(value, inferred_deps)
        if base_type.name in _PRIMITIVE_TYPES or base_type.name == "any":
            # Primitive methods stay dynamic; the result is an explicit
            # unknown rather than a guessed type.
            return UNKNOWN
        bound_name = f"{base_type.name}.{expr.method}"
        operation = self.table.resolve_operation(bound_name)
        if operation is not None:
            inferred_deps.add(operation.name)
            return self._result_of(operation)
        self._warn(
            ESEM009,
            expr.span,
            f"method '{expr.method}' on type '{base_type.name}' has no bound operation [{bound_name}]",
            f"Define [{bound_name}] or call a free operation instead.",
        )
        return UNKNOWN


def _build_symbol_table(
    module: IRModule, result: SemanticCheckResult, file_token: str
) -> _SymbolTable:
    table = _SymbolTable()
    table.imports = {
        name.strip().replace("-", "_") for name in module.imports if name.strip()
    }
    for record in module.types:
        table.records[record.name] = {
            f.name: f.type_ref for f in record.fields
        }
    snake_seen: dict[str, str] = {}
    for op in module.operations:
        if op.name in table.operations:
            result.errors.append(
                Diagnostic(
                    code=ESEM007,
                    file=file_token,
                    line=op.span.line if op.span else None,
                    col=None,
                    message=f"duplicate operation identifier '[{op.name}]'",
                    hint="Rename one of the definitions.",
                )
            )
            continue
        table.operations[op.name] = op
        alias = _snake(op.name)
        existing = snake_seen.get(alias)
        if existing is not None and existing != op.name:
            result.errors.append(
                Diagnostic(
                    code=ESEM007,
                    file=file_token,
                    line=op.span.line if op.span else None,
                    col=None,
                    message=(
                        f"'[{op.name}]' collides with '[{existing}]': both lower "
                        f"to the target name '{alias}'"
                    ),
                    hint="Rename one operation; kebab-case and snake_case must not collide.",
                )
            )
        else:
            snake_seen[alias] = op.name
            table.snake_to_kebab[alias] = op.name
    return table


def _declared_depends(anlu: ANLU) -> set[str]:
    declared = set()
    for dep in anlu.depends:
        stripped = dep.strip().strip("[]").strip()
        if stripped and stripped.lower() != "none":
            declared.add(stripped)
    return declared


def check_module(nl_file: NLFile, *, file_token: str = "<source>") -> SemanticCheckResult:
    """Type-check every operation in the module against its signatures."""
    result = SemanticCheckResult()
    module = lower_module(nl_file)

    from .controlflow import check_control

    control = check_control(module, file_token=file_token)
    result.errors.extend(control.errors)
    result.warnings.extend(control.warnings)

    table = _build_symbol_table(module, result, file_token)
    # Module names that compile to stdlib-shadowing filenames break
    # generated test/run imports (#142 example corpus footgun).
    import sys as _sys

    shadow_names = {nl_file.module.name.replace("-", "_")}
    if nl_file.source_path:
        from pathlib import Path as _Path

        shadow_names.add(_Path(nl_file.source_path).stem)
    for shadow in sorted(shadow_names & set(_sys.stdlib_module_names)):
        result.warnings.append(
            Diagnostic(
                code=ESEM013,
                file=file_token,
                line=None,
                col=None,
                message=(
                    f"'{shadow}' compiles to '{shadow}.py', which shadows a "
                    "Python standard-library module and breaks generated "
                    "test/run imports"
                ),
                hint="Rename the module or file to something project-specific.",
            )
        )

    for literal in nl_file.literals:
        for match in re.finditer(r"^def\s+([A-Za-z_]\w*)\s*\(", literal, re.MULTILINE):
            table.literal_functions.add(match.group(1))

    declared_by_op = {anlu.identifier: _declared_depends(anlu) for anlu in nl_file.anlus}

    for operation in module.operations:
        for guard in operation.guards:
            if guard.error is None or guard.error.error_type is None:
                continue
            error_type = guard.error.error_type.strip()
            if (
                error_type
                and error_type not in _KNOWN_ERROR_TYPES
                and error_type not in table.records
            ):
                result.warnings.append(
                    Diagnostic(
                        code=ESEM012,
                        file=file_token,
                        line=operation.span.line if operation.span else None,
                        col=None,
                        message=(
                            f"{operation.name}: guard error type '{error_type}' is "
                            "not a builtin and not a declared @type"
                        ),
                        hint=(
                            "Use a builtin error type or declare the error type; "
                            "default compilation generates a minimal class."
                        ),
                    )
                )

        checker = _OperationChecker(operation, table, result, file_token)
        inferred = checker.run()

        declared = declared_by_op.get(operation.name, set())
        for missing in sorted(inferred - declared):
            if missing == operation.name:
                continue  # self-recursion needs no self-declaration
            result.warnings.append(
                Diagnostic(
                    code=ESEM008,
                    file=file_token,
                    line=operation.span.line if operation.span else None,
                    col=None,
                    message=(
                        f"{operation.name}: calls [{missing}] but DEPENDS does not declare it"
                    ),
                    hint=f"Add [{missing}] to DEPENDS so the contract matches the implementation.",
                )
            )
        for unused in sorted(declared - inferred):
            if unused == operation.name:
                continue
            result.warnings.append(
                Diagnostic(
                    code=ESEM008,
                    file=file_token,
                    line=operation.span.line if operation.span else None,
                    col=None,
                    message=(
                        f"{operation.name}: DEPENDS declares [{unused}] but nothing calls it"
                    ),
                    hint=f"Remove [{unused}] from DEPENDS or add the call it was declared for.",
                )
            )

    return result
