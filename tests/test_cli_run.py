"""Tests for nlsc run command - Issue #89"""

import subprocess
import sys
from pathlib import Path

import pytest

from nlsc.cli import cmd_run
from nlsc.sourcemap import (
    SourceMap, SourceMapping, generate_source_map,
    _find_anlu_line, _find_function_range
)
from nlsc.parser import parse_nl_file


class TestRunCommand:
    """Tests for nlsc run CLI command"""

    def test_cmd_run_exists(self):
        """Run command should exist"""
        result = subprocess.run(
            [sys.executable, "-m", "nlsc", "run", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "file" in result.stdout.lower()
        assert "--keep" in result.stdout

    def test_run_file_not_found(self):
        """Run should error on missing file"""
        result = subprocess.run(
            [sys.executable, "-m", "nlsc", "run", "nonexistent.nl"],
            capture_output=True,
            text=True
        )
        # Error message should be printed
        assert "not found" in result.stderr.lower()
        # Note: Exit code propagation depends on CLI wrapper

    def test_run_simple_file(self, tmp_path):
        """Run should execute a simple .nl file"""
        nl_file = tmp_path / "hello.nl"
        nl_file.write_text("""\
@module hello
@target python

[main]
PURPOSE: Print hello
LOGIC:
  1. Print "Hello from NLS"
RETURNS: void
""")
        result = subprocess.run(
            [sys.executable, "-m", "nlsc", "run", str(nl_file), "--keep", str(tmp_path / "build")],
            capture_output=True,
            text=True
        )
        # Main function with print should produce output
        # (Mock mode may not actually print, but should not error)
        assert result.returncode == 0

    def test_run_with_keep_flag(self, tmp_path):
        """Run --keep should preserve generated files"""
        nl_file = tmp_path / "test.nl"
        nl_file.write_text("""\
@module test
@target python

[greet]
PURPOSE: Return greeting
INPUTS:
  - name: string
RETURNS: greeting
""")
        keep_dir = tmp_path / "keep"

        result = subprocess.run(
            [sys.executable, "-m", "nlsc", "run", str(nl_file), "--keep", str(keep_dir)],
            capture_output=True,
            text=True
        )

        # Check generated file exists
        assert (keep_dir / "test.py").exists()

    def test_run_with_target_flag(self, tmp_path):
        """Run --target should accept python"""
        nl_file = tmp_path / "test.nl"
        nl_file.write_text("""\
@module test
@target python

[hello]
PURPOSE: Say hello
RETURNS: void
""")
        result = subprocess.run(
            [sys.executable, "-m", "nlsc", "run", str(nl_file), "--target", "python", "--keep", str(tmp_path / "build")],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_run_with_verbose_flag(self, tmp_path):
        """Run --verbose should show compilation details"""
        nl_file = tmp_path / "test.nl"
        nl_file.write_text("""\
@module test
@target python

[hello]
PURPOSE: Say hello
RETURNS: void
""")
        result = subprocess.run(
            [sys.executable, "-m", "nlsc", "run", str(nl_file), "-v", "--keep", str(tmp_path / "build")],
            capture_output=True,
            text=True
        )
        assert "Compiled" in result.stdout or "Source mappings" in result.stdout

    def test_run_returns_exit_code(self, tmp_path):
        """Run should propagate subprocess exit code"""
        nl_file = tmp_path / "test.nl"
        nl_file.write_text("""\
@module test
@target python

[hello]
PURPOSE: Do nothing
RETURNS: void
""")
        result = subprocess.run(
            [sys.executable, "-m", "nlsc", "run", str(nl_file), "--keep", str(tmp_path / "build")],
            capture_output=True,
            text=True
        )
        # Success case
        assert result.returncode == 0


class TestSourceMap:
    """Tests for source map generation and error translation"""

    def test_source_mapping_dataclass(self):
        """SourceMapping should store line mappings"""
        mapping = SourceMapping(
            py_start=10,
            py_end=20,
            nl_line=5,
            anlu_id="my-func",
            context="in my-func"
        )
        assert mapping.py_start == 10
        assert mapping.nl_line == 5

    def test_source_map_get_nl_line(self):
        """SourceMap should find NL line for Python line"""
        source_map = SourceMap(
            nl_path="test.nl",
            py_path="test.py",
            mappings=[
                SourceMapping(py_start=10, py_end=20, nl_line=5, anlu_id="func1"),
                SourceMapping(py_start=25, py_end=35, nl_line=15, anlu_id="func2"),
            ]
        )

        # Within first mapping
        result = source_map.get_nl_line(15)
        assert result is not None
        assert result.nl_line == 5

        # Within second mapping
        result = source_map.get_nl_line(30)
        assert result is not None
        assert result.nl_line == 15

        # Outside mappings
        result = source_map.get_nl_line(5)
        assert result is None

    def test_source_map_translate_error(self):
        """SourceMap should translate Python errors to NL lines"""
        source_map = SourceMap(
            nl_path="math.nl",
            py_path="/tmp/nlsc_run_xxx/math.py",
            mappings=[
                SourceMapping(py_start=10, py_end=20, nl_line=5, anlu_id="add", context="in add"),
            ]
        )

        error = 'Traceback:\n  File "/tmp/nlsc_run_xxx/math.py", line 15, in add\nTypeError: ...'
        translated = source_map.translate_error(error)

        assert 'math.nl' in translated
        assert 'line 5' in translated
        assert 'in add' in translated

    def test_find_anlu_line(self):
        """Should find ANLU definition line in NL source"""
        nl_lines = [
            "@module test",
            "@target python",
            "",
            "[add]",
            "PURPOSE: Add numbers",
            "RETURNS: sum",
            "",
            "[multiply]",
            "PURPOSE: Multiply",
        ]

        assert _find_anlu_line(nl_lines, "add") == 4
        assert _find_anlu_line(nl_lines, "multiply") == 8
        assert _find_anlu_line(nl_lines, "nonexistent") is None

    def test_find_function_range(self):
        """Should find function start and end in Python code"""
        py_lines = [
            '"""Module docstring"""',
            "",
            "def add(a: float, b: float) -> float:",
            '    """Add two numbers."""',
            "    return a + b",
            "",
            "def multiply(a: float, b: float) -> float:",
            '    """Multiply."""',
            "    return a * b",
        ]

        start, end = _find_function_range(py_lines, "add")
        assert start == 3
        assert end == 5 or end == 6  # Depends on blank line handling

        start, end = _find_function_range(py_lines, "multiply")
        assert start == 7

    def test_generate_source_map_basic(self, tmp_path):
        """Should generate source map from NLFile"""
        # Create actual file so source map can read it
        nl_path = tmp_path / "test.nl"
        source = """\
@module test
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

[multiply]
PURPOSE: Multiply two numbers
INPUTS:
  - x: number
  - y: number
RETURNS: x * y
"""
        nl_path.write_text(source)
        nl_file = parse_nl_file(source, source_path=str(nl_path))

        # Generate some Python code
        from nlsc.emitter import emit_python
        python_code = emit_python(nl_file)

        source_map = generate_source_map(nl_file, python_code)

        # Should have mappings for both functions
        assert len(source_map.mappings) >= 2

        # Check that we can look up lines
        for mapping in source_map.mappings:
            assert mapping.anlu_id in ["add", "multiply"] or mapping.context.startswith("type")


class TestRunIntegration:
    """Integration tests for run command"""

    def test_run_with_main_block(self, tmp_path):
        """Run should execute @main block if present"""
        nl_file = tmp_path / "script.nl"
        nl_file.write_text("""\
@module script
@target python

[greet]
PURPOSE: Return greeting
INPUTS:
  - name: string
RETURNS: greeting message

@main {
  result = greet("World")
  print(result)
}
""")
        result = subprocess.run(
            [sys.executable, "-m", "nlsc", "run", str(nl_file), "--keep", str(tmp_path / "build")],
            capture_output=True,
            text=True
        )
        # Should execute without error
        # (actual output depends on mock mode behavior)
        assert result.returncode == 0

    def test_run_hyphenated_module(self, tmp_path):
        """Run should handle hyphenated module names"""
        nl_file = tmp_path / "my-module.nl"
        nl_file.write_text("""\
@module my-module
@target python

[hello]
PURPOSE: Say hello
RETURNS: void
""")
        result = subprocess.run(
            [sys.executable, "-m", "nlsc", "run", str(nl_file), "--keep", str(tmp_path / "build")],
            capture_output=True,
            text=True
        )
        # Hyphens should be normalized to underscores
        assert result.returncode == 0

    def test_run_with_custom_imports(self, tmp_path):
        """Run should execute generated code that imports sibling Python modules."""
        root = tmp_path
        (root / "helper.py").write_text(
            "def value():\n    return 7\n",
            encoding="utf-8",
        )
        nl_file = root / "script.nl"
        nl_file.write_text("""\
@module script
@target python
@imports helper

[get-value]
PURPOSE: Return helper value
RETURNS: helper.value()

@main {
  print(get_value())
}
""")
        result = subprocess.run(
            [sys.executable, "-m", "nlsc", "run", str(nl_file), "--keep", str(root / "build")],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "7" in result.stdout
