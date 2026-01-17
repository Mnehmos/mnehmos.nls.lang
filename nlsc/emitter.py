"""
NLS Emitter - Generate Python code from ANLUs

Uses mock/template-based generation for V0.
LLM integration can be added as a separate backend.
"""

import re
from typing import Optional

from .schema import ANLU, NLFile, TypeDefinition


class EmitError(Exception):
    """Error during code emission"""
    pass


def emit_type_definition(type_def: TypeDefinition) -> str:
    """
    Generate Python dataclass from TypeDefinition.

    Args:
        type_def: The type definition to emit

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
        for field in type_def.fields:
            py_type = field.to_python_type()
            lines.append(f"    {field.name}: {py_type}")

        # Emit __post_init__ for constraints
        constraint_checks = _emit_constraint_checks(type_def)
        if constraint_checks:
            lines.append("")
            lines.append("    def __post_init__(self):")
            lines.extend(constraint_checks)

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
                checks.append(f"        if self.{field.name} < {min_val}:")
                checks.append(f"            raise ValueError('{field.name} must be at least {min_val}')")

            elif constraint_lower.startswith("max:"):
                max_val = constraint_lower.split(":", 1)[1].strip()
                checks.append(f"        if self.{field.name} > {max_val}:")
                checks.append(f"            raise ValueError('{field.name} must be at most {max_val}')")

    return checks


def emit_function_signature(anlu: ANLU) -> str:
    """Generate Python function signature from ANLU"""
    # Build parameter list
    params = []
    for inp in anlu.inputs:
        param = inp.name
        py_type = inp.to_python_type()
        params.append(f"{param}: {py_type}")
    
    param_str = ", ".join(params)
    return_type = anlu.to_python_return_type()
    
    return f"def {anlu.python_name}({param_str}) -> {return_type}:"


def emit_docstring(anlu: ANLU) -> str:
    """Generate docstring from ANLU purpose and inputs"""
    lines = [f'    """', f"    {anlu.purpose}"]
    
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

    if lines:
        lines.append(f"    return {returns_expr}")
    else:
        # No logic steps - just return the expression
        lines.append(f"    return {returns_expr}")

    return "\n".join(lines)


def _extract_action(step) -> Optional[str]:
    """
    Extract executable Python action from a logic step.

    Returns the action string, or None if it's purely descriptive.
    """
    desc = step.description.strip()

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
    if "=" in desc and not desc.startswith("=") and not "==" in desc:
        # This is an assignment - return it
        return desc

    # Check if step has explicit assigns from output binding
    if step.output_binding and step.assigns:
        # Generate assignment from description
        # Try to extract meaningful action
        return f"{step.output_binding} = {_desc_to_expr(desc)}"

    # Not an assignment - purely descriptive
    return None


def _desc_to_expr(desc: str) -> str:
    """
    Convert descriptive text to a Python expression placeholder.

    For V1, we keep descriptive steps as function calls to be defined.
    """
    # Clean up the description
    desc = desc.strip()

    # If it looks like a function call already, return it
    if "(" in desc and ")" in desc:
        return desc

    # Otherwise, convert to a TODO function call
    func_name = desc.lower().replace(" ", "_").replace("-", "_")
    # Keep only valid identifier characters
    func_name = re.sub(r'[^a-z0-9_]', '', func_name)
    return f"{func_name}()  # TODO: implement"


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

    # Direct expression returns (a + b, a × b, etc.)
    # Replace math symbols
    expr = returns.replace("×", "*").replace("÷", "/")

    # Check if it's a simple expression with known operators
    if re.match(r"^[a-z_][a-z0-9_]*\s*[\+\-\*\/]\s*[a-z_][a-z0-9_]*$", expr, re.IGNORECASE):
        return f"    return {expr}"

    # Check for function-like returns: "result with field1, field2"
    if " with " in returns.lower():
        # For now, just return a dict
        parts = returns.split(" with ", 1)
        return f'    # TODO: Return {parts[0]} with fields: {parts[1]}\n    return {{}}'

    # If raw logic is provided but no logic_steps, generate comments
    if anlu.logic:
        lines = ["    # Generated from LOGIC steps:"]
        for i, step in enumerate(anlu.logic, 1):
            lines.append(f"    # {i}. {step}")
        lines.append(f"    return {expr}")
        return "\n".join(lines)

    # If guards are provided, generate guard validation code
    if anlu.guards:
        lines = emit_guards(anlu)
        lines.append(f"    return {expr}")
        return "\n".join(lines)

    # Fallback: return the expression as-is if it looks like valid Python
    if expr and " " not in expr:
        return f"    return {expr}"

    # Last resort - return the expression
    return f"    return {expr}"


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


def emit_python(nl_file: NLFile, mode: str = "mock") -> str:
    """
    Emit complete Python module from NLFile.

    Args:
        nl_file: Parsed NLFile
        mode: Emission mode ("mock" or "llm")

    Returns:
        Complete Python source code
    """
    # Normalize path for cross-platform docstrings
    source_display = str(nl_file.source_path).replace("\\", "/") if nl_file.source_path else "unknown"
    lines = [
        f'"""',
        f"Generated by nlsc from {source_display}",
        f"Module: {nl_file.module.name}",
        f'"""',
        ""
    ]

    # Track imports to add
    imports_needed = []

    # Add dataclass import if types exist
    if nl_file.module.types:
        imports_needed.append("from dataclasses import dataclass")

    # Add type imports if needed
    has_any = any(
        "any" in (inp.type for inp in anlu.inputs)
        for anlu in nl_file.anlus
    )
    if has_any:
        imports_needed.append("from typing import Any")

    # Emit collected imports
    if imports_needed:
        for imp in imports_needed:
            lines.append(imp)
        lines.append("")

    # Add user-specified imports
    if nl_file.module.imports:
        for imp in nl_file.module.imports:
            lines.append(f"import {imp.strip()}")
        lines.append("")

    # Emit types first (before functions)
    if nl_file.module.types:
        # Order types: base types before derived types
        ordered_types = _order_types(nl_file.module.types)
        for type_def in ordered_types:
            lines.append("")
            lines.append(emit_type_definition(type_def))
            lines.append("")

    # Emit each ANLU in dependency order
    ordered = nl_file.dependency_order()
    for anlu in ordered:
        lines.append("")
        lines.append(emit_anlu(anlu, mode))
        lines.append("")

    # Add any literal blocks
    if nl_file.literals:
        lines.append("")
        lines.append("# --- Literal blocks ---")
        for literal in nl_file.literals:
            lines.append(literal)

    return "\n".join(lines)


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
        f'"""',
        f"Tests generated by nlsc from {source_display}",
        f'"""',
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
