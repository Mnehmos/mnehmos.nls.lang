"""
NLS Parser - Parse .nl files into AST structures

Converts Natural Language Source files into structured ANLU objects.
Uses regex-based parsing for V0 (sufficient for math example).
"""

import re
from pathlib import Path
from typing import Optional

from .schema import ANLU, Module, NLFile, Input, Guard, EdgeCase, TestSuite, TestCase, TypeDefinition, TypeField, LogicStep


class ParseError(Exception):
    """Error during .nl file parsing"""
    def __init__(self, message: str, line_number: int = 0, line_content: str = ""):
        self.line_number = line_number
        self.line_content = line_content
        super().__init__(f"Line {line_number}: {message}")


# Regex patterns for parsing
PATTERNS = {
    "anlu_header": re.compile(r"^\[([A-Za-z][A-Za-z0-9.-]*)\]\s*$"),
    "directive": re.compile(r"^@(module|version|target|imports|types|type|test|literal)\s*(.*)$"),
    "purpose": re.compile(r"^PURPOSE:\s*(.+)$", re.IGNORECASE),
    "inputs": re.compile(r"^INPUTS:\s*$", re.IGNORECASE),
    "guards": re.compile(r"^GUARDS:\s*$", re.IGNORECASE),
    "logic": re.compile(r"^LOGIC:\s*$", re.IGNORECASE),
    "returns": re.compile(r"^RETURNS:\s*(.+)$", re.IGNORECASE),
    "edge_cases": re.compile(r"^EDGE\s*CASES:\s*$", re.IGNORECASE),
    "depends": re.compile(r"^DEPENDS:\s*(.+)$", re.IGNORECASE),
    "bullet": re.compile(r"^\s*[•\-\*]\s*(.+)$"),
    "numbered": re.compile(r"^\s*(\d+)\.\s*(.+)$"),
    "comment": re.compile(r"^\s*#.*$"),
    "empty": re.compile(r"^\s*$"),
    "indented_field": re.compile(r"^\s+(\w+)\s*:\s*(.+)$"),
}


def parse_input(text: str) -> Input:
    """
    Parse an input line like:
    • a: number
    • token: string, required, "The JWT to validate"
    """
    # Split on first colon
    if ":" not in text:
        return Input(name=text.strip(), type="any")
    
    name, rest = text.split(":", 1)
    name = name.strip()
    rest = rest.strip()
    
    # Parse type and optional constraints/description
    parts = [p.strip() for p in rest.split(",")]
    type_spec = parts[0] if parts else "any"
    constraints = []
    description = None
    
    for part in parts[1:]:
        if part.startswith('"') and part.endswith('"'):
            description = part[1:-1]
        else:
            constraints.append(part)
    
    return Input(
        name=name,
        type=type_spec,
        constraints=constraints,
        description=description
    )


def parse_guard(text: str) -> Guard:
    """
    Parse a guard line like:
    • token must not be empty → AuthError(MISSING, "Token required")
    """
    # Split on arrow
    if "→" in text:
        condition, error_part = text.split("→", 1)
    elif "->" in text:
        condition, error_part = text.split("->", 1)
    else:
        return Guard(condition=text.strip())
    
    condition = condition.strip()
    error_part = error_part.strip()
    
    # Parse error specification like AuthError(MISSING, "Token required")
    error_match = re.match(r"(\w+)\(([^,]+),\s*\"([^\"]+)\"\)", error_part)
    if error_match:
        return Guard(
            condition=condition,
            error_type=error_match.group(1),
            error_code=error_match.group(2),
            error_message=error_match.group(3)
        )
    
    return Guard(condition=condition, error_message=error_part)


def parse_type_field(text: str) -> TypeField:
    """
    Parse a type field line like:
    • name: string
    • age: number, "Person's age in years"
    • items: list of string, required
    """
    # Split on first colon
    if ":" not in text:
        return TypeField(name=text.strip(), type="any")

    name, rest = text.split(":", 1)
    name = name.strip()
    rest = rest.strip()

    # Parse type and optional constraints/description
    parts = [p.strip() for p in rest.split(",")]
    type_spec = parts[0] if parts else "any"
    constraints = []
    description = None

    for part in parts[1:]:
        if part.startswith('"') and part.endswith('"'):
            description = part[1:-1]
        else:
            constraints.append(part)

    return TypeField(
        name=name,
        type=type_spec,
        constraints=constraints,
        description=description
    )


def extract_variables(expression: str) -> list[str]:
    """
    Extract variable names from an expression.
    Excludes literals, operators, and function names.
    """
    # Remove string literals
    expression = re.sub(r'"[^"]*"', '', expression)
    expression = re.sub(r"'[^']*'", '', expression)

    # Find all word tokens
    tokens = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', expression)

    # Filter out common keywords, functions, and literals
    keywords = {
        'True', 'False', 'None', 'and', 'or', 'not', 'in', 'is',
        'if', 'else', 'for', 'while', 'return', 'def', 'class',
        'sum', 'len', 'min', 'max', 'abs', 'round', 'int', 'float', 'str',
        'list', 'dict', 'set', 'tuple', 'range', 'enumerate', 'zip',
        'IF', 'THEN', 'ELSE', 'AND', 'OR', 'NOT'
    }

    return [t for t in tokens if t not in keywords]


def parse_logic_step(number: int, text: str, previous_assigns: dict[str, int]) -> LogicStep:
    """
    Parse a LOGIC step line, extracting assignment and variable usage.

    Args:
        number: Step number (1-indexed)
        text: The step description
        previous_assigns: Map of variable name -> step number that assigned it

    Returns:
        LogicStep with dataflow information
    """
    assigns = []
    uses = []
    depends_on = []

    # Check for assignment pattern: var = expression
    assignment_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$', text.strip())

    if assignment_match:
        var_name = assignment_match.group(1)
        expression = assignment_match.group(2)
        assigns = [var_name]
        uses = extract_variables(expression)
    else:
        # No assignment - just extract any variables mentioned
        uses = extract_variables(text)

    # Build dependencies based on which previous steps assigned variables we use
    for var in uses:
        if var in previous_assigns:
            step_num = previous_assigns[var]
            if step_num not in depends_on:
                depends_on.append(step_num)

    depends_on.sort()

    return LogicStep(
        number=number,
        description=text.strip(),
        assigns=assigns,
        uses=uses,
        depends_on=depends_on
    )


def parse_edge_case(text: str) -> EdgeCase:
    """
    Parse an edge case line like:
    • Zero income → zero tax
    """
    if "→" in text:
        condition, behavior = text.split("→", 1)
    elif "->" in text:
        condition, behavior = text.split("->", 1)
    else:
        return EdgeCase(condition=text.strip(), behavior="")
    
    return EdgeCase(
        condition=condition.strip(),
        behavior=behavior.strip()
    )


def parse_nl_file(source: str, source_path: Optional[str] = None) -> NLFile:
    """
    Parse a .nl file source string into an NLFile AST.
    
    Args:
        source: The .nl file contents as a string
        source_path: Optional path to the source file (for error messages)
    
    Returns:
        NLFile with parsed module info and ANLUs
    """
    lines = source.split("\n")
    
    # Initialize module with defaults
    module = Module(name="unnamed")
    anlus: list[ANLU] = []
    tests: list[TestSuite] = []
    literals: list[str] = []
    
    # Current parsing state
    current_anlu: Optional[ANLU] = None
    current_section: Optional[str] = None  # inputs, guards, logic, edge_cases
    current_test: Optional[TestSuite] = None
    current_type: Optional[TypeDefinition] = None
    in_literal_block = False
    literal_lang = ""
    literal_buffer: list[str] = []
    brace_depth = 0
    # Track variable assignments for dataflow analysis
    logic_assigns: dict[str, int] = {}
    
    for line_num, line in enumerate(lines, start=1):
        # Handle literal blocks
        if in_literal_block:
            if "{" in line:
                brace_depth += line.count("{")
            if "}" in line:
                brace_depth -= line.count("}")
                if brace_depth <= 0:
                    # End of literal block
                    literals.append("\n".join(literal_buffer))
                    in_literal_block = False
                    literal_buffer = []
                    continue
            literal_buffer.append(line)
            continue
        
        # Skip comments and empty lines (unless in a section)
        if PATTERNS["comment"].match(line):
            continue
        if PATTERNS["empty"].match(line) and current_section is None:
            continue
        
        # Check for directives
        directive_match = PATTERNS["directive"].match(line)
        if directive_match:
            directive_type = directive_match.group(1)
            directive_value = directive_match.group(2).strip()
            
            if directive_type == "module":
                module.name = directive_value
            elif directive_type == "version":
                module.version = directive_value
            elif directive_type == "target":
                module.target = directive_value
            elif directive_type == "imports":
                module.imports = [i.strip() for i in directive_value.split(",")]
            elif directive_type == "literal":
                # Start literal block
                in_literal_block = True
                brace_depth = 1 if "{" in line else 0
                literal_lang = directive_value.split("{")[0].strip()
            elif directive_type == "test":
                # Parse test header like: @test [add] {
                test_match = re.match(r"\[([a-z][a-z0-9-]*)\]\s*\{?", directive_value)
                if test_match:
                    current_test = TestSuite(anlu_id=test_match.group(1))
                    tests.append(current_test)
            elif directive_type == "type":
                # Parse type header like: @type Person {
                # or @type Person extends Entity {
                type_match = re.match(r"([A-Z][a-zA-Z0-9]*)\s*(?:extends\s+([A-Z][a-zA-Z0-9]*))?\s*\{?", directive_value)
                if type_match:
                    current_type = TypeDefinition(
                        name=type_match.group(1),
                        base=type_match.group(2),
                        line_number=line_num
                    )
                    module.types.append(current_type)

            # Save current ANLU if switching context
            if current_anlu and directive_type in ("module", "literal", "test", "type"):
                current_section = None
            continue
        
        # Check for ANLU header
        anlu_match = PATTERNS["anlu_header"].match(line)
        if anlu_match:
            # Save previous ANLU
            if current_anlu:
                anlus.append(current_anlu)

            # Start new ANLU
            current_anlu = ANLU(
                identifier=anlu_match.group(1),
                purpose="",
                returns="",
                line_number=line_num
            )
            # Reset dataflow tracking for new ANLU
            logic_assigns = {}
            current_section = None
            continue
        
        # Parse ANLU fields
        if current_anlu:
            # PURPOSE:
            purpose_match = PATTERNS["purpose"].match(line)
            if purpose_match:
                current_anlu.purpose = purpose_match.group(1).strip()
                current_section = None
                continue
            
            # INPUTS:
            if PATTERNS["inputs"].match(line):
                current_section = "inputs"
                continue
            
            # GUARDS:
            if PATTERNS["guards"].match(line):
                current_section = "guards"
                continue
            
            # LOGIC:
            if PATTERNS["logic"].match(line):
                current_section = "logic"
                continue
            
            # EDGE CASES:
            if PATTERNS["edge_cases"].match(line):
                current_section = "edge_cases"
                continue
            
            # RETURNS:
            returns_match = PATTERNS["returns"].match(line)
            if returns_match:
                current_anlu.returns = returns_match.group(1).strip()
                current_section = None
                continue
            
            # DEPENDS:
            depends_match = PATTERNS["depends"].match(line)
            if depends_match:
                deps = depends_match.group(1).strip()
                current_anlu.depends = [d.strip() for d in deps.split(",")]
                current_section = None
                continue
            
            # Parse section content
            if current_section:
                # Bullet point
                bullet_match = PATTERNS["bullet"].match(line)
                if bullet_match:
                    content = bullet_match.group(1)
                    if current_section == "inputs":
                        current_anlu.inputs.append(parse_input(content))
                    elif current_section == "guards":
                        current_anlu.guards.append(parse_guard(content))
                    elif current_section == "edge_cases":
                        current_anlu.edge_cases.append(parse_edge_case(content))
                    continue
                
                # Numbered item (for LOGIC)
                numbered_match = PATTERNS["numbered"].match(line)
                if numbered_match:
                    if current_section == "logic":
                        step_num = int(numbered_match.group(1))
                        step_text = numbered_match.group(2)
                        # Keep raw logic for backwards compatibility
                        current_anlu.logic.append(step_text)
                        # Parse with dataflow extraction
                        logic_step = parse_logic_step(step_num, step_text, logic_assigns)
                        current_anlu.logic_steps.append(logic_step)
                        # Update assigns tracker
                        for var in logic_step.assigns:
                            logic_assigns[var] = step_num
                    continue
        
        # Parse type fields
        if current_type:
            # Check for closing brace
            if line.strip() == "}":
                current_type = None
                continue

            # Bullet point field
            bullet_match = PATTERNS["bullet"].match(line)
            if bullet_match:
                content = bullet_match.group(1)
                current_type.fields.append(parse_type_field(content))
                continue

            # Indented field (no bullet): "  name: type, constraint"
            indented_match = PATTERNS["indented_field"].match(line)
            if indented_match:
                field_name = indented_match.group(1)
                field_rest = indented_match.group(2)
                content = f"{field_name}: {field_rest}"
                current_type.fields.append(parse_type_field(content))
                continue

        # Parse test assertions
        if current_test:
            # Simple assertion like: add(2, 3) == 5
            if "==" in line:
                expr, expected = line.split("==", 1)
                current_test.cases.append(TestCase(
                    expression=expr.strip(),
                    expected=expected.strip()
                ))
            elif line.strip() == "}":
                current_test = None
    
    # Don't forget the last ANLU
    if current_anlu:
        anlus.append(current_anlu)
    
    return NLFile(
        module=module,
        anlus=anlus,
        tests=tests,
        literals=literals,
        source_path=source_path
    )


def parse_nl_path(path: Path) -> NLFile:
    """Parse a .nl file from a filesystem path"""
    if not path.exists():
        raise ParseError(f"File not found: {path}")
    if not path.suffix == ".nl":
        raise ParseError(f"Expected .nl file, got: {path.suffix}")
    
    source = path.read_text(encoding="utf-8")
    return parse_nl_file(source, source_path=str(path))
