"""
NLS Parser - Parse .nl files into AST structures

Converts Natural Language Source files into structured ANLU objects.
Uses regex-based parsing for V0 (sufficient for math example).
"""

import ast
import re
from pathlib import Path
from typing import Optional

from .localization import (
    ANLU_IDENTIFIER_PATTERN,
    IDENTIFIER_PATTERN,
    extract_expression_identifiers,
    normalize_expression_text,
    normalize_localized_source,
    normalize_type_text,
)
from .schema import (
    ANLU,
    Module,
    NLFile,
    Input,
    Guard,
    EdgeCase,
    TestSuite,
    TestCase,
    TypeDefinition,
    TypeField,
    LogicStep,
    PropertyTest,
    PropertyAssertion,
    RetryPolicy,
    TimeoutPolicy,
    Invariant,
)


class ParseError(Exception):
    """Error during .nl file parsing"""

    def __init__(self, message: str, line_number: int = 0, line_content: str = ""):
        self.line_number = line_number
        self.line_content = line_content
        super().__init__(f"Line {line_number}: {message}")


# Regex patterns for parsing
PATTERNS = {
    "anlu_header": re.compile(rf"^\[({ANLU_IDENTIFIER_PATTERN})\]\s*$"),
    "directive": re.compile(
        r"^@(module|version|nls|target|imports|use|types|type|test|property|invariant|literal|main|states)\s*(.*)$"
    ),
    "purpose": re.compile(r"^PURPOSE:\s*(.+)$", re.IGNORECASE),
    "inputs": re.compile(r"^INPUTS:\s*$", re.IGNORECASE),
    "guards": re.compile(r"^GUARDS:\s*$", re.IGNORECASE),
    "logic": re.compile(r"^LOGIC:\s*$", re.IGNORECASE),
    "returns": re.compile(r"^RETURNS:\s*(.+)$", re.IGNORECASE),
    "edge_cases": re.compile(r"^EDGE\s*CASES:\s*$", re.IGNORECASE),
    "effects": re.compile(r"^EFFECTS:\s*(.*)$", re.IGNORECASE),
    "retry": re.compile(r"^RETRY:\s*$", re.IGNORECASE),
    "timeout": re.compile(r"^TIMEOUT:\s*$", re.IGNORECASE),
    "retry_inline": re.compile(r"^RETRY:\s*(\S.*)$", re.IGNORECASE),
    "timeout_inline": re.compile(r"^TIMEOUT:\s*(\S.*)$", re.IGNORECASE),
    "depends": re.compile(r"^DEPENDS:\s*(.+)$", re.IGNORECASE),
    "bullet": re.compile(r"^\s*[•\-\*]\s*(.+)$"),
    "numbered": re.compile(r"^\s*(\d+)\.\s*(.+)$"),
    "comment": re.compile(r"^\s*#.*$"),
    "empty": re.compile(r"^\s*$"),
    "indented_field": re.compile(r"^\s+(\w+)\s*:\s*(.+)$"),
}


SAFE_IMPORT_TOKEN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*$")


def _validate_import_token(token: str, line_num: int) -> str:
    """Validate a single @imports token and raise ParseError when unsafe."""
    candidate = token.strip()
    if not candidate:
        raise ParseError("Invalid import token in @imports directive", line_num, token)
    if not SAFE_IMPORT_TOKEN.match(candidate):
        raise ParseError(
            f"Unsafe import token in @imports: {candidate}", line_num, token
        )
    return candidate


def apply_module_directive(
    module: Module, directive_type: str, directive_value: str, line_num: int
) -> None:
    """Apply a module-level directive to a Module object."""
    if directive_type == "module":
        module.name = directive_value
    elif directive_type == "version":
        module.version = directive_value
    elif directive_type == "nls":
        module.spec_version = directive_value
    elif directive_type == "target":
        module.target = directive_value
    elif directive_type == "imports":
        module.imports = [
            _validate_import_token(i, line_num) for i in directive_value.split(",")
        ]
    elif directive_type == "use":
        if directive_value:
            module.uses.append(directive_value)
    elif directive_type == "states":
        # @states Order: Pending, Validated, Charged (#200)
        protocol, separator, states_text = directive_value.partition(":")
        protocol = protocol.strip()
        states = tuple(
            state.strip() for state in states_text.split(",") if state.strip()
        )
        if not separator or not protocol or not states:
            raise ParseError(
                "Invalid @states directive; expected '@states Name: State1, State2'",
                line_num,
                directive_value,
            )
        if len(set(states)) != len(states):
            raise ParseError(
                f"Duplicate state in @states {protocol}", line_num, directive_value
            )
        if protocol in module.states:
            raise ParseError(
                f"@states {protocol} is already declared", line_num, directive_value
            )
        module.states[protocol] = states



_SECTION_HEADER_PATTERNS = (
    "purpose",
    "inputs",
    "guards",
    "logic",
    "returns",
    "edge_cases",
    "depends",
    "effects",
    "retry",
    "timeout",
)


def _is_section_header_line(line_match: str) -> bool:
    """True when a line opens a known ANLU section (used to end a policy
    section without treating the header as a stray bullet)."""
    if any(PATTERNS[name].match(line_match) for name in _SECTION_HEADER_PATTERNS):
        return True
    # Bare headers (no value) also end a section; they are malformed
    # elsewhere, but must not be reported as stray policy bullets.
    return bool(
        re.match(
            r"^(PURPOSE|INPUTS|GUARDS|LOGIC|RETURNS|DEPENDS|EDGE\s*CASES|"
            r"EFFECTS|RETRY|TIMEOUT)\s*:\s*$",
            line_match,
            re.IGNORECASE,
        )
    )


def _parse_retry_bullet(
    policy: "RetryPolicy | None", text: str, line_num: int, raw: str
) -> None:
    """Parse one RETRY: bullet into the policy (#201)."""
    if policy is None:
        return
    attempts_match = re.match(
        r"up to\s+(\d+)\s+attempts?(?:\s+on\s+(.+))?$", text, re.IGNORECASE
    )
    if attempts_match:
        policy.attempts = int(attempts_match.group(1))
        errors = attempts_match.group(2)
        if errors:
            policy.error_types = [part.strip() for part in errors.split(",") if part.strip()]
        return
    key_match = re.match(r"idempotency key:\s*(\S+)$", text, re.IGNORECASE)
    if key_match:
        policy.idempotency_key = key_match.group(1)
        return
    raise ParseError(
        "Invalid RETRY bullet; expected 'up to N attempts [on Err1, Err2]' "
        "or 'idempotency key: name'",
        line_num,
        raw,
    )


def _parse_timeout_bullet(
    policy: "TimeoutPolicy | None", text: str, line_num: int, raw: str
) -> None:
    """Parse one TIMEOUT: bullet into the policy (#201)."""
    if policy is None:
        return
    after_match = re.match(
        r"after\s+(\d+)\s*ms(?:\s*->\s*(\S+))?$", text, re.IGNORECASE
    )
    if after_match:
        policy.after_ms = int(after_match.group(1))
        policy.outcome = after_match.group(2)
        return
    raise ParseError(
        "Invalid TIMEOUT bullet; expected 'after Nms -> outcome'",
        line_num,
        raw,
    )


def parse_module_directives(source: str) -> Module:
    """Parse top-level module directives from source using shared regex rules."""
    source = normalize_localized_source(source)
    module = Module(name="unnamed")

    for line_num, line in enumerate(source.split("\n"), start=1):
        directive_match = PATTERNS["directive"].match(line.lstrip())
        if not directive_match:
            continue

        directive_type = directive_match.group(1)
        directive_value = directive_match.group(2).strip()
        apply_module_directive(module, directive_type, directive_value, line_num)

    return module


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
    type_spec = normalize_type_text(parts[0] if parts else "any")
    constraints = []
    description = None

    for part in parts[1:]:
        if part.startswith('"') and part.endswith('"'):
            description = part[1:-1]
        else:
            constraints.append(part)

    return Input(
        name=name, type=type_spec, constraints=constraints, description=description
    )


def parse_guard(text: str) -> Guard:
    """
    Parse a guard line like:
    • token must not be empty → AuthError(MISSING, "Token required")
    • amount > 0 → ValueError(Amount must be positive)
    """
    # Split on arrow
    if "→" in text:
        condition, error_part = text.split("→", 1)
    elif "->" in text:
        condition, error_part = text.split("->", 1)
    elif "|" in text:
        condition, error_part = text.split("|", 1)
    else:
        return Guard(condition=normalize_expression_text(text.strip()))

    condition = normalize_expression_text(condition.strip())
    error_part = error_part.strip()

    colon_match = re.match(rf"({IDENTIFIER_PATTERN})\s*:\s*(.+)$", error_part)
    if colon_match:
        return Guard(
            condition=condition,
            error_type=colon_match.group(1),
            error_message=_parse_guard_message(colon_match.group(2).strip()),
        )

    # Parse error specification like AuthError(MISSING, "Token required")
    error_match = re.match(rf"({IDENTIFIER_PATTERN})\((.+)\)$", error_part)
    if error_match:
        error_type = error_match.group(1)
        inner = error_match.group(2).strip()
        if inner.startswith(("'", '"', "f'", 'f"')):
            return Guard(
                condition=condition,
                error_type=error_type,
                error_message=_parse_guard_message(inner),
            )
        code_part, message_part = _split_guard_args(inner)
        if message_part:
            return Guard(
                condition=condition,
                error_type=error_type,
                error_code=code_part.strip(),
                error_message=_parse_guard_message(message_part.strip()),
            )
        return Guard(
            condition=condition,
            error_type=error_type,
            error_message=_parse_guard_message(inner),
        )

    return Guard(condition=condition, error_message=error_part)


def _parse_guard_message(text: str) -> str:
    """Parse a guard message payload from string-like syntax."""
    candidate = text.strip()
    if not candidate:
        return candidate

    literal_candidate = (
        candidate[1:] if candidate.startswith(("f'", 'f"')) else candidate
    )
    try:
        parsed = ast.literal_eval(literal_candidate)
        if isinstance(parsed, str):
            return parsed
    except (SyntaxError, ValueError):
        pass
    return candidate


def _split_guard_args(text: str) -> tuple[str, str]:
    """Split `Error(code, message)` args on the first top-level comma."""
    depth = 0
    in_string = False
    string_char = ""
    escaped = False

    for index, char in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == string_char:
                in_string = False
            continue

        if char in {"'", '"'}:
            in_string = True
            string_char = char
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth = max(0, depth - 1)
        elif char == "," and depth == 0:
            return text[:index], text[index + 1 :]

    return text, ""


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
    type_spec = normalize_type_text(parts[0] if parts else "any")
    constraints = []
    description = None

    for part in parts[1:]:
        if part.startswith('"') and part.endswith('"'):
            description = part[1:-1]
        else:
            constraints.append(part)

    return TypeField(
        name=name, type=type_spec, constraints=constraints, description=description
    )


def extract_variables(expression: str) -> list[str]:
    """
    Extract variable names from an expression.
    Excludes literals, operators, and function names.
    """
    return extract_expression_identifiers(expression)


def parse_logic_step(
    number: int, text: str, previous_assigns: dict[str, int]
) -> LogicStep:
    """
    Parse a LOGIC step line, extracting assignment, variable usage, and FSM features.

    Args:
        number: Step number (1-indexed)
        text: The step description
        previous_assigns: Map of variable name -> step number that assigned it

    Returns:
        LogicStep with dataflow and FSM information
    """
    assigns = []
    uses = []
    depends_on = []
    state_name = None
    output_binding = None
    condition = None
    else_action = None

    working_text = normalize_expression_text(text.strip())

    # 1. Parse [state_name] prefix
    state_match = re.match(rf"^\[({ANLU_IDENTIFIER_PATTERN})\]\s*(.+)$", working_text)
    if state_match:
        candidate_state = state_match.group(1)
        remainder = state_match.group(2)
        if not remainder.startswith("("):
            state_name = candidate_state
            working_text = remainder

    # 2. Parse IF condition THEN [action] [ELSE action] first so arm
    # bindings are not mistaken for the step's trailing binding.
    if_else_match = re.match(
        r"^IF\s+(.+?)\s+THEN\s+(.+?)\s+ELSE\s+(.+)$",
        working_text,
        re.IGNORECASE,
    )
    if if_else_match:
        condition = if_else_match.group(1).strip()
        working_text = if_else_match.group(2).strip()
        else_action = if_else_match.group(3).strip()
        uses.extend(extract_variables(condition))
    else:
        if_match = re.match(
            r"^IF\s+(.+?)\s+THEN\s+(.+)$", working_text, re.IGNORECASE
        )
        if if_match:
            condition = if_match.group(1).strip()
            working_text = if_match.group(2).strip()
            uses.extend(extract_variables(condition))

    # 3. Parse → variable or -> variable output binding (at end)
    output_match = re.search(rf"\s*(?:→|->)\s*({IDENTIFIER_PATTERN})$", working_text)
    if output_match:
        output_binding = output_match.group(1)
        working_text = working_text[: output_match.start()].strip()
        # Output binding is also an assignment
        assigns.append(output_binding)

    # The ELSE arm carries its own binding/assignment for dataflow.
    if else_action is not None:
        else_binding_match = re.search(
            rf"\s*(?:→|->)\s*({IDENTIFIER_PATTERN})$", else_action
        )
        if else_binding_match:
            else_text = else_action[: else_binding_match.start()].strip()
            assigns.append(else_binding_match.group(1))
        else:
            else_text = else_action
        else_assign_match = re.match(
            rf"^({IDENTIFIER_PATTERN})\s*=\s*(.+)$", else_text
        )
        if else_assign_match:
            assigns.append(else_assign_match.group(1))
            uses.extend(extract_variables(else_assign_match.group(2)))
        else:
            uses.extend(extract_variables(else_text))

    # 4. Check for assignment pattern: var = expression
    assignment_match = re.match(rf"^({IDENTIFIER_PATTERN})\s*=\s*(.+)$", working_text)

    if assignment_match:
        var_name = assignment_match.group(1)
        expression = assignment_match.group(2)
        if var_name not in assigns:  # Don't duplicate if already from output binding
            assigns.append(var_name)
        uses.extend(extract_variables(expression))
    else:
        # No assignment - just extract any variables mentioned
        uses.extend(extract_variables(working_text))

    # Remove duplicates from assigns and uses while preserving order
    assigns = list(dict.fromkeys(assigns))
    seen = set()
    unique_uses = []
    for var in uses:
        if var not in seen:
            seen.add(var)
            unique_uses.append(var)
    uses = unique_uses

    # Build dependencies based on which previous steps assigned variables we use
    for var in uses:
        if var in previous_assigns:
            step_num = previous_assigns[var]
            if step_num not in depends_on:
                depends_on.append(step_num)

    depends_on.sort()

    return LogicStep(
        number=number,
        description=working_text.strip(),
        assigns=assigns,
        uses=uses,
        depends_on=depends_on,
        state_name=state_name,
        output_binding=output_binding,
        condition=condition,
        else_action=else_action,
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
        return EdgeCase(condition=normalize_expression_text(text.strip()), behavior="")

    return EdgeCase(
        condition=normalize_expression_text(condition.strip()),
        behavior=normalize_expression_text(behavior.strip()),
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
    source = normalize_localized_source(source)
    lines = source.split("\n")

    # Initialize module with defaults
    module = Module(name="unnamed")
    anlus: list[ANLU] = []
    tests: list[TestSuite] = []
    properties: list[PropertyTest] = []
    invariants: list[Invariant] = []
    literals: list[str] = []

    # Current parsing state
    current_anlu: Optional[ANLU] = None
    current_section: Optional[str] = None  # inputs, guards, logic, edge_cases
    current_test: Optional[TestSuite] = None
    current_type: Optional[TypeDefinition] = None
    current_property: Optional[PropertyTest] = None
    current_invariant: Optional[Invariant] = None
    in_literal_block = False
    literal_buffer: list[str] = []
    brace_depth = 0
    in_main_block = False
    main_buffer: list[str] = []
    main_brace_depth = 0
    # Track variable assignments for dataflow analysis
    logic_assigns: dict[str, int] = {}
    # Track step-number identities per ANLU (#192)
    logic_step_lines: dict[int, int] = {}

    for line_num, line in enumerate(lines, start=1):
        # Normalize matching to allow leading indentation in embedded strings.
        # We keep the original `line` for error reporting and for parsing
        # indentation-sensitive constructs (bullets, generated blocks, etc.).
        line_match = line.lstrip()

        # Handle main blocks
        if in_main_block:
            if "{" in line:
                main_brace_depth += line.count("{")
            if "}" in line:
                main_brace_depth -= line.count("}")
                if main_brace_depth <= 0:
                    # End of main block
                    in_main_block = False
                    continue
            # Add line to main block (strip leading indent)
            main_buffer.append(line.strip())
            continue

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
            if current_section == "inputs":
                raise ParseError(
                    "Invalid INPUTS bullet marker; expected one of: •, -, *",
                    line_num,
                    line,
                )
            continue
        if PATTERNS["empty"].match(line) and current_section is None:
            continue

        # Check for directives
        directive_match = PATTERNS["directive"].match(line_match)
        if directive_match:
            directive_type = directive_match.group(1)
            directive_value = directive_match.group(2).strip()

            if directive_type in {
                "module",
                "version",
                "nls",
                "target",
                "imports",
                "use",
                "states",
            }:
                apply_module_directive(
                    module, directive_type, directive_value, line_num
                )
            elif directive_type == "main":
                # Start main block
                in_main_block = True
                main_brace_depth = 1 if "{" in line else 0
            elif directive_type == "literal":
                # Start literal block
                in_literal_block = True
                brace_depth = 1 if "{" in line else 0
                directive_value.split("{")[0].strip()
            elif directive_type == "test":
                # Parse test header like: @test [add] {
                test_match = re.match(
                    rf"\[({ANLU_IDENTIFIER_PATTERN})\]\s*\{{?", directive_value
                )
                if test_match:
                    current_test = TestSuite(anlu_id=test_match.group(1))
                    tests.append(current_test)
            elif directive_type == "type":
                # Parse type header like: @type Person {
                # or @type Person extends Entity {
                type_match = re.match(
                    rf"({IDENTIFIER_PATTERN})\s*(?:extends\s+({IDENTIFIER_PATTERN}))?\s*\{{?",
                    directive_value,
                )
                if type_match:
                    current_type = TypeDefinition(
                        name=type_match.group(1),
                        base=type_match.group(2),
                        line_number=line_num,
                    )
                    module.types.append(current_type)
            elif directive_type == "property":
                # Parse property header like: @property [add] {
                prop_match = re.match(
                    rf"\[({ANLU_IDENTIFIER_PATTERN})\]\s*\{{?", directive_value
                )
                if prop_match:
                    current_property = PropertyTest(anlu_id=prop_match.group(1))
                    properties.append(current_property)
            elif directive_type == "invariant":
                # Parse invariant header like: @invariant Account {
                inv_match = re.match(rf"({IDENTIFIER_PATTERN})\s*\{{?", directive_value)
                if inv_match:
                    current_invariant = Invariant(type_name=inv_match.group(1))
                    invariants.append(current_invariant)

            # Save current ANLU if switching context
            if current_anlu and directive_type in (
                "module",
                "literal",
                "test",
                "type",
                "property",
                "invariant",
            ):
                current_section = None
            continue

        # Check for ANLU header
        anlu_match = PATTERNS["anlu_header"].match(line_match)
        if anlu_match:
            # Save previous ANLU
            if current_anlu:
                anlus.append(current_anlu)

            # Start new ANLU
            current_anlu = ANLU(
                identifier=anlu_match.group(1),
                purpose="",
                returns="",
                line_number=line_num,
            )
            # Reset dataflow tracking for new ANLU
            logic_assigns = {}
            logic_step_lines = {}
            current_section = None
            continue

        # Parse ANLU fields
        if current_anlu:
            # PURPOSE:
            purpose_match = PATTERNS["purpose"].match(line_match)
            if purpose_match:
                current_anlu.purpose = purpose_match.group(1).strip()
                current_section = None
                continue

            # INPUTS:
            if PATTERNS["inputs"].match(line_match):
                current_section = "inputs"
                continue

            # GUARDS:
            if PATTERNS["guards"].match(line_match):
                current_section = "guards"
                continue

            # LOGIC:
            if PATTERNS["logic"].match(line_match):
                current_section = "logic"
                continue

            # EDGE CASES:
            if PATTERNS["edge_cases"].match(line_match):
                current_section = "edge_cases"
                continue

            # RETURNS:
            returns_match = PATTERNS["returns"].match(line_match)
            if returns_match:
                current_anlu.returns = normalize_expression_text(
                    returns_match.group(1).strip()
                )
                current_section = None
                continue

            # RETRY: / TIMEOUT: sections (#201)
            if PATTERNS["retry_inline"].match(line_match):
                raise ParseError(
                    "RETRY bullets go on their own lines under 'RETRY:'",
                    line_num,
                    line,
                )
            if PATTERNS["timeout_inline"].match(line_match):
                raise ParseError(
                    "TIMEOUT bullets go on their own lines under 'TIMEOUT:'",
                    line_num,
                    line,
                )
            if PATTERNS["retry"].match(line_match):
                if current_anlu.retry is not None:
                    raise ParseError(
                        "Duplicate RETRY section for this ANLU", line_num, line
                    )
                current_anlu.retry = RetryPolicy(line_number=line_num)
                current_section = "retry"
                continue
            if PATTERNS["timeout"].match(line_match):
                if current_anlu.timeout is not None:
                    raise ParseError(
                        "Duplicate TIMEOUT section for this ANLU", line_num, line
                    )
                current_anlu.timeout = TimeoutPolicy(line_number=line_num)
                current_section = "timeout"
                continue
            if current_section in ("retry", "timeout") and line_match.strip():
                bullet = PATTERNS["bullet"].match(line_match)
                if bullet is not None:
                    text_value = bullet.group(1).strip()
                    if current_section == "retry":
                        _parse_retry_bullet(
                            current_anlu.retry, text_value, line_num, line
                        )
                    else:
                        _parse_timeout_bullet(
                            current_anlu.timeout, text_value, line_num, line
                        )
                    continue
                if not _is_section_header_line(line_match):
                    raise ParseError(
                        "Invalid "
                        + current_section.upper()
                        + " bullet marker; expected one of: •, -, *",
                        line_num,
                        line,
                    )
                # A section header ends the policy section: fall through so
                # the header handlers below can process it.

            # EFFECTS: (#197)
            effects_match = PATTERNS["effects"].match(line_match)
            if effects_match:
                current_anlu.declared_effects = effects_match.group(1).strip()
                current_section = None
                continue

            # DEPENDS:
            depends_match = PATTERNS["depends"].match(line_match)
            if depends_match:
                deps = depends_match.group(1).strip()
                current_anlu.depends = [d.strip() for d in deps.split(",")]
                current_section = None
                continue

            # Parse section content
            if current_section:
                if PATTERNS["empty"].match(line):
                    continue

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
                        # Step numbers are node identities (#192): a
                        # duplicate would silently collapse graph nodes.
                        if step_num in logic_step_lines:
                            raise ParseError(
                                f"Duplicate LOGIC step number {step_num} in "
                                f"[{current_anlu.identifier}] "
                                f"(first defined at line {logic_step_lines[step_num]}, "
                                f"repeated at line {line_num})",
                                line_num,
                                line,
                            )
                        logic_step_lines[step_num] = line_num
                        # Keep raw logic for backwards compatibility
                        current_anlu.logic.append(step_text)
                        # Parse with dataflow extraction
                        logic_step = parse_logic_step(
                            step_num, step_text, logic_assigns
                        )
                        logic_step.line_number = line_num
                        current_anlu.logic_steps.append(logic_step)
                        # Update assigns tracker
                        for var in logic_step.assigns:
                            logic_assigns[var] = step_num
                    continue

                if current_section == "inputs":
                    raise ParseError(
                        "Invalid INPUTS bullet marker; expected one of: •, -, *",
                        line_num,
                        line,
                    )
                if current_section == "guards":
                    raise ParseError(
                        "Invalid GUARDS bullet marker; expected one of: •, -, *",
                        line_num,
                        line,
                    )
                if current_section == "logic":
                    raise ParseError(
                        "Invalid LOGIC step format; expected numbered step like '1. ...'",
                        line_num,
                        line,
                    )

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
                current_test.cases.append(
                    TestCase(expression=expr.strip(), expected=expected.strip())
                )
            elif line.strip() == "}":
                current_test = None

        # Parse property assertions
        if current_property:
            stripped = line.strip()
            if stripped == "}":
                current_property = None
            elif stripped and not stripped.startswith("#"):
                # Remove trailing comments
                if "#" in stripped:
                    stripped = stripped.split("#")[0].strip()
                if stripped:
                    # Check for forall quantifier: forall x: type -> assertion
                    forall_match = re.match(
                        rf"forall\s+({IDENTIFIER_PATTERN}):\s*({IDENTIFIER_PATTERN})\s*->\s*(.+)",
                        stripped,
                    )
                    if forall_match:
                        current_property.assertions.append(
                            PropertyAssertion(
                                expression=forall_match.group(3).strip(),
                                quantifier="forall",
                                variable=forall_match.group(1),
                                variable_type=forall_match.group(2),
                            )
                        )
                    else:
                        # Simple property assertion
                        current_property.assertions.append(
                            PropertyAssertion(expression=stripped)
                        )

        # Parse invariant conditions
        if current_invariant:
            stripped = line.strip()
            if stripped == "}":
                current_invariant = None
            elif stripped and not stripped.startswith("#"):
                current_invariant.conditions.append(stripped)

    # Don't forget the last ANLU
    if current_anlu:
        anlus.append(current_anlu)

    return NLFile(
        module=module,
        anlus=anlus,
        tests=tests,
        properties=properties,
        invariants=invariants,
        literals=literals,
        main_block=main_buffer,
        source_path=source_path,
    )


def parse_nl_path(path: Path) -> NLFile:
    """Parse a .nl file from a filesystem path"""
    if not path.exists():
        raise ParseError(f"File not found: {path}")
    if not path.suffix == ".nl":
        raise ParseError(f"Expected .nl file, got: {path.suffix}")

    source = path.read_text(encoding="utf-8")
    return parse_nl_file(source, source_path=str(path))
