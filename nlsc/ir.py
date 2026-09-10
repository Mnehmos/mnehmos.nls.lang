"""Target-neutral NLS intermediate representation (IR).

This module defines the checked-IR boundary between the surface AST
(``nlsc.schema``) and the language emitters.  An ``IRModule`` is a
deterministic, target-neutral lowering of one ``.nl`` file:

* The same source always produces byte-identical canonical text,
  regardless of ``@target``.
* Every node carries a stable deterministic id and a :class:`SourceSpan`
  that identifies the contributing surface syntax (ANLU, LOGIC step
  number, and source line).
* Constructs that are not part of the structurally supported core are
  represented *explicitly* as :class:`ForeignExpr` / :class:`ForeignStmt`
  nodes.  They never silently become target source or placeholders; the
  lowering records a diagnostic for each one, and
  :func:`assert_checked_module` refuses to mark a module eligible for
  checked emission while any remain.

The schema is versioned (``IR_SCHEMA_VERSION``).  Serialization is both
human-readable canonical text (:func:`module_to_canonical`) and JSON
(:func:`module_to_json`); both are stable interchange formats intended
for LLM/tooling round-trips.  See ``docs/ir-spec.md`` for the grammar
and the extension policy.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterator, Optional, Union

IR_SCHEMA_VERSION = "0.1"

# --------------------------------------------------------------------------
# Identity: spans and ids
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class SourceSpan:
    """Where an IR node came from in the original ``.nl`` source."""

    anlu: str
    line: Optional[int] = None
    step: Optional[int] = None

    def to_json(self) -> dict[str, object]:
        return {"anlu": self.anlu, "line": self.line, "step": self.step}

    def render(self) -> str:
        parts = [f"anlu={self.anlu}"]
        if self.step is not None:
            parts.append(f"step={self.step}")
        if self.line is not None:
            parts.append(f"line={self.line}")
        return " ".join(parts)


def make_span(anlu: str, line: Optional[int] = None, step: Optional[int] = None) -> SourceSpan:
    return SourceSpan(anlu=anlu, line=line, step=step)


# --------------------------------------------------------------------------
# Type references (target-neutral)
# --------------------------------------------------------------------------

_PRIMITIVE_TYPES = ("number", "integer", "string", "boolean", "void", "any", "none")


@dataclass(frozen=True)
class TypeRef:
    """A target-neutral type reference.

    ``name`` is one of the primitives, ``list`` (with one argument), or a
    declared record type name.  ``unknown=True`` marks an unresolved name
    (an *explicit* unknown, never a silent ``any``).
    """

    name: str
    args: tuple["TypeRef", ...] = ()
    optional: bool = False
    raw: str = ""

    @property
    def is_primitive(self) -> bool:
        return not self.args and self.name in _PRIMITIVE_TYPES

    def render(self) -> str:
        if self.args:
            inner = " ".join(arg.render() for arg in self.args)
            rendered = f"({self.name} {inner})"
        else:
            rendered = self.name
        if self.optional:
            rendered += " optional"
        return rendered

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {"name": self.name}
        if self.args:
            data["args"] = [arg.to_json() for arg in self.args]
        if self.optional:
            data["optional"] = True
        if self.raw:
            data["raw"] = self.raw
        return data


def type_ref_from_text(text: str) -> TypeRef:
    """Parse a surface type spelling into a target-neutral TypeRef."""
    raw = text.strip()
    candidate = raw
    optional = False
    if candidate.endswith("?"):
        candidate = candidate[:-1].strip()
        optional = True

    lowered = candidate.lower()
    alias_map = {
        "integer": "integer",
        "float": "number",
        "dict": "dictionary",
        "dictionary": "dictionary",
        "list": "list",
        "none": "void",
        "null": "void",
    }
    if lowered in ("number", "string", "boolean", "any", "void"):
        name: str = lowered
        return TypeRef(name=name, optional=optional, raw=raw)
    if lowered in alias_map:
        return TypeRef(name=alias_map[lowered], optional=optional, raw=raw)

    if lowered.startswith("list of "):
        inner = type_ref_from_text(candidate[8:])
        return TypeRef(name="list", args=(inner,), optional=optional, raw=raw)
    if lowered.startswith("list[") and candidate.endswith("]"):
        inner = type_ref_from_text(candidate[5:-1])
        return TypeRef(name="list", args=(inner,), optional=optional, raw=raw)

    # "X or null" / "X or none" nullable spelling
    or_none = None
    for sep in (" or null", " or none"):
        if lowered.endswith(sep):
            or_none = candidate[: -len(sep)]
            break
    if or_none is not None:
        return TypeRef(
            name=type_ref_from_text(or_none).name,
            args=type_ref_from_text(or_none).args,
            optional=True,
            raw=raw,
        )

    # Unknown/custom type name — preserved verbatim and marked via name.
    return TypeRef(name=candidate, optional=optional, raw=raw)


# --------------------------------------------------------------------------
# Values (expressions)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class IRLiteral:
    """A literal whose raw token is preserved exactly.

    ``raw`` is the exact source token (strings keep their quotes);
    ``value`` is the decoded value used for canonical rendering, so
    equivalent ``'x'`` and ``"x"`` spellings serialize identically.
    """

    kind: str  # "number" | "string" | "boolean" | "none"
    raw: str
    value: object = None
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        if self.kind == "string":
            return f"(lit {json.dumps(self.value)})"
        return f"(lit {self.raw})"

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "kind": "literal",
            "literal_kind": self.kind,
            "raw": self.raw,
            "value": self.value,
            "id": self.id,
            "span": self.span.to_json() if self.span else None,
        }
        return data


@dataclass(frozen=True)
class IRRef:
    """A reference to a local binding or parameter."""

    name: str
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        return f"(ref {self.name})"

    def to_json(self) -> dict[str, object]:
        return {
            "kind": "ref",
            "name": self.name,
            "id": self.id,
            "span": self.span.to_json() if self.span else None,
        }


@dataclass(frozen=True)
class IRFieldAccess:
    """``base.field`` access."""

    base: "IRExpr"
    field_name: str
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        return f"(get {self.base.render()} {self.field_name})"

    def to_json(self) -> dict[str, object]:
        return {
            "kind": "field",
            "base": self.base.to_json(),
            "field": self.field_name,
            "id": self.id,
            "span": self.span.to_json() if self.span else None,
        }


@dataclass(frozen=True)
class IRIndexAccess:
    """``base[index]`` access."""

    base: "IRExpr"
    index: "IRExpr"
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        return f"(at {self.base.render()} {self.index.render()})"

    def to_json(self) -> dict[str, object]:
        return {
            "kind": "index",
            "base": self.base.to_json(),
            "index": self.index.to_json(),
            "id": self.id,
            "span": self.span.to_json() if self.span else None,
        }


@dataclass(frozen=True)
class IRList:
    """List construction ``[a, b, ...]``."""

    items: tuple["IRExpr", ...]
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        return "(list {})".format(" ".join(item.render() for item in self.items))

    def to_json(self) -> dict[str, object]:
        return {
            "kind": "list",
            "items": [item.to_json() for item in self.items],
            "id": self.id,
            "span": self.span.to_json() if self.span else None,
        }


@dataclass(frozen=True)
class IRUnary:
    """Unary operation; op is one of ``neg``, ``not``."""

    op: str
    operand: "IRExpr"
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        return f"(unary {self.op} {self.operand.render()})"

    def to_json(self) -> dict[str, object]:
        return {
            "kind": "unary",
            "op": self.op,
            "operand": self.operand.to_json(),
            "id": self.id,
            "span": self.span.to_json() if self.span else None,
        }


# Normalized binary operator names (target-neutral).
BINARY_OPS = {
    "+": "add",
    "-": "sub",
    "*": "mul",
    "×": "mul",
    "/": "div",
    "÷": "div",
    "//": "floor_div",
    "%": "mod",
    "**": "pow",
    "==": "eq",
    "!=": "ne",
    "<": "lt",
    "<=": "le",
    ">": "gt",
    ">=": "ge",
    "and": "and",
    "or": "or",
    "is": "is",
    "in": "in",
}


@dataclass(frozen=True)
class IRBinary:
    """Binary operation with a normalized operator name."""

    op: str  # add sub mul div floor_div mod pow eq ne lt le gt ge and or is in
    left: "IRExpr"
    right: "IRExpr"
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        return f"(binary {self.op} {self.left.render()} {self.right.render()})"

    def to_json(self) -> dict[str, object]:
        return {
            "kind": "binary",
            "op": self.op,
            "left": self.left.to_json(),
            "right": self.right.to_json(),
            "id": self.id,
            "span": self.span.to_json() if self.span else None,
        }


@dataclass(frozen=True)
class IRCall:
    """A resolved call: ANLU call, builtin, constructor, or foreign function.

    ``anlu`` is True for ``[anlu-name](args)`` calls (kebab-case target).
    ``kwargs`` preserves keyword construction arguments.
    """

    target: str
    args: tuple["IRExpr", ...] = ()
    kwargs: tuple[tuple[str, "IRExpr"], ...] = ()
    anlu: bool = False
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        pieces = [self.target]
        pieces.extend(arg.render() for arg in self.args)
        pieces.extend(f"({name} {value.render()})" for name, value in self.kwargs)
        marker = "anlu" if self.anlu else "call"
        return f"({marker} {' '.join(pieces)})"

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "kind": "anlu_call" if self.anlu else "call",
            "target": self.target,
            "args": [arg.to_json() for arg in self.args],
        }
        if self.kwargs:
            data["kwargs"] = [
                {"name": name, "value": value.to_json()} for name, value in self.kwargs
            ]
        data["id"] = self.id
        data["span"] = self.span.to_json() if self.span else None
        return data


@dataclass(frozen=True)
class IRMethodCall:
    """``base.method(args)`` — structurally represented; resolution is a later pass."""

    base: "IRExpr"
    method: str
    args: tuple["IRExpr", ...] = ()
    kwargs: tuple[tuple[str, "IRExpr"], ...] = ()
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        pieces = [self.base.render(), f".{self.method}"]
        pieces.extend(arg.render() for arg in self.args)
        pieces.extend(f"({name} {value.render()})" for name, value in self.kwargs)
        return f"(method {' '.join(pieces)})"

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "kind": "method_call",
            "base": self.base.to_json(),
            "method": self.method,
            "args": [arg.to_json() for arg in self.args],
        }
        if self.kwargs:
            data["kwargs"] = [
                {"name": name, "value": value.to_json()} for name, value in self.kwargs
            ]
        data["id"] = self.id
        data["span"] = self.span.to_json() if self.span else None
        return data


@dataclass(frozen=True)
class ForeignExpr:
    """An expression kept verbatim because it is outside the supported core.

    A foreign expression is *never* evidence of validity: lowering always
    records a diagnostic for it, and a checked module cannot contain one.
    ``reason`` documents why (e.g. ``comprehension``, ``ternary``,
    ``fstring``, ``prose``, ``unsupported-syntax``).
    """

    raw: str
    reason: str
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        return f"(foreign reason={self.reason} {json.dumps(self.raw)})"

    def to_json(self) -> dict[str, object]:
        return {
            "kind": "foreign_expr",
            "raw": self.raw,
            "reason": self.reason,
            "id": self.id,
            "span": self.span.to_json() if self.span else None,
        }


IRExpr = Union[
    IRLiteral,
    IRRef,
    IRFieldAccess,
    IRIndexAccess,
    IRList,
    IRUnary,
    IRBinary,
    IRCall,
    IRMethodCall,
    ForeignExpr,
]


def iter_expr_nodes(expr: IRExpr) -> Iterator[IRExpr]:
    """Yield ``expr`` and every nested value node."""
    yield expr
    children: tuple[IRExpr, ...] = ()
    if isinstance(expr, IRFieldAccess):
        children = (expr.base,)
    elif isinstance(expr, IRIndexAccess):
        children = (expr.base, expr.index)
    elif isinstance(expr, IRList):
        children = tuple(expr.items)
    elif isinstance(expr, IRUnary):
        children = (expr.operand,)
    elif isinstance(expr, IRBinary):
        children = (expr.left, expr.right)
    elif isinstance(expr, IRCall):
        children = tuple(expr.args) + tuple(v for _, v in expr.kwargs)
    elif isinstance(expr, IRMethodCall):
        children = (expr.base,) + tuple(expr.args) + tuple(v for _, v in expr.kwargs)
    for child in children:
        yield from iter_expr_nodes(child)


# --------------------------------------------------------------------------
# Statements and regions
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class IRBind:
    """Bind a name to a value; ``aug`` marks an augmented rebind (e.g. +=)."""

    name: str
    value: IRExpr
    aug: Optional[str] = None  # add sub mul div mod ... when augmented
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        aug_part = f" aug={self.aug}" if self.aug else ""
        return f"(bind{aug_part} {self.name} {self.value.render()})"

    def to_json(self) -> dict[str, object]:
        return {
            "kind": "bind",
            "name": self.name,
            "value": self.value.to_json(),
            "aug": self.aug,
            "id": self.id,
            "span": self.span.to_json() if self.span else None,
        }


@dataclass(frozen=True)
class IRDiscard:
    """An expression evaluated for its effects; its value is intentionally unused."""

    value: IRExpr
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        return f"(expr {self.value.render()})"

    def to_json(self) -> dict[str, object]:
        return {
            "kind": "discard",
            "value": self.value.to_json(),
            "id": self.id,
            "span": self.span.to_json() if self.span else None,
        }


@dataclass(frozen=True)
class IRReturn:
    """The operation's result expression."""

    value: IRExpr
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        return f"(return {self.value.render()})"

    def to_json(self) -> dict[str, object]:
        return {
            "kind": "return",
            "value": self.value.to_json(),
            "id": self.id,
            "span": self.span.to_json() if self.span else None,
        }


@dataclass(frozen=True)
class IRErrorSpec:
    """Normalized error identity and payload for guard failures."""

    error_type: str
    message: Optional[str] = None
    code: Optional[str] = None

    def render(self) -> str:
        parts = [self.error_type]
        if self.code:
            parts.append(f"code={self.code}")
        if self.message is not None:
            parts.append(json.dumps(self.message))
        return f"(error {' '.join(parts)})"

    def to_json(self) -> dict[str, object]:
        return {
            "type": self.error_type,
            "code": self.code,
            "message": self.message,
        }


@dataclass(frozen=True)
class IRGuard:
    """Raise ``error`` unless ``condition`` holds; guards evaluate in order."""

    condition: IRExpr
    error: Optional[IRErrorSpec] = None
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        error = self.error.render() if self.error else "(error unknown)"
        return f"(guard {self.condition.render()} -> {error})"

    def to_json(self) -> dict[str, object]:
        return {
            "kind": "guard",
            "condition": self.condition.to_json(),
            "error": self.error.to_json() if self.error else None,
            "id": self.id,
            "span": self.span.to_json() if self.span else None,
        }


@dataclass(frozen=True)
class IRBranch:
    """Conditional region: ``then`` always present, ``otherwise`` may be empty."""

    condition: IRExpr
    then_body: tuple["IRStmt", ...]
    otherwise: tuple["IRStmt", ...] = ()
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        parts = [f"(branch {self.condition.render()}"]
        parts.append("  " + _render_block(self.then_body, 2))
        if self.otherwise:
            parts.append("  else " + _render_block(self.otherwise, 2))
        parts.append(")")
        return "\n".join(parts)

    def to_json(self) -> dict[str, object]:
        return {
            "kind": "branch",
            "condition": self.condition.to_json(),
            "then": [stmt.to_json() for stmt in self.then_body],
            "else": [stmt.to_json() for stmt in self.otherwise],
            "id": self.id,
            "span": self.span.to_json() if self.span else None,
        }


@dataclass(frozen=True)
class IRLoop:
    """Explicit loop region (reserved: no ANLU LOGIC loop syntax lowers here yet)."""

    condition: IRExpr
    body: tuple["IRStmt", ...] = ()
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        return "(loop while {} {})".format(
            self.condition.render(), _render_block(self.body, 1)
        )

    def to_json(self) -> dict[str, object]:
        return {
            "kind": "loop",
            "condition": self.condition.to_json(),
            "body": [stmt.to_json() for stmt in self.body],
            "id": self.id,
            "span": self.span.to_json() if self.span else None,
        }


@dataclass(frozen=True)
class IRNote:
    """Attached narrative: executable order preserved, semantics-free."""

    text: str
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        return f"(note {json.dumps(self.text)})"

    def to_json(self) -> dict[str, object]:
        return {
            "kind": "note",
            "text": self.text,
            "id": self.id,
            "span": self.span.to_json() if self.span else None,
        }


@dataclass(frozen=True)
class ForeignStmt:
    """A statement kept verbatim because it is outside the supported core."""

    raw: str
    reason: str
    id: str = ""
    span: Optional[SourceSpan] = None

    def render(self) -> str:
        return f"(foreign-stmt reason={self.reason} {json.dumps(self.raw)})"

    def to_json(self) -> dict[str, object]:
        return {
            "kind": "foreign_stmt",
            "raw": self.raw,
            "reason": self.reason,
            "id": self.id,
            "span": self.span.to_json() if self.span else None,
        }


IRStmt = Union[
    IRBind,
    IRDiscard,
    IRReturn,
    IRGuard,
    IRBranch,
    IRLoop,
    IRNote,
    ForeignStmt,
]


def iter_stmt_nodes(stmts: tuple[IRStmt, ...]) -> Iterator[IRStmt]:
    """Yield every statement including nested branch/loop regions."""
    for stmt in stmts:
        yield stmt
        if isinstance(stmt, IRBranch):
            yield from iter_stmt_nodes(stmt.then_body)
            yield from iter_stmt_nodes(stmt.otherwise)
        elif isinstance(stmt, IRLoop):
            yield from iter_stmt_nodes(stmt.body)


def _render_block(stmts: tuple[IRStmt, ...], indent: int) -> str:
    if not stmts:
        return "()"
    pad = " " * indent
    inner = "\n".join(pad + stmt.render() for stmt in stmts)
    return "(\n" + inner + "\n" + " " * (indent - 1) + ")"


# --------------------------------------------------------------------------
# Operations, types, modules
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class IRParam:
    name: str
    type_ref: TypeRef
    optional: bool = False
    constraints: tuple[str, ...] = ()

    def render(self) -> str:
        opt = " optional" if self.optional else ""
        rendered = f"(param {self.name} {self.type_ref.render()}{opt}"
        for constraint in self.constraints:
            rendered += f" {json.dumps(constraint)}"
        return rendered + ")"

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "name": self.name,
            "type": self.type_ref.to_json(),
        }
        if self.optional:
            data["optional"] = True
        if self.constraints:
            data["constraints"] = list(self.constraints)
        return data


@dataclass(frozen=True)
class IRReturnSpec:
    """The semantic split of RETURNS into a declared type and a value expression.

    Both slots are optional and independently meaningful: a declared type
    alone is a contract, not a default value; a value expression alone is
    an inferred result.  ``raw`` preserves the surface spelling.
    """

    declared_type: Optional[TypeRef] = None
    value: Optional[IRExpr] = None
    raw: str = ""

    def render(self) -> str:
        inner = []
        if self.declared_type:
            inner.append(f"(type {self.declared_type.render()})")
        if self.value is not None:
            inner.append(f"(value {self.value.render()})")
        return f"(result {' '.join(inner)})" if inner else "(result)"

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {"raw": self.raw}
        if self.declared_type:
            data["type"] = self.declared_type.to_json()
        if self.value is not None:
            data["value"] = self.value.to_json()
        return data


@dataclass(frozen=True)
class IRRecordField:
    name: str
    type_ref: TypeRef
    constraints: tuple[str, ...] = ()
    description: Optional[str] = None

    def render(self) -> str:
        parts = [f"(field {self.name} {self.type_ref.render()}"]
        for constraint in self.constraints:
            parts.append(json.dumps(constraint))
        if self.description is not None:
            parts.append(json.dumps(self.description))
        parts.append(")")
        return " ".join(parts)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "name": self.name,
            "type": self.type_ref.to_json(),
        }
        if self.constraints:
            data["constraints"] = list(self.constraints)
        if self.description is not None:
            data["description"] = self.description
        return data


@dataclass(frozen=True)
class IRRecordType:
    name: str
    fields: tuple[IRRecordField, ...] = ()
    base: Optional[str] = None

    def render(self) -> str:
        header = f"(type {self.name}"
        if self.base:
            header += f" extends {self.base}"
        if not self.fields:
            return header + ")"
        lines = [header]
        lines.extend("  " + f.render() for f in self.fields)
        lines.append(")")
        return "\n".join(lines)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "name": self.name,
            "fields": [f.to_json() for f in self.fields],
        }
        if self.base:
            data["extends"] = self.base
        return data


@dataclass
class IROperation:
    """A lowered ANLU: executable structure plus attached narrative."""

    name: str  # kebab-case ANLU identifier
    purpose: str = ""
    params: tuple[IRParam, ...] = ()
    guards: tuple[IRGuard, ...] = ()
    body: tuple[IRStmt, ...] = ()
    result: Optional[IRReturnSpec] = None
    depends: tuple[str, ...] = ()
    literal: Optional[str] = None
    edge_cases: tuple[tuple[str, str], ...] = ()  # (condition, behavior) narrative
    span: Optional[SourceSpan] = None

    # Contract slots populated by later passes.  None means *not analyzed* —
    # it is never implicit proof of purity or absence of failures.
    effects: Optional[dict[str, object]] = None
    failures: Optional[tuple[object, ...]] = None
    typestate: Optional[dict[str, object]] = None

    def render(self, indent: str = "  ") -> str:
        return _render_operation(self, indent)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "name": self.name,
            "purpose": self.purpose,
            "params": [p.to_json() for p in self.params],
            "guards": [g.to_json() for g in self.guards],
            "body": [stmt.to_json() for stmt in self.body],
        }
        if self.result is not None:
            data["result"] = self.result.to_json()
        if self.depends:
            data["depends"] = list(self.depends)
        if self.literal is not None:
            data["literal"] = self.literal
        if self.edge_cases:
            data["edge_cases"] = [
                {"condition": c, "behavior": b} for c, b in self.edge_cases
            ]
        data["span"] = self.span.to_json() if self.span else None
        data["effects"] = self.effects
        data["failures"] = None if self.failures is None else [f for f in self.failures]
        data["typestate"] = self.typestate
        return data


@dataclass
class IRModule:
    """Deterministic target-neutral lowering of one ``.nl`` file.

    ``checked`` distinguishes unchecked lowering output from a module that
    is eligible for checked emission.  Lowering itself never sets it; a
    later checking pass (see :func:`assert_checked_module`) does.
    """

    module_name: str
    version: str = "0.1.0"
    target: Optional[str] = None  # informational only; IR content is target-neutral
    types: tuple[IRRecordType, ...] = ()
    operations: tuple[IROperation, ...] = ()
    imports: tuple[str, ...] = ()
    uses: tuple[str, ...] = ()
    diagnostics: tuple["object", ...] = ()  # Diagnostic instances from lowering
    checked: bool = False
    source_path: Optional[str] = None

    def render(self) -> str:
        return module_to_canonical(self)

    def to_json(self) -> dict[str, object]:
        return module_to_json(self)


# --------------------------------------------------------------------------
# Canonical serialization
# --------------------------------------------------------------------------


def _render_operation(
    op: IROperation,
    indent: str,
    *,
    with_spans: bool = True,
    with_purpose: bool = True,
    with_notes: bool = True,
) -> str:
    lines: list[str] = []
    header = f"(op {op.name}"
    if with_spans and op.span and op.span.line:
        header += f" (line {op.span.line})"
    lines.append(header)
    if with_purpose and op.purpose:
        lines.append(f"{indent}(purpose {json.dumps(op.purpose)})")
    for param in op.params:
        lines.append(f"{indent}{param.render()}")
    for guard in op.guards:
        lines.append(f"{indent}{guard.render()}")
    if op.body:
        body_stmts: list[IRStmt] = list(op.body)
        if not with_notes:
            body_stmts = [stmt for stmt in body_stmts if not isinstance(stmt, IRNote)]
        if body_stmts:
            lines.append(f"{indent}(body")
            for stmt in body_stmts:
                rendered = _render_stmt_with_span(stmt) if with_spans else stmt.render()
                for stmt_line in rendered.split("\n"):
                    lines.append(f"{indent}  {stmt_line}")
            lines.append(f"{indent})")
    if op.result is not None:
        lines.append(f"{indent}{op.result.render()}")
    if op.depends:
        lines.append(f"{indent}(depends {' '.join(op.depends)})")
    if op.literal is not None:
        lines.append(f"{indent}(literal {json.dumps(op.literal)})")
    for condition, behavior in op.edge_cases:
        lines.append(
            f"{indent}(edge-case {json.dumps(condition)} -> {json.dumps(behavior)})"
        )
    lines.append(")")
    return "\n".join(lines)


def operation_to_canonical(op: IROperation, *, with_spans: bool = True) -> str:
    """Canonical text of one operation (used by `nlsc ir`)."""
    return _render_operation(op, "  ", with_spans=with_spans)


def operation_semantic_canonical(op: IROperation) -> str:
    """Canonical *executable semantics* of one operation.

    Excludes source spans, PURPOSE narrative, and free-text notes so the
    rendering captures meaning only: parameters and constraints, guards
    with error payloads, ordered body statements, result contract,
    dependencies, literals, and edge cases.  This is the input hashed
    for lockfile semantic identity (#193).
    """
    return _render_operation(
        op, "  ", with_spans=False, with_purpose=False, with_notes=False
    )


def _render_stmt_with_span(stmt: IRStmt) -> str:
    """Render a top-level body statement annotated with its source span."""
    rendered = stmt.render()
    if stmt.span is not None and (stmt.span.step or stmt.span.line):
        parts: list[str] = []
        if stmt.span.step:
            parts.append(f"step={stmt.span.step}")
        if stmt.span.line:
            parts.append(f"line={stmt.span.line}")
        return rendered + f"  ;; {' '.join(parts)}"
    return rendered


def module_to_canonical(module: IRModule) -> str:
    """Render the canonical, deterministic, human-readable IR text."""
    header = f";; nls-ir {IR_SCHEMA_VERSION} target-neutral module={module.module_name}"
    if module.version:
        header += f" version={module.version}"
    lines: list[str] = [header]

    if module.imports:
        lines.append("(imports {})".format(" ".join(module.imports)))
    if module.uses:
        lines.append("(uses {})".format(" ".join(module.uses)))

    for record in module.types:
        lines.append(record.render())

    for op in module.operations:
        lines.append(_render_operation(op, "  "))

    return "\n".join(lines) + "\n"


def module_to_json(module: IRModule) -> dict[str, object]:
    """Render the deterministic JSON interchange form."""
    data: dict[str, object] = {
        "ir_version": IR_SCHEMA_VERSION,
        "module": module.module_name,
        "version": module.version,
        "types": [t.to_json() for t in module.types],
        "operations": [op.to_json() for op in module.operations],
        "checked": module.checked,
    }
    if module.target:
        data["declared_target"] = module.target
    if module.imports:
        data["imports"] = list(module.imports)
    if module.uses:
        data["uses"] = list(module.uses)
    if module.diagnostics:
        data["diagnostics"] = [
            d.to_dict() if hasattr(d, "to_dict") else d for d in module.diagnostics
        ]
    if module.source_path:
        data["source"] = module.source_path
    return data


def module_to_json_text(module: IRModule) -> str:
    """Canonical JSON text (sorted keys, stable formatting)."""
    return json.dumps(module_to_json(module), indent=2, sort_keys=True, ensure_ascii=False)


# --------------------------------------------------------------------------
# Checked-IR boundary
# --------------------------------------------------------------------------


class UncheckedIRError(Exception):
    """Raised when a module with unresolved content is treated as checked."""

    def __init__(self, diagnostics: list):
        self.diagnostics = list(diagnostics)
        message = "; ".join(
            getattr(d, "message", str(d)) for d in self.diagnostics
        )
        super().__init__(message or "module is not eligible for checked emission")


def find_unchecked_nodes(module: IRModule) -> list[Union[ForeignExpr, ForeignStmt]]:
    """Return every foreign node that blocks checked emission."""
    blockers: list[Union[ForeignExpr, ForeignStmt]] = []
    for op in module.operations:
        for guard in op.guards:
            for node in iter_expr_nodes(guard.condition):
                if isinstance(node, ForeignExpr):
                    blockers.append(node)
        for stmt in iter_stmt_nodes(op.body):
            if isinstance(stmt, ForeignStmt):
                blockers.append(stmt)
                continue
            value: Optional[IRExpr] = None
            if isinstance(stmt, IRBind):
                value = stmt.value
            elif isinstance(stmt, IRDiscard):
                value = stmt.value
            elif isinstance(stmt, IRReturn):
                value = stmt.value
            elif isinstance(stmt, IRBranch):
                for node in iter_expr_nodes(stmt.condition):
                    if isinstance(node, ForeignExpr):
                        blockers.append(node)
                value = None
            if value is not None:
                for node in iter_expr_nodes(value):
                    if isinstance(node, ForeignExpr):
                        blockers.append(node)
        if op.result is not None and op.result.value is not None:
            for node in iter_expr_nodes(op.result.value):
                if isinstance(node, ForeignExpr):
                    blockers.append(node)
    return blockers


def operation_unchecked_nodes(op: IROperation) -> list[Union[ForeignExpr, ForeignStmt]]:
    """Return foreign nodes in one operation that block checked emission."""
    blockers: list[Union[ForeignExpr, ForeignStmt]] = []

    def scan_expr(expr: IRExpr) -> None:
        for node in iter_expr_nodes(expr):
            if isinstance(node, ForeignExpr):
                blockers.append(node)

    for guard in op.guards:
        scan_expr(guard.condition)
    for stmt in iter_stmt_nodes(op.body):
        if isinstance(stmt, ForeignStmt):
            blockers.append(stmt)
            continue
        if isinstance(stmt, IRBind):
            scan_expr(stmt.value)
        elif isinstance(stmt, IRDiscard):
            scan_expr(stmt.value)
        elif isinstance(stmt, IRReturn):
            scan_expr(stmt.value)
        elif isinstance(stmt, IRBranch):
            scan_expr(stmt.condition)
    if op.result is not None and op.result.value is not None:
        scan_expr(op.result.value)
    return blockers


def assert_checked_module(module: IRModule) -> None:
    """Refuse checked status for any module containing unresolved content.

    A module passes only when lowering produced no foreign nodes anywhere
    in executable position.  Unfilled effect/failure contract slots do
    not block this check (they are *checked* structure), but they also
    never imply validity — see the slot documentation on IROperation.
    """
    blockers = find_unchecked_nodes(module)
    if blockers:
        raise UncheckedIRError(
            [
                getattr(node, "reason", "foreign")
                for node in blockers
            ]
        )
