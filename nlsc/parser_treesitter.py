"""
NLS Tree-sitter Parser - Parse .nl files using tree-sitter grammar

This module provides an alternative parser implementation using tree-sitter
for more robust parsing with better error recovery.

See: https://github.com/tree-sitter/py-tree-sitter/discussions/251
"""

import re
import sys
from ctypes import cdll, c_void_p
from pathlib import Path
from typing import Optional

try:
    from tree_sitter import Language, Parser, Node
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False
    Language = None
    Parser = None
    Node = None

from .schema import (
    ANLU, Module, NLFile, Input, Guard, EdgeCase,
    TestSuite, TestCase, TypeDefinition, TypeField, LogicStep,
    PropertyTest, PropertyAssertion, Invariant
)
from .parser import ParseError


# =============================================================================
# REGEX FALLBACK FOR BLOCKS NOT IN TREE-SITTER GRAMMAR
# =============================================================================
# Tree-sitter grammar doesn't support @property, @invariant, @main blocks yet.
# These are parsed using simple regex patterns for feature parity with regex parser.

def _parse_property_blocks(source: str) -> list[PropertyTest]:
    """Parse @property blocks using regex fallback."""
    properties = []
    current_property = None

    for line in source.split("\n"):
        stripped = line.strip()

        # Start of @property block
        if stripped.startswith("@property"):
            prop_match = re.match(r"@property\s+\[([a-z][a-z0-9-]*)\]\s*\{?", stripped)
            if prop_match:
                current_property = PropertyTest(anlu_id=prop_match.group(1))
                properties.append(current_property)
            continue

        # Inside property block
        if current_property:
            if stripped == "}":
                current_property = None
            elif stripped and not stripped.startswith("#"):
                # Remove trailing comments
                if "#" in stripped:
                    stripped = stripped.split("#")[0].strip()
                if stripped:
                    # Check for forall quantifier: forall x: type -> assertion
                    forall_match = re.match(r"forall\s+(\w+):\s*(\w+)\s*->\s*(.+)", stripped)
                    if forall_match:
                        current_property.assertions.append(PropertyAssertion(
                            expression=forall_match.group(3).strip(),
                            quantifier="forall",
                            variable=forall_match.group(1),
                            variable_type=forall_match.group(2)
                        ))
                    else:
                        # Simple property assertion
                        current_property.assertions.append(PropertyAssertion(
                            expression=stripped
                        ))

    return properties


def _parse_invariant_blocks(source: str) -> list[Invariant]:
    """Parse @invariant blocks using regex fallback."""
    invariants = []
    current_invariant = None

    for line in source.split("\n"):
        stripped = line.strip()

        # Start of @invariant block
        if stripped.startswith("@invariant"):
            inv_match = re.match(r"@invariant\s+([A-Z][a-zA-Z0-9]*)\s*\{?", stripped)
            if inv_match:
                current_invariant = Invariant(type_name=inv_match.group(1))
                invariants.append(current_invariant)
            continue

        # Inside invariant block
        if current_invariant:
            if stripped == "}":
                current_invariant = None
            elif stripped and not stripped.startswith("#"):
                current_invariant.conditions.append(stripped)

    return invariants


def _parse_main_block(source: str) -> list[str]:
    """Parse @main block using regex fallback.

    Tracks brace depth to handle nested braces correctly.
    """
    main_buffer = []
    in_main = False
    brace_depth = 0

    for line in source.split("\n"):
        stripped = line.strip()

        # Start of @main block
        if stripped.startswith("@main"):
            in_main = True
            # Check if opening brace is on same line
            if "{" in stripped:
                brace_depth = 1
            continue

        # Inside main block
        if in_main:
            # Count braces in this line
            open_braces = stripped.count("{")
            close_braces = stripped.count("}")

            # Update depth before processing
            brace_depth += open_braces - close_braces

            # Block ends when depth reaches 0
            if brace_depth <= 0:
                in_main = False
            elif stripped and not stripped.startswith("#"):
                main_buffer.append(stripped)

    return main_buffer


# Path to the tree-sitter-nl grammar
GRAMMAR_PATH = Path(__file__).parent.parent / "tree-sitter-nl"

# Platform-specific library extension
if sys.platform == "win32":
    LANGUAGE_LIB_PATH = GRAMMAR_PATH / "build" / "nl.dll"
elif sys.platform == "darwin":
    LANGUAGE_LIB_PATH = GRAMMAR_PATH / "build" / "nl.dylib"
else:
    LANGUAGE_LIB_PATH = GRAMMAR_PATH / "build" / "nl.so"


_nl_language = None
_parser = None


def _load_language_from_lib(lib_path: Path, lang_name: str) -> "Language":
    """
    Load a tree-sitter Language from a compiled shared library.

    For tree-sitter 0.22+, we need to manually load the library and
    get the language function pointer using ctypes.
    """
    lib = cdll.LoadLibrary(str(lib_path))
    language_func = getattr(lib, f"tree_sitter_{lang_name}")
    language_func.restype = c_void_p
    language_ptr = language_func()
    return Language(language_ptr)


def _get_parser() -> "Parser":
    """Get or create the tree-sitter parser for NL."""
    global _nl_language, _parser

    if not TREE_SITTER_AVAILABLE:
        raise ImportError(
            "tree-sitter is not installed. "
            "Install with: pip install nlsc[treesitter]"
        )

    if _parser is not None:
        return _parser

    # Check if the language library exists
    if not LANGUAGE_LIB_PATH.exists():
        raise FileNotFoundError(
            f"Tree-sitter NL language library not found at {LANGUAGE_LIB_PATH}. "
            f"Build it with: cd tree-sitter-nl && npx tree-sitter build -o build/nl.dll"
        )

    # Load the language from compiled library
    _nl_language = _load_language_from_lib(LANGUAGE_LIB_PATH, "nl")
    _parser = Parser()
    _parser.language = _nl_language

    return _parser


def _get_child_by_field(node: "Node", field_name: str) -> Optional["Node"]:
    """Get a child node by field name."""
    return node.child_by_field_name(field_name)


def _get_children_by_type(node: "Node", type_name: str) -> list["Node"]:
    """Get all children of a specific type."""
    return [child for child in node.children if child.type == type_name]


def _get_text(node: "Node", source: bytes) -> str:
    """Extract text content from a node."""
    return source[node.start_byte:node.end_byte].decode("utf-8")


def _parse_type_spec(node: "Node", source: bytes) -> str:
    """Parse a type_spec node into a type string."""
    result = []

    for child in node.children:
        if child.type == "primitive_type":
            result.append(_get_text(child, source))
        elif child.type == "list_type":
            element = _get_child_by_field(child, "element")
            if element:
                inner_type = _parse_type_spec_inner(element, source)
                result.append(f"list of {inner_type}")
        elif child.type == "map_type":
            key = _get_child_by_field(child, "key")
            value = _get_child_by_field(child, "value")
            if key and value:
                key_type = _parse_type_spec_inner(key, source)
                value_type = _parse_type_spec_inner(value, source)
                result.append(f"map of {key_type} to {value_type}")
        elif child.type == "custom_type":
            type_name = _get_children_by_type(child, "type_name")
            if type_name:
                result.append(_get_text(type_name[0], source))
        elif child.type == "?":
            result.append("?")

    return "".join(result)


def _parse_type_spec_inner(node: "Node", source: bytes) -> str:
    """Parse inner type for list/map (primitive_type, custom_type, etc.)."""
    if node.type == "primitive_type":
        return _get_text(node, source)
    elif node.type == "custom_type":
        type_name = _get_children_by_type(node, "type_name")
        if type_name:
            return _get_text(type_name[0], source)
    elif node.type == "type_spec":
        return _parse_type_spec(node, source)
    return _get_text(node, source)


def _parse_input_item(node: "Node", source: bytes) -> Input:
    """Parse an input_item node into an Input object."""
    name_node = _get_child_by_field(node, "name")
    type_node = _get_child_by_field(node, "type")

    name = _get_text(name_node, source) if name_node else "unknown"
    type_str = _parse_type_spec(type_node, source) if type_node else "any"

    # Parse constraints
    constraints = []
    description = None

    constraint_nodes = _get_children_by_type(node, "input_constraints")
    for constraint_node in constraint_nodes:
        for child in constraint_node.children:
            if child.type == "quoted_string":
                text = _get_text(child, source)
                description = text[1:-1]  # Remove quotes
            elif child.type in ("identifier", "required", "optional"):
                text = _get_text(child, source)
                if text not in (",",):
                    constraints.append(text)

    return Input(
        name=name,
        type=type_str,
        constraints=constraints,
        description=description
    )


def _parse_guard_item(node: "Node", source: bytes) -> Guard:
    """Parse a guard_item node into a Guard object."""
    condition_node = _get_child_by_field(node, "condition")
    error_node = _get_child_by_field(node, "error")

    condition = _get_text(condition_node, source).strip() if condition_node else ""

    error_type = None
    error_code = None
    error_message = None

    if error_node:
        if error_node.type == "error_spec":
            # Check for error_call or error_text
            for child in error_node.children:
                if child.type == "error_call":
                    type_node = _get_child_by_field(child, "type")
                    if type_node:
                        error_type = _get_text(type_node, source)

                    args_node = _get_children_by_type(child, "error_args")
                    if args_node:
                        args = []
                        for arg_child in args_node[0].children:
                            if arg_child.type in ("identifier", "quoted_string"):
                                args.append(_get_text(arg_child, source))

                        if len(args) >= 2:
                            error_code = args[0]
                            error_message = args[1].strip('"\'')
                        elif len(args) == 1:
                            msg = args[0]
                            if msg.startswith('"') or msg.startswith("'"):
                                error_message = msg.strip('"\'')
                            else:
                                error_message = msg

                elif child.type == "error_text":
                    # Parse error text like "ValueError("Division by zero")"
                    text = _get_text(child, source).strip()
                    # Try to parse as function call
                    match = re.match(r'(\w+)\(([^,]+),\s*"([^"]+)"\)', text)
                    if match:
                        error_type = match.group(1)
                        error_code = match.group(2)
                        error_message = match.group(3)
                    else:
                        match = re.match(r'(\w+)\("([^"]+)"\)', text)
                        if match:
                            error_type = match.group(1)
                            error_message = match.group(2)
                        else:
                            error_message = text

    return Guard(
        condition=condition,
        error_type=error_type,
        error_code=error_code,
        error_message=error_message
    )


def _extract_variables(expression: str) -> list[str]:
    """Extract variable names from an expression."""
    # Remove string literals
    expression = re.sub(r'"[^"]*"', '', expression)
    expression = re.sub(r"'[^']*'", '', expression)

    tokens = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', expression)

    keywords = {
        'True', 'False', 'None', 'and', 'or', 'not', 'in', 'is',
        'if', 'else', 'for', 'while', 'return', 'def', 'class',
        'sum', 'len', 'min', 'max', 'abs', 'round', 'int', 'float', 'str',
        'list', 'dict', 'set', 'tuple', 'range', 'enumerate', 'zip',
        'IF', 'THEN', 'ELSE', 'AND', 'OR', 'NOT'
    }

    return [t for t in tokens if t not in keywords]


def _parse_logic_item(node: "Node", source: bytes, previous_assigns: dict[str, int]) -> LogicStep:
    """Parse a logic_item node into a LogicStep object."""
    number_node = _get_child_by_field(node, "number")
    number = int(_get_text(number_node, source)) if number_node else 0

    # Find the logic_step child
    logic_step_node = None
    for child in node.children:
        if child.type == "logic_step":
            logic_step_node = child
            break

    if not logic_step_node:
        return LogicStep(number=number, description="")

    # Extract components
    state_name = None
    condition = None
    output_binding = None
    description = ""

    for child in logic_step_node.children:
        if child.type == "state_prefix":
            state_node = _get_child_by_field(child, "state")
            if state_node:
                state_name = _get_text(state_node, source)
        elif child.type == "condition_prefix":
            # Extract condition text
            condition_text_node = _get_children_by_type(child, "condition_text")
            if condition_text_node:
                condition = _get_text(condition_text_node[0], source).strip()
        elif child.type == "step_text":
            desc_text = _get_text(child, source).strip()
            if desc_text:
                description = desc_text
        elif child.type == "output_binding":
            var_node = _get_child_by_field(child, "variable")
            if var_node:
                output_binding = _get_text(var_node, source)

    # Build full description for compatibility
    full_description = description

    # Parse assigns and uses
    assigns = []
    uses = []

    # Output binding is an assignment
    if output_binding:
        assigns.append(output_binding)

    # Check for inline assignment (var = expr)
    assignment_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$', description)
    if assignment_match:
        var_name = assignment_match.group(1)
        expr = assignment_match.group(2)
        if var_name not in assigns:
            assigns.append(var_name)
        uses.extend(_extract_variables(expr))
    else:
        uses.extend(_extract_variables(description))

    # Extract variables from condition
    if condition:
        uses.extend(_extract_variables(condition))

    # Deduplicate uses
    seen = set()
    unique_uses = []
    for var in uses:
        if var not in seen and var not in assigns:
            seen.add(var)
            unique_uses.append(var)
    uses = unique_uses

    # Build dependencies
    depends_on = []
    for var in uses:
        if var in previous_assigns:
            step_num = previous_assigns[var]
            if step_num not in depends_on:
                depends_on.append(step_num)
    depends_on.sort()

    return LogicStep(
        number=number,
        description=full_description,
        assigns=assigns,
        uses=uses,
        depends_on=depends_on,
        state_name=state_name,
        output_binding=output_binding,
        condition=condition
    )


def _parse_edge_case_item(node: "Node", source: bytes) -> EdgeCase:
    """Parse an edge_case_item node into an EdgeCase object."""
    condition_node = _get_child_by_field(node, "condition")
    behavior_node = _get_child_by_field(node, "behavior")

    condition = _get_text(condition_node, source).strip() if condition_node else ""
    behavior = _get_text(behavior_node, source).strip() if behavior_node else ""

    return EdgeCase(condition=condition, behavior=behavior)


def _parse_type_field(node: "Node", source: bytes) -> TypeField:
    """Parse a type_field node into a TypeField object."""
    name_node = _get_child_by_field(node, "name")
    type_node = _get_child_by_field(node, "type")

    name = _get_text(name_node, source) if name_node else "unknown"
    type_str = _parse_type_spec(type_node, source) if type_node else "any"

    constraints = []
    description = None

    constraint_nodes = _get_children_by_type(node, "field_constraints")
    for constraint_node in constraint_nodes:
        for child in constraint_node.children:
            if child.type == "quoted_string":
                text = _get_text(child, source)
                description = text[1:-1]
            elif child.type in ("identifier", "required", "optional"):
                text = _get_text(child, source)
                if text not in (",",):
                    constraints.append(text)

    return TypeField(
        name=name,
        type=type_str,
        constraints=constraints,
        description=description
    )


def _parse_test_assertion(node: "Node", source: bytes) -> TestCase:
    """Parse a test_assertion node into a TestCase object."""
    call_node = _get_child_by_field(node, "call")
    expected_node = _get_child_by_field(node, "expected")

    expression = _get_text(call_node, source).strip() if call_node else ""
    expected = ""

    if expected_node:
        # test_value wraps the actual value
        for child in expected_node.children:
            if child.type in ("number", "quoted_string", "boolean", "identifier"):
                expected = _get_text(child, source)
                break
        if not expected:
            expected = _get_text(expected_node, source)

    return TestCase(expression=expression, expected=expected)


def _parse_anlu_block(node: "Node", source: bytes) -> ANLU:
    """Parse an anlu_block node into an ANLU object."""
    # Get header
    header = _get_children_by_type(node, "anlu_header")
    identifier = ""
    line_number = node.start_point[0] + 1

    if header:
        name_node = _get_child_by_field(header[0], "name")
        if name_node:
            identifier = _get_text(name_node, source)

    purpose = ""
    returns = ""
    inputs = []
    guards = []
    logic = []
    logic_steps = []
    edge_cases = []
    depends = []

    # Track assignments for dataflow
    logic_assigns: dict[str, int] = {}

    # Parse sections
    for child in node.children:
        if child.type == "purpose_section":
            desc_node = _get_child_by_field(child, "description")
            if desc_node:
                purpose = _get_text(desc_node, source).strip()

        elif child.type == "inputs_section":
            for item in _get_children_by_type(child, "input_item"):
                inputs.append(_parse_input_item(item, source))

        elif child.type == "guards_section":
            for item in _get_children_by_type(child, "guard_item"):
                guards.append(_parse_guard_item(item, source))

        elif child.type == "logic_section":
            for item in _get_children_by_type(child, "logic_item"):
                step = _parse_logic_item(item, source, logic_assigns)
                logic_steps.append(step)
                logic.append(step.description)
                # Update assigns tracker
                for var in step.assigns:
                    logic_assigns[var] = step.number

        elif child.type == "returns_section":
            value_node = _get_child_by_field(child, "value")
            if value_node:
                returns = _get_text(value_node, source).strip()

        elif child.type == "depends_section":
            deps_node = _get_child_by_field(child, "dependencies")
            if deps_node:
                for ref in _get_children_by_type(deps_node, "anlu_reference"):
                    ref_text = _get_text(ref, source).strip()
                    depends.append(ref_text)

        elif child.type == "edge_cases_section":
            for item in _get_children_by_type(child, "edge_case_item"):
                edge_cases.append(_parse_edge_case_item(item, source))

    return ANLU(
        identifier=identifier,
        purpose=purpose,
        returns=returns,
        inputs=inputs,
        guards=guards,
        logic=logic,
        logic_steps=logic_steps,
        edge_cases=edge_cases,
        depends=depends,
        line_number=line_number
    )


def _parse_type_block(node: "Node", source: bytes) -> TypeDefinition:
    """Parse a type_block node into a TypeDefinition object."""
    header = _get_children_by_type(node, "type_header")

    name = ""
    base = None
    line_number = node.start_point[0] + 1

    if header:
        name_node = _get_child_by_field(header[0], "name")
        if name_node:
            name = _get_text(name_node, source)

        extends = _get_children_by_type(header[0], "extends_clause")
        if extends:
            base_node = _get_child_by_field(extends[0], "base")
            if base_node:
                base = _get_text(base_node, source)

    fields = []
    for field_node in _get_children_by_type(node, "type_field"):
        fields.append(_parse_type_field(field_node, source))

    return TypeDefinition(
        name=name,
        fields=fields,
        base=base,
        line_number=line_number
    )


def _parse_test_block(node: "Node", source: bytes) -> TestSuite:
    """Parse a test_block node into a TestSuite object."""
    header = _get_children_by_type(node, "test_header")

    anlu_id = ""
    if header:
        anlu_node = _get_child_by_field(header[0], "anlu")
        if anlu_node:
            anlu_id = _get_text(anlu_node, source)

    cases = []
    for assertion in _get_children_by_type(node, "test_assertion"):
        cases.append(_parse_test_assertion(assertion, source))

    return TestSuite(anlu_id=anlu_id, cases=cases)


def _parse_literal_block(node: "Node", source: bytes) -> str:
    """Parse a literal_block node and return its content."""
    content_node = _get_child_by_field(node, "content")
    if content_node:
        return _get_text(content_node, source)
    return ""


def parse_nl_file_treesitter(source: str, source_path: Optional[str] = None) -> NLFile:
    """
    Parse a .nl file source string into an NLFile AST using tree-sitter.

    Args:
        source: The .nl file contents as a string
        source_path: Optional path to the source file (for error messages)

    Returns:
        NLFile with parsed module info and ANLUs
    """
    parser = _get_parser()
    source_bytes = source.encode("utf-8")
    tree = parser.parse(source_bytes)

    root = tree.root_node

    # Initialize module with defaults
    module = Module(name="unnamed")
    anlus = []
    tests = []
    literals = []

    # Process top-level nodes
    for child in root.children:
        if child.type == "directive":
            # Process directives
            for directive_child in child.children:
                if directive_child.type == "module_directive":
                    name_node = _get_child_by_field(directive_child, "name")
                    if name_node:
                        module.name = _get_text(name_node, source_bytes)

                elif directive_child.type == "version_directive":
                    version_node = _get_child_by_field(directive_child, "version")
                    if version_node:
                        module.version = _get_text(version_node, source_bytes)

                elif directive_child.type == "target_directive":
                    target_node = _get_child_by_field(directive_child, "target")
                    if target_node:
                        module.target = _get_text(target_node, source_bytes)

                elif directive_child.type == "imports_directive":
                    imports_node = _get_child_by_field(directive_child, "imports")
                    if imports_node:
                        imports = []
                        for import_child in imports_node.children:
                            if import_child.type == "identifier":
                                imports.append(_get_text(import_child, source_bytes))
                        module.imports = imports

        elif child.type == "anlu_block":
            anlus.append(_parse_anlu_block(child, source_bytes))

        elif child.type == "type_block":
            module.types.append(_parse_type_block(child, source_bytes))

        elif child.type == "test_block":
            tests.append(_parse_test_block(child, source_bytes))

        elif child.type == "literal_block":
            literals.append(_parse_literal_block(child, source_bytes))

    # Parse blocks not supported by tree-sitter grammar using regex fallback
    properties = _parse_property_blocks(source)
    invariants = _parse_invariant_blocks(source)
    main_block = _parse_main_block(source)

    return NLFile(
        module=module,
        anlus=anlus,
        tests=tests,
        properties=properties,
        invariants=invariants,
        literals=literals,
        main_block=main_block,
        source_path=source_path
    )


def parse_nl_path_treesitter(path: Path) -> NLFile:
    """Parse a .nl file from a filesystem path using tree-sitter."""
    if not path.exists():
        raise ParseError(f"File not found: {path}")
    if not path.suffix == ".nl":
        raise ParseError(f"Expected .nl file, got: {path.suffix}")

    source = path.read_text(encoding="utf-8")
    return parse_nl_file_treesitter(source, source_path=str(path))


def is_available() -> bool:
    """Check if tree-sitter parser is available.

    Returns True only if both:
    1. tree-sitter Python module is installed
    2. Compiled NL grammar library exists
    """
    return TREE_SITTER_AVAILABLE and LANGUAGE_LIB_PATH.exists()
