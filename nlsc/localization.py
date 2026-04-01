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


def normalize_localized_source(source: str) -> str:
    """Normalize localized directives and section headers to canonical NLS."""
    return "\n".join(normalize_localized_line(line) for line in source.split("\n"))


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
    """Normalize localized expression fragments to Python-compatible syntax."""
    normalized = text

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

    return normalized


def extract_expression_identifiers(expression: str) -> list[str]:
    """Extract identifiers from an expression, including Unicode names."""
    expression = normalize_expression_text(expression)
    stripped = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', "", expression)
    stripped = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", "", stripped)
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
