"""Generate TypeScript code from parsed NLS files."""

from __future__ import annotations

import re
from typing import Optional

from .localization import (
    ANLU_IDENTIFIER_PATTERN,
    IDENTIFIER_PATTERN,
    normalize_expression_text,
)
from .schema import ANLU, Invariant, LogicStep, NLFile, TypeDefinition


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


def _input_type_to_typescript(inp) -> str:
    return _python_type_to_typescript(inp.to_python_type())


def _return_type_to_typescript(anlu: ANLU) -> str:
    return _python_type_to_typescript(anlu.to_python_return_type())


def _translate_expression(expression: str) -> str:
    translated = normalize_expression_text(expression.strip())
    translated = translated.replace("×", "*").replace("÷", "/")
    translated = _replace_anlu_calls(translated)
    translated = _translate_list_comprehension(translated)
    translated = _translate_len_calls(translated)
    translated = _translate_ternary(translated)
    translated = re.sub(r"(?<![<>=!])==(?![=])", "===", translated)
    translated = re.sub(r"(?<![<>=!])!=(?![=])", "!==", translated)
    translated = re.sub(r"(?<![\w.])True(?![\w.])", "true", translated)
    translated = re.sub(r"(?<![\w.])False(?![\w.])", "false", translated)
    translated = re.sub(r"(?<![\w.])None(?![\w.])", "null", translated)
    translated = re.sub(r"(?<![\w.])and(?![\w.])", "&&", translated)
    translated = re.sub(r"(?<![\w.])or(?![\w.])", "||", translated)
    translated = re.sub(r"(?<![\w.])not\s+(?=[^=])", "!", translated)
    return translated


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
    return f"{_translate_expression(condition)} ? {_translate_expression(truthy)} : {_translate_expression(falsy)}"


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


def _emit_guard_lines(anlu: ANLU) -> list[str]:
    lines = []
    for guard in anlu.guards:
        condition = _translate_expression(guard.condition)
        error_type = guard.error_type or "Error"
        error_message = guard.error_message or "Guard condition failed"
        lines.append(f"  if (!({condition})) {{")
        lines.append(f"    throw new {error_type}({error_message!r});")
        lines.append("  }")
    return lines


def _emit_edge_cases(anlu: ANLU) -> list[str]:
    lines = []
    for edge_case in anlu.edge_cases:
        condition = _translate_expression(edge_case.condition)
        behavior = normalize_expression_text(edge_case.behavior.strip())
        if behavior.lower().startswith("return "):
            return_expr = _translate_return_expression(anlu, behavior[7:])
            lines.append(f"  if ({condition}) {{")
            if return_expr is None:
                lines.append("    return;")
            else:
                lines.append(f"    return {return_expr};")
            lines.append("  }")
        elif behavior:
            translated = _translate_expression(behavior)
            lines.append(f"  if ({condition}) {{")
            lines.append(f"    {translated};")
            lines.append("  }")
    return lines


def _emit_body(anlu: ANLU) -> str:
    lines: list[str] = []
    lines.extend(_emit_edge_cases(anlu))
    lines.extend(_emit_guard_lines(anlu))

    for step in anlu.logic_steps:
        if step.condition:
            condition = _translate_expression(step.condition)
            lines.append(f"  if ({condition}) {{")
            action = _extract_action(step)
            if action:
                lines.append(f"    {action}")
            lines.append("  }")
            continue

        action = _extract_action(step)
        if action:
            lines.append(f"  {action}")

    return_expr = _translate_return_expression(anlu, anlu.returns)
    if return_expr is None:
        lines.append("  return;")
    else:
        lines.append(f"  return {return_expr};")
    return "\n".join(lines)


def _extract_action(step: LogicStep) -> Optional[str]:
    desc = normalize_expression_text(step.description.strip())
    assignment_match = re.match(rf"^({IDENTIFIER_PATTERN})\s*=\s*(.+)$", desc)
    if assignment_match:
        variable_name, expression = assignment_match.groups()
        return f"const {variable_name} = {_translate_expression(expression)};"

    expr = _desc_to_expression(desc)
    if step.output_binding:
        if expr:
            return f"const {step.output_binding} = {expr};"
        return f"const {step.output_binding} = undefined;"
    if expr:
        return f"{expr};"
    return None


def _desc_to_expression(desc: str) -> Optional[str]:
    translated = _translate_expression(desc)
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


def emit_typescript(nl_file: NLFile) -> str:
    source_display = (
        str(nl_file.source_path).replace("\\", "/")
        if nl_file.source_path
        else "unknown"
    )
    lines = [
        "/**",
        f" * Generated by nlsc from {source_display}",
        f" * Module: {nl_file.module.name}",
        " */",
        "",
    ]

    if nl_file.module.imports:
        for imp in nl_file.module.imports:
            imp_name = imp.strip()
            lines.append(f'import * as {imp_name.replace("-", "_")} from "{imp_name}";')
        lines.append("")

    invariant_map = {inv.type_name: inv for inv in nl_file.invariants}
    for type_def in _order_types(nl_file.module.types):
        lines.append(_emit_type_definition(type_def, invariant_map.get(type_def.name)))
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
