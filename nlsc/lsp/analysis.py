"""Document analysis utilities for the NLS language server.

Provides utilities for finding symbols at positions, extracting
hover information, and other analysis tasks.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nlsc.schema import ANLU, NLFile, TypeDefinition


@dataclass
class SymbolLocation:
    """Location of a symbol in the source."""

    line: int  # 0-indexed
    start_char: int
    end_char: int
    name: str
    kind: str  # "anlu", "type", "field", "input", "guard"


def find_symbol_at_position(
    text: str,
    nl_file: NLFile,
    line: int,
    character: int,
) -> SymbolLocation | None:
    """Find the symbol at a given position in the document.

    Args:
        text: The document text
        nl_file: Parsed NLFile
        line: 0-indexed line number
        character: 0-indexed character position

    Returns:
        SymbolLocation if a symbol is found, None otherwise
    """
    lines = text.split("\n")
    if line >= len(lines):
        return None

    current_line = lines[line]

    # Strip trailing \r if present (Windows line endings)
    if current_line.endswith("\r"):
        current_line = current_line[:-1]

    # Helper to check if character is within span
    def in_span(start: int, end: int) -> bool:
        return start <= character <= end

    # 1. ANLU identifier/reference [name]
    for m in re.finditer(r"\[([a-zA-Z][a-zA-Z0-9_-]*)\]", current_line):
        if in_span(*m.span(0)):  # Include brackets
            line_upper = current_line.upper()
            is_ref = "DEPENDS" in line_upper or "CALLS" in line_upper
            return SymbolLocation(
                line=line, start_char=m.start(0), end_char=m.end(0),
                name=m.group(1), kind="anlu_ref" if is_ref else "anlu"
            )

    # 2. Directives: @module, @version, @target, @type, @test, @main, etc.
    for m in re.finditer(r"@(module|version|target|type|test|property|invariant|literal|main)\b", current_line):
        if in_span(*m.span(0)):
            directive = m.group(1)
            return SymbolLocation(
                line=line, start_char=m.start(0), end_char=m.end(0),
                name=f"@{directive}", kind="directive"
            )

    # 3. Section keywords: PURPOSE, INPUTS, GUARDS, LOGIC, RETURNS, etc.
    for m in re.finditer(r"\b(PURPOSE|INPUTS|GUARDS|LOGIC|RETURNS|DEPENDS|CALLS|NOTES|EXAMPLES|EDGE\s+CASES)\s*:", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1).strip(), kind="section"
            )

    # 4. Builtin types: number, string, boolean, list, dict, any
    for m in re.finditer(r"\b(number|string|boolean|list|dict|any|void)\b", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="builtin_type"
            )

    # 5. Constraints: required, positive, non-negative, min:X, max:X, optional
    for m in re.finditer(r"\b(required|optional|positive|non-negative|unique)\b", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="constraint"
            )
    for m in re.finditer(r"\b(min|max):\s*(\d+)", current_line):
        if in_span(*m.span(0)):
            return SymbolLocation(
                line=line, start_char=m.start(0), end_char=m.end(0),
                name=f"{m.group(1)}:{m.group(2)}", kind="constraint"
            )

    # 6. Custom type names (PascalCase) after @type or @invariant or :
    for m in re.finditer(r"@type\s+([A-Z][a-zA-Z0-9]*)", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="type"
            )
    for m in re.finditer(r"@invariant\s+([A-Z][a-zA-Z0-9]*)", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="type_ref"
            )
    for m in re.finditer(r":\s*([A-Z][a-zA-Z0-9]*)", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="type_ref"
            )
    for m in re.finditer(r"list\s+of\s+([A-Z][a-zA-Z0-9]*)", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="type_ref"
            )

    # 7. Field/parameter names (after - in INPUTS or in type blocks)
    for m in re.finditer(r"^\s*-\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="field"
            )
    for m in re.finditer(r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:", current_line):
        if in_span(*m.span(1)):
            # Check this isn't a section keyword
            name = m.group(1)
            if name.upper() not in ["PURPOSE", "INPUTS", "GUARDS", "LOGIC", "RETURNS", "DEPENDS", "CALLS", "NOTES", "EXAMPLES"]:
                return SymbolLocation(
                    line=line, start_char=m.start(1), end_char=m.end(1),
                    name=name, kind="field"
                )

    # 8. Guard/logic operators: →, •, ->
    for m in re.finditer(r"(→|->|•)", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="operator"
            )

    # 9. Comments
    for m in re.finditer(r"(#.*)$", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name="comment", kind="comment"
            )

    # 10. Function calls like calculate_tax(...) - link to ANLU
    for m in re.finditer(r"\b([a-z][a-z0-9_]*)\s*\(", current_line):
        if in_span(*m.span(1)):
            # Convert snake_case to kebab-case for ANLU lookup
            func_name = m.group(1)
            anlu_name = func_name.replace("_", "-")
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=anlu_name, kind="anlu_ref"
            )
    # 11. Constructor calls like LineItem(...) - PascalCase with parens
    for m in re.finditer(r"\b([A-Z][a-zA-Z0-9]*)\s*\(", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="type_ref"
            )

    # 12. Keyword arguments like quantity=1, unit_price=99.99
    for m in re.finditer(r"\b([a-z][a-z0-9_]*)\s*=", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="kwarg"
            )

    # 13. String literals "..." or '...'
    for m in re.finditer(r'(["\'])([^"\']*)\1', current_line):
        if in_span(*m.span(0)):
            return SymbolLocation(
                line=line, start_char=m.start(0), end_char=m.end(0),
                name=m.group(2), kind="string"
            )

    # 14. Numbers (integers and floats) - match digits possibly with decimal
    for m in re.finditer(r"(?<![a-zA-Z_])(\d+\.?\d*)(?![a-zA-Z_])", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="number"
            )

    # 15. Comparison/equality operators
    for m in re.finditer(r"(==|!=|>=|<=|>|<)", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="comparison"
            )

    # 16. Math operators
    for m in re.finditer(r"(\+|-(?!\>)|\*|/|%)", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="math_op"
            )

    # 17. Error types like ValueError, TypeError
    for m in re.finditer(r"\b([A-Z][a-z]+Error)\s*\(", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="error_type"
            )

    # 18. Test block keywords: GIVEN, WHEN, THEN
    for m in re.finditer(r"\b(GIVEN|WHEN|THEN)\s*:", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="test_keyword"
            )

    # 19. Property block keywords: FOR_ALL, ASSERT, WHERE
    for m in re.finditer(r"\b(FOR_ALL|ASSERT|WHERE)\s*:", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="property_keyword"
            )

    # 20. Boolean literals
    for m in re.finditer(r"\b(true|false|True|False)\b", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1).lower(), kind="boolean"
            )

    # 21. Identifiers (catch-all for remaining lowercase words)
    for m in re.finditer(r"\b([a-z][a-z0-9_]*)\b", current_line):
        if in_span(*m.span(1)):
            return SymbolLocation(
                line=line, start_char=m.start(1), end_char=m.end(1),
                name=m.group(1), kind="identifier"
            )

    return None


def get_anlu_hover_content(anlu: ANLU) -> str:
    """Generate hover content for an ANLU.

    Args:
        anlu: The ANLU to generate hover content for

    Returns:
        Markdown formatted hover content
    """
    lines = [f"### [{anlu.identifier}]"]

    if anlu.purpose:
        lines.append(f"\n**PURPOSE:** {anlu.purpose}")

    if anlu.inputs:
        lines.append("\n**INPUTS:**")
        for inp in anlu.inputs:
            constraint_str = ""
            if inp.constraints:
                constraint_str = f" ({', '.join(inp.constraints)})"
            lines.append(f"- `{inp.name}`: {inp.type}{constraint_str}")

    if anlu.guards:
        lines.append(f"\n**GUARDS:** {len(anlu.guards)} guard(s)")

    if anlu.logic:
        lines.append(f"\n**LOGIC:** {len(anlu.logic)} step(s)")

    if anlu.returns:
        lines.append(f"\n**RETURNS:** `{anlu.returns}`")

    if anlu.depends:
        lines.append(f"\n**DEPENDS:** {', '.join(anlu.depends)}")

    return "\n".join(lines)


def get_type_hover_content(type_def: TypeDefinition) -> str:
    """Generate hover content for a type definition.

    Args:
        type_def: The TypeDefinition to generate hover content for

    Returns:
        Markdown formatted hover content
    """
    lines = [f"### @type {type_def.name}"]

    if type_def.fields:
        lines.append("\n**Fields:**")
        for field in type_def.fields:
            constraint_str = ""
            if field.constraints:
                constraint_str = f" ({', '.join(field.constraints)})"
            lines.append(f"- `{field.name}`: {field.type}{constraint_str}")

    return "\n".join(lines)


def find_anlu_by_name(nl_file: NLFile, name: str) -> ANLU | None:
    """Find an ANLU by its identifier."""
    for anlu in nl_file.anlus:
        if anlu.identifier == name:
            return anlu
    return None


def find_type_by_name(nl_file: NLFile, name: str) -> TypeDefinition | None:
    """Find a type definition by its name."""
    for type_def in nl_file.module.types:
        if type_def.name == name:
            return type_def
    return None


def find_definition_location(
    text: str,
    name: str,
    kind: str,
) -> SymbolLocation | None:
    """Find the definition location of a symbol.

    Args:
        text: Document text
        name: Symbol name to find
        kind: Symbol kind ("anlu", "anlu_ref", "type", "type_ref")

    Returns:
        SymbolLocation of the definition, or None
    """
    lines = text.split("\n")

    if kind in ("anlu", "anlu_ref"):
        # Look for [name] at the start of a line (ANLU definition)
        pattern = rf"^\s*\[({re.escape(name)})\]"
        for i, line in enumerate(lines):
            match = re.search(pattern, line)
            if match:
                return SymbolLocation(
                    line=i,
                    start_char=match.start(1),
                    end_char=match.end(1),
                    name=name,
                    kind="anlu",
                )

    elif kind in ("type", "type_ref"):
        # Look for @type Name
        pattern = rf"@type\s+({re.escape(name)})\b"
        for i, line in enumerate(lines):
            match = re.search(pattern, line)
            if match:
                return SymbolLocation(
                    line=i,
                    start_char=match.start(1),
                    end_char=match.end(1),
                    name=name,
                    kind="type",
                )

    return None


def find_all_references(
    text: str,
    name: str,
    kind: str,
) -> list[SymbolLocation]:
    """Find all references to a symbol.

    Args:
        text: Document text
        name: Symbol name to find
        kind: Symbol kind ("anlu", "type")

    Returns:
        List of SymbolLocations for all references
    """
    lines = text.split("\n")
    references: list[SymbolLocation] = []

    if kind in ("anlu", "anlu_ref"):
        # Find all [name] occurrences
        pattern = rf"\[({re.escape(name)})\]"
        for i, line in enumerate(lines):
            for match in re.finditer(pattern, line):
                references.append(
                    SymbolLocation(
                        line=i,
                        start_char=match.start(1),
                        end_char=match.end(1),
                        name=name,
                        kind="anlu_ref",
                    )
                )

    elif kind in ("type", "type_ref"):
        # Find @type Name definitions
        type_pattern = rf"@type\s+({re.escape(name)})\b"
        for i, line in enumerate(lines):
            type_match = re.search(type_pattern, line)
            if type_match:
                references.append(
                    SymbolLocation(
                        line=i,
                        start_char=type_match.start(1),
                        end_char=type_match.end(1),
                        name=name,
                        kind="type",
                    )
                )

        # Find type references after :
        ref_pattern = rf":\s*({re.escape(name)})\b"
        for i, line in enumerate(lines):
            for ref_match in re.finditer(ref_pattern, line):
                references.append(
                    SymbolLocation(
                        line=i,
                        start_char=ref_match.start(1),
                        end_char=ref_match.end(1),
                        name=name,
                        kind="type_ref",
                    )
                )

    return references
