"""Source map generation for NLS to Python mapping.

Maps generated Python line numbers back to original .nl source lines.
This enables meaningful error messages that reference .nl files.
"""

import re
from dataclasses import dataclass, field
from typing import Optional

from .schema import NLFile


@dataclass
class SourceMapping:
    """Maps a range of Python lines to an NL source location."""
    py_start: int  # Python line number (1-indexed)
    py_end: int    # Python line number (1-indexed, inclusive)
    nl_line: int   # Original .nl line number
    anlu_id: Optional[str] = None  # Which ANLU this belongs to
    context: str = ""  # Description like "function definition", "guard", etc.


@dataclass
class SourceMap:
    """Complete source map for a generated Python file."""
    nl_path: str
    py_path: str
    mappings: list[SourceMapping] = field(default_factory=list)

    def get_nl_line(self, py_line: int) -> Optional[SourceMapping]:
        """Find the NL source line for a Python line number."""
        for mapping in self.mappings:
            if mapping.py_start <= py_line <= mapping.py_end:
                return mapping
        return None

    def translate_error(self, error_text: str) -> str:
        """Translate Python error message to reference .nl lines.

        Looks for patterns like 'File "path.py", line N' and translates
        to 'File "path.nl", line M (in function-name)'.
        """
        # Pattern: File "...", line N
        pattern = r'File "([^"]+)", line (\d+)'

        def replace_line(match: re.Match) -> str:
            file_path = match.group(1)
            py_line = int(match.group(2))

            # Only translate if it's our generated file
            if self.py_path not in file_path:
                return str(match.group(0))

            mapping = self.get_nl_line(py_line)
            if mapping:
                context = f" (in {mapping.anlu_id})" if mapping.anlu_id else ""
                if mapping.context:
                    context = f" ({mapping.context})"
                return f'File "{self.nl_path}", line {mapping.nl_line}{context}'

            return str(match.group(0))

        return re.sub(pattern, replace_line, error_text)


def generate_source_map(nl_file: NLFile, python_code: str) -> SourceMap:
    """Generate a source map from NLFile to generated Python code.

    This is a best-effort mapping - we match function definitions and
    other recognizable patterns.
    """
    source_map = SourceMap(
        nl_path=nl_file.source_path or "unknown.nl",
        py_path="",  # Set by caller
        mappings=[]
    )

    py_lines = python_code.split("\n")
    nl_source = ""

    # Try to read the original NL source for line mapping
    if nl_file.source_path:
        try:
            from pathlib import Path
            nl_path = Path(nl_file.source_path)
            if nl_path.exists():
                nl_source = nl_path.read_text(encoding="utf-8")
        except Exception:
            pass

    nl_lines = nl_source.split("\n") if nl_source else []

    # Map each ANLU to its Python function
    for anlu in nl_file.anlus:
        # Find the ANLU in the NL source
        nl_line = _find_anlu_line(nl_lines, anlu.identifier)

        # Find the function in Python code
        # Function name is normalized (hyphens to underscores)
        func_name = anlu.identifier.replace("-", "_")
        py_start, py_end = _find_function_range(py_lines, func_name)

        if py_start and nl_line:
            source_map.mappings.append(SourceMapping(
                py_start=py_start,
                py_end=py_end or py_start,
                nl_line=nl_line,
                anlu_id=anlu.identifier,
                context=f"in {anlu.identifier}"
            ))

    # Map type definitions
    for type_def in nl_file.module.types:
        nl_line = _find_type_line(nl_lines, type_def.name)
        py_start, py_end = _find_class_range(py_lines, type_def.name)

        if py_start and nl_line:
            source_map.mappings.append(SourceMapping(
                py_start=py_start,
                py_end=py_end or py_start,
                nl_line=nl_line,
                anlu_id=None,
                context=f"type {type_def.name}"
            ))

    return source_map


def _find_anlu_line(nl_lines: list[str], identifier: str) -> Optional[int]:
    """Find the line number where an ANLU is defined."""
    pattern = re.compile(rf"^\s*\[{re.escape(identifier)}\]")
    for i, line in enumerate(nl_lines, start=1):
        if pattern.match(line):
            return i
    return None


def _find_type_line(nl_lines: list[str], type_name: str) -> Optional[int]:
    """Find the line number where a type is defined."""
    pattern = re.compile(rf"^\s*@type\s+{re.escape(type_name)}")
    for i, line in enumerate(nl_lines, start=1):
        if pattern.match(line):
            return i
    return None


def _find_function_range(py_lines: list[str], func_name: str) -> tuple[Optional[int], Optional[int]]:
    """Find the start and end line of a Python function."""
    pattern = re.compile(rf"^def {re.escape(func_name)}\s*\(")
    start = None
    end = None

    for i, line in enumerate(py_lines, start=1):
        if pattern.match(line):
            start = i
        elif start and line and not line.startswith(" ") and not line.startswith("\t"):
            # Non-indented line after function start = end of function
            end = i - 1
            break

    if start and not end:
        end = len(py_lines)

    return start, end


def _find_class_range(py_lines: list[str], class_name: str) -> tuple[Optional[int], Optional[int]]:
    """Find the start and end line of a Python class."""
    pattern = re.compile(rf"^class {re.escape(class_name)}\s*[\(:]")
    start = None
    end = None

    for i, line in enumerate(py_lines, start=1):
        if pattern.match(line):
            start = i
        elif start and line and not line.startswith(" ") and not line.startswith("\t"):
            end = i - 1
            break

    if start and not end:
        end = len(py_lines)

    return start, end
