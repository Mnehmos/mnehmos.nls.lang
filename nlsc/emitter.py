"""
NLS Emitter - Generate Python code from ANLUs

Uses mock/template-based generation for V0.
LLM integration can be added as a separate backend.
"""

import ast
import math
import re
from typing import Optional

from .schema import ANLU, NLFile, TypeDefinition, Invariant, LogicStep


class EmitterError(Exception):
    """Raised when emitted code fails validation."""

    def __init__(self, message: str, line: int | None = None, details: str | None = None):
        self.line = line
        self.details = details
        super().__init__(message)


def validate_python(code: str) -> list[dict]:
    """
    Validate that the emitted code is syntactically valid Python.

    Args:
        code: The Python source code to validate

    Returns:
        List of error dicts with keys: line, column, message
        Empty list if code is valid
    """
    errors = []
    try:
        ast.parse(code)
    except SyntaxError as e:
        errors.append({
            "line": e.lineno,
            "column": e.offset,
            "message": e.msg,
            "text": e.text.strip() if e.text else None
        })
    return errors


def _is_safe_numeric(value: str) -> bool:
    """Validate that a constraint value is a safe numeric literal.

    Checks that the value can be parsed as a finite number (int or float).
    Rejects special values (inf, nan) and any non-numeric strings that
    could lead to code injection when interpolated into generated code.

    Args:
        value: The string value to validate

    Returns:
        True if the value is a safe, finite numeric literal
    """
    try:
        num = float(value)
        # Reject infinity and NaN
        if math.isnan(num) or math.isinf(num):
            return False
        return True
    except ValueError:
        return False


def _is_valid_return_expr(expr: str) -> bool:
    """Check if an expression is valid Python for a return statement.

    Uses Python's ast.parse to validate expression syntax.

    Returns False if it appears to be descriptive text or invalid syntax.
    """
    import ast

    expr = expr.strip()

    # Empty is not valid
    if not expr:
        return False

    # No spaces - likely a valid identifier, number, or literal
    if " " not in expr:
        return True

    # Use ast.parse to validate - it handles undefined variables correctly
    try:
        ast.parse(expr, mode='eval')
        return True
    except SyntaxError:
        return False


class EmitError(Exception):
    """Error during code emission"""
    pass


def emit_type_definition(type_def: TypeDefinition, invariant: Optional[Invariant] = None) -> str:
    """
    Generate Python dataclass from TypeDefinition.

    Args:
        type_def: The type definition to emit
        invariant: Optional invariant block for this type

    Returns:
        Python dataclass as a string
    """
    lines = []

    # Emit decorator and class line
    lines.append("@dataclass")
    if type_def.base:
        lines.append(f"class {type_def.name}({type_def.base}):")
    else:
        lines.append(f"class {type_def.name}:")

    # Emit fields
    if not type_def.fields:
        lines.append("    pass")
    else:
        # Sort fields: required fields first, then optional fields (with defaults)
        required_fields = [f for f in type_def.fields if not any(c.lower().strip() == "optional" for c in f.constraints)]
        optional_fields = [f for f in type_def.fields if any(c.lower().strip() == "optional" for c in f.constraints)]

        for field in required_fields:
            py_type = field.to_python_type()
            lines.append(f"    {field.name}: {py_type}")

        for field in optional_fields:
            py_type = field.to_python_type()
            lines.append(f"    {field.name}: {py_type} = None")

        # Emit __post_init__ for constraints and invariants
        constraint_checks = _emit_constraint_checks(type_def)
        field_names = [f.name for f in type_def.fields]
        invariant_checks = _emit_invariant_checks(invariant, field_names) if invariant else []

        if constraint_checks or invariant_checks:
            lines.append("")
            lines.append("    def __post_init__(self):")
            lines.extend(constraint_checks)
            lines.extend(invariant_checks)

    return "\n".join(lines)


def _emit_constraint_checks(type_def: TypeDefinition) -> list[str]:
    """
    Generate constraint validation code for __post_init__.

    Returns list of indented check lines.
    """
    checks = []

    for field in type_def.fields:
        for constraint in field.constraints:
            constraint_lower = constraint.lower().strip()

            if constraint_lower == "non-negative":
                checks.append(f"        if self.{field.name} < 0:")
                checks.append(f"            raise ValueError('{field.name} must be non-negative')")

            elif constraint_lower == "required":
                checks.append(f"        if not self.{field.name}:")
                checks.append(f"            raise ValueError('{field.name} is required')")

            elif constraint_lower == "positive":
                checks.append(f"        if self.{field.name} <= 0:")
                checks.append(f"            raise ValueError('{field.name} must be positive')")

            elif constraint_lower.startswith("min:"):
                min_val = constraint_lower.split(":", 1)[1].strip()
                if _is_safe_numeric(min_val):
                    checks.append(f"        if self.{field.name} < {min_val}:")
                    checks.append(f"            raise ValueError('{field.name} must be at least {min_val}')")
                # Skip non-numeric min constraints to prevent code injection

            elif constraint_lower.startswith("max:"):
                max_val = constraint_lower.split(":", 1)[1].strip()
                if _is_safe_numeric(max_val):
                    checks.append(f"        if self.{field.name} > {max_val}:")
                    checks.append(f"            raise ValueError('{field.name} must be at most {max_val}')")
                # Skip non-numeric max constraints to prevent code injection

    return checks


def _emit_invariant_checks(invariant: Invariant, field_names: list[str]) -> list[str]:
    """
    Generate invariant validation code for __post_init__.

    Args:
        invariant: The invariant block containing conditions
        field_names: List of field names from the type definition

    Returns list of indented check lines.
    """
    checks = []

    for condition in invariant.conditions:
        normalized = condition.strip()

        # Prefix all field references with self.
        # Use word boundaries to avoid partial matches (e.g., 'low' in 'allow')
        for field_name in field_names:
            # Match field name as a whole word, not already prefixed with self.
            pattern = rf'\b(?<!self\.)({re.escape(field_name)})\b'
            normalized = re.sub(pattern, r'self.\1', normalized)

        checks.append(f"        if not ({normalized}):")
        checks.append(f'            raise ValueError("Invariant violated: {condition}")')

    return checks


def emit_function_signature(anlu: ANLU) -> str:
    """Generate Python function signature from ANLU"""
    # Separate required and optional parameters
    required_inputs = [inp for inp in anlu.inputs if not any(c.lower().strip() == "optional" for c in inp.constraints)]
    optional_inputs = [inp for inp in anlu.inputs if any(c.lower().strip() == "optional" for c in inp.constraints)]

    # Build parameter list: required first, then optional with defaults
    params = []
    for inp in required_inputs:
        py_type = inp.to_python_type()
        params.append(f"{inp.name}: {py_type}")

    for inp in optional_inputs:
        py_type = inp.to_python_type()
        params.append(f"{inp.name}: {py_type} = None")

    param_str = ", ".join(params)
    return_type = anlu.to_python_return_type()

    return f"def {anlu.python_name}({param_str}) -> {return_type}:"


def emit_docstring(anlu: ANLU) -> str:
    """Generate docstring from ANLU purpose and inputs"""
    lines = ['    """', f"    {anlu.purpose}"]

    if anlu.inputs:
        lines.append("")
        lines.append("    Args:")
        for inp in anlu.inputs:
            desc = inp.description or inp.type
            lines.append(f"        {inp.name}: {desc}")

    if anlu.returns:
        lines.append("")
        lines.append("    Returns:")
        lines.append(f"        {anlu.returns}")

    lines.append('    """')
    return "\n".join(lines)


def emit_guards(anlu: ANLU) -> list[str]:
    """
    Generate guard validation code.

    Returns list of indented lines that implement guard checks.
    Guards are emitted as if-not-raise blocks.
    """
    lines = []

    for guard in anlu.guards:
        condition = guard.condition.strip()
        try:
            ast.parse(condition, mode="eval")
        except SyntaxError as e:
            raise EmitterError(
                f"invalid guard expression: '{condition}'. Guards must use an explicit Python guard expression and not natural language",
                details=str(e),
            ) from e
        error_type = guard.error_type or "ValueError"
        error_message = guard.error_message or "Guard condition failed"

        # Generate the if-not check
        lines.append(f"    if not ({condition}):")

        # Generate the raise statement
        if guard.error_code:
            lines.append(f"        raise {error_type}('{guard.error_code}', '{error_message}')")
        else:
            lines.append(f"        raise {error_type}('{error_message}')")

    return lines


def emit_body_from_logic(anlu: ANLU) -> str:
    """
    Generate function body deterministically from LOGIC steps.

    Uses dataflow information to generate proper Python code:
    - Assignment steps (var = expr) become Python assignments
    - Conditional steps (IF cond THEN action) become if statements
    - Output bindings (→ var) become assignments
    - RETURNS becomes the return statement
    """
    lines = []

    # Emit guards first
    guard_lines = emit_guards(anlu)
    lines.extend(guard_lines)

    # Process each logic step
    for step in anlu.logic_steps:
        # Check if this is a conditional step
        if step.condition:
            # Generate if statement
            condition = step.condition.strip()
            # Handle NOT prefix
            if condition.upper().startswith("NOT "):
                condition = f"not {condition[4:]}"
            lines.append(f"    if {condition}:")

            # Generate the action inside the if block
            action = _extract_action(step)
            if action:
                lines.append(f"        {action}")
            else:
                lines.append(f"        pass  # {step.description}")
        else:
            # Non-conditional step
            action = _extract_action(step)
            if action:
                lines.append(f"    {action}")
            elif step.description:
                # Descriptive step without assignment - emit as comment
                lines.append(f"    # {step.description}")

    # Generate return statement
    returns = anlu.returns.strip()
    returns_expr = returns.replace("×", "*").replace("÷", "/")

    # Check if returns_expr is a type name that needs conversion
    returns_expr = _convert_type_return(returns_expr, anlu)

    # Validate that returns_expr is valid Python
    if _is_valid_return_expr(returns_expr):
        lines.append(f"    return {returns_expr}")
    else:
        # Descriptive text - emit NotImplementedError with the description
        safe_desc = returns_expr.replace("'", "\\'")
        lines.append(f"    raise NotImplementedError('TODO: {safe_desc}')")

    return "\n".join(lines)


def _convert_type_return(returns_expr: str, anlu: ANLU) -> str:
    """
    Convert type name returns to valid Python expressions.

    If RETURNS is a type name like "dictionary" that wasn't assigned
    in LOGIC steps, convert to an appropriate empty value or placeholder.
    """
    # Check if returns_expr was assigned in logic steps
    assigned_vars = set()
    for step in anlu.logic_steps:
        assigned_vars.update(step.assigns)

    # If it's a variable that was assigned, use it as-is
    if returns_expr in assigned_vars:
        return returns_expr

    # Check if it's an input parameter name
    input_names = {inp.name for inp in anlu.inputs}
    if returns_expr in input_names:
        return returns_expr

    # Type name mappings to empty values
    type_defaults = {
        "dictionary": "{}",
        "dict": "{}",
        "list": "[]",
        "string": '""',
        "str": '""',
        "number": "0",
        "float": "0.0",
        "int": "0",
        "boolean": "False",
        "bool": "False",
    }

    # Check if it's a type name
    returns_lower = returns_expr.lower()
    if returns_lower in type_defaults:
        return type_defaults[returns_lower]

    # Otherwise return as-is (might be a valid expression)
    return returns_expr


def _extract_action(step: LogicStep) -> Optional[str]:
    """
    Extract executable Python action from a logic step.

    Returns the action string, or None if it's purely descriptive.
    """
    desc: str = step.description.strip()

    # Remove state name prefix if present
    if desc.startswith("["):
        bracket_end = desc.find("]")
        if bracket_end > 0:
            desc = desc[bracket_end + 1:].strip()

    # Remove output binding suffix
    for arrow in ["→", "->"]:
        if arrow in desc:
            desc = desc.split(arrow)[0].strip()

    # Remove IF...THEN wrapper if present
    if desc.upper().startswith("IF ") and " THEN " in desc.upper():
        then_pos = desc.upper().find(" THEN ")
        desc = desc[then_pos + 6:].strip()

    # Check for assignment pattern
    if "=" in desc and not desc.startswith("=") and "==" not in desc:
        # Validate this is actually valid Python before returning
        # Check: must start with a valid identifier, then =
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*=', desc):
            # Try to parse as Python to validate
            try:
                ast.parse(desc)
                return desc
            except SyntaxError:
                # Contains = but isn't valid Python - treat as descriptive
                pass

    # Check if step has explicit assigns from output binding
    if step.output_binding and step.assigns:
        # Try to extract meaningful action from description
        expr = _desc_to_expr(desc)
        if expr:
            return f"{step.output_binding} = {expr}"
        # Descriptive text only - emit as single-line comment + placeholder to preserve indentation
        return f"{step.output_binding} = None  # TODO: {desc}"

    # Not an assignment - purely descriptive
    return None


def _desc_to_expr(desc: str) -> Optional[str]:
    """
    Convert a logic step description to a Python expression.

    Returns:
        - Python function call if description contains [anlu-name]
        - The expression if it looks like strictly valid code (single call or assignment)
        - None if it's purely descriptive text (no valid code to emit)
    """
    # Clean up the description
    desc = desc.strip()

    # Check for explicit ANLU reference: [anlu-name](args)
    anlu_call = re.match(r'\[([a-zA-Z][a-zA-Z0-9_-]*)\]\s*\(([^)]*)\)', desc)
    if anlu_call:
        # Convert kebab-case to snake_case for Python
        func_name = anlu_call.group(1).replace("-", "_")
        args = anlu_call.group(2).strip()
        return f"{func_name}({args})"

    # Check for ANLU reference without args: [anlu-name]
    anlu_ref = re.match(r'\[([a-zA-Z][a-zA-Z0-9_-]*)\]', desc)
    if anlu_ref:
        func_name = anlu_ref.group(1).replace("-", "_")
        # Extract any following text as potential args
        remaining = desc[anlu_ref.end():].strip()
        if remaining.startswith("(") and remaining.endswith(")"):
            # Has args
            args = remaining[1:-1].strip()
            return f"{func_name}({args})"
        return f"{func_name}()"

    # Check if strictly looks like a Python assignment: identifier = expr
    # Must start with identifier, have =, and not be ==
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*=(?!=)', desc):
        return desc

    # Check if strictly looks like a Python function call: identifier(args)
    # Must start with identifier, have (, end with ), and nothing else
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*\(.*\)$', desc):
        return desc

    # Purely descriptive text - return None, caller should emit as comment
    return None


def _convert_main_line(line: str) -> Optional[str]:
    """
    Convert an NLS main block line to Python.

    Handles:
    - WHILE condition { -> while condition:
    - } -> (closing brace, returns None)
    - PRINT expr -> print(expr)
    - var = func-name(args) -> var = func_name(args)
    - Comments: # ... -> # ...
    """
    line = line.strip()

    # Skip empty lines
    if not line:
        return None

    # Skip comments
    if line.startswith("#"):
        return line

    # Closing brace (handled by indentation logic in caller)
    if line == "}":
        return None

    # WHILE condition {
    while_match = re.match(r'^WHILE\s+(.+?)\s*\{?\s*$', line, re.IGNORECASE)
    if while_match:
        condition = while_match.group(1)
        # Convert kebab-case to snake_case in condition
        condition = re.sub(r'([a-z])-([a-z])', r'\1_\2', condition)
        return f"while {condition}:"

    # PRINT statement
    print_match = re.match(r'^PRINT\s+(.+)$', line, re.IGNORECASE)
    if print_match:
        expr = print_match.group(1)
        # Convert kebab-case to snake_case
        expr = re.sub(r'([a-z])-([a-z])', r'\1_\2', expr)
        return f"print({expr})"

    # General statement (assignment, function call)
    # Convert kebab-case function names to snake_case
    converted = re.sub(r'([a-z])-([a-z])', r'\1_\2', line)
    return converted


def emit_body_mock(anlu: ANLU) -> str:
    """
    Generate function body using mock/template approach.

    Handles simple patterns deterministically:
    - RETURNS: a + b -> return a + b
    - RETURNS: a × b -> return a * b
    - RETURNS: a - b -> return a - b
    - RETURNS: a / b -> return a / b
    """
    # If we have logic_steps, use deterministic emission
    if anlu.logic_steps:
        return emit_body_from_logic(anlu)

    returns = anlu.returns.strip()

    # Handle void return - no return statement or just pass
    if returns.lower() == "void" or returns.lower() == "none":
        if anlu.guards:
            lines = emit_guards(anlu)
            lines.append("    return None")
            return "\n".join(lines)
        return "    return None"

    # Direct expression returns (a + b, a × b, etc.)
    # Replace math symbols
    expr = returns.replace("×", "*").replace("÷", "/")

    # Helper to generate the return line (or NotImplementedError for invalid)
    def make_return(e: str) -> str:
        if _is_valid_return_expr(e):
            return f"    return {e}"
        safe_desc = e.replace("'", "\\'")
        return f"    raise NotImplementedError('TODO: {safe_desc}')"

    # If guards are provided, generate guard validation code first
    if anlu.guards:
        lines = emit_guards(anlu)
        lines.append(make_return(expr))
        return "\n".join(lines)

    # Check if it's a simple expression with known operators
    if re.match(r"^[a-z_][a-z0-9_]*\s*[\+\-\*\/]\s*[a-z_][a-z0-9_]*$", expr, re.IGNORECASE):
        if anlu.guards:
            lines = emit_guards(anlu)
            lines.append(f"    return {expr}")
            return "\n".join(lines)
        return f"    return {expr}"

    # Check for function-like returns: "result with field1, field2"
    if " with " in returns.lower():
        # Descriptive return - emit NotImplementedError
        safe_desc = returns.replace("'", "\\'")
        return f"    raise NotImplementedError('TODO: {safe_desc}')"

    # If raw logic is provided but no logic_steps, generate comments
    if anlu.logic:
        lines = ["    # Generated from LOGIC steps:"]
        for i, step in enumerate(anlu.logic, 1):
            lines.append(f"    # {i}. {step}")
        lines.append(make_return(expr))
        return "\n".join(lines)

    # Fallback: validate and return
    return make_return(expr)


def emit_anlu(anlu: ANLU, mode: str = "mock") -> str:
    """
    Emit Python code for a single ANLU.

    Args:
        anlu: The ANLU to emit
        mode: "mock" for template-based, "llm" for LLM-based (future)

    Returns:
        Python function as a string
    """
    parts = [
        emit_function_signature(anlu),
        emit_docstring(anlu),
        emit_body_mock(anlu)
    ]

    return "\n".join(parts)


def emit_python(nl_file: NLFile, mode: str = "mock", validate: bool = True) -> str:
    """
    Emit complete Python module from NLFile.

    Args:
        nl_file: Parsed NLFile
        mode: Emission mode ("mock" or "llm")
        validate: If True, validate the output is valid Python syntax

    Returns:
        Complete Python source code

    Raises:
        EmitterError: If validate=True and the generated code has syntax errors
    """
    # Normalize path for cross-platform docstrings
    source_display = str(nl_file.source_path).replace("\\", "/") if nl_file.source_path else "unknown"
    lines = [
        '"""',
        f"Generated by nlsc from {source_display}",
        f"Module: {nl_file.module.name}",
        '"""',
        "",
        "from __future__ import annotations",  # Enable forward references in type hints
        ""
    ]

    # Track imports to add
    imports_needed = []

    # Add dataclass import if types exist
    if nl_file.module.types:
        imports_needed.append("from dataclasses import dataclass")

    # Add type imports if needed
    has_any = any(
        "any" in (inp.type for inp in anlu.inputs) or anlu.to_python_return_type() == "Any"
        for anlu in nl_file.anlus
    )

    # Check for Optional types (fields or inputs with "optional" constraint)
    has_optional = False
    for type_def in nl_file.module.types:
        for field in type_def.fields:
            if any(c.lower().strip() == "optional" for c in field.constraints):
                has_optional = True
                break
        if has_optional:
            break
    if not has_optional:
        for anlu in nl_file.anlus:
            for inp in anlu.inputs:
                if any(c.lower().strip() == "optional" for c in inp.constraints):
                    has_optional = True
                    break
            if has_optional:
                break

    # Check for cast() usage in RETURNS expressions
    has_cast = any(
        anlu.returns and "cast(" in anlu.returns
        for anlu in nl_file.anlus
    )

    # Build typing imports
    typing_imports = []
    if has_any:
        typing_imports.append("Any")
    if has_cast:
        typing_imports.append("cast")
    if has_optional:
        typing_imports.append("Optional")

    if typing_imports:
        imports_needed.append(f"from typing import {', '.join(typing_imports)}")

    # Emit collected imports
    if imports_needed:
        for imp in imports_needed:
            lines.append(imp)
        lines.append("")

    # Add user-specified imports
    # Standard library modules use regular import, custom modules use relative import
    STDLIB_MODULES = {
        "os", "sys", "re", "json", "math", "random", "time", "datetime",
        "collections", "itertools", "functools", "typing", "pathlib",
        "threading", "multiprocessing", "ctypes", "subprocess", "io",
        "copy", "pickle", "hashlib", "base64", "urllib", "http",
        "logging", "unittest", "dataclasses", "abc", "enum", "asyncio",
        "socket", "struct", "array", "queue", "heapq", "bisect",
        "statistics", "decimal", "fractions", "operator", "contextlib",
    }
    if nl_file.module.imports:
        for imp in nl_file.module.imports:
            imp_name = imp.strip()
            if imp_name in STDLIB_MODULES:
                lines.append(f"import {imp_name}")
            else:
                # Custom module - use relative import for cross-module type access
                lines.append(f"from .{imp_name} import *")
        lines.append("")

    # Emit types first (before functions)
    if nl_file.module.types:
        # Build invariant lookup map
        invariant_map = {inv.type_name: inv for inv in nl_file.invariants}

        # Order types: base types before derived types
        ordered_types = _order_types(nl_file.module.types)
        for type_def in ordered_types:
            lines.append("")
            # Look up invariant for this type
            invariant = invariant_map.get(type_def.name)
            lines.append(emit_type_definition(type_def, invariant))
            lines.append("")

    # Extract function names defined in literal blocks to avoid duplicates
    literal_functions = set()
    if nl_file.literals:
        for literal in nl_file.literals:
            # Find all "def funcname(" patterns
            for match in re.finditer(r'^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', literal, re.MULTILINE):
                literal_functions.add(match.group(1))

    # Emit each ANLU in dependency order, skipping those overridden by literal blocks
    ordered = nl_file.dependency_order()
    for anlu in ordered:
        if anlu.python_name in literal_functions:
            # Skip - this ANLU is implemented by a literal block
            continue
        lines.append("")
        lines.append(emit_anlu(anlu, mode))
        lines.append("")

    # Add any literal blocks
    if nl_file.literals:
        lines.append("")
        lines.append("# --- Literal blocks ---")
        for literal in nl_file.literals:
            lines.append(literal)

    # Add main block if present
    if nl_file.main_block:
        lines.append("")
        lines.append("")
        lines.append("if __name__ == '__main__':")
        indent_depth = 1  # Start at 1 for main block
        for main_line in nl_file.main_block:
            stripped = main_line.strip()

            # Handle closing brace - decrease indent
            if stripped == "}":
                indent_depth = max(1, indent_depth - 1)
                continue

            # Convert NLS main syntax to Python
            py_line = _convert_main_line(main_line)
            if py_line:
                indent = "    " * indent_depth
                lines.append(f"{indent}{py_line}")

                # If this line ends with :, next lines are indented
                if py_line.endswith(":"):
                    indent_depth += 1

    code = "\n".join(lines)

    # Validate the generated Python if requested
    if validate:
        errors = validate_python(code)
        if errors:
            err = errors[0]  # Report first error
            error_line = err.get("line", "?")
            error_msg = err.get("message", "Unknown syntax error")
            error_text = err.get("text", "")

            # Build helpful error message
            details = f"Line {error_line}: {error_msg}"
            if error_text:
                details += f"\n  Code: {error_text}"

            raise EmitterError(
                f"Generated Python has syntax errors. {details}",
                line=err.get("line"),
                details=error_text
            )

    return code


def _order_types(types: list[TypeDefinition]) -> list[TypeDefinition]:
    """
    Order types so base types come before derived types.
    """
    ordered = []
    remaining = list(types)
    resolved = set()

    # Simple topological sort
    while remaining:
        made_progress = False
        for type_def in remaining[:]:
            # If no base or base already resolved, add it
            if type_def.base is None or type_def.base in resolved:
                ordered.append(type_def)
                resolved.add(type_def.name)
                remaining.remove(type_def)
                made_progress = True

        if not made_progress and remaining:
            # Circular dependency or external base - add remaining
            ordered.extend(remaining)
            break

    return ordered


def emit_tests(nl_file: NLFile) -> Optional[str]:
    """
    Emit pytest tests from @test blocks.

    Returns:
        Python test file content, or None if no tests
    """
    if not nl_file.tests:
        return None

    module_name = nl_file.module.name.replace("-", "_")

    # Normalize path for cross-platform docstrings
    source_display = str(nl_file.source_path).replace("\\", "/") if nl_file.source_path else "unknown"
    lines = [
        '"""',
        f"Tests generated by nlsc from {source_display}",
        '"""',
        "",
        "import pytest",
        f"from .{module_name} import *",
        ""
    ]

    for test_suite in nl_file.tests:
        lines.append("")
        lines.append(f"class Test{test_suite.anlu_id.replace('-', '_').title()}:")

        for i, case in enumerate(test_suite.cases):
            lines.append(f"    def test_case_{i + 1}(self):")
            lines.append(f"        assert {case.expression} == {case.expected}")
            lines.append("")

    return "\n".join(lines)


def emit_property_tests(nl_file: NLFile) -> Optional[str]:
    """
    Emit hypothesis property-based tests from @property blocks.

    Returns:
        Python test file content with hypothesis decorators, or None if no properties
    """
    if not nl_file.properties:
        return None

    module_name = nl_file.module.name.replace("-", "_")

    lines = [
        '"""',
        f"Property-based tests generated by nlsc from {nl_file.source_path or 'unknown'}",
        '"""',
        "",
        "from hypothesis import given, strategies as st",
        f"from .{module_name} import *",
        ""
    ]

    for prop_test in nl_file.properties:
        func_name = prop_test.anlu_id.replace("-", "_")
        lines.append("")
        lines.append(f"class TestProperty{func_name.title().replace('_', '')}:")

        for i, assertion in enumerate(prop_test.assertions):
            if assertion.quantifier == "forall":
                # Generate hypothesis @given decorator
                var = assertion.variable or "x"
                var_type = assertion.variable_type or "number"
                strategy = _type_to_hypothesis_strategy(var_type)

                lines.append(f"    @given({var}={strategy})")
                lines.append(f"    def test_property_{i + 1}(self, {var}):")
                # Extract the assertion after ->
                expr = assertion.expression.split("->", 1)[-1].strip()
                lines.append(f"        assert {expr}")
                lines.append("")
            else:
                # Simple property assertion
                lines.append("    @given(a=st.floats(allow_nan=False), b=st.floats(allow_nan=False))")
                lines.append(f"    def test_property_{i + 1}(self, a, b):")
                lines.append(f"        assert {assertion.expression}")
                lines.append("")

    return "\n".join(lines)


def _type_to_hypothesis_strategy(nls_type: str) -> str:
    """Convert NLS type to hypothesis strategy"""
    type_map = {
        "number": "st.floats(allow_nan=False, allow_infinity=False)",
        "integer": "st.integers()",
        "string": "st.text()",
        "boolean": "st.booleans()",
    }
    return type_map.get(nls_type.lower(), "st.none()")
