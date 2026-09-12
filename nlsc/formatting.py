"""Canonical formatting for .nl files (Issue #95).

``nlsc fmt`` normalizes the review surface, not the meaning: consistent
headers, bullets, and arrows; canonical section order inside ANLU
blocks; aligned INPUTS entries; one blank line between top-level
constructs; LF line endings; no trailing whitespace.

Design constraints:

- **Comments and their relative positions are preserved.** Formatting is
  line-based: section runs move together with the comments attached
  immediately above them, and leading comment regions are never touched.
- **@literal and @main bodies are verbatim** and skipped entirely.
- **Safety first.** Formatting is applied only when the formatted text
  re-parses to the same structure (same ANLUs, sections, expressions,
  tests, types, and module metadata). Otherwise the file is left
  unchanged and ``EFMT001`` is reported.
- **Idempotent.** Formatting formatted output changes nothing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from .schema import NLFile

SECTION_ORDER = [
    "PURPOSE",
    "INPUTS",
    "GUARDS",
    "LOGIC",
    "EDGE CASES",
    "RETURNS",
    "DEPENDS",
]

_SECTION_HEADER = re.compile(
    r"^(?P<indent>\s*)(?P<name>purpose|inputs|guards|logic|returns|depends|edge\s*cases)"
    r"\s*:\s*(?P<rest>.*)$",
    re.IGNORECASE,
)
_DIRECTIVE = re.compile(r"^(?P<indent>\s*)@(?P<name>[A-Za-z_]\w*)(?P<rest>.*)$")
_ANLU_HEADER = re.compile(r"^\s*\[[^\]]+\]\s*$")
_COMMENT = re.compile(r"^\s*#")
_BULLET = re.compile(r"^\s*[•*\-]\s*(.*)$")
_NUMBERED = re.compile(r"^\s*\d+\.\s+.*$")
_INPUT_ENTRY = re.compile(r"^\s*-\s+(?P<name>[^:]+?)\s*:\s*(?P<rest>.*)$")
_STRING_TOKEN = re.compile(r"(?:'[^'\\]*(?:\\.[^'\\]*)*'|\"[^\"\\]*(?:\\.[^\"\\]*)*\")")

_VERBATIM_DIRECTIVES = ("literal", "main")


@dataclass
class FormatResult:
    """Outcome of formatting one source text."""

    text: str
    changed: bool
    safe: bool
    reason: Optional[str] = None


def _collapse_spaces_outside_strings(text: str) -> str:
    """Collapse runs of spaces/tabs, leaving string literals untouched."""
    parts: list[str] = []
    position = 0
    for match in _STRING_TOKEN.finditer(text):
        parts.append(re.sub(r"[ \t]{2,}", " ", text[position : match.start()]))
        parts.append(match.group(0))
        position = match.end()
    parts.append(re.sub(r"[ \t]{2,}", " ", text[position:]))
    return "".join(parts)


def _normalize_line(line: str) -> str:
    """Normalize one non-verbatim line.

    Indentation is preserved for structural content (type fields, literal
    bodies' surrounding braces) and canonicalized only where the layout
    defines it: two spaces for section bullets and numbered steps, none
    for section headers and directives.
    """
    line = line.rstrip()
    indent_match = re.match(r"^(\s*)", line)
    indent = indent_match.group(1) if indent_match else ""
    content = line[len(indent) :]

    # Bullets: • / * / - -> "- " with a single space.
    bullet = _BULLET.match(content)
    if bullet:
        content = f"- {bullet.group(1).rstrip()}"
        indent = "  "

    if _NUMBERED.match(content):
        indent = "  "

    # Arrows: unicode -> ASCII.
    content = content.replace("→", "->")

    # Section headers to canonical uppercase names, unindented.
    header = _SECTION_HEADER.match(content)
    if header:
        name = re.sub(r"\s+", " ", header.group("name")).upper()
        rest = header.group("rest").strip()
        content = f"{name}:"
        if rest:
            content += f" {rest}"
        indent = ""

    # Directive names to lowercase; top-level directives are unindented.
    directive = _DIRECTIVE.match(content)
    if directive:
        content = f"@{directive.group('name').lower()}{directive.group('rest').rstrip()}"
        indent = ""

    # Collapse interior runs of spaces outside string literals.
    content = _collapse_spaces_outside_strings(content)
    return (indent + content).rstrip()


def _align_inputs(lines: list[str]) -> list[str]:
    """Pad INPUTS entries after the colon so types line up in a column."""
    entries: list[tuple[int, str, str]] = []
    for index, line in enumerate(lines):
        match = _INPUT_ENTRY.match(line)
        if match:
            entries.append((index, match.group("name").strip(), match.group("rest").strip()))
    if len(entries) < 2:
        return lines
    width = max(len(name) for _, name, _ in entries)
    result = list(lines)
    for index, name, rest in entries:
        padding = " " * (width - len(name) + 1)
        result[index] = f"  - {name}:{padding}{rest}".rstrip()
    return result


def _section_name(line: str) -> Optional[str]:
    match = _SECTION_HEADER.match(line)
    if not match:
        return None
    return re.sub(r"\s+", " ", match.group("name")).upper()


def _is_section_header(line: str) -> bool:
    return bool(_SECTION_HEADER.match(line))


def _reorder_anlu_block(block: list[str]) -> list[str]:
    """Reorder sections inside one ANLU block to canonical order."""
    # Separators are owned by the global blank-line policy; an interior
    # blank line would otherwise travel with whichever run it lands in.
    block = [line for line in block if line.strip()]

    # Only the ANLU header line itself is pinned: it identifies the block.
    # Comments directly below it attach to whatever section follows, so
    # they travel with that section when it is reordered.
    leading: list[str] = block[:1]
    position = 1

    runs: list[tuple[Optional[str], list[str]]] = []
    comment_run: list[str] = []
    while position < len(block):
        line = block[position]
        if _COMMENT.match(line):
            comment_run.append(line)
            position += 1
            continue
        if _is_section_header(line):
            body = list(comment_run) + [line]
            comment_run = []
            position += 1
            while position < len(block) and not _is_section_header(block[position]):
                body.append(block[position])
                position += 1
            runs.append((_section_name(line), body))
            continue
        # Unrecognized line: keep as its own unordered run.
        runs.append((None, list(comment_run) + [line]))
        comment_run = []
        position += 1
    if comment_run:
        runs.append((None, comment_run))

    def sort_key(indexed_run: tuple) -> tuple:
        index, (name, _body) = indexed_run
        if name in SECTION_ORDER:
            return (0, SECTION_ORDER.index(name), index)
        return (1, 0, index)

    ordered_lines: list[str] = []
    for _, (_name, body) in sorted(enumerate(runs), key=sort_key):
        ordered_lines.extend(body)
    result = leading + ordered_lines

    # Align INPUTS entries after ordering.
    aligned: list[str] = []
    position = 0
    while position < len(result):
        line = result[position]
        if _section_name(line) == "INPUTS":
            body_end = position + 1
            while body_end < len(result) and not _is_section_header(result[body_end]):
                body_end += 1
            aligned.append(line)
            aligned.extend(_align_inputs(result[position + 1 : body_end]))
            position = body_end
            continue
        aligned.append(line)
        position += 1
    return aligned


def _canonical_expr(text: str) -> str:
    """Whitespace-normalized comparison form for an expression."""
    return _collapse_spaces_outside_strings(text.strip()).strip()


def _fingerprint(nl_file: NLFile) -> tuple:
    """Structural identity used to prove formatting preserved meaning.

    Expression fields compare under whitespace normalization (formatting
    is allowed to normalize spacing); @literal bodies compare exactly.
    """
    return (
        nl_file.module.name,
        nl_file.module.version,
        nl_file.module.spec_version,
        nl_file.module.target,
        tuple(nl_file.module.imports),
        tuple(nl_file.module.uses),
        tuple(
            (
                t.name,
                t.base,
                tuple((f.name, f.type, tuple(f.constraints)) for f in t.fields),
            )
            for t in nl_file.module.types
        ),
        tuple(
            (
                a.identifier,
                a.purpose,
                _canonical_expr(a.returns),
                tuple((i.name, i.type, tuple(i.constraints)) for i in a.inputs),
                tuple(
                    (
                        _canonical_expr(g.condition),
                        g.error_type,
                        g.error_code,
                        g.error_message,
                    )
                    for g in a.guards
                ),
                tuple(_canonical_expr(s.description) for s in a.logic_steps),
                tuple(
                    (_canonical_expr(e.condition), _canonical_expr(e.behavior))
                    for e in a.edge_cases
                ),
                tuple(a.depends),
                a.literal or "",
            )
            for a in nl_file.anlus
        ),
        tuple(
            (
                t.anlu_id,
                tuple(
                    (_canonical_expr(c.expression), _canonical_expr(c.expected))
                    for c in t.cases
                ),
            )
            for t in nl_file.tests
        ),
        tuple(
            (p.anlu_id, tuple(_canonical_expr(a.expression) for a in p.assertions))
            for p in nl_file.properties
        ),
        tuple((i.type_name, tuple(i.conditions)) for i in nl_file.invariants),
        tuple(nl_file.literals),
        bool(nl_file.main_block),
    )


def _is_directive(text: str) -> bool:
    return bool(_DIRECTIVE.match(text))


def format_source(source: str) -> FormatResult:
    """Format .nl source into the canonical layout."""
    original = source.replace("\r\n", "\n").replace("\r", "\n")
    lines = original.split("\n")

    output: list[str] = []
    verbatim_depth = 0
    index = 0
    while index < len(lines):
        line = lines[index]

        if verbatim_depth > 0:
            output.append(line.rstrip())
            verbatim_depth += line.count("{") - line.count("}")
            index += 1
            continue

        directive = _DIRECTIVE.match(line)
        if directive and directive.group("name").lower() in _VERBATIM_DIRECTIVES:
            output.append(_normalize_line(line))
            verbatim_depth += line.count("{") - line.count("}")
            index += 1
            continue

        if _ANLU_HEADER.match(line):
            block_end = index + 1
            while block_end < len(lines):
                candidate = lines[block_end]
                if _ANLU_HEADER.match(candidate) or _DIRECTIVE.match(candidate):
                    break
                block_end += 1
            block = [_normalize_line(entry) for entry in lines[index:block_end]]
            output.extend(_reorder_anlu_block(block))
            index = block_end
            continue

        output.append(_normalize_line(line))
        index += 1

    # Blank-line policy: collapse runs of blank lines to one, exactly one
    # blank line between top-level constructs, and no blanks inside a
    # consecutive run of directives or before a construct's own comments.
    collapsed: list[str] = []
    for line in output:
        if not line.strip():
            if collapsed and not collapsed[-1].strip():
                continue
            collapsed.append("")
            continue
        collapsed.append(line)

    spaced: list[str] = []
    for line in collapsed:
        if not line.strip():
            if spaced and not spaced[-1].strip():
                continue
            spaced.append("")
            continue
        starts_top_level = bool(_ANLU_HEADER.match(line) or _DIRECTIVE.match(line))
        previous = spaced[-1] if spaced else ""
        if (
            starts_top_level
            and spaced
            and previous.strip()
            and not previous.lstrip().startswith("#")
            and not (_is_directive(previous) and _is_directive(line))
        ):
            spaced.append("")
        spaced.append(line)

    formatted = "\n".join(spaced).strip("\n") + "\n"

    if formatted == original:
        return FormatResult(text=original, changed=False, safe=True)

    # Safety net: the reformatted text must parse to the same structure.
    from .parser import ParseError, parse_nl_file

    try:
        before = parse_nl_file(original, source_path="<fmt>")
        after = parse_nl_file(formatted, source_path="<fmt>")
    except ParseError as exc:
        return FormatResult(
            text=original,
            changed=False,
            safe=False,
            reason=f"reformatted source does not parse: {exc}",
        )
    if _fingerprint(before) != _fingerprint(after):
        return FormatResult(
            text=original,
            changed=False,
            safe=False,
            reason="reformatted source would change the module structure",
        )
    return FormatResult(text=formatted, changed=True, safe=True)
