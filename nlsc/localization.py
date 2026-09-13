"""Localization helpers for NLS surface syntax."""

from __future__ import annotations

import re


IDENTIFIER_PATTERN = r"(?:[^\W\d]|_)\w*"
ANLU_IDENTIFIER_PATTERN = r"(?:[^\W\d]|_)[\w.-]*"


_DIRECTIVE_ALIASES = {
    "module": "module",
    "モジュール": "module",
    "version": "version",
    "バージョン": "version",
    "target": "target",
    "ターゲット": "target",
    "imports": "imports",
    "インポート": "imports",
    "use": "use",
    "使用": "use",
    "type": "type",
    "型": "type",
    "test": "test",
    "テスト": "test",
    "property": "property",
    "性質": "property",
    "invariant": "invariant",
    "不変条件": "invariant",
    "literal": "literal",
    "リテラル": "literal",
    "main": "main",
    "メイン": "main",
}

_SECTION_ALIASES = {
    "PURPOSE": {"PURPOSE", "目的"},
    "INPUTS": {"INPUTS", "入力", "引数"},
    "GUARDS": {"GUARDS", "ガード"},
    "LOGIC": {"LOGIC", "ロジック", "処理"},
    "RETURNS": {"RETURNS", "返り値", "戻り値", "返す"},
    "EDGE CASES": {
        "EDGE CASES",
        "EDGE_CASES",
        "エッジケース",
        "境界事例",
        "境界ケース",
    },
    "DEPENDS": {"DEPENDS", "依存"},
}

_TARGET_ALIASES = {
    "python": "python",
    "パイソン": "python",
    "typescript": "typescript",
    "タイプスクリプト": "typescript",
    "rust": "rust",
    "ラスト": "rust",
}

_NONE_ALIASES = {"none": "none", "なし": "none", "無し": "none"}

_TYPE_ALIASES = {
    "number": "number",
    "数": "number",
    "数値": "number",
    "integer": "integer",
    "整数": "integer",
    "string": "string",
    "文字列": "string",
    "boolean": "boolean",
    "bool": "boolean",
    "真偽値": "boolean",
    "ブール": "boolean",
    "any": "any",
    "任意": "any",
    "void": "void",
    "none": "void",
    "なし": "void",
    "無し": "void",
    "dictionary": "dictionary",
    "dict": "dict",
    "辞書": "dictionary",
}

_EXPRESSION_ALIASES = {
    "かつ": "and",
    "または": "or",
    "真": "True",
    "偽": "False",
    "なし": "None",
    "無し": "None",
}

# Localized builtin aliases are substituted anywhere they stand alone, so
# a user definition with one of these names would be silently redirected to
# the builtin (#256).  They are reserved: definitions are rejected (ESEM022)
# rather than reinterpreted.
RESERVED_ALIASES: frozenset[str] = frozenset(
    {
        "長さ",
        "なし",
        "無し",
        "真",
        "偽",
        "かつ",
        "または",
        # Post-normalization spellings of the same aliases, so a binding that
        # was rewritten before analysis is still caught.
        "True",
        "False",
        "None",
        "len",
    }
)


_KEYWORDS = {
    "True",
    "False",
    "None",
    "and",
    "or",
    "not",
    "in",
    "is",
    "if",
    "else",
    "for",
    "while",
    "return",
    "def",
    "class",
    "sum",
    "len",
    "min",
    "max",
    "abs",
    "round",
    "int",
    "float",
    "str",
    "list",
    "dict",
    "set",
    "tuple",
    "range",
    "enumerate",
    "zip",
    "IF",
    "THEN",
    "ELSE",
    "AND",
    "OR",
    "NOT",
}

_SECTION_LOOKUP: dict[str, str] = {}
for canonical, aliases in _SECTION_ALIASES.items():
    for alias in aliases:
        _SECTION_LOOKUP[alias.casefold()] = canonical


def normalize_type_text(type_text: str) -> str:
    """Normalize localized type names to canonical NLS type strings."""
    candidate = type_text.strip()
    if not candidate:
        return candidate

    suffix_optional = ""
    if candidate.endswith("?"):
        candidate = candidate[:-1].strip()
        suffix_optional = "?"

    lowered = candidate.casefold()
    if lowered in _TYPE_ALIASES:
        return _TYPE_ALIASES[lowered] + suffix_optional

    list_match = re.fullmatch(r"(.+?)\s*のリスト", candidate)
    if list_match:
        inner = normalize_type_text(list_match.group(1))
        return f"list of {inner}{suffix_optional}"

    nullable_match = re.fullmatch(r"(.+?)\s+または\s+(なし|無し)", candidate)
    if nullable_match:
        inner = normalize_type_text(nullable_match.group(1))
        return f"{inner} or none"

    return candidate + suffix_optional


# --------------------------------------------------------------------------
# String-literal masking (#251, #252)
# --------------------------------------------------------------------------
#
# Alias substitution must never rewrite text inside string literals. Every
# substitution pass runs against a version of the text with literals
# replaced by opaque placeholders, which are restored afterwards.

_MASK_ESCAPE = "\0"


def _scan_string_spans(text: str) -> list[tuple[int, int]]:
    """Spans of string literals, including prefixes and triple quotes.

    An unterminated quote spans to the end of the text.  That is the safe
    direction: text after a stray quote is treated as opaque and alias
    substitution stops there, rather than rewriting prose that contains an
    apostrophe.
    """
    spans: list[tuple[int, int]] = []
    index = 0
    length = len(text)
    while index < length:
        char = text[index]
        prefix_start = index
        raw = False
        if char in "rRbBuUfF":
            probe = index
            while probe < length and text[probe] in "rRbBuUfF":
                probe += 1
            if probe >= length or text[probe] not in "'\"":
                index += 1
                continue
            raw = "r" in text[index:probe].lower()
            index = probe
            char = text[index]
        elif char not in "'\"":
            index += 1
            continue

        quote = char * 3 if text.startswith(char * 3, index) else char
        end = index + len(quote)
        while end < length:
            if not raw and text[end] == "\\":
                end += 2
                continue
            if text.startswith(quote, end):
                end += len(quote)
                break
            end += 1
        else:
            end = length
        spans.append((prefix_start, end))
        index = end
    return spans


def mask_string_literals(text: str) -> tuple[str, list[str]]:
    """Replace string literals with placeholders; return (masked, literals)."""
    spans = _scan_string_spans(text)
    if not spans:
        return text, []
    pieces: list[str] = []
    literals: list[str] = []
    last = 0
    for start, end in spans:
        pieces.append(text[last:start])
        pieces.append(f"{_MASK_ESCAPE}{len(literals)}{_MASK_ESCAPE}")
        literals.append(text[start:end])
        last = end
    pieces.append(text[last:])
    return "".join(pieces), literals


def restore_string_literals(text: str, literals: list[str]) -> str:
    # Reverse order: a literal that itself contains a placeholder-looking
    # sequence for a lower index cannot be clobbered by a later pass.
    for index in range(len(literals) - 1, -1, -1):
        text = text.replace(
            f"{_MASK_ESCAPE}{index}{_MASK_ESCAPE}", literals[index]
        )
    return text


def strip_string_literals(text: str) -> str:
    """Remove string literals (used by heuristics that scan for operators)."""
    masked, _ = mask_string_literals(text)
    return masked


def is_pure_string_literal(text: str) -> bool:
    """True when the whole (trimmed) text is a single string literal."""
    stripped = text.strip()
    if not stripped:
        return False
    spans = _scan_string_spans(stripped)
    return len(spans) == 1 and spans[0] == (0, len(stripped))


# The parser only accepts the canonical directive (localized spellings are
# aliased earlier), so recognition keys on the canonical form.
_LITERAL_DIRECTIVE = re.compile(r"^\s*@literal\b")


def normalize_localized_source(source: str) -> str:
    """Normalize localized directives and section headers to canonical NLS.

    ``@literal`` bodies are copied byte-for-byte: they are documented as
    verbatim passthrough, so every line inside the braces skips
    normalization (#252).  The output stays one line per input line, which
    keeps diagnostics aligned.
    """
    lines = source.split("\n")
    normalized_lines: list[str] = []
    in_literal = False
    brace_depth = 0

    for line in lines:
        if in_literal:
            if "{" in line:
                brace_depth += line.count("{")
            if "}" in line:
                brace_depth -= line.count("}")
                if brace_depth <= 0:
                    normalized_lines.append(line)
                    in_literal = False
                    continue
            normalized_lines.append(line)
            continue

        normalized = normalize_localized_line(line)
        normalized_lines.append(normalized)
        if _LITERAL_DIRECTIVE.match(normalized):
            in_literal = True
            # Mirrors the parser's opener rule (parser.py literal branch):
            # any brace on the directive line opens exactly one level.
            brace_depth = 1 if "{" in normalized else 0

    return "\n".join(normalized_lines)


def normalize_localized_line(line: str) -> str:
    """Normalize one source line without changing line count."""
    directive_match = re.match(r"^(\s*)@([^\s]+)(.*)$", line)
    if directive_match:
        indent, directive, rest = directive_match.groups()
        canonical = _DIRECTIVE_ALIASES.get(
            directive.casefold(), _DIRECTIVE_ALIASES.get(directive)
        )
        if canonical:
            normalized_rest = rest
            if canonical == "target":
                normalized_rest = _normalize_target_rest(rest)
            return f"{indent}@{canonical}{normalized_rest}"

    section_match = re.match(r"^(\s*)([^:：]+?)\s*[:：](.*)$", line)
    if section_match:
        indent, section, rest = section_match.groups()
        canonical = _SECTION_LOOKUP.get(section.strip().casefold())
        if canonical:
            normalized_rest = rest
            if canonical == "INPUTS":
                stripped_rest = rest.strip()
                normalized_none = _NONE_ALIASES.get(
                    stripped_rest.casefold(), _NONE_ALIASES.get(stripped_rest)
                )
                if normalized_none:
                    normalized_rest = f" {normalized_none}"
            return f"{indent}{canonical}:{normalized_rest}"

    if_then_match = re.match(r"^(\s*)もし\s+(.+?)\s+なら\s+(.+)$", line)
    if if_then_match:
        indent, condition, action = if_then_match.groups()
        return f"{indent}IF {condition} THEN {action}"

    while_match = re.match(r"^(\s*)繰り返し\s+(.+)$", line)
    if while_match:
        indent, condition = while_match.groups()
        return f"{indent}WHILE {condition}"

    print_match = re.match(r"^(\s*)表示\s+(.+)$", line)
    if print_match:
        indent, expr = print_match.groups()
        return f"{indent}PRINT {expr}"

    return line


def normalize_expression_text(text: str) -> str:
    """Normalize localized expression fragments to Python-compatible syntax.

    String literals are masked first: an alias token that happens to stand
    alone inside a string is user-visible text, not an operator (#251).
    """
    masked, literals = mask_string_literals(text)
    normalized = masked

    return_match = re.match(r"^(\s*)返す\s+(.+)$", normalized)
    if return_match:
        indent, expr = return_match.groups()
        normalized = f"{indent}return {expr}"

    normalized = re.sub(r"(?<![\w.])長さ\s*\(", "len(", normalized)
    normalized = _normalize_japanese_list_comprehensions(normalized)

    for alias, canonical in _EXPRESSION_ALIASES.items():
        normalized = re.sub(
            rf"(?<![\w.]){re.escape(alias)}(?![\w.])",
            canonical,
            normalized,
        )

    return restore_string_literals(normalized, literals)


def extract_expression_identifiers(expression: str) -> list[str]:
    """Extract identifiers from an expression, including Unicode names."""
    expression = normalize_expression_text(expression)
    stripped = strip_string_literals(expression)
    tokens = re.findall(IDENTIFIER_PATTERN, stripped)
    return [token for token in tokens if token not in _KEYWORDS]


def _normalize_target_rest(rest: str) -> str:
    stripped = rest.strip()
    if not stripped:
        return rest

    normalized = _TARGET_ALIASES.get(stripped.casefold(), _TARGET_ALIASES.get(stripped))
    if normalized is None:
        return rest

    leading = rest[: len(rest) - len(rest.lstrip())]
    return f"{leading}{normalized}"


def _normalize_japanese_list_comprehensions(text: str) -> str:
    pattern = re.compile(
        r"\[\s*(?P<item>[^\]\s]+)\s+を\s+(?P<iter>.+?)\s+から(?:\s+もし\s+(?P<cond>.+?))?\s*\]"
    )

    normalized = text
    while True:
        updated = pattern.sub(_replace_japanese_list_comprehension, normalized)
        if updated == normalized:
            return updated
        normalized = updated


def _replace_japanese_list_comprehension(match: re.Match[str]) -> str:
    item = normalize_expression_text(match.group("item").strip())
    iterable = normalize_expression_text(match.group("iter").strip())
    condition = match.group("cond")

    parts = [f"[{item}", f"for {item} in {iterable}"]
    if condition:
        parts.append(f"if {normalize_expression_text(condition.strip())}")
    return " ".join(parts) + "]"
