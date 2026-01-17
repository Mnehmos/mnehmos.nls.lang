"""
NLS Atomize - Extract ANLUs from Python source code

Converts Python functions to NL specification format.
"""

import ast
from pathlib import Path
from typing import Any


# Python type to NL type mapping
TYPE_MAP = {
    "int": "number",
    "float": "number",
    "str": "string",
    "bool": "boolean",
    "None": "void",
    "list": "list",
    "dict": "dictionary",
    "Any": "any",
}


def python_type_to_nl(type_node: ast.expr | None) -> str:
    """
    Convert Python type annotation to NL type.

    Args:
        type_node: AST node representing the type annotation

    Returns:
        NL type string
    """
    if type_node is None:
        return "any"

    if isinstance(type_node, ast.Name):
        return TYPE_MAP.get(type_node.id, type_node.id)

    if isinstance(type_node, ast.Subscript):
        # Handle generic types like list[int]
        if isinstance(type_node.value, ast.Name):
            base_type = type_node.value.id.lower()
            if base_type == "list":
                inner_type = python_type_to_nl(type_node.slice)
                return f"list of {inner_type}"
            elif base_type == "dict":
                return "dictionary"
            elif base_type == "optional":
                inner_type = python_type_to_nl(type_node.slice)
                return f"{inner_type} or null"

    if isinstance(type_node, ast.Constant):
        if type_node.value is None:
            return "void"

    # Fallback: try to get the string representation
    return ast.unparse(type_node) if hasattr(ast, "unparse") else "any"


def extract_return_expression(func: ast.FunctionDef) -> str:
    """
    Extract the return expression from a function.

    For simple functions, returns the expression as a string.
    For complex functions, returns a placeholder.
    """
    # Find return statements
    for node in ast.walk(func):
        if isinstance(node, ast.Return) and node.value:
            # For simple expressions, return them directly
            try:
                expr = ast.unparse(node.value)
                # Only return simple expressions
                if len(expr) < 50 and "\n" not in expr:
                    return expr
            except Exception:
                pass

    # Fallback: use return type annotation
    if func.returns:
        return_type = python_type_to_nl(func.returns)
        return return_type

    return "result"


def snake_to_kebab(name: str) -> str:
    """Convert snake_case to kebab-case."""
    return name.replace("_", "-")


def extract_anlu_from_function(func: ast.FunctionDef) -> dict[str, Any]:
    """
    Extract ANLU specification from a Python function.

    Args:
        func: AST node for the function definition

    Returns:
        Dictionary with ANLU fields
    """
    # Get docstring
    docstring = ast.get_docstring(func)
    if docstring:
        # Use first line as purpose
        purpose = docstring.split("\n")[0].strip()
    else:
        # Generate purpose from function name
        words = func.name.replace("_", " ").title()
        purpose = f"{words} operation"

    # Extract inputs
    inputs = []
    for arg in func.args.args:
        if arg.arg == "self":
            continue

        input_def = {
            "name": arg.arg,
            "type": python_type_to_nl(arg.annotation),
        }
        inputs.append(input_def)

    # Extract return expression
    returns = extract_return_expression(func)

    return {
        "identifier": snake_to_kebab(func.name),
        "purpose": purpose,
        "inputs": inputs,
        "returns": returns,
    }


def atomize_python_file(code: str) -> list[dict[str, Any]]:
    """
    Extract ANLUs from Python source code.

    Args:
        code: Python source code as string

    Returns:
        List of ANLU dictionaries
    """
    tree = ast.parse(code)
    anlus = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Skip private functions
            if node.name.startswith("_"):
                continue

            anlu = extract_anlu_from_function(node)
            anlus.append(anlu)

    return anlus


def atomize_to_nl(code: str, module_name: str = "extracted") -> str:
    """
    Convert Python source code to NL specification.

    Args:
        code: Python source code
        module_name: Name for the generated module

    Returns:
        NL specification as string
    """
    anlus = atomize_python_file(code)

    lines = [
        f"@module {module_name}",
        "@target python",
        "",
    ]

    for anlu in anlus:
        lines.append(f"[{anlu['identifier']}]")
        lines.append(f"PURPOSE: {anlu['purpose']}")

        if anlu["inputs"]:
            lines.append("INPUTS:")
            for inp in anlu["inputs"]:
                lines.append(f"  - {inp['name']}: {inp['type']}")

        lines.append(f"RETURNS: {anlu['returns']}")
        lines.append("")

    return "\n".join(lines)


def atomize_file(source_path: Path, output_path: Path | None = None, module_name: str | None = None) -> str:
    """
    Atomize a Python file and optionally write to output.

    Args:
        source_path: Path to Python file
        output_path: Optional output path for .nl file
        module_name: Optional module name (defaults to stem)

    Returns:
        Generated NL content
    """
    code = source_path.read_text(encoding="utf-8")

    if module_name is None:
        module_name = source_path.stem.replace("_", "-")

    nl_content = atomize_to_nl(code, module_name)

    if output_path is None:
        output_path = source_path.with_suffix(".nl")

    output_path.write_text(nl_content, encoding="utf-8")

    return nl_content
