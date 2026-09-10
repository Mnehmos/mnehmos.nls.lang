"""Deterministic lowering from the NLS surface AST to the target-neutral IR.

Contract (shared by both parser backends):

* Every executable surface construct either lowers to a structural IR
  node or becomes an explicitly marked foreign node with a diagnostic.
  Nothing is silently dropped, guessed, or turned into a placeholder.
* Localized surface keywords are normalized at *token* level only, so
  string literals are never rewritten.
* The pass is pure: the same ``NLFile`` always lowers to the same
  ``IRModule`` (stable node ids, stable canonical text), independent of
  ``@target``.

``strict=True`` raises :class:`LoweringError` (with the same
diagnostics) instead of producing unchecked IR.  See ``docs/ir-spec.md``.
"""

from __future__ import annotations

import ast
import re
from dataclasses import replace
from typing import Optional

from .diagnostics import Diagnostic
from .error_catalog import EIR001, EIR002, EIR003
from .ir import (
    BINARY_OPS,
    IRBind,
    IRBinary,
    IRBranch,
    IRCall,
    IRDiscard,
    IRErrorSpec,
    IRExpr,
    IRFieldAccess,
    IRGuard,
    IRIndexAccess,
    IRList,
    IRLiteral,
    IRLoop,
    IRMethodCall,
    IRModule,
    IRNote,
    IROperation,
    IRParam,
    IRRecordField,
    IRRecordType,
    IRRef,
    IRReturn,
    IRReturnSpec,
    IRStmt,
    IRUnary,
    ForeignExpr,
    ForeignStmt,
    SourceSpan,
    type_ref_from_text,
)
from .localization import ANLU_IDENTIFIER_PATTERN, IDENTIFIER_PATTERN
from .schema import ANLU, Guard, Input, LogicStep, NLFile, TypeDefinition

IR_FILE_TOKEN = "<lowering>"

# Normalized surface keyword aliases applied at token level (outside literals).
_TOKEN_KEYWORD_ALIASES = {
    "かつ": "and",
    "または": "or",
    "真": "True",
    "偽": "False",
    "なし": "None",
    "無し": "None",
    "長さ": "len",
}

_KEYWORD_TOKENS = {
    "lambda",
    "def",
    "class",
    "return",
    "import",
    "from",
    "await",
    "yield",
    "assert",
    "del",
    "global",
    "pass",
    "try",
    "except",
    "raise",
    "with",
}

# Kebab case ANLU ids lower to snake_case locals, matching emitter naming.
_KEBAB_TO_SNAKE = re.compile(r"-")

_NUMBER_TOKEN = re.compile(r"\d+(?:\.\d+)?(?:[eE][+-]?\d+)?")
_IDENTIFIER_TOKEN = re.compile(IDENTIFIER_PATTERN)
_ANLU_NAME_TOKEN = re.compile(ANLU_IDENTIFIER_PATTERN)

_AUG_OPS = {
    "+=": "add",
    "-=": "sub",
    "*=": "mul",
    "/=": "div",
    "//=": "floor_div",
    "%=": "mod",
    "**=": "pow",
}


class LoweringError(Exception):
    """Raised in strict mode when lowering produces blocking diagnostics."""

    def __init__(self, diagnostics: list[Diagnostic]):
        self.diagnostics = list(diagnostics)
        summary = "; ".join(d.message for d in self.diagnostics)
        super().__init__(summary or "lowering produced blocking diagnostics")


class _TokenizeError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class _UnsupportedError(Exception):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class _Tok:
    __slots__ = ("kind", "text", "pos")

    def __init__(self, kind: str, text: str, pos: int):
        self.kind = kind  # NUMBER STRING IDENT OP ( ) [ ] { } , . : =
        self.text = text
        self.pos = pos

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"_Tok({self.kind},{self.text!r})"


def tokenize_expression(text: str) -> list[_Tok]:
    """Tokenize an expression, preserving string literal tokens exactly."""
    tokens: list[_Tok] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit():
            match = _NUMBER_TOKEN.match(text, i)
            assert match is not None
            tokens.append(_Tok("NUMBER", match.group(0), i))
            i = match.end()
            continue
        if ch in "'\"":
            j = i + 1
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text[j] == ch:
                    break
                j += 1
            if j >= n:
                raise _TokenizeError(f"unterminated string literal starting at {ch}")
            tokens.append(_Tok("STRING", text[i : j + 1], i))
            i = j + 1
            continue
        if ch == "f" or ch == "r":
            # f-string / raw-string prefixes bind only directly to a quote.
            if i + 1 < n and text[i + 1] in "'\"":
                raise _UnsupportedError("fstring" if ch == "f" else "raw-string")
        ident = _IDENTIFIER_TOKEN.match(text, i)
        if ident is not None and ident.start() == i:
            word = ident.group(0)
            normalized = _TOKEN_KEYWORD_ALIASES.get(word, word)
            if normalized == "len" and word != "len":
                tokens.append(_Tok("IDENT", "len", i))
                i = ident.end()
                continue
            if normalized in _KEYWORD_TOKENS:
                raise _UnsupportedError(f"keyword-{normalized}")
            tokens.append(_Tok("IDENT", normalized, i))
            i = ident.end()
            continue
        for op in ("**", "//", "==", "!=", "<=", ">=", "+=", "-=", "*=", "/=", "%="):
            if text.startswith(op, i):
                if op in _AUG_OPS and not tokens:
                    raise _UnsupportedError("augmented-binding")
                if op in _AUG_OPS:
                    # Only valid as a statement operator; expressions reject it.
                    tokens.append(_Tok("OP", op, i))
                    i += len(op)
                    continue
                tokens.append(_Tok("OP", op, i))
                i += len(op)
                break
        else:
            if ch == "×":
                tokens.append(_Tok("OP", "×", i))
                i += 1
                continue
            if ch == "÷":
                tokens.append(_Tok("OP", "÷", i))
                i += 1
                continue
            if ch == "[":
                # [anlu-name] / [anlu-name](args) — the bracket content is a
                # single ANLU identifier (kebab/dotted); anything else is a list.
                close = text.find("]", i + 1)
                if close > i + 1:
                    candidate = text[i + 1 : close]
                    if _ANLU_NAME_TOKEN.fullmatch(candidate):
                        tokens.append(_Tok("ANLU_NAME", candidate, i))
                        i = close + 1
                        continue
                tokens.append(_Tok("[", "[", i))
                i += 1
                continue
            if ch in "()]{},.:":
                tokens.append(_Tok(ch, ch, i))
                i += 1
                continue
            if ch == "=":
                tokens.append(_Tok("=", "=", i))
                i += 1
                continue
            if ch in "+-*/%<>!":
                tokens.append(_Tok("OP", ch, i))
                i += 1
                continue
            if ch == ";":
                raise _UnsupportedError("multiple-statements")
            raise _TokenizeError(f"unexpected character {ch!r}")
    return tokens


class _ExprParser:
    """Precedence parser over the token stream; fully consumes input."""

    def __init__(self, tokens: list[_Tok], text: str):
        self.tokens = tokens
        self.text = text
        self.pos = 0

    # -- token helpers ----------------------------------------------------
    def peek(self, offset: int = 0) -> Optional[_Tok]:
        index = self.pos + offset
        return self.tokens[index] if index < len(self.tokens) else None

    def advance(self) -> _Tok:
        tok = self.peek()
        if tok is None:
            raise _UnsupportedError("unexpected-end")
        self.pos += 1
        return tok

    def expect(self, kind: str) -> _Tok:
        tok = self.peek()
        if tok is None or tok.kind != kind:
            raise _UnsupportedError("unexpected-token")
        return self.advance()

    # -- grammar -----------------------------------------------------------
    def parse_expression(self) -> IRExpr:
        expr = self.parse_or()
        if self.peek() is not None:
            tok = self.peek()
            if tok is not None and tok.kind == "OP" and tok.text in _AUG_OPS:
                raise _UnsupportedError("augmented-binding")
            if tok is not None and tok.kind == "=":
                raise _UnsupportedError("assignment-in-expression")
            if tok is not None and tok.kind == "IDENT" and tok.text in ("if", "else"):
                raise _UnsupportedError("ternary")
            if tok is not None and tok.kind == "IDENT" and tok.text == "for":
                raise _UnsupportedError("generator-expression")
            raise _UnsupportedError("trailing-tokens")
        return expr

    def parse_or(self) -> IRExpr:
        left = self.parse_and()
        while (tok := self.peek()) and tok.kind == "IDENT" and tok.text == "or":
            self.advance()
            right = self.parse_and()
            left = IRBinary(op="or", left=left, right=right)
        return left

    def parse_and(self) -> IRExpr:
        left = self.parse_not()
        while (tok := self.peek()) and tok.kind == "IDENT" and tok.text == "and":
            self.advance()
            right = self.parse_not()
            left = IRBinary(op="and", left=left, right=right)
        return left

    def parse_not(self) -> IRExpr:
        tok = self.peek()
        if tok and tok.kind == "IDENT" and tok.text == "not":
            self.advance()
            return IRUnary(op="not", operand=self.parse_not())
        return self.parse_comparison()

    def parse_comparison(self) -> IRExpr:
        left = self.parse_additive()
        while True:
            tok = self.peek()
            if tok is None:
                return left
            if tok.kind == "IDENT" and tok.text == "is":
                self.advance()
                if (nxt := self.peek()) and nxt.kind == "IDENT" and nxt.text == "not":
                    self.advance()
                    op = "is_not"
                else:
                    op = "is"
            elif tok.kind == "IDENT" and tok.text == "in":
                self.advance()
                op = "in"
            elif tok.kind == "IDENT" and tok.text == "not":
                nxt = self.peek(1)
                if nxt and nxt.kind == "IDENT" and nxt.text == "in":
                    self.advance()
                    self.advance()
                    op = "not_in"
                else:
                    return left
            elif tok.kind == "OP" and tok.text in ("==", "!=", "<", "<=", ">", ">="):
                self.advance()
                op = BINARY_OPS[tok.text]
            else:
                return left
            right = self.parse_additive()
            left = IRBinary(op=op, left=left, right=right)

    def parse_additive(self) -> IRExpr:
        left = self.parse_multiplicative()
        while (tok := self.peek()) and tok.kind == "OP" and tok.text in ("+", "-"):
            self.advance()
            right = self.parse_multiplicative()
            left = IRBinary(op=BINARY_OPS[tok.text], left=left, right=right)
        return left

    def parse_multiplicative(self) -> IRExpr:
        left = self.parse_unary()
        while (tok := self.peek()) and tok.kind == "OP" and tok.text in (
            "*",
            "/",
            "//",
            "%",
            "×",
            "÷",
        ):
            self.advance()
            right = self.parse_unary()
            left = IRBinary(op=BINARY_OPS[tok.text], left=left, right=right)
        return left

    def parse_unary(self) -> IRExpr:
        tok = self.peek()
        if tok and tok.kind == "OP" and tok.text in ("-", "+"):
            self.advance()
            operand = self.parse_unary()
            if tok.text == "-":
                return IRUnary(op="neg", operand=operand)
            return operand
        return self.parse_power()

    def parse_power(self) -> IRExpr:
        base = self.parse_postfix()
        tok = self.peek()
        if tok and tok.kind == "OP" and tok.text == "**":
            self.advance()
            exponent = self.parse_unary()  # right-associative
            return IRBinary(op="pow", left=base, right=exponent)
        return base

    def parse_postfix(self) -> IRExpr:
        expr = self.parse_primary()
        while True:
            tok = self.peek()
            if tok is None:
                return expr
            if tok.kind == ".":
                self.advance()
                name = self.expect("IDENT").text
                nxt = self.peek()
                if nxt is not None and nxt.kind == "(":
                    args, kwargs = self.parse_call_args()
                    expr = IRMethodCall(base=expr, method=name, args=args, kwargs=kwargs)
                else:
                    expr = IRFieldAccess(base=expr, field_name=name)
                continue
            if tok.kind == "[":
                self.advance()
                index = self.parse_or()
                closing = self.peek()
                if closing is not None and closing.kind == ":":
                    raise _UnsupportedError("slice")
                self.expect("]")
                expr = IRIndexAccess(base=expr, index=index)
                continue
            if tok.kind == "(":
                if not isinstance(expr, IRRef):
                    raise _UnsupportedError("call-on-non-name")
                args, kwargs = self.parse_call_args()
                expr = IRCall(target=expr.name, args=args, kwargs=kwargs)
                continue
            return expr

    def parse_call_args(self) -> tuple[tuple[IRExpr, ...], tuple[tuple[str, IRExpr], ...]]:
        self.expect("(")
        args: list[IRExpr] = []
        kwargs: list[tuple[str, IRExpr]] = []
        if (tok := self.peek()) and tok.kind == ")" :
            self.advance()
            return tuple(args), tuple(kwargs)
        while True:
            if kwargs:
                pass
            tok = self.peek()
            if tok and tok.kind == "OP" and tok.text in ("*", "**"):
                raise _UnsupportedError("star-args")
            if tok and tok.kind == "OP" and tok.text in _AUG_OPS:
                raise _UnsupportedError("augmented-binding")
            if (
                tok
                and tok.kind == "IDENT"
                and (nxt := self.peek(1))
                and nxt.kind == "="
            ):
                self.advance()
                self.advance()
                value = self.parse_or()
                kwargs.append((tok.text, value))
            else:
                if kwargs:
                    raise _UnsupportedError("positional-after-keyword")
                expr = self.parse_or()
                nxt = self.peek()
                if nxt and nxt.kind == "IDENT" and nxt.text == "for":
                    raise _UnsupportedError("generator-expression")
                args.append(expr)
            sep = self.peek()
            if sep is not None and sep.kind == ",":
                self.advance()
                continue
            self.expect(")")
            return tuple(args), tuple(kwargs)

    def parse_primary(self) -> IRExpr:
        tok = self.peek()
        if tok is None:
            raise _UnsupportedError("unexpected-end")
        if tok.kind == "NUMBER":
            self.advance()
            return IRLiteral(kind="number", raw=tok.text, value=_number_value(tok.text))
        if tok.kind == "STRING":
            self.advance()
            return IRLiteral(
                kind="string", raw=tok.text, value=_decode_string(tok.text)
            )
        if tok.kind == "IDENT":
            if tok.text == "True" or tok.text == "False":
                self.advance()
                return IRLiteral(kind="boolean", raw=tok.text, value=tok.text == "True")
            if tok.text == "None":
                self.advance()
                return IRLiteral(kind="none", raw=tok.text, value=None)
            if tok.text in ("if", "else"):
                raise _UnsupportedError("ternary")
            if tok.text == "for":
                raise _UnsupportedError("generator-expression")
            self.advance()
            return IRRef(name=tok.text)
        if tok.kind == "(":
            self.advance()
            inner = self.parse_or()
            closing = self.peek()
            if closing is not None and closing.kind == ",":
                raise _UnsupportedError("tuple")
            self.expect(")")
            return inner
        if tok.kind == "[":
            return self.parse_bracket()
        if tok.kind == "ANLU_NAME":
            # [anlu-name] / [anlu-name](args) — structural ANLU reference
            # with the kebab-case target preserved verbatim.
            self.advance()
            if (after := self.peek()) is not None and after.kind == "(":
                args, kwargs = self.parse_call_args()
                return IRCall(
                    target=tok.text, args=args, kwargs=kwargs, anlu=True
                )
            return IRCall(target=tok.text, anlu=True)
        if tok.kind == "{":
            raise _UnsupportedError("dict-literal")
        if tok.kind == "OP" and tok.text in _AUG_OPS:
            raise _UnsupportedError("augmented-binding")
        if tok.kind == ":":
            raise _UnsupportedError("walrus-or-slice")
        raise _UnsupportedError("unexpected-token")

    def parse_bracket(self) -> IRExpr:
        self.expect("[")
        tok = self.peek()
        if tok is not None and tok.kind == "]" :
            self.advance()
            return IRList(items=())
        items: list[IRExpr] = []
        while True:
            expr = self.parse_or()
            if (nxt := self.peek()) and nxt.kind == "IDENT":
                if nxt.text == "for":
                    raise _UnsupportedError("comprehension")
                if nxt.text == "if":
                    raise _UnsupportedError("ternary")
            items.append(expr)
            sep = self.peek()
            if sep is not None and sep.kind == ",":
                self.advance()
                if (nxt := self.peek()) and nxt.kind == "]":
                    self.advance()
                    return IRList(items=tuple(items))
                continue
            self.expect("]")
            return IRList(items=tuple(items))


def _number_value(raw: str) -> object:
    if re.fullmatch(r"\d+", raw):
        return int(raw)
    return float(raw)


def _decode_string(token: str) -> object:
    try:
        return ast.literal_eval(token)
    except (ValueError, SyntaxError):  # pragma: no cover - defensive
        return token[1:-1]


# --------------------------------------------------------------------------
# Node ids
# --------------------------------------------------------------------------


def _assign_expr_ids(expr: IRExpr, path: str) -> IRExpr:
    if isinstance(expr, ForeignExpr):
        return replace(expr, id=path)
    if isinstance(expr, (IRLiteral, IRRef)):
        return replace(expr, id=path)
    if isinstance(expr, IRFieldAccess):
        return replace(
            expr,
            id=path,
            base=_assign_expr_ids(expr.base, f"{path}.base"),
        )
    if isinstance(expr, IRIndexAccess):
        return replace(
            expr,
            id=path,
            base=_assign_expr_ids(expr.base, f"{path}.base"),
            index=_assign_expr_ids(expr.index, f"{path}.index"),
        )
    if isinstance(expr, IRList):
        return replace(
            expr,
            id=path,
            items=tuple(
                _assign_expr_ids(item, f"{path}.item{i}") for i, item in enumerate(expr.items)
            ),
        )
    if isinstance(expr, IRUnary):
        return replace(expr, id=path, operand=_assign_expr_ids(expr.operand, f"{path}.operand"))
    if isinstance(expr, IRBinary):
        return replace(
            expr,
            id=path,
            left=_assign_expr_ids(expr.left, f"{path}.left"),
            right=_assign_expr_ids(expr.right, f"{path}.right"),
        )
    if isinstance(expr, IRCall):
        return replace(
            expr,
            id=path,
            args=tuple(_assign_expr_ids(a, f"{path}.arg{i}") for i, a in enumerate(expr.args)),
            kwargs=tuple(
                (name, _assign_expr_ids(v, f"{path}.kwarg.{name}")) for name, v in expr.kwargs
            ),
        )
    if isinstance(expr, IRMethodCall):
        return replace(
            expr,
            id=path,
            base=_assign_expr_ids(expr.base, f"{path}.base"),
            args=tuple(_assign_expr_ids(a, f"{path}.arg{i}") for i, a in enumerate(expr.args)),
            kwargs=tuple(
                (name, _assign_expr_ids(v, f"{path}.kwarg.{name}")) for name, v in expr.kwargs
            ),
        )
    return expr


def _assign_stmt_ids(stmt: IRStmt, path: str) -> IRStmt:
    if isinstance(stmt, (IRNote, ForeignStmt)):
        return replace(stmt, id=path)
    if isinstance(stmt, IRBind):
        return replace(stmt, id=path, value=_assign_expr_ids(stmt.value, f"{path}.value"))
    if isinstance(stmt, IRDiscard):
        return replace(stmt, id=path, value=_assign_expr_ids(stmt.value, f"{path}.value"))
    if isinstance(stmt, IRReturn):
        return replace(stmt, id=path, value=_assign_expr_ids(stmt.value, f"{path}.value"))
    if isinstance(stmt, IRGuard):
        return replace(
            stmt,
            id=path,
            condition=_assign_expr_ids(stmt.condition, f"{path}.cond"),
        )
    if isinstance(stmt, IRBranch):
        return replace(
            stmt,
            id=path,
            condition=_assign_expr_ids(stmt.condition, f"{path}.cond"),
            then_body=tuple(_assign_stmt_ids(s, f"{path}.then{k}") for k, s in enumerate(stmt.then_body)),
            otherwise=tuple(
                _assign_stmt_ids(s, f"{path}.else{k}") for k, s in enumerate(stmt.otherwise)
            ),
        )
    if isinstance(stmt, IRLoop):
        rebuilt: IRLoop = replace(
            stmt,
            id=path,
            condition=_assign_expr_ids(stmt.condition, f"{path}.cond"),
            body=tuple(_assign_stmt_ids(s, f"{path}.body{k}") for k, s in enumerate(stmt.body)),
        )
        return rebuilt
    return stmt


# --------------------------------------------------------------------------
# Expression lowering entry point
# --------------------------------------------------------------------------


def _is_prose_reason(reason: str) -> bool:
    """Reasons that mean 'this is narrative text', not broken code."""
    return reason in ("prose", "tokenize-error", "unexpected-end")


def _classify_unsupported(reason: str, raw: str) -> str:
    """Refine parser reasons into stable foreign-node reasons."""
    if reason == "trailing-tokens" and len(raw.split()) > 1:
        return "prose"
    return reason


def lower_expression(
    text: str,
    span: SourceSpan,
    *,
    strict: bool = False,
    diagnostics: Optional[list] = None,
    file_token: str = IR_FILE_TOKEN,
    context: str = "",
) -> IRExpr:
    """Lower one expression, never silently dropping content.

    Tolerant mode returns ForeignExpr with a diagnostic for anything the
    structural core does not cover.  Strict mode raises LoweringError.
    """
    raw = text.strip()
    prefix = f"{context}: " if context else ""
    try:
        tokens = tokenize_expression(raw)
        parser = _ExprParser(tokens, raw)
        expr = parser.parse_expression()
        return expr
    except _TokenizeError as exc:
        diagnostic = Diagnostic(
            code=EIR001,
            file=file_token,
            line=span.line,
            col=None,
            message=f"{prefix}expression could not be tokenized: {exc.message}",
            hint="Balance quotes and remove invalid characters, or move the text into PURPOSE/notes.",
        )
        return _foreign(raw, "tokenize-error", span, diagnostic, strict, diagnostics)
    except _UnsupportedError as exc:
        reason = _classify_unsupported(exc.reason, raw)
        diagnostic = Diagnostic(
            code=EIR002,
            file=file_token,
            line=span.line,
            col=None,
            message=f"{prefix}expression uses unsupported construct '{reason}': {raw}",
            hint="Rewrite using the supported expression core (literals, refs, fields, calls, operators), or declare it via @literal.",
        )
        return _foreign(raw, reason, span, diagnostic, strict, diagnostics)


def _foreign(
    raw: str,
    reason: str,
    span: SourceSpan,
    diagnostic: Diagnostic,
    strict: bool,
    diagnostics: Optional[list],
) -> ForeignExpr:
    if strict:
        raise LoweringError([diagnostic])
    if diagnostics is not None:
        diagnostics.append(diagnostic)
    return ForeignExpr(raw=raw, reason=reason, span=span)


# --------------------------------------------------------------------------
# Statement lowering
# --------------------------------------------------------------------------


def _lower_step(
    anlu: ANLU, step: LogicStep, strict: bool, diagnostics: list
) -> list[IRStmt]:
    """Lower one parsed LOGIC step using its decomposed fields."""
    span = SourceSpan(anlu=anlu.identifier, line=step.line_number or None, step=step.number)
    raw = step.description.strip()

    if not raw:
        if step.output_binding:
            diagnostic = Diagnostic(
                code=EIR002,
                file=IR_FILE_TOKEN,
                line=span.line,
                col=None,
                message=f"{anlu.identifier} step {step.number}: output binding '{step.output_binding}' has no executable action",
                hint="Provide an action such as '[charge-payment](order) -> payment', or drop the binding.",
            )
            if strict:
                raise LoweringError([diagnostic])
            diagnostics.append(diagnostic)
            return [ForeignStmt(raw=raw, reason="empty-binding", span=span)]
        if step.state_name:
            return [IRNote(text=f"[{step.state_name}]", span=span)]
        return []

    action_stmts = _lower_action(
        anlu, raw, step.output_binding, span, strict, diagnostics
    )

    if step.condition is not None:
        condition = lower_expression(
            step.condition,
            span,
            strict=strict,
            diagnostics=diagnostics,
            context=f"{anlu.identifier} step {step.number} IF condition",
        )
        return [
            IRBranch(
                condition=condition,
                then_body=tuple(action_stmts),
                otherwise=(),
                span=span,
            )
        ]

    return action_stmts


def _lower_action(
    anlu: ANLU,
    text: str,
    binding: Optional[str],
    span: SourceSpan,
    strict: bool,
    diagnostics: list,
) -> list[IRStmt]:
    raw = text.strip()
    context = f"{span.anlu} step {span.step}" if span.step else span.anlu

    aug_match = re.match(
        rf"^({IDENTIFIER_PATTERN})\s*(\+=|-=|\*=|/=|//=|%=|\*\*=)\s*(.+)$", raw
    )
    if aug_match and binding is None:
        value = lower_expression(
            aug_match.group(3),
            span,
            strict=strict,
            diagnostics=diagnostics,
            context=context,
        )
        return [
            IRBind(
                name=aug_match.group(1),
                value=value,
                aug=_AUG_OPS[aug_match.group(2)],
                span=span,
            )
        ]

    assign_match = re.match(rf"^({IDENTIFIER_PATTERN})\s*=\s*(.+)$", raw)
    if assign_match and binding is None:
        name = assign_match.group(1)
        value_text = assign_match.group(2)
    elif binding is not None:
        name = binding
        value_text = raw
    else:
        # No binding: either narrative prose (a Note) or a complete
        # expression statement such as a discarded call.
        sub_diagnostics: list[Diagnostic] = []
        value = lower_expression(
            raw, span, strict=False, diagnostics=sub_diagnostics, context=context
        )
        if isinstance(value, ForeignExpr) and _is_prose_reason(value.reason):
            return [IRNote(text=raw, span=span)]
        if strict and isinstance(value, ForeignExpr):
            raise LoweringError(sub_diagnostics)
        diagnostics.extend(sub_diagnostics)
        if isinstance(value, ForeignExpr):
            diagnostic = Diagnostic(
                code=EIR002,
                file=IR_FILE_TOKEN,
                line=span.line,
                col=None,
                message=f"{context}: unsupported statement '{raw}' ({value.reason})",
                hint="Rewrite the step with a supported action or bind it to an output variable.",
            )
            if strict:
                raise LoweringError([diagnostic])
            diagnostics.append(diagnostic)
            return [ForeignStmt(raw=raw, reason=value.reason, span=span)]
        return [IRDiscard(value=value, span=span)]

    value = lower_expression(
        value_text, span, strict=strict, diagnostics=diagnostics, context=context
    )
    if isinstance(value, ForeignExpr) and _is_prose_reason(value.reason):
        # Executable intent (a binding) without a recognized action stays
        # visible and diagnosed instead of becoming a silent placeholder.
        return [
            IRBind(
                name=name,
                value=ForeignExpr(raw=value_text.strip(), reason=value.reason, span=span),
                span=span,
            )
        ]
    return [IRBind(name=name, value=value, span=span)]


# --------------------------------------------------------------------------
# Operation / module lowering
# --------------------------------------------------------------------------


_PRIMITIVE_RETURN_WORDS = {
    "number",
    "integer",
    "string",
    "boolean",
    "bool",
    "void",
    "none",
    "any",
    "dictionary",
    "dict",
}


def _looks_like_type_name(text: str, declared_types: set[str]) -> bool:
    candidate = text.strip()
    if not candidate or " " in candidate:
        return False
    if candidate.lower() in _PRIMITIVE_RETURN_WORDS:
        return True
    lowered = candidate.lower()
    if lowered.startswith("list of ") or lowered.startswith("list["):
        return True
    if candidate.endswith("?") or " or none" in lowered or " or null" in lowered:
        return True
    if candidate in declared_types:
        return True
    return bool(re.fullmatch(r"[A-Z][A-Za-z0-9_]*", candidate))


def _lower_return_spec(
    anlu: ANLU, declared_types: set[str], strict: bool, diagnostics: list
) -> Optional[IRReturnSpec]:
    raw = anlu.returns.strip()
    if not raw:
        return None
    span = SourceSpan(anlu=anlu.identifier, line=anlu.line_number or None, step=None)
    if _looks_like_type_name(raw, declared_types):
        return IRReturnSpec(declared_type=type_ref_from_text(raw), raw=raw)
    value = lower_expression(raw, span, strict=strict, diagnostics=diagnostics)
    return IRReturnSpec(value=value, raw=raw)


def _lower_input(input_: Input) -> IRParam:
    optional = input_.type.strip().endswith("?") or any(
        c.lower().strip() == "optional" for c in input_.constraints
    )
    return IRParam(
        name=input_.name,
        type_ref=type_ref_from_text(input_.type),
        optional=optional,
        constraints=tuple(input_.constraints),
    )


def _lower_guard(
    anlu: ANLU, guard: Guard, index: int, strict: bool, diagnostics: list
) -> IRGuard:
    span = SourceSpan(
        anlu=anlu.identifier, line=anlu.line_number or None, step=None
    )
    condition = lower_expression(
        guard.condition, span, strict=strict, diagnostics=diagnostics
    )
    error = None
    if guard.error_type:
        error = IRErrorSpec(
            error_type=guard.error_type,
            message=guard.error_message,
            code=guard.error_code,
        )
    return IRGuard(condition=condition, error=error, span=span)


def lower_anlu(
    anlu: ANLU, declared_types: set[str], *, strict: bool = False
) -> tuple[IROperation, list[Diagnostic]]:
    """Lower one ANLU into an IROperation plus its lowering diagnostics."""
    diagnostics: list[Diagnostic] = []
    span = SourceSpan(anlu=anlu.identifier, line=anlu.line_number or None)

    body: list[IRStmt] = []
    step_ids: list[str] = []
    for step in anlu.logic_steps:
        stmts = _lower_step(anlu, step, strict, diagnostics)
        for offset, _stmt in enumerate(stmts):
            body.append(_stmt)
            step_ids.append(f"{anlu.identifier}.step{step.number}" + (f".{offset}" if len(stmts) > 1 else ""))

    result = _lower_return_spec(anlu, declared_types, strict, diagnostics)

    guards = tuple(
        _lower_guard(anlu, guard, index, strict, diagnostics)
        for index, guard in enumerate(anlu.guards)
    )

    body_with_ids = tuple(
        _assign_stmt_ids(stmt, step_id) for stmt, step_id in zip(body, step_ids)
    )
    guards_with_ids = tuple(
        replace(guard, id=f"{anlu.identifier}.guard{index}")
        for index, guard in enumerate(guards)
    )
    if result is not None and result.value is not None:
        result = IRReturnSpec(
            declared_type=result.declared_type,
            value=_assign_expr_ids(result.value, f"{anlu.identifier}.result"),
            raw=result.raw,
        )

    operation = IROperation(
        name=anlu.identifier,
        purpose=anlu.purpose,
        params=tuple(_lower_input(i) for i in anlu.inputs),
        guards=guards_with_ids,
        body=body_with_ids,
        result=result,
        depends=tuple(anlu.depends),
        literal=anlu.literal,
        edge_cases=tuple((ec.condition, ec.behavior) for ec in anlu.edge_cases),
        span=span,
    )
    return operation, diagnostics


def _lower_type(definition: TypeDefinition) -> IRRecordType:
    fields = tuple(
        IRRecordField(
            name=field.name,
            type_ref=type_ref_from_text(field.type),
            constraints=tuple(field.constraints),
            description=field.description,
        )
        for field in definition.fields
    )
    return IRRecordType(name=definition.name, fields=fields, base=definition.base)


def lower_module(nl_file: NLFile, *, strict: bool = False) -> IRModule:
    """Lower a parsed .nl file into the deterministic target-neutral IR.

    Both parser backends produce ``NLFile`` objects, so both share this
    one lowering contract.  ``strict`` flips foreign diagnostics into
    ``LoweringError``; the default produces unchecked IR.
    """
    diagnostics: list[Diagnostic] = []
    declared_types = {t.name for t in nl_file.module.types}

    operations: list[IROperation] = []
    for anlu in nl_file.anlus:
        operation, op_diagnostics = lower_anlu(
            anlu, declared_types, strict=strict
        )
        operations.append(operation)
        diagnostics.extend(op_diagnostics)

    return IRModule(
        module_name=nl_file.module.name,
        version=nl_file.module.version,
        target=nl_file.module.target,
        types=tuple(_lower_type(t) for t in nl_file.module.types),
        operations=tuple(operations),
        imports=tuple(nl_file.module.imports),
        uses=tuple(nl_file.module.uses),
        diagnostics=tuple(diagnostics),
        checked=False,
        source_path=nl_file.source_path,
    )


def check_module_eligibility(module: IRModule) -> list[Diagnostic]:
    """Diagnostics explaining why a module is not eligible for checked emission."""
    from .ir import find_unchecked_nodes

    blockers = find_unchecked_nodes(module)
    diagnostics: list[Diagnostic] = []
    for node in blockers:
        span = getattr(node, "span", None)
        reason = getattr(node, "reason", "foreign")
        raw = getattr(node, "raw", "")
        line = span.line if span else None
        step = f" step {span.step}" if span and span.step else ""
        diagnostics.append(
            Diagnostic(
                code=EIR003,
                file=IR_FILE_TOKEN,
                line=line,
                col=None,
                message=f"foreign {reason} node blocks checked emission{step}: {raw}",
                hint="Lower all executable constructs structurally before requesting checked emission.",
            )
        )
    return diagnostics
