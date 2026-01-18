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


def extract_guards(func: ast.FunctionDef | ast.AsyncFunctionDef) -> list[dict[str, str]]:
    """
    Extract GUARDS from if/raise patterns at the start of function body.

    Patterns detected:
    - if not condition: raise Error("message")
    - if condition: raise Error("message")

    Returns list of dicts with 'condition', 'error_type', 'error_message'.
    """
    guards = []

    for node in func.body:
        # Skip docstring
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue

        # Look for if statements that raise exceptions
        if isinstance(node, ast.If):
            # Check if body is just a raise statement
            if len(node.body) == 1 and isinstance(node.body[0], ast.Raise):
                raise_node = node.body[0]

                # Extract condition (invert if it's a guard pattern)
                try:
                    condition = ast.unparse(node.test)
                except Exception:
                    continue

                # Convert "if not X" to guard "X"
                if isinstance(node.test, ast.UnaryOp) and isinstance(node.test.op, ast.Not):
                    # Guard is the positive condition
                    condition = ast.unparse(node.test.operand)
                else:
                    # Guard is the negation of the condition
                    # e.g., "if x < 0" -> guard is "x >= 0"
                    # For simplicity, we'll express it as "NOT (original)"
                    condition = f"NOT ({condition})"

                # Extract error type and message
                error_type = "ValueError"
                error_message = "Guard condition failed"

                if raise_node.exc:
                    if isinstance(raise_node.exc, ast.Call):
                        # Get error type name
                        if isinstance(raise_node.exc.func, ast.Name):
                            error_type = raise_node.exc.func.id

                        # Get error message from first argument
                        if raise_node.exc.args:
                            try:
                                msg_node = raise_node.exc.args[0]
                                if isinstance(msg_node, ast.Constant):
                                    error_message = str(msg_node.value)
                                else:
                                    error_message = ast.unparse(msg_node)
                            except Exception:
                                pass

                guards.append({
                    "condition": condition,
                    "error_type": error_type,
                    "error_message": error_message,
                })
            else:
                # Not a simple guard pattern, stop looking
                break
        elif isinstance(node, ast.Assign):
            # Assignments can come after guards, keep looking
            continue
        else:
            # Any other statement type means guards section is over
            break

    return guards


def extract_logic_steps(func: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    """
    Extract LOGIC steps from function body.

    Captures:
    - Assignments (x = expr)
    - Augmented assignments (x += expr)
    - Expression statements (method calls like obj.update(args))
    - For loops (FOR each X IN Y: body)

    Returns list of step strings.
    """
    logic_steps = []

    # Skip guards at the start (if/raise patterns)
    in_guards = True

    # Only look at direct children of the function body (not nested)
    for node in func.body:
        # Skip docstring
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue

        # Skip guard patterns
        if in_guards and isinstance(node, ast.If):
            if len(node.body) == 1 and isinstance(node.body[0], ast.Raise):
                continue
            else:
                in_guards = False

        # Any non-guard statement means we're past guards
        if isinstance(node, (ast.Assign, ast.AugAssign, ast.Expr, ast.For)):
            if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)):
                in_guards = False

        # Capture assignments
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    try:
                        expr = ast.unparse(node.value)
                        if len(expr) < 80:  # Keep it readable
                            logic_steps.append(f"{target.id} = {expr}")
                    except Exception:
                        pass

        # Capture augmented assignments (+=, -=, etc.)
        if isinstance(node, ast.AugAssign):
            if isinstance(node.target, ast.Name):
                try:
                    op_map = {
                        ast.Add: "+=", ast.Sub: "-=", ast.Mult: "*=",
                        ast.Div: "/=", ast.Mod: "%=", ast.FloorDiv: "//=",
                    }
                    op_str = op_map.get(type(node.op), "?=")
                    expr = ast.unparse(node.value)
                    if len(expr) < 60:
                        logic_steps.append(f"{node.target.id} {op_str} {expr}")
                except Exception:
                    pass

        # Capture expression statements (method calls like obj.method(args))
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            try:
                call_str = ast.unparse(node.value)
                if len(call_str) < 80:
                    logic_steps.append(call_str)
            except Exception:
                pass

        # Capture for loops
        if isinstance(node, ast.For):
            try:
                target = ast.unparse(node.target)  # type: ignore[assignment]
                iter_expr = ast.unparse(node.iter)
                # Extract the body as a simple statement if possible
                body_stmts = _extract_for_body(node.body)
                if body_stmts and len(iter_expr) < 40:
                    for stmt in body_stmts:
                        logic_steps.append(f"FOR each {target} IN {iter_expr}: {stmt}")
            except Exception:
                pass

        # Stop at return
        if isinstance(node, ast.Return):
            break

    return logic_steps


def _extract_for_body(body: list) -> list[str]:
    """Extract simple statements from a for loop body."""
    stmts = []
    for node in body:
        try:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                # Method call like result.extend(sublist)
                call_str = ast.unparse(node.value)
                if len(call_str) < 60:
                    stmts.append(call_str)
            elif isinstance(node, ast.Assign):
                # Assignment
                if isinstance(node.targets[0], ast.Name):
                    expr = ast.unparse(node.value)
                    if len(expr) < 60:
                        stmts.append(f"{node.targets[0].id} = {expr}")
            elif isinstance(node, ast.AugAssign):
                # Augmented assignment
                if isinstance(node.target, ast.Name):
                    op_map = {
                        ast.Add: "+=", ast.Sub: "-=", ast.Mult: "*=",
                        ast.Div: "/=", ast.Mod: "%=",
                    }
                    op_str = op_map.get(type(node.op), "?=")
                    expr = ast.unparse(node.value)
                    if len(expr) < 60:
                        stmts.append(f"{node.target.id} {op_str} {expr}")
        except Exception:
            pass
    return stmts


def extract_return_expression(func: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """
    Extract the return expression from a function.

    Handles:
    - Simple return statements
    - Conditional returns (if/else with returns in both branches)
    - Early returns with default follow-up
    - Try/except with returns (expresses as "X, or Y on ErrorType")

    For simple functions, returns the expression as a string.
    For conditional returns, expresses as "X if condition else Y".
    For try/except, expresses as "X, or Y on ErrorType".
    For complex functions, returns a placeholder.
    """
    # First, check for try/except pattern
    for node in func.body:
        # Skip docstring
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue

        if isinstance(node, ast.Try):
            try_return = _get_branch_return(node.body)
            if try_return and node.handlers:
                # Get the except handler return
                handler = node.handlers[0]
                except_return = _get_branch_return(handler.body)
                if except_return:
                    # Get error type name
                    error_type = "error"
                    if handler.type:
                        if isinstance(handler.type, ast.Name):
                            error_type = handler.type.id
                        elif isinstance(handler.type, ast.Attribute):
                            error_type = handler.type.attr
                        else:
                            try:
                                error_type = ast.unparse(handler.type)
                            except Exception:
                                pass

                    if len(try_return) < 40 and len(except_return) < 20:
                        return f"{try_return}, or {except_return} on {error_type}"
            break

    # Check for conditional return pattern in the function body
    for node in func.body:
        # Skip docstring
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue

        # Skip guard patterns (if/raise)
        if isinstance(node, ast.If):
            if len(node.body) == 1 and isinstance(node.body[0], ast.Raise):
                continue

            # Check for if/else with returns in both branches
            if_returns = _get_branch_return(node.body)
            else_returns = _get_branch_return(node.orelse) if node.orelse else None

            if if_returns and else_returns:
                # Express as conditional: "X if condition else Y"
                try:
                    condition = ast.unparse(node.test)
                    if len(if_returns) < 30 and len(else_returns) < 30 and len(condition) < 30:
                        return f"{if_returns} if {condition} else {else_returns}"
                except Exception:
                    pass

            # Early return with default follow-up
            if if_returns and not node.orelse:
                # Look for a return after this if block
                idx = func.body.index(node)
                for following in func.body[idx + 1:]:
                    if isinstance(following, ast.Return) and following.value:
                        try:
                            default_expr = ast.unparse(following.value)
                            condition = ast.unparse(node.test)
                            if len(if_returns) < 30 and len(default_expr) < 30 and len(condition) < 30:
                                return f"{if_returns} if {condition} else {default_expr}"
                        except Exception:
                            pass
                        break

    # Fallback: find any return statement
    for node in ast.walk(func):  # type: ignore[assignment]
        if isinstance(node, ast.Return) and node.value:
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


def _get_branch_return(body: list) -> str | None:
    """Get return expression from a branch body, if it's a simple return."""
    if len(body) == 1 and isinstance(body[0], ast.Return) and body[0].value:
        try:
            return ast.unparse(body[0].value)
        except Exception:
            pass
    return None


def snake_to_kebab(name: str) -> str:
    """Convert snake_case to kebab-case."""
    return name.replace("_", "-")


def extract_type_from_class(cls: ast.ClassDef) -> dict[str, Any] | None:
    """
    Extract type definition from a Python class (especially dataclasses).

    Args:
        cls: AST node for the class definition

    Returns:
        Dictionary with type fields, or None if not extractable
    """
    # Get docstring
    docstring = ast.get_docstring(cls)
    description = ""
    if docstring:
        description = docstring.split("\n")[0].strip()

    # Check if it's a dataclass (has @dataclass decorator)
    is_dataclass = False
    for decorator in cls.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id == "dataclass":
            is_dataclass = True
            break
        if isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name) and decorator.func.id == "dataclass":
                is_dataclass = True
                break

    # Extract fields from class body
    fields = []
    for node in cls.body:
        # Skip docstring
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue

        # Annotated assignment (field: type or field: type = default)
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                field_name = node.target.id
                field_type = python_type_to_nl(node.annotation)

                # Check for default value
                default = None
                if node.value:
                    try:
                        default = ast.unparse(node.value)
                    except Exception:
                        pass

                fields.append({
                    "name": field_name,
                    "type": field_type,
                    "default": default,
                })

    # Only extract classes with annotated fields (dataclasses or typed classes)
    if not fields:
        return None

    return {
        "name": cls.name,
        "description": description,
        "fields": fields,
        "is_dataclass": is_dataclass,
    }


def extract_anlu_from_function(func: ast.FunctionDef | ast.AsyncFunctionDef) -> dict[str, Any]:
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

    # Extract GUARDS (if/raise patterns)
    guards = extract_guards(func)

    # Extract LOGIC steps (intermediate assignments)
    logic_steps = extract_logic_steps(func)

    # Extract return expression
    returns = extract_return_expression(func)

    return {
        "identifier": snake_to_kebab(func.name),
        "purpose": purpose,
        "inputs": inputs,
        "guards": guards,
        "logic": logic_steps,
        "returns": returns,
    }


def atomize_python_file(code: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Extract ANLUs and type definitions from Python source code.

    Args:
        code: Python source code as string

    Returns:
        Tuple of (list of ANLU dictionaries, list of type definitions)
    """
    tree = ast.parse(code)
    anlus = []
    types = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Skip private functions
            if node.name.startswith("_"):
                continue

            anlu = extract_anlu_from_function(node)
            anlu["is_async"] = isinstance(node, ast.AsyncFunctionDef)
            anlus.append(anlu)

        if isinstance(node, ast.ClassDef):
            # Skip private classes
            if node.name.startswith("_"):
                continue

            type_def = extract_type_from_class(node)
            if type_def:
                types.append(type_def)

    return anlus, types


def atomize_to_nl(code: str, module_name: str = "extracted") -> str:
    """
    Convert Python source code to NL specification.

    Args:
        code: Python source code
        module_name: Name for the generated module

    Returns:
        NL specification as string
    """
    anlus, types = atomize_python_file(code)

    lines = [
        f"@module {module_name}",
        "@target python",
        "",
    ]

    # Output type definitions first
    for type_def in types:
        lines.append(f"@type {type_def['name']}")
        if type_def["description"]:
            lines.append(f"  # {type_def['description']}")
        for field in type_def["fields"]:
            field_str = f"  - {field['name']}: {field['type']}"
            if field["default"]:
                field_str += f" (default: {field['default']})"
            lines.append(field_str)
        lines.append("")

    for anlu in anlus:
        lines.append(f"[{anlu['identifier']}]")
        lines.append(f"PURPOSE: {anlu['purpose']}")

        if anlu.get("is_async"):
            lines.append("ASYNC: true")

        if anlu["inputs"]:
            lines.append("INPUTS:")
            for inp in anlu["inputs"]:
                lines.append(f"  - {inp['name']}: {inp['type']}")

        if anlu.get("guards"):
            lines.append("GUARDS:")
            for guard in anlu["guards"]:
                lines.append(f"  - {guard['condition']} | {guard['error_type']}: \"{guard['error_message']}\"")

        if anlu.get("logic"):
            lines.append("LOGIC:")
            for i, step in enumerate(anlu["logic"], 1):
                lines.append(f"  {i}. {step}")

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
