"""NLS Language Server Protocol implementation.

Provides editor-agnostic language intelligence for .nl files using LSP.
"""

from nlsc.lsp.server import NLSLanguageServer, start_server

__all__ = ["NLSLanguageServer", "start_server"]
