"""
Natural Language Source Compiler (nlsc)

The conversation is the programming. The .nl file is the receipt. The code is the artifact.
"""

__version__ = "0.1.0"
__author__ = "Vario (Mnehmos)"

from .schema import ANLU, Module, NLFile
from .parser import parse_nl_file
from .emitter import emit_python

__all__ = [
    "ANLU",
    "Module",
    "NLFile",
    "parse_nl_file",
    "emit_python",
]
