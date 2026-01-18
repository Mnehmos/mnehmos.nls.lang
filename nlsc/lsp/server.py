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
        # Cache of parse errors: uri -> list of diagnostics
        self.diagnostics_cache: dict[str, list[lsp.Diagnostic]] = {}


# Create the server instance
server = NLSLanguageServer()


@server.feature(lsp.TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: NLSLanguageServer, params: lsp.DidOpenTextDocumentParams) -> None:
    """Handle document open - parse and publish diagnostics."""
    uri = params.text_document.uri
    text = params.text_document.text
    _parse_and_publish_diagnostics(ls, uri, text)


@server.feature(lsp.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: NLSLanguageServer, params: lsp.DidChangeTextDocumentParams) -> None:
    """Handle document change - reparse and publish diagnostics."""
    uri = params.text_document.uri
    # Get the full text from the change (we use full sync)
    if params.content_changes:
        text = params.content_changes[-1].text
        _parse_and_publish_diagnostics(ls, uri, text)


@server.feature(lsp.TEXT_DOCUMENT_DID_CLOSE)
def did_close(ls: NLSLanguageServer, params: lsp.DidCloseTextDocumentParams) -> None:
    """Handle document close - clean up caches."""
    uri = params.text_document.uri
    ls.parsed_files.pop(uri, None)
    ls.diagnostics_cache.pop(uri, None)
    # Clear diagnostics for closed file
    ls.publish_diagnostics(uri, [])


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
