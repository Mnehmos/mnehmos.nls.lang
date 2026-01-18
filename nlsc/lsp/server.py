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
    find_anlu_by_name,
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
    ls.publish_diagnostics(uri, [])


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
    ls.publish_diagnostics(uri, diagnostics)


def _check_semantic_issues(nl_file: NLFile) -> list[lsp.Diagnostic]:
    """Check for semantic issues in parsed NLFile."""
    diagnostics: list[lsp.Diagnostic] = []

    # Check for missing PURPOSE in ANLUs
    for anlu in nl_file.anlus:
        if not anlu.purpose:
            diagnostics.append(
                lsp.Diagnostic(
                    range=lsp.Range(
                        start=lsp.Position(line=0, character=0),
                        end=lsp.Position(line=0, character=100),
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
                        start=lsp.Position(line=0, character=0),
                        end=lsp.Position(line=0, character=100),
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
