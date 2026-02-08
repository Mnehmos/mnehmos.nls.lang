"""NLS Language Server implementation using pygls.

Provides language intelligence features for .nl files:
- Diagnostics (parse errors, warnings)
- Hover information
- Completions
- Go to definition
- Find references
"""

from __future__ import annotations

import logging
import re

from lsprotocol import types as lsp
from pygls.lsp.server import LanguageServer

# Keep the server's advertised version single-sourced from the package version.
from nlsc import __version__ as NLSC_VERSION
from nlsc.lsp.analysis import (
    SymbolLocation,
    find_all_references,
    find_anlu_by_name,
    find_definition_location,
    find_symbol_at_position,
    find_type_by_name,
    get_anlu_hover_content,
    get_type_hover_content,
)
from nlsc.parser import parse_nl_file
from nlsc.schema import NLFile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NLSLanguageServer(LanguageServer):
    """Language server for NLS (.nl) files."""

    def __init__(self) -> None:
        super().__init__(
            name="nls-language-server",
            version=NLSC_VERSION,
            text_document_sync_kind=lsp.TextDocumentSyncKind.Full,
        )
        # Cache of parsed files: uri -> NLFile
        self.parsed_files: dict[str, NLFile] = {}
        # Cache of document content: uri -> text
        self.document_content: dict[str, str] = {}
        # Cache of parse errors: uri -> list of diagnostics
        self.diagnostics_cache: dict[str, list[lsp.Diagnostic]] = {}


# Create the server instance
server = NLSLanguageServer()


@server.feature(lsp.TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: NLSLanguageServer, params: lsp.DidOpenTextDocumentParams) -> None:
    """Handle document open - parse and publish diagnostics."""
    uri = params.text_document.uri
    text = params.text_document.text
    ls.document_content[uri] = text
    _parse_and_publish_diagnostics(ls, uri, text)


@server.feature(lsp.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: NLSLanguageServer, params: lsp.DidChangeTextDocumentParams) -> None:
    """Handle document change - reparse and publish diagnostics."""
    uri = params.text_document.uri
    # Get the full text from the change (we use full sync)
    if params.content_changes:
        text = params.content_changes[-1].text
        ls.document_content[uri] = text
        _parse_and_publish_diagnostics(ls, uri, text)


@server.feature(lsp.TEXT_DOCUMENT_DID_CLOSE)
def did_close(ls: NLSLanguageServer, params: lsp.DidCloseTextDocumentParams) -> None:
    """Handle document close - clean up caches."""
    uri = params.text_document.uri
    ls.parsed_files.pop(uri, None)
    ls.document_content.pop(uri, None)
    ls.diagnostics_cache.pop(uri, None)
    # Clear diagnostics for closed file
    ls.text_document_publish_diagnostics(lsp.PublishDiagnosticsParams(uri=uri, diagnostics=[]))


def _get_hover_content(nl_file: NLFile, symbol: SymbolLocation) -> str | None:
    """Get hover content for a symbol.

    Args:
        nl_file: Parsed NLFile
        symbol: Symbol location info

    Returns:
        Markdown hover content or None
    """
    kind = symbol.kind
    name = symbol.name

    if kind in ("anlu", "anlu_ref"):
        anlu = find_anlu_by_name(nl_file, name)
        if anlu:
            return get_anlu_hover_content(anlu)
        return f"**ANLU Reference:** `[{name}]`\n\n_Definition not found in this file_"

    elif kind in ("type", "type_ref"):
        type_def = find_type_by_name(nl_file, name)
        if type_def:
            return get_type_hover_content(type_def)
        return f"**Type Reference:** `{name}`\n\n_Definition not found in this file_"

    elif kind == "directive":
        directives = {
            "@module": "**@module** - Declares the module name for this NLS file.\n\n```nl\n@module my-module-name\n```",
            "@version": "**@version** - Specifies the semantic version of this module.\n\n```nl\n@version 1.0.0\n```",
            "@target": "**@target** - Specifies the compilation target language.\n\nSupported: `python`, `typescript`, `rust`\n\n```nl\n@target python\n```",
            "@type": "**@type** - Defines a custom data type with fields.\n\n```nl\n@type MyType {\n  field_name: type, constraints\n}\n```",
            "@test": "**@test** - Defines a property-based test block.\n\n```nl\n@test test-name {\n  GIVEN: initial conditions\n  WHEN: action\n  THEN: expected result\n}\n```",
            "@property": "**@property** - Defines an invariant property that must hold.\n\n```nl\n@property property-name {\n  FOR_ALL: x: Type\n  ASSERT: condition\n}\n```",
            "@invariant": "**@invariant** - Defines runtime invariants for a type.\n\n```nl\n@invariant TypeName {\n  field_name >= 0\n  field_name <= 100\n}\n```",
            "@literal": "**@literal** - Defines a literal/constant value.\n\n```nl\n@literal CONSTANT_NAME = value\n```",
            "@main": "**@main** - Defines the program entry point.\n\n```nl\n@main {\n  # Main program logic\n}\n```",
        }
        return directives.get(name, f"**Directive:** `{name}`")

    elif kind == "section":
        sections = {
            "PURPOSE": "**PURPOSE:** - Describes what this ANLU does in plain English.",
            "INPUTS": "**INPUTS:** - Lists input parameters with types and constraints.\n\n```nl\nINPUTS:\n  - param_name: type, constraints\n```",
            "GUARDS": "**GUARDS:** - Pre-conditions that must be true. Uses `→` for results.\n\n```nl\nGUARDS:\n  - condition → ValueError(\"message\")\n```",
            "LOGIC": "**LOGIC:** - Step-by-step computation logic. Uses `•` for assignments.\n\n```nl\nLOGIC:\n  1. Calculate intermediate • result = expr\n  2. Process further\n```",
            "RETURNS": "**RETURNS:** - The value or expression returned by this ANLU.",
            "DEPENDS": "**DEPENDS:** - Lists other ANLUs this one depends on.\n\n```nl\nDEPENDS: [other-anlu], [another]\n```",
            "CALLS": "**CALLS:** - External functions/APIs this ANLU calls.",
            "NOTES": "**NOTES:** - Additional implementation notes or documentation.",
            "EXAMPLES": "**EXAMPLES:** - Usage examples for this ANLU.",
            "EDGE CASES": "**EDGE CASES:** - Special cases and how they're handled.",
        }
        return sections.get(name, f"**Section:** `{name}`")

    elif kind == "builtin_type":
        builtins = {
            "number": "**number** - Numeric type (int or float in Python, number in TypeScript).",
            "string": "**string** - Text string type.",
            "boolean": "**boolean** - True/False type.",
            "list": "**list** - Ordered collection. Use `list of Type` for typed lists.",
            "dict": "**dict** - Key-value mapping type.",
            "any": "**any** - Any type (use sparingly).",
            "void": "**void** - No return value.",
        }
        return builtins.get(name, f"**Built-in Type:** `{name}`")

    elif kind == "constraint":
        constraints = {
            "required": "**required** - Field must be provided (non-null).",
            "optional": "**optional** - Field can be omitted (nullable).",
            "positive": "**positive** - Number must be > 0.",
            "non-negative": "**non-negative** - Number must be >= 0.",
            "unique": "**unique** - Values must be unique in collection.",
        }
        if name in constraints:
            return constraints[name]
        if name.startswith("min:"):
            return f"**min:{name[4:]}** - Minimum value constraint."
        if name.startswith("max:"):
            return f"**max:{name[4:]}** - Maximum value constraint."
        return f"**Constraint:** `{name}`"

    elif kind == "field":
        return f"**Field/Parameter:** `{name}`\n\n_Hover over the type for more info_"

    elif kind == "operator":
        operators = {
            "→": "**→** (arrow) - Guard result operator.\n\n`condition → result`",
            "->": "**->** (arrow) - Guard result operator.\n\n`condition -> result`",
            "•": "**•** (bullet) - Assignment in LOGIC steps.\n\n`variable • expression`",
            "||": "**||** - Logical OR operator.",
            "&&": "**&&** - Logical AND operator.",
        }
        return operators.get(name, f"**Operator:** `{name}`")

    elif kind == "comment":
        return "**Comment** - Documentation or notes. Comments start with `#`."

    elif kind == "test":
        return f"**Test Block:** `{name}`\n\nProperty-based test definition."

    elif kind == "property":
        return f"**Property Block:** `{name}`\n\nInvariant property that must always hold."

    elif kind == "invariant":
        return f"**Invariant Block:** Constraints for type `{name}`."

    elif kind == "literal":
        return f"**Literal:** `{name}`\n\nConstant value definition."

    elif kind == "kwarg":
        return f"**Keyword Argument:** `{name}`\n\nNamed parameter in function/constructor call."

    elif kind == "string":
        if len(name) > 50:
            display = name[:50] + "..."
        else:
            display = name
        return f"**String Literal:** `\"{display}\"`"

    elif kind == "identifier":
        return f"**Identifier:** `{name}`\n\n_Local variable or reference_"

    elif kind == "number":
        if "." in name:
            return f"**Float Literal:** `{name}`"
        return f"**Integer Literal:** `{name}`"

    elif kind == "comparison":
        comparisons = {
            "==": "**==** (equals) - Test equality.",
            "!=": "**!=** (not equals) - Test inequality.",
            ">=": "**>=** (greater or equal) - Test if left >= right.",
            "<=": "**<=** (less or equal) - Test if left <= right.",
            ">": "**>** (greater) - Test if left > right.",
            "<": "**<** (less) - Test if left < right.",
        }
        return comparisons.get(name, f"**Comparison:** `{name}`")

    elif kind == "math_op":
        ops = {
            "+": "**+** (plus) - Addition operator.",
            "-": "**-** (minus) - Subtraction operator.",
            "*": "**\\*** (times) - Multiplication operator.",
            "/": "**//** (divide) - Division operator.",
            "%": "**%** (modulo) - Remainder operator.",
        }
        return ops.get(name, f"**Math Operator:** `{name}`")

    elif kind == "error_type":
        errors = {
            "ValueError": "**ValueError** - Raised when a value is invalid.\n\nCommon in GUARDS for input validation.",
            "TypeError": "**TypeError** - Raised when a type is incorrect.",
            "IndexError": "**IndexError** - Raised when index is out of range.",
            "KeyError": "**KeyError** - Raised when key not found in dict.",
        }
        return errors.get(name, f"**Error Type:** `{name}`\n\nPython exception type.")

    elif kind == "test_keyword":
        keywords = {
            "GIVEN": "**GIVEN:** - Sets up initial test conditions.\n\n```nl\n@test example {\n  GIVEN: initial state\n  WHEN: action\n  THEN: expected result\n}\n```",
            "WHEN": "**WHEN:** - Describes the action being tested.\n\n```nl\nWHEN: [function-name](inputs)\n```",
            "THEN": "**THEN:** - Describes expected outcome.\n\n```nl\nTHEN: result == expected_value\n```",
        }
        return keywords.get(name, f"**Test Keyword:** `{name}`")

    elif kind == "property_keyword":
        keywords = {
            "FOR_ALL": "**FOR_ALL:** - Universal quantifier.\n\nDeclares variables that must satisfy the property for all values.\n\n```nl\nFOR_ALL: x: number, y: number\n```",
            "ASSERT": "**ASSERT:** - The property assertion.\n\nThe condition that must be true.\n\n```nl\nASSERT: [add](x, y) == [add](y, x)\n```",
            "WHERE": "**WHERE:** - Constraints on FOR_ALL variables.\n\n```nl\nWHERE: x > 0, y > 0\n```",
        }
        return keywords.get(name, f"**Property Keyword:** `{name}`")

    elif kind == "boolean":
        if name == "true":
            return "**true** - Boolean true value."
        return "**false** - Boolean false value."

    return None


@server.feature(lsp.TEXT_DOCUMENT_HOVER)
def hover(ls: NLSLanguageServer, params: lsp.HoverParams) -> lsp.Hover | None:
    """Provide hover information for symbols."""
    uri = params.text_document.uri
    position = params.position

    # Get document text and parsed file
    text = ls.document_content.get(uri)
    nl_file = ls.parsed_files.get(uri)

    if not text or not nl_file:
        return None

    # Find symbol at position
    symbol = find_symbol_at_position(text, nl_file, position.line, position.character)

    if not symbol:
        return None

    # Generate hover content based on symbol type
    content = _get_hover_content(nl_file, symbol)

    if content:
        return lsp.Hover(
            contents=lsp.MarkupContent(
                kind=lsp.MarkupKind.Markdown,
                value=content,
            ),
            range=lsp.Range(
                start=lsp.Position(line=symbol.line, character=symbol.start_char),
                end=lsp.Position(line=symbol.line, character=symbol.end_char),
            ),
        )

    return None


# NLS keywords and built-in types for completions
NLS_KEYWORDS = [
    "PURPOSE",
    "INPUTS",
    "GUARDS",
    "LOGIC",
    "RETURNS",
    "DEPENDS",
    "CALLS",
    "NOTES",
    "EXAMPLES",
]

NLS_BUILTIN_TYPES = [
    "number",
    "string",
    "boolean",
    "list",
    "dict",
    "any",
]

NLS_CONSTRAINTS = [
    "required",
    "positive",
    "non-negative",
    "min:",
    "max:",
]


def _has_type_in_prefix(prefix: str, types: list[str]) -> bool:
    """Check if prefix contains a type name as a whole word."""
    for t in types:
        if re.search(rf"\b{re.escape(t)}\b", prefix):
            return True
    return False


@server.feature(
    lsp.TEXT_DOCUMENT_COMPLETION,
    lsp.CompletionOptions(trigger_characters=["[", ":", "@", " "]),
)
def completions(
    ls: NLSLanguageServer,
    params: lsp.CompletionParams,
) -> lsp.CompletionList | None:
    """Provide completion suggestions."""
    uri = params.text_document.uri
    position = params.position

    text = ls.document_content.get(uri)
    nl_file = ls.parsed_files.get(uri)

    if not text:
        return None

    lines = text.split("\n")
    if position.line >= len(lines):
        return None

    current_line = lines[position.line]
    prefix = current_line[:position.character]

    items: list[lsp.CompletionItem] = []

    # Check context and provide appropriate completions

    # After [ - suggest ANLU names
    if "[" in prefix and "]" not in prefix[prefix.rfind("["):]:
        if nl_file:
            for anlu in nl_file.anlus:
                items.append(
                    lsp.CompletionItem(
                        label=anlu.identifier,
                        kind=lsp.CompletionItemKind.Function,
                        detail=anlu.purpose or "ANLU",
                        documentation=f"RETURNS: {anlu.returns}" if anlu.returns else None,
                    )
                )

    # After : - suggest types
    elif prefix.rstrip().endswith(":") or ": " in prefix[-5:]:
        # Built-in types
        for type_name in NLS_BUILTIN_TYPES:
            items.append(
                lsp.CompletionItem(
                    label=type_name,
                    kind=lsp.CompletionItemKind.TypeParameter,
                    detail="Built-in type",
                )
            )
        # Custom types from file
        if nl_file:
            for type_def in nl_file.module.types:
                items.append(
                    lsp.CompletionItem(
                        label=type_def.name,
                        kind=lsp.CompletionItemKind.Class,
                        detail=f"@type with {len(type_def.fields)} fields",
                    )
                )

    # After @ - suggest directives
    elif prefix.rstrip().endswith("@"):
        directives = ["module", "target", "version", "type", "invariant", "property", "test", "main"]
        for directive in directives:
            items.append(
                lsp.CompletionItem(
                    label=directive,
                    kind=lsp.CompletionItemKind.Keyword,
                    detail="NLS directive",
                )
            )

    # Start of line after ANLU header - suggest keywords
    elif prefix.strip() == "" or prefix.strip().isupper():
        for keyword in NLS_KEYWORDS:
            items.append(
                lsp.CompletionItem(
                    label=keyword,
                    kind=lsp.CompletionItemKind.Keyword,
                    detail="NLS section keyword",
                    insert_text=f"{keyword}:",
                )
            )

    # After type declaration - suggest constraints (use word-boundary matching)
    elif _has_type_in_prefix(prefix, NLS_BUILTIN_TYPES) or (nl_file and _has_type_in_prefix(prefix, [t.name for t in nl_file.module.types])):
        for constraint in NLS_CONSTRAINTS:
            items.append(
                lsp.CompletionItem(
                    label=constraint,
                    kind=lsp.CompletionItemKind.Property,
                    detail="Field constraint",
                )
            )

    if not items:
        return None

    return lsp.CompletionList(is_incomplete=False, items=items)


@server.feature(lsp.TEXT_DOCUMENT_DEFINITION)
def definition(
    ls: NLSLanguageServer,
    params: lsp.DefinitionParams,
) -> lsp.Location | None:
    """Go to definition of a symbol."""
    uri = params.text_document.uri
    position = params.position

    text = ls.document_content.get(uri)
    nl_file = ls.parsed_files.get(uri)

    if not text or not nl_file:
        return None

    # Find symbol at position
    symbol = find_symbol_at_position(text, nl_file, position.line, position.character)

    if not symbol:
        return None

    # Find definition location
    def_location = find_definition_location(text, symbol.name, symbol.kind)

    if def_location:
        return lsp.Location(
            uri=uri,
            range=lsp.Range(
                start=lsp.Position(line=def_location.line, character=def_location.start_char),
                end=lsp.Position(line=def_location.line, character=def_location.end_char),
            ),
        )

    return None


@server.feature(lsp.TEXT_DOCUMENT_REFERENCES)
def references(
    ls: NLSLanguageServer,
    params: lsp.ReferenceParams,
) -> list[lsp.Location] | None:
    """Find all references to a symbol."""
    uri = params.text_document.uri
    position = params.position

    text = ls.document_content.get(uri)
    nl_file = ls.parsed_files.get(uri)

    if not text or not nl_file:
        return None

    # Find symbol at position
    symbol = find_symbol_at_position(text, nl_file, position.line, position.character)

    if not symbol:
        return None

    # Find all references
    refs = find_all_references(text, symbol.name, symbol.kind)

    if not refs:
        return None

    return [
        lsp.Location(
            uri=uri,
            range=lsp.Range(
                start=lsp.Position(line=ref.line, character=ref.start_char),
                end=lsp.Position(line=ref.line, character=ref.end_char),
            ),
        )
        for ref in refs
    ]


@server.feature(lsp.TEXT_DOCUMENT_FORMATTING)
def formatting(
    ls: NLSLanguageServer,
    params: lsp.DocumentFormattingParams,
) -> list[lsp.TextEdit] | None:
    """Format the entire document."""
    uri = params.text_document.uri
    text = ls.document_content.get(uri)

    if not text:
        return None

    formatted = _format_nl_document(text)

    if formatted == text:
        return None

    # Return a single edit that replaces the entire document
    lines = text.split("\n")
    end_line = max(0, len(lines) - 1)
    end_char = len(lines[-1]) if lines else 0
    return [
        lsp.TextEdit(
            range=lsp.Range(
                start=lsp.Position(line=0, character=0),
                end=lsp.Position(line=end_line, character=end_char),
            ),
            new_text=formatted,
        )
    ]


def _format_nl_document(text: str) -> str:
    """Format an NLS document.

    Formatting rules:
    - Normalize section keywords to uppercase
    - Ensure consistent indentation (2 spaces for list items)
    - Single blank line between major sections
    - Trim trailing whitespace
    - Ensure file ends with newline
    """
    lines = text.split("\n")
    formatted_lines: list[str] = []
    in_section = False
    prev_was_blank = False

    section_keywords = {
        "purpose", "inputs", "guards", "logic", "returns",
        "depends", "calls", "notes", "examples",
    }

    for line in lines:
        stripped = line.strip()

        # Handle blank lines
        if not stripped:
            if not prev_was_blank and formatted_lines:
                formatted_lines.append("")
                prev_was_blank = True
            continue

        prev_was_blank = False

        # Check for section keywords
        lower_stripped = stripped.lower()
        if lower_stripped.rstrip(":") in section_keywords:
            # Normalize to uppercase with colon
            keyword = lower_stripped.rstrip(":").upper()
            formatted_lines.append(f"{keyword}:")
            in_section = True
            continue

        # Check for ANLU header [name]
        if stripped.startswith("[") and "]" in stripped:
            # Add blank line before ANLU if needed
            if formatted_lines and formatted_lines[-1] != "":
                formatted_lines.append("")
            formatted_lines.append(stripped)
            in_section = False
            continue

        # Check for directives (@module, @type, etc.)
        if stripped.startswith("@"):
            formatted_lines.append(stripped)
            in_section = stripped.startswith("@type")
            continue

        # Check for list items
        if stripped.startswith("-"):
            # Ensure 2-space indent for list items
            content = stripped[1:].strip()
            formatted_lines.append(f"  - {content}")
            continue

        # Check for numbered items (handles multi-digit: 1., 10., 100., etc.)
        if stripped and stripped[0].isdigit():
            # Find where the number ends
            dot_pos = 0
            while dot_pos < len(stripped) and stripped[dot_pos].isdigit():
                dot_pos += 1
            if dot_pos < len(stripped) and stripped[dot_pos] == ".":
                # Ensure 2-space indent for numbered items
                number = stripped[:dot_pos]
                content = stripped[dot_pos + 1 :].strip()
                formatted_lines.append(f"  {number}. {content}")
                continue

        # Type field lines (inside @type block)
        if in_section and ":" in stripped:
            # Indent type fields
            formatted_lines.append(f"  {stripped}")
            continue

        # Check for closing brace
        if stripped == "}":
            formatted_lines.append("}")
            in_section = False
            continue

        # Default: preserve line with trimmed trailing space
        formatted_lines.append(stripped)

    # Ensure file ends with newline
    result = "\n".join(formatted_lines)
    if result and not result.endswith("\n"):
        result += "\n"

    return result


def _parse_and_publish_diagnostics(
    ls: NLSLanguageServer,
    uri: str,
    text: str,
) -> None:
    """Parse document and publish diagnostics."""
    diagnostics: list[lsp.Diagnostic] = []

    try:
        nl_file = parse_nl_file(text)
        ls.parsed_files[uri] = nl_file

        # Check for semantic issues
        diagnostics.extend(_check_semantic_issues(nl_file))

    except Exception as e:
        # Parse error - create diagnostic
        error_msg = str(e)
        line = 0
        character = 0

        # Try to extract line number from error message
        if "line" in error_msg.lower():
            match = re.search(r"line\s*(\d+)", error_msg, re.IGNORECASE)
            if match:
                line = max(0, int(match.group(1)) - 1)  # LSP is 0-indexed

        diagnostics.append(
            lsp.Diagnostic(
                range=lsp.Range(
                    start=lsp.Position(line=line, character=character),
                    end=lsp.Position(line=line, character=1000),
                ),
                message=error_msg,
                severity=lsp.DiagnosticSeverity.Error,
                source="nlsc",
            )
        )

    ls.diagnostics_cache[uri] = diagnostics
    ls.text_document_publish_diagnostics(
        lsp.PublishDiagnosticsParams(uri=uri, diagnostics=diagnostics)
    )

def _check_semantic_issues(nl_file: NLFile) -> list[lsp.Diagnostic]:
    """Check for semantic issues in parsed NLFile."""
    diagnostics: list[lsp.Diagnostic] = []

    # Standard library modules that should use regular import
    STDLIB_MODULES = {
        "os", "sys", "re", "json", "math", "random", "time", "datetime",
        "collections", "itertools", "functools", "typing", "pathlib",
        "threading", "multiprocessing", "ctypes", "subprocess", "io",
        "copy", "pickle", "hashlib", "base64", "urllib", "http",
        "logging", "unittest", "dataclasses", "abc", "enum", "asyncio",
    }

    # Check @imports for any issues
    if nl_file.module.imports:
        for imp in nl_file.module.imports:
            imp_name = imp.strip()
            if imp_name in STDLIB_MODULES:
                # Info: stdlib modules will be imported correctly
                pass
            elif imp_name and not imp_name[0].islower():
                # Custom module names should be lowercase
                diagnostics.append(
                    lsp.Diagnostic(
                        range=lsp.Range(
                            start=lsp.Position(line=0, character=0),
                            end=lsp.Position(line=0, character=100),
                        ),
                        message=f"Import '{imp_name}' should be lowercase for custom modules",
                        severity=lsp.DiagnosticSeverity.Hint,
                        source="nlsc",
                    )
                )

    # Check type definitions for invalid syntax
    for type_def in nl_file.module.types:
        type_line = max(0, type_def.line_number - 1) if type_def.line_number else 0
        for field in type_def.fields:
            # Check for type? syntax with redundant optional constraint
            if field.type.endswith("?") and "optional" in [c.lower() for c in field.constraints]:
                diagnostics.append(
                    lsp.Diagnostic(
                        range=lsp.Range(
                            start=lsp.Position(line=type_line, character=0),
                            end=lsp.Position(line=type_line + 5, character=100),
                        ),
                        message=f"Field '{field.name}' uses both '?' suffix and 'optional' constraint - redundant",
                        severity=lsp.DiagnosticSeverity.Hint,
                        source="nlsc",
                    )
                )

    # Build set of all defined ANLU names for validation
    defined_anlus = {a.identifier for a in nl_file.anlus}

    # Check for missing PURPOSE in ANLUs and other logic issues
    for anlu in nl_file.anlus:
        # Convert 1-indexed parser line_number to 0-indexed LSP position
        anlu_line = max(0, anlu.line_number - 1) if anlu.line_number else 0

        if not anlu.purpose:
            diagnostics.append(
                lsp.Diagnostic(
                    range=lsp.Range(
                        start=lsp.Position(line=anlu_line, character=0),
                        end=lsp.Position(line=anlu_line, character=100),
                    ),
                    message=f"ANLU [{anlu.identifier}] is missing PURPOSE",
                    severity=lsp.DiagnosticSeverity.Warning,
                    source="nlsc",
                )
            )

        # Validate RETURNS consistency
        if anlu.returns:
            input_names = {i.name for i in anlu.inputs}
            assigned_vars = set()
            for step in anlu.logic_steps:
                assigned_vars.update(step.assigns)

            # Extract simple variable name from RETURNS (ignore expressions for now)
            # Only check if it's a simple identifier
            ret_var = anlu.returns.strip()
            if ret_var.isidentifier() and not ret_var.startswith("f'") and not ret_var.startswith('"'):
                if ret_var not in input_names and ret_var not in assigned_vars:
                    # Check if it's a literal or type
                    is_literal = ret_var in ["True", "False", "None"] or ret_var[0].isupper() or ret_var.isdigit()
                    if not is_literal:
                        diagnostics.append(
                            lsp.Diagnostic(
                                range=lsp.Range(
                                    start=lsp.Position(line=anlu_line, character=0),
                                    end=lsp.Position(line=anlu_line, character=100),
                                ),
                                message=f"RETURNS '{ret_var}' is undefined (not in INPUTS or LOGIC assignments)",
                                severity=lsp.DiagnosticSeverity.Error,
                                source="nlsc",
                            )
                        )

        # Validate LOGIC steps
        for step in anlu.logic_steps:
            # Check for undefined ANLU references in logic
            # Regex to find [anlu-name] in description
            for m in re.finditer(r'\[([a-zA-Z][a-zA-Z0-9_-]*)\]', step.description):
                ref_name = m.group(1)
                if ref_name not in defined_anlus:
                    diagnostics.append(
                        lsp.Diagnostic(
                            range=lsp.Range(
                                start=lsp.Position(line=anlu_line, character=0),
                                end=lsp.Position(line=anlu_line, character=100),
                            ),
                            message=f"LOGIC references undefined ANLU [{ref_name}]",
                            severity=lsp.DiagnosticSeverity.Warning,
                            source="nlsc",
                        )
                    )

            # Check for descriptive steps with bindings but no code
            # If step has output binding (-> var) but no [anlu] ref and no assignment (=)
            is_assignment = "=" in step.description and "==" not in step.description
            has_anlu_ref = "[" in step.description and "]" in step.description

            if step.output_binding and not is_assignment and not has_anlu_ref:
                diagnostics.append(
                    lsp.Diagnostic(
                        range=lsp.Range(
                            start=lsp.Position(line=anlu_line, character=0),
                            end=lsp.Position(line=anlu_line, character=100),
                        ),
                        message=f"Logic step {step.number} has binding '{step.output_binding}' but no executable action. Use [anlu-name] or explicit assignment.",
                        severity=lsp.DiagnosticSeverity.Warning,
                        source="nlsc",
                    )
                )

    return diagnostics



@server.feature(lsp.TEXT_DOCUMENT_CODE_LENS)
def code_lens(ls: NLSLanguageServer, params: lsp.CodeLensParams) -> list[lsp.CodeLens] | None:
    """Provide code lenses for runnable blocks (@test, @main)."""
    uri = params.text_document.uri
    text = ls.document_content.get(uri)

    if not text:
        return None

    lenses: list[lsp.CodeLens] = []
    lines = text.split("\n")

    for i, line in enumerate(lines):
        stripped = line.strip()

        # @test block -> Run Test
        if stripped.startswith("@test") and "{" in stripped:
            # Extract test name, handling brackets: @test [name] or @test name
            match = re.search(r"@test\s+(?:\[)?([a-zA-Z0-9_-]+)(?:\])?", stripped)
            if match:
                raw_name = match.group(1)
                # Normalize to match emit_tests class name: TestName (TitleCase with underscores)
                # calculate-tax -> calculate_tax -> Calculate_Tax
                norm_name = raw_name.replace("-", "_").title()
                test_class = f"Test{norm_name}"

                lenses.append(
                    lsp.CodeLens(
                        range=lsp.Range(
                            start=lsp.Position(line=i, character=0),
                            end=lsp.Position(line=i, character=len(line)),
                        ),
                        command=lsp.Command(
                            title="Run Test",
                            command="nls.test",
                            arguments=[test_class],
                        ),
                    )
                )

        # @main block -> Run Program
        elif stripped.startswith("@main") and "{" in stripped:
            lenses.append(
                lsp.CodeLens(
                    range=lsp.Range(
                        start=lsp.Position(line=i, character=0),
                        end=lsp.Position(line=i, character=len(line)),
                    ),
                    command=lsp.Command(
                        title="Run Program",
                        command="nls.run",
                    ),
                )
            )

    return lenses


def start_server(
    transport: str = "stdio",
    host: str = "127.0.0.1",
    port: int = 2087,
) -> None:
    """Start the NLS language server.

    Args:
        transport: Communication transport ("stdio" or "tcp")
        host: Host address for TCP mode (default: "127.0.0.1")
        port: Port number for TCP mode (default: 2087)
    """
    if transport == "stdio":
        server.start_io()
    elif transport == "tcp":
        server.start_tcp(host, port)
    else:
        raise ValueError(f"Unknown transport: {transport}")


if __name__ == "__main__":
    start_server()
