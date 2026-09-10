"""Generate TypeScript code from parsed NLS files."""

from __future__ import annotations

import json
import re
from typing import Callable, Optional

from .localization import (
    ANLU_IDENTIFIER_PATTERN,
    IDENTIFIER_PATTERN,
    normalize_expression_text,
)
from .ir import IRExpr
from .schema import ANLU, Input, Invariant, LogicStep, NLFile, TypeDefinition


def _python_type_to_typescript(py_type: str) -> str:
    py_type = py_type.strip()

    if py_type.startswith("Optional[") and py_type.endswith("]"):
        inner = py_type[len("Optional[") : -1]
        return f"{_python_type_to_typescript(inner)} | null"

    if py_type.startswith("list[") and py_type.endswith("]"):
        inner = py_type[5:-1]
        return f"{_python_type_to_typescript(inner)}[]"

    mapping = {
        "float": "number",
        "int": "number",
        "str": "string",
        "bool": "boolean",
        "None": "void",
        "Any": "unknown",
        "dict": "Record<string, unknown>",
    }
    return mapping.get(py_type, py_type)


def _input_type_to_typescript(inp: Input) -> str:
    return _python_type_to_typescript(inp.to_python_type())


def _return_type_to_typescript(anlu: ANLU) -> str:
    return _python_type_to_typescript(anlu.to_python_return_type())


_STRING_TOKEN = re.compile(r"(?:'[^'\\]*(?:\\.[^'\\]*)*'|\"[^\"\\]*(?:\\.[^\"\\]*)*\")")


def _map_outside_strings(text: str, fn: Callable[[str], str]) -> str:
    """Apply fn to the segments outside string literals only (#202)."""
    parts: list[str] = []
    pos = 0
    for match in _STRING_TOKEN.finditer(text):
        parts.append(fn(text[pos : match.start()]))
        parts.append(match.group(0))
        pos = match.end()
    parts.append(fn(text[pos:]))
    return "".join(parts)


def _word_replacements(text: str) -> str:
    """Operator/keyword rewrite, applied only outside string literals."""
    text = re.sub(r"(?<![<>=!])==(?![=])", "===", text)
    text = re.sub(r"(?<![<>=!])!=(?![=])", "!==", text)
    text = re.sub(r"(?<![\w.])True(?![\w.])", "true", text)
    text = re.sub(r"(?<![\w.])False(?![\w.])", "false", text)
    text = re.sub(r"(?<![\w.])None(?![\w.])", "null", text)
    text = re.sub(r"(?<![\w.])and(?![\w.])", "&&", text)
    text = re.sub(r"(?<![\w.])or(?![\w.])", "||", text)
    text = re.sub(r"(?<![\w.])not\s+(?=[^=])", "!", text)
    return text


def _route_declared_constructors(text: str) -> str:
    """Rewrite declared-type constructor calls to their factories (#202)."""
    for type_name in sorted(_DECLARED_TYPES):
        text = re.sub(
            re.compile("\\b" + re.escape(type_name) + r"\s*\("),
            f"make_{type_name}(",
            text,
        )
    return text


def _translate_expression(expression: str) -> str:
    stripped = expression.strip()
    structural = _translate_structural_expression(stripped)
    if structural is not None:
        return structural
    translated = normalize_expression_text(stripped)
    translated = translated.replace("×", "*").replace("÷", "/")
    translated = _replace_anlu_calls(translated)
    translated = _translate_list_comprehension(translated)
    translated = _translate_len_calls(translated)
    translated = _translate_ternary(translated)
    translated = _map_outside_strings(translated, _word_replacements)
    return _route_declared_constructors(translated)


_NLS_RUNTIME_PRELUDE = """// NLS runtime helpers: structural equality, NLS truthiness, and
// Python-compatible division/modulo semantics (#202).
function __nls_eq(a: any, b: any): boolean {
  if (a === b) { return true; }
  if (typeof a === "number" && typeof b === "number") {
    return Number.isNaN(a) && Number.isNaN(b);
  }
  if (Array.isArray(a) && Array.isArray(b)) {
    if (a.length !== b.length) { return false; }
    for (let i = 0; i < a.length; i++) {
      if (!__nls_eq(a[i], b[i])) { return false; }
    }
    return true;
  }
  if (a !== null && b !== null && typeof a === "object" && typeof b === "object") {
    const ka = Object.keys(a as object);
    const kb = Object.keys(b as object);
    if (ka.length !== kb.length) { return false; }
    for (const k of ka) {
      if (!__nls_eq((a as any)[k], (b as any)[k])) { return false; }
    }
    return true;
  }
  return false;
}
function __nls_truthy(v: any): boolean {
  if (v === null || v === undefined) { return false; }
  if (Array.isArray(v)) { return v.length > 0; }
  if (typeof v === "string") { return v.length > 0; }
  return Boolean(v);
}
class ZeroDivisionError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ZeroDivisionError";
  }
}
function __nls_div(a: number, b: number): number {
  if (b === 0) { throw new ZeroDivisionError("division by zero"); }
  return a / b;
}
function __nls_floor_div(a: number, b: number): number {
  if (b === 0) { throw new ZeroDivisionError("integer division or modulo by zero"); }
  return Math.floor(a / b);
}
function __nls_mod(a: number, b: number): number {
  if (b === 0) { throw new ZeroDivisionError("integer division or modulo by zero"); }
  return ((a % b) + b) % b;
}
function __nls_len(v: any): number {
  if (Array.isArray(v) || typeof v === "string") { return v.length; }
  if (v !== null && typeof v === "object") { return Object.keys(v).length; }
  throw new TypeError("object of no length");
}
function __nls_sum(items: any): number {
  return (items as any[]).reduce((acc: number, item: any) => acc + item, 0);
}
function __nls_max(...args: any[]): any {
  const items = args.length === 1 && Array.isArray(args[0]) ? args[0] : args;
  return items.reduce((best: any, item: any) => (item > best ? item : best));
}
function __nls_min(...args: any[]): any {
  const items = args.length === 1 && Array.isArray(args[0]) ? args[0] : args;
  return items.reduce((best: any, item: any) => (item < best ? item : best));
}

"""

# Method names whose semantics differ between the reference runtime and
# JavaScript; everything else passes through unchanged.
_METHOD_NAME_MAP = {
    "append": "push",
    "lower": "toLowerCase",
    "upper": "toUpperCase",
    "strip": "trim",
}

_BINARY_TS_OPS = {
    "add": "+",
    "sub": "-",
    "mul": "*",
    "pow": "**",
    "lt": "<",
    "le": "<=",
    "gt": ">",
    "ge": ">=",
    "and": "&&",
    "or": "||",
}


def _ts_precedence(op: str) -> int:
    """Binding power for minimal-parenthesis rendering."""
    if op in ("or",):
        return 1
    if op in ("and",):
        return 2
    if op in ("eq", "ne", "lt", "le", "gt", "ge", "is", "is_not", "in", "not_in"):
        return 3
    if op in ("add", "sub"):
        return 4
    if op in ("mul", "div", "mod", "floor_div"):
        return 5
    if op == "pow":
        return 7
    return 100


def _render_ts_expr(expr: IRExpr, min_prec: int = 0) -> Optional[str]:
    """Render a lowered IR expression as TypeScript (#202).

    Uses minimal parentheses via operand precedence.  Returns None for
    nodes the renderer does not cover yet; the caller falls back to the
    legacy translator for those expressions.
    """
    from .ir import (
        IRBinary,
        IRCall,
        IRFieldAccess,
        IRIndexAccess,
        IRList,
        IRLiteral,
        IRMethodCall,
        IRRef,
        IRUnary,
    )

    def _paren_if_needed(rendered: str, prec: int) -> str:
        if prec < min_prec:
            return f"({rendered})"
        return rendered

    if isinstance(expr, IRLiteral):
        if expr.kind == "boolean":
            return "true" if expr.value else "false"
        if expr.kind == "none":
            return "null"
        return expr.raw
    if isinstance(expr, IRRef):
        return expr.name
    if isinstance(expr, IRFieldAccess):
        base = _render_ts_expr(expr.base, 100)
        return None if base is None else f"{base}.{expr.field_name}"
    if isinstance(expr, IRIndexAccess):
        base = _render_ts_expr(expr.base, 100)
        index = _render_ts_expr(expr.index, 0)
        if base is None or index is None:
            return None
        return f"{base}[{index}]"
    if isinstance(expr, IRList):
        rendered: list[str] = []
        for item in expr.items:
            part = _render_ts_expr(item, 0)
            if part is None:
                return None
            rendered.append(part)
        if not rendered:
            return "[] as any[]"
        return "[" + ", ".join(rendered) + "]"
    if isinstance(expr, IRUnary):
        operand = _render_ts_expr(expr.operand, 6)
        if operand is None:
            return None
        if expr.op == "not":
            return f"!__nls_truthy({operand})"
        return _paren_if_needed(f"-{operand}", 6)
    if isinstance(expr, IRBinary):
        op = expr.op
        if op == "eq":
            left = _render_ts_expr(expr.left, 100)
            right = _render_ts_expr(expr.right, 100)
            if left is None or right is None:
                return None
            return f"__nls_eq({left}, {right})"
        if op == "ne":
            left = _render_ts_expr(expr.left, 100)
            right = _render_ts_expr(expr.right, 100)
            if left is None or right is None:
                return None
            return f"!__nls_eq({left}, {right})"
        if op == "is":
            left = _render_ts_expr(expr.left, 4)
            right = _render_ts_expr(expr.right, 5)
            if left is None or right is None:
                return None
            return _paren_if_needed(f"{left} === {right}", 3)
        if op == "is_not":
            left = _render_ts_expr(expr.left, 4)
            right = _render_ts_expr(expr.right, 5)
            if left is None or right is None:
                return None
            return _paren_if_needed(f"{left} !== {right}", 3)
        if op == "in":
            left = _render_ts_expr(expr.left, 100)
            right = _render_ts_expr(expr.right, 100)
            if left is None or right is None:
                return None
            return _paren_if_needed(f"{right}.includes({left})", 3)
        if op == "not_in":
            left = _render_ts_expr(expr.left, 100)
            right = _render_ts_expr(expr.right, 100)
            if left is None or right is None:
                return None
            return _paren_if_needed(f"!{right}.includes({left})", 3)
        if op in ("div", "mod", "floor_div"):
            left = _render_ts_expr(expr.left, 6)
            right = _render_ts_expr(expr.right, 7)
            if left is None or right is None:
                return None
            helper = {"div": "__nls_div", "mod": "__nls_mod", "floor_div": "__nls_floor_div"}[op]
            return f"{helper}({left}, {right})"
        ts_op = _BINARY_TS_OPS.get(op)
        if ts_op is None:
            return None
        prec = _ts_precedence(op)
        # Left-associative: right operand with equal precedence needs parens.
        left = _render_ts_expr(expr.left, prec)
        right_min = prec if op == "pow" else prec + 1
        left_min = prec + 1 if op == "pow" else prec
        left = _render_ts_expr(expr.left, left_min)
        right = _render_ts_expr(expr.right, right_min)
        if left is None or right is None:
            return None
        return _paren_if_needed(f"{left} {ts_op} {right}", prec)
    if isinstance(expr, IRCall):
        args: list[str] = []
        for argument in expr.args:
            part = _render_ts_expr(argument, 0)
            if part is None:
                return None
            args.append(part)
        kwargs: list[str] = []
        for name, value in expr.kwargs:
            kwarg_value = _render_ts_expr(value, 0)
            if kwarg_value is None:
                return None
            kwargs.append(f"{name}: {kwarg_value}")
        all_args = ", ".join(args + kwargs)
        if expr.anlu:
            return f"{expr.target.replace('-', '_')}({all_args})"
        target = expr.target
        if target[:1].isupper() and target in _DECLARED_TYPES:
            # Constructor of a declared record: route to its validating
            # factory with arguments in field order (#202).
            field_order = _DECLARED_TYPES[target]
            kwarg_values: dict[str, str] = {}
            for name, value in expr.kwargs:
                rendered_kw = _render_ts_expr(value, 0)
                if rendered_kw is None:
                    return None
                kwarg_values[name] = rendered_kw
            ordered: list[str] = []
            positional = list(args)
            used_kwargs: set[str] = set()
            for field_name in field_order:
                if field_name in kwarg_values:
                    ordered.append(kwarg_values[field_name])
                    used_kwargs.add(field_name)
                elif positional:
                    ordered.append(positional.pop(0))
            for leftover_name in kwarg_values:
                if leftover_name not in used_kwargs:
                    return None
            if positional:
                return None
            return f"make_{target}({', '.join(ordered)})"
        builtin_map = {
            "len": "__nls_len",
            "sum": "__nls_sum",
            "max": "__nls_max",
            "min": "__nls_min",
            "abs": "Math.abs",
            "round": "Math.round",
            "sqrt": "Math.sqrt",
            "str": "String",
            "int": "Math.trunc",
            "float": "Number",
            "bool": "__nls_truthy",
        }
        if target in builtin_map:
            return f"{builtin_map[target]}({', '.join(args)})"
        return f"{target}({all_args})"
    if isinstance(expr, IRMethodCall):
        base = _render_ts_expr(expr.base, 100)
        if base is None:
            return None
        method_args: list[str] = []
        for argument in expr.args:
            part = _render_ts_expr(argument, 0)
            if part is None:
                return None
            method_args.append(part)
        method = _METHOD_NAME_MAP.get(expr.method, expr.method)
        return f"{base}.{method}({', '.join(method_args)})"
    return None


def _translate_structural_expression(expression: str) -> Optional[str]:
    """Translate via the target-neutral IR when the expression lowers cleanly.

    Expressions that lower to foreign nodes (comprehensions, ternaries,
    f-strings, ...) keep the legacy translator; anything structural gets
    NLS runtime semantics: structural equality, NLS truthiness, and
    Python-compatible division/modulo.
    """
    from .ir import ForeignExpr, SourceSpan
    from .lowering import lower_expression

    expr = lower_expression(expression, SourceSpan(anlu="typescript"))
    if isinstance(expr, ForeignExpr):
        return None
    return _render_ts_expr(expr)


def _replace_anlu_calls(expression: str) -> str:
    expression = re.sub(
        rf"\[({ANLU_IDENTIFIER_PATTERN})\]\s*\(([^)]*)\)",
        lambda match: f"{match.group(1).replace('-', '_')}({_translate_expression(match.group(2))})",
        expression,
    )
    expression = re.sub(
        rf"\[({ANLU_IDENTIFIER_PATTERN})\]",
        lambda match: f"{match.group(1).replace('-', '_')}()",
        expression,
    )
    return expression


def _translate_list_comprehension(expression: str) -> str:
    match = re.fullmatch(
        rf"\[(?P<expr>.+?)\s+for\s+(?P<var>{IDENTIFIER_PATTERN})\s+in\s+(?P<iter>.+?)(?:\s+if\s+(?P<cond>.+))?\]",
        expression,
    )
    if not match:
        return expression

    expr = _translate_expression(match.group("expr"))
    var_name = match.group("var")
    iterable = _translate_expression(match.group("iter"))
    condition = match.group("cond")

    if condition:
        filtered = (
            f"{iterable}.filter(({var_name}) => {_translate_expression(condition)})"
        )
    else:
        filtered = iterable

    if expr == var_name:
        return filtered
    return f"{filtered}.map(({var_name}) => {expr})"


def _translate_len_calls(expression: str) -> str:
    pattern = re.compile(r"\blen\(([^()]+)\)")
    translated = expression
    while True:
        updated = pattern.sub(
            lambda match: f"{match.group(1).strip()}.length", translated
        )
        if updated == translated:
            return updated
        translated = updated


def _translate_ternary(expression: str) -> str:
    match = re.fullmatch(r"(.+?)\s+if\s+(.+?)\s+else\s+(.+)", expression)
    if not match:
        return expression
    truthy, condition, falsy = match.groups()
    # NLS truthiness: an empty list is falsy, unlike raw JS (#202).
    condition_ts = f"__nls_truthy({_translate_expression(condition)})"
    return f"{condition_ts} ? {_translate_expression(truthy)} : {_translate_expression(falsy)}"


def _translate_return_expression(anlu: ANLU, expression: str) -> Optional[str]:
    normalized = normalize_expression_text(expression.strip())
    if normalized.lower() in {"void", "none"}:
        return None

    return_type = _return_type_to_typescript(anlu)
    if return_type.endswith("[]"):
        parts = _split_top_level_plus(normalized)
        if len(parts) > 1:
            translated_parts = ", ".join(
                f"...{_translate_expression(part)}" for part in parts
            )
            return f"[{translated_parts}]"

    translated = _translate_expression(normalized)
    defaults = {
        "dictionary": "{}",
        "dict": "{}",
        "list": "[]",
        "string": '""',
        "str": '""',
        "number": "0",
        "float": "0",
        "int": "0",
        "boolean": "false",
        "bool": "false",
    }
    return defaults.get(translated.lower(), translated)


def _split_top_level_plus(expression: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for char in expression:
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth = max(0, depth - 1)
        if char == "+" and depth == 0:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    if current:
        parts.append("".join(current).strip())
    return [part for part in parts if part]


# Declared @type names for the current emission; constructor calls to
# these route to their validating factories (#202).  Full plumbing of
# module context through every translate call arrives with the
# checked-IR emitter migration.
_DECLARED_TYPES: dict[str, list[str]] = {}


def _emit_type_factory(
    type_def: TypeDefinition, invariant: Optional[Invariant] = None
) -> list[str]:
    """Emit a validating constructor factory for a record type (#202).

    Mirrors the Python dataclass ``__post_init__`` semantics: required /
    non-negative / positive / min / max constraint checks and invariant
    conditions throw ``ValueError`` with the same messages as Python.
    """
    name = type_def.name
    lines = [f"export function make_{name}("]
    params: list[str] = []
    for field in type_def.fields:
        optional = any(c.lower().strip() == "optional" for c in field.constraints)
        marker = "?" if optional else ""
        ts_type = _python_type_to_typescript(field.to_python_type())
        params.append(f"  {field.name}{marker}: {ts_type}")
    lines.append(",\n".join(params))
    lines.append(f"): {name} {{")

    def check(condition: str, message: str) -> None:
        lines.append(f"  if ({condition}) {{")
        lines.append(f'    throw new ValueError("{message}");')
        lines.append("  }")

    for field in type_def.fields:
        for constraint in field.constraints:
            lowered = constraint.lower().strip()
            if lowered == "required":
                check(
                    f"!__nls_truthy({field.name})",
                    f"{field.name} is required",
                )
            elif lowered == "non-negative":
                check(f"{field.name} < 0", f"{field.name} must be non-negative")
            elif lowered == "positive":
                check(f"{field.name} <= 0", f"{field.name} must be positive")
            elif lowered.startswith("min:"):
                bound = lowered.split(":", 1)[1].strip()
                if bound.replace(".", "", 1).isdigit() or (
                    bound.startswith("-") and bound[1:].replace(".", "", 1).isdigit()
                ):
                    check(f"{field.name} < {bound}", f"{field.name} must be at least {bound}")
            elif lowered.startswith("max:"):
                bound = lowered.split(":", 1)[1].strip()
                if bound.replace(".", "", 1).isdigit() or (
                    bound.startswith("-") and bound[1:].replace(".", "", 1).isdigit()
                ):
                    check(f"{field.name} > {bound}", f"{field.name} must be at most {bound}")

    if invariant is not None:
        for condition in invariant.conditions:
            translated = _translate_expression(condition)
            check(
                f"!__nls_truthy({translated})",
                f"Invariant violated: {condition}",
            )

    body = ", ".join(field.name for field in type_def.fields)
    lines.append(f"  return {{ {body} }};")
    lines.append("}")
    return lines


def _emit_type_definition(
    type_def: TypeDefinition, invariant: Optional[Invariant] = None
) -> str:
    lines = []
    extends_clause = f" extends {type_def.base}" if type_def.base else ""
    lines.append(f"export interface {type_def.name}{extends_clause} {{")
    for field in type_def.fields:
        optional = any(c.lower().strip() == "optional" for c in field.constraints)
        optional_marker = "?" if optional else ""
        lines.append(
            f"  {field.name}{optional_marker}: {_python_type_to_typescript(field.to_python_type())};"
        )
    lines.append("}")
    if invariant and invariant.conditions:
        lines.append("")
        lines.append(f"// Invariants for {type_def.name}:")
        for condition in invariant.conditions:
            lines.append(f"// - {condition}")
    return "\n".join(lines)


def _emit_jsdoc(anlu: ANLU) -> str:
    lines = ["/**", f" * {anlu.purpose}"]
    for inp in anlu.inputs:
        desc = inp.description or inp.type
        lines.append(f" * @param {inp.name} {desc}")
    if anlu.returns:
        lines.append(f" * @returns {anlu.returns}")
    lines.append(" */")
    return "\n".join(lines)


def _emit_function_signature(anlu: ANLU) -> str:
    required_inputs = [
        inp
        for inp in anlu.inputs
        if not any(c.lower().strip() == "optional" for c in inp.constraints)
    ]
    optional_inputs = [
        inp
        for inp in anlu.inputs
        if any(c.lower().strip() == "optional" for c in inp.constraints)
    ]

    params = [
        f"{inp.name}: {_input_type_to_typescript(inp)}" for inp in required_inputs
    ]
    params.extend(
        f"{inp.name}: {_input_type_to_typescript(inp)} = null"
        for inp in optional_inputs
    )
    return_type = _return_type_to_typescript(anlu)
    return f"export function {anlu.python_name}({', '.join(params)}): {return_type} {{"


TYPESCRIPT_BUILTIN_ERRORS = {
    "Error",
    "EvalError",
    "RangeError",
    "ReferenceError",
    "SyntaxError",
    "TypeError",
    "URIError",
}


def collect_guard_error_types(nl_file: NLFile) -> list[str]:
    collected = _collect_guard_error_types_raw(nl_file)
    # Factory checks (#202) raise ValueError for constraint/invariant
    # violations, mirroring the Python dataclass behavior.
    has_factory_checks = any(
        any(field.constraints for field in type_def.fields)
        or any(
            inv.type_name == type_def.name and inv.conditions
            for inv in nl_file.invariants
        )
        for type_def in nl_file.module.types
    )
    if has_factory_checks and "ValueError" not in collected:
        collected.append("ValueError")
    return collected


def _collect_guard_error_types_raw(nl_file: NLFile) -> list[str]:
    """Distinct non-builtin guard error types, in first-use order."""
    seen: list[str] = []
    for anlu in nl_file.anlus:
        for guard in anlu.guards:
            error_type = (guard.error_type or "").strip()
            if (
                error_type
                and error_type not in TYPESCRIPT_BUILTIN_ERRORS
                and error_type not in seen
            ):
                seen.append(error_type)
    return seen


def _emit_guard_error_runtime(nl_file: NLFile) -> list[str]:
    """Emit portable error classes for guard failure identities (#198).

    Guard failures must preserve type, code, and message on both targets
    without referencing undefined exception constructors.
    """
    lines: list[str] = []
    for error_type in collect_guard_error_types(nl_file):
        lines.append(
            f"class {error_type} extends Error {{"
        )
        lines.append("  code?: string;")
        lines.append("  constructor(message: string, code?: string) {")
        lines.append("    super(message);")
        lines.append(f'    this.name = "{error_type}";')
        lines.append("    if (code !== undefined) {")
        lines.append("      this.code = code;")
        lines.append("    }")
        lines.append("  }")
        lines.append("}")
        lines.append("")
    return lines


def _emit_guard_lines(anlu: ANLU) -> list[str]:
    lines = []
    for guard in anlu.guards:
        condition = _translate_expression(guard.condition)
        error_type = guard.error_type or "Error"
        error_message = guard.error_message or "Guard condition failed"
        message_literal = json.dumps(error_message)
        code_literal = json.dumps(guard.error_code) if guard.error_code else None
        lines.append(f"  if (!__nls_truthy({condition})) {{")
        if code_literal is not None:
            lines.append(
                f"    throw new {error_type}({message_literal}, {code_literal});"
            )
        else:
            lines.append(f"    throw new {error_type}({message_literal});")
        lines.append("  }")
    return lines


def _emit_edge_cases(anlu: ANLU) -> list[str]:
    lines = []
    for edge_case in anlu.edge_cases:
        condition = _translate_expression(edge_case.condition)
        behavior = normalize_expression_text(edge_case.behavior.strip())
        if behavior.lower().startswith("return "):
            return_expr = _translate_return_expression(anlu, behavior[7:])
            lines.append(f"  if (__nls_truthy({condition})) {{")
            if return_expr is None:
                lines.append("    return;")
            else:
                lines.append(f"    return {return_expr};")
            lines.append("  }")
        elif behavior:
            translated = _translate_expression(behavior)
            lines.append(f"  if (__nls_truthy({condition})) {{")
            lines.append(f"    {translated};")
            lines.append("  }")
    return lines


def _multi_bound_names(anlu: ANLU) -> set[str]:
    """Names bound more than once (rebounds or joined branch arms).

    These must be declared with ``let`` at function scope; ``const``
    inside a block would not escape the branch or would collide.
    """
    counts: dict[str, int] = {}
    for step in anlu.logic_steps:
        for name in step.assigns:
            counts[name] = counts.get(name, 0) + 1
        # A total branch joins the same binding in both arms of one step.
        if step.else_action and step.output_binding:
            match = re.search(
                rf"\s*(?:→|->)\s*({IDENTIFIER_PATTERN})$", step.else_action.strip()
            )
            if match and match.group(1) == step.output_binding:
                counts[step.output_binding] = counts.get(step.output_binding, 0) + 1
    return {name for name, count in counts.items() if count > 1}


def _else_action_line(
    step: LogicStep,
    multi_bound: Optional[set[str]] = None,
    hoisted: Optional[set[str]] = None,
) -> Optional[str]:
    """Emit the ELSE arm of an IF/THEN/ELSE step as a TypeScript action."""
    if not step.else_action:
        return None
    raw = step.else_action.strip()
    binding = step.output_binding
    binding_match = re.search(
        rf"\s*(?:→|->)\s*({IDENTIFIER_PATTERN})$", raw
    )
    if binding_match:
        binding = binding_match.group(1)
        raw = raw[: binding_match.start()].strip()
    arm_step = LogicStep(
        number=step.number,
        description=raw,
        assigns=[binding] if binding else [],
        output_binding=binding,
    )
    action = _extract_action(arm_step, multi_bound, hoisted)
    if action:
        return action
    return None


def _emit_body(anlu: ANLU) -> str:
    lines: list[str] = []
    lines.extend(_emit_edge_cases(anlu))
    lines.extend(_emit_guard_lines(anlu))

    multi_bound = _multi_bound_names(anlu)
    hoisted: set[str] = set()

    for step in anlu.logic_steps:
        if step.condition:
            condition = _translate_expression(step.condition)
            # A total branch that joins a value needs the binding declared
            # at function scope before the if/else arms assign it.
            joined = (
                step.output_binding
                if step.else_action
                and step.output_binding in multi_bound
                else None
            )
            if joined and joined not in hoisted:
                lines.append(f"  let {joined};")
                hoisted.add(joined)
            lines.append(f"  if (__nls_truthy({condition})) {{")
            action = _extract_action(step, multi_bound, hoisted)
            if action:
                lines.append(f"    {action}")
            if step.else_action:
                lines.append("  } else {")
                else_action = _else_action_line(step, multi_bound, hoisted)
                if else_action:
                    lines.append(f"    {else_action}")
            lines.append("  }")
            continue

        action = _extract_action(step, multi_bound, hoisted)
        if action:
            lines.append(f"  {action}")

    return_expr = _translate_return_expression(anlu, anlu.returns)
    if return_expr is None:
        lines.append("  return;")
    else:
        lines.append(f"  return {return_expr};")
    return "\n".join(lines)


def _extract_action(
    step: LogicStep,
    multi_bound: Optional[set[str]] = None,
    hoisted: Optional[set[str]] = None,
) -> Optional[str]:
    desc = normalize_expression_text(step.description.strip())
    assignment_match = re.match(rf"^({IDENTIFIER_PATTERN})\s*=\s*(.+)$", desc)
    if assignment_match:
        variable_name, expression = assignment_match.groups()
        translated = _translate_expression(expression)
        if multi_bound and variable_name in multi_bound:
            if hoisted is not None and variable_name in hoisted:
                return f"{variable_name} = {translated};"
            if hoisted is not None:
                hoisted.add(variable_name)
                return f"let {variable_name} = {translated};"
        return f"const {variable_name} = {translated};"

    expr = _desc_to_expression(desc)
    if step.output_binding:
        if expr:
            if multi_bound and step.output_binding in multi_bound:
                if hoisted is not None and step.output_binding in hoisted:
                    return f"{step.output_binding} = {expr};"
                if hoisted is not None:
                    hoisted.add(step.output_binding)
                    return f"let {step.output_binding} = {expr};"
            return f"const {step.output_binding} = {expr};"
        return f"const {step.output_binding} = undefined;"
    if expr:
        return f"{expr};"
    return None


def _desc_to_expression(desc: str) -> Optional[str]:
    translated = _translate_expression(desc)
    if re.fullmatch(
        r"-?\d+(?:\.\d+)?|'[^']*'|\"[^\"]*\"|True|False|None",
        translated,
    ):
        return translated
    if re.match(rf"^({IDENTIFIER_PATTERN})\s*\(.*\)$", translated):
        return translated
    if translated.startswith("[") and translated.endswith("]"):
        return translated
    if any(
        operator in translated
        for operator in [
            ".",
            "(",
            ")",
            "[",
            "]",
            "+",
            "-",
            "*",
            "/",
            "<",
            ">",
            "==",
            "!=",
        ]
    ):
        return translated
    if re.match(rf"^{IDENTIFIER_PATTERN}$", translated):
        return translated
    return None


def emit_typescript(
    nl_file: NLFile, scaffold_anlus: set[str] | None = None
) -> str:
    source_display = (
        str(nl_file.source_path).replace("\\", "/")
        if nl_file.source_path
        else "unknown"
    )
    lines = [
        "/**",
        f" * Generated by nlsc from {source_display}",
        f" * Module: {nl_file.module.name}",
    ]
    if scaffold_anlus:
        lines.append(
            f" * Status: INCOMPLETE SCAFFOLD - {len(scaffold_anlus)} ANLU(s) have "
            "unresolved executable content: " + ", ".join(sorted(scaffold_anlus))
        )
    lines.extend([" */", ""])

    if nl_file.module.imports:
        for imp in nl_file.module.imports:
            imp_name = imp.strip()
            lines.append(f'import * as {imp_name.replace("-", "_")} from "{imp_name}";')
        lines.append("")

    # NLS runtime helpers: structural equality, NLS truthiness, and
    # Python-compatible division/modulo semantics (#202).
    lines.append(_NLS_RUNTIME_PRELUDE)

    # Portable error runtime for guard failure identities (#198).
    guard_error_runtime = _emit_guard_error_runtime(nl_file)
    if guard_error_runtime:
        lines.extend(guard_error_runtime)

    invariant_map = {inv.type_name: inv for inv in nl_file.invariants}
    _DECLARED_TYPES.clear()
    _DECLARED_TYPES.update({t.name: [f.name for f in t.fields] for t in nl_file.module.types})
    for type_def in _order_types(nl_file.module.types):
        lines.append(_emit_type_definition(type_def, invariant_map.get(type_def.name)))
        lines.append("")
        # Validating constructor factories (#202): construction-time
        # constraint and invariant checks, identical to the Python
        # dataclass __post_init__ behavior.
        lines.extend(_emit_type_factory(type_def, invariant_map.get(type_def.name)))
        lines.append("")

    for anlu in nl_file.dependency_order():
        lines.append(_emit_jsdoc(anlu))
        lines.append(_emit_function_signature(anlu))
        lines.append(_emit_body(anlu))
        lines.append("}")
        lines.append("")

    if nl_file.main_block:
        for main_line in nl_file.main_block:
            stripped = main_line.strip()
            if not stripped or stripped == "}":
                continue
            lines.append(_translate_expression(stripped) + ";")

    return "\n".join(lines).rstrip() + "\n"


def emit_tests_typescript(nl_file: NLFile) -> Optional[str]:
    if not nl_file.tests:
        return None

    module_name = nl_file.module.name.replace("-", "_")
    imported_names = ", ".join(test.anlu_id.replace("-", "_") for test in nl_file.tests)
    source_display = (
        str(nl_file.source_path).replace("\\", "/")
        if nl_file.source_path
        else "unknown"
    )

    lines = [
        "/**",
        f" * Tests generated by nlsc from {source_display}",
        " */",
        "",
        'import assert from "node:assert/strict";',
        f'import {{ {imported_names} }} from "./{module_name}";',
        "",
    ]

    for test_suite in nl_file.tests:
        for case in test_suite.cases:
            expression = _translate_expression(case.expression)
            expected = _translate_expression(case.expected)
            lines.append(f"assert.deepStrictEqual({expression}, {expected});")

    lines.append('console.log("All generated tests passed.");')
    return "\n".join(lines) + "\n"


def _order_types(types: list[TypeDefinition]) -> list[TypeDefinition]:
    ordered: list[TypeDefinition] = []
    remaining = list(types)
    resolved: set[str] = set()

    while remaining:
        made_progress = False
        for type_def in remaining[:]:
            if type_def.base is None or type_def.base in resolved:
                ordered.append(type_def)
                resolved.add(type_def.name)
                remaining.remove(type_def)
                made_progress = True
        if not made_progress:
            ordered.extend(remaining)
            break

    return ordered
