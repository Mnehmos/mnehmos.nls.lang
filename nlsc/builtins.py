"""Target-neutral builtin function table.

Shared by the type checker (signatures and `ESEM009` foreign-call
diagnostics) and the effect analysis (builtins are world-free, so they
must not infer an `unknown` effect — issue #197).
"""

from __future__ import annotations

# Documented builtin signatures.  Everything here is target-neutral;
# anything outside this table is a foreign call (see ESEM009).
BUILTIN_SIGNATURES: dict[str, tuple[tuple[str, ...], str]] = {
    "len": (("any",), "integer"),
    "sum": (("list of number",), "number"),
    "max": (("number",), "number"),  # variadic or list
    "min": (("number",), "number"),
    "abs": (("number",), "number"),
    "round": (("number",), "number"),
    "sqrt": (("number",), "number"),
    "str": (("any",), "string"),
    "int": (("any",), "integer"),
    "float": (("any",), "number"),
    "bool": (("any",), "boolean"),
}

BUILTIN_NAMES: frozenset[str] = frozenset(BUILTIN_SIGNATURES)
