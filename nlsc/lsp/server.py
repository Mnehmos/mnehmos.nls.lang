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
from typing import TYPE_CHECKING

from lsprotocol import types as lsp
from pygls.lsp.server import LanguageServer

from nlsc.lsp.analysis import (
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

if TYPE_CHECKING:
    pass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NLSLanguageServer(LanguageServer):
    """Language server for NLS (.nl) files."""

    def __init__(self) -> None:
        super().__init__(
            name="nls-language-server",
            version="0.1.0",
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
    content: str | None = None

    if symbol.kind == "anlu":
        anlu = find_anlu_by_name(nl_file, symbol.name)
        if anlu:
            content = get_anlu_hover_content(anlu)

    elif symbol.kind == "anlu_ref":
        anlu = find_anlu_by_name(nl_file, symbol.name)
        if anlu:
            content = get_anlu_hover_content(anlu)

    elif symbol.kind == "type":
        type_def = find_type_by_name(nl_file, symbol.name)
        if type_def:
            content = get_type_hover_content(type_def)

    elif symbol.kind == "type_ref":
        type_def = find_type_by_name(nl_file, symbol.name)
        if type_def:
            content = get_type_hover_content(type_def)

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

    # After type declaration - suggest constraints
    elif any(t in prefix for t in NLS_BUILTIN_TYPES) or (nl_file and any(t.name in prefix for t in nl_file.module.types)):
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
            import re
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

    # Check for missing PURPOSE in ANLUs
    for anlu in nl_file.anlus:
        anlu_line = anlu.line_number if anlu.line_number else 0
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

        # Check for RETURNS without LOGIC in functions with complex returns
        if anlu.returns and not anlu.logic and "+" in anlu.returns:
            diagnostics.append(
                lsp.Diagnostic(
                    range=lsp.Range(
                        start=lsp.Position(line=anlu_line, character=0),
                        end=lsp.Position(line=anlu_line, character=100),
                    ),
                    message=f"ANLU [{anlu.identifier}] has complex RETURNS but no LOGIC steps",
                    severity=lsp.DiagnosticSeverity.Hint,
                    source="nlsc",
                )
            )

    return diagnostics


def start_server(transport: str = "stdio") -> None:
    """Start the NLS language server.

    Args:
        transport: Communication transport ("stdio" or "tcp")
    """
    if transport == "stdio":
        server.start_io()
    elif transport == "tcp":
        server.start_tcp("127.0.0.1", 2087)
    else:
        raise ValueError(f"Unknown transport: {transport}")


if __name__ == "__main__":
    start_server()
