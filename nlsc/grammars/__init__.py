"""
Bundled tree-sitter grammar libraries for NLS.

This package contains pre-compiled tree-sitter grammar libraries
for parsing .nl files. Platform-specific libraries:
- nl.dll (Windows)
- nl.so (Linux)
- nl.dylib (macOS)
"""

from pathlib import Path

GRAMMAR_DIR = Path(__file__).parent


def get_grammar_path() -> Path:
    """Get the path to the grammar directory."""
    return GRAMMAR_DIR
