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

    # Check for ANLU identifier/reference [name]
    anlu_match = re.search(r"\[([a-zA-Z][a-zA-Z0-9_-]*)\]", current_line)
    if anlu_match:
        start, end = anlu_match.span(1)
        if start <= character <= end:
            # Determine if this is a reference (DEPENDS/CALLS) or definition
            line_upper = current_line.upper()
            kind = "anlu_ref" if ("DEPENDS" in line_upper or "CALLS" in line_upper) else "anlu"
            return SymbolLocation(
                line=line,
                start_char=start,
                end_char=end,
                name=anlu_match.group(1),
                kind=kind,
            )

    # Check for @type Name
    type_match = re.search(r"@type\s+([A-Z][a-zA-Z0-9]*)", current_line)
    if type_match:
        start, end = type_match.span(1)
        if start <= character <= end:
            return SymbolLocation(
                line=line,
                start_char=start,
                end_char=end,
                name=type_match.group(1),
                kind="type",
            )

    # Check for type references in INPUTS or fields
    type_ref_match = re.search(r":\s*([A-Z][a-zA-Z0-9]*)", current_line)
    if type_ref_match:
        start, end = type_ref_match.span(1)
        if start <= character <= end:
            return SymbolLocation(
                line=line,
                start_char=start,
                end_char=end,
                name=type_ref_match.group(1),
                kind="type_ref",
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
