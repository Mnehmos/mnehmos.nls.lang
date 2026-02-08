"""Tests for nlsc diff command - Issue #15"""

import subprocess
import sys
import pytest
from pathlib import Path
from argparse import Namespace

from nlsc.cli import cmd_diff


class TestDiffCommand:
    """Tests for nlsc diff CLI command"""

    def test_cmd_diff_exists(self):
        """cmd_diff function should exist"""
        assert callable(cmd_diff)

    def test_diff_file_not_found(self):
        """nlsc diff should error on missing file"""
        args = Namespace(file="nonexistent.nl", stat=False, full=False)
        result = cmd_diff(args)
        assert result == 1

    def test_diff_no_lockfile(self, tmp_path):
        """nlsc diff should handle missing lockfile"""
        nl_file = tmp_path / "test.nl"
        nl_file.write_text("""\
@module test
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
""")
        args = Namespace(file=str(nl_file), stat=False, full=False)
        result = cmd_diff(args)
        # Should succeed but show everything as new
        assert result == 0

    def test_diff_command_name_works_from_cli(self, tmp_path):
        """`nlsc diff` should be recognized by argparse."""
        nl_file = tmp_path / "test.nl"
        nl_file.write_text("""\
@module test
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
""")
        result = subprocess.run(
            [sys.executable, "-m", "nlsc", "diff", str(nl_file), "--stat"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0


class TestDiffDetection:
    """Tests for detecting changes between .nl and lockfile"""

    def test_detect_unchanged_anlu(self, tmp_path):
        """Unchanged ANLU should be reported correctly"""
        from nlsc.diff import get_anlu_changes
        from nlsc.parser import parse_nl_file
        from nlsc.lockfile import generate_lockfile
        from nlsc.emitter import emit_python

        nl_source = """\
@module test
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
"""
        nl_file = parse_nl_file(nl_source)
        py_code = emit_python(nl_file)
        lockfile = generate_lockfile(nl_file, py_code, "test.py", "mock")

        # Compare same source - should be unchanged
        changes = get_anlu_changes(nl_file, lockfile)
        assert len(changes) == 1
        assert changes[0].status == "unchanged"

    def test_detect_modified_anlu(self, tmp_path):
        """Modified ANLU should be detected"""
        from nlsc.diff import get_anlu_changes
        from nlsc.parser import parse_nl_file
        from nlsc.lockfile import generate_lockfile
        from nlsc.emitter import emit_python

        original_nl = """\
@module test
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
"""
        modified_nl = """\
@module test
@target python

[add]
PURPOSE: Add two numbers together
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
"""
        # Generate lockfile from original
        nl_file_orig = parse_nl_file(original_nl)
        py_code = emit_python(nl_file_orig)
        lockfile = generate_lockfile(nl_file_orig, py_code, "test.py", "mock")

        # Compare with modified
        nl_file_mod = parse_nl_file(modified_nl)
        changes = get_anlu_changes(nl_file_mod, lockfile)

        assert len(changes) == 1
        assert changes[0].status == "modified"

    def test_detect_new_anlu(self, tmp_path):
        """New ANLU should be detected"""
        from nlsc.diff import get_anlu_changes
        from nlsc.parser import parse_nl_file
        from nlsc.lockfile import generate_lockfile
        from nlsc.emitter import emit_python

        original_nl = """\
@module test
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
"""
        extended_nl = """\
@module test
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

[subtract]
PURPOSE: Subtract b from a
INPUTS:
  - a: number
  - b: number
RETURNS: a - b
"""
        # Generate lockfile from original
        nl_file_orig = parse_nl_file(original_nl)
        py_code = emit_python(nl_file_orig)
        lockfile = generate_lockfile(nl_file_orig, py_code, "test.py", "mock")

        # Compare with extended
        nl_file_ext = parse_nl_file(extended_nl)
        changes = get_anlu_changes(nl_file_ext, lockfile)

        assert len(changes) == 2
        statuses = {c.identifier: c.status for c in changes}
        assert statuses["add"] == "unchanged"
        assert statuses["subtract"] == "new"

    def test_detect_removed_anlu(self, tmp_path):
        """Removed ANLU should be detected"""
        from nlsc.diff import get_anlu_changes
        from nlsc.parser import parse_nl_file
        from nlsc.lockfile import generate_lockfile
        from nlsc.emitter import emit_python

        original_nl = """\
@module test
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

[subtract]
PURPOSE: Subtract b from a
INPUTS:
  - a: number
  - b: number
RETURNS: a - b
"""
        reduced_nl = """\
@module test
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
"""
        # Generate lockfile from original
        nl_file_orig = parse_nl_file(original_nl)
        py_code = emit_python(nl_file_orig)
        lockfile = generate_lockfile(nl_file_orig, py_code, "test.py", "mock")

        # Compare with reduced
        nl_file_red = parse_nl_file(reduced_nl)
        changes = get_anlu_changes(nl_file_red, lockfile)

        assert len(changes) == 2
        statuses = {c.identifier: c.status for c in changes}
        assert statuses["add"] == "unchanged"
        assert statuses["subtract"] == "removed"


class TestDiffOutput:
    """Tests for diff output formatting"""

    def test_stat_output(self, tmp_path):
        """--stat should show summary"""
        from nlsc.diff import format_stat_output

        changes = [
            type("Change", (), {"identifier": "add", "status": "unchanged"})(),
            type("Change", (), {"identifier": "sub", "status": "modified"})(),
            type("Change", (), {"identifier": "mul", "status": "new"})(),
        ]

        output = format_stat_output(changes)
        assert "1 unchanged" in output
        assert "1 modified" in output
        assert "1 new" in output


class TestFullDiff:
    """Tests for unified diff output"""

    def test_full_diff_shows_python_changes(self, tmp_path):
        """--full should show unified diff of Python output"""
        from nlsc.diff import generate_full_diff
        from nlsc.parser import parse_nl_file
        from nlsc.emitter import emit_python

        original_nl = """\
@module test
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
"""
        modified_nl = """\
@module test
@target python

[add]
PURPOSE: Add two values
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
"""
        nl_file_orig = parse_nl_file(original_nl)
        py_orig = emit_python(nl_file_orig)

        nl_file_mod = parse_nl_file(modified_nl)
        py_mod = emit_python(nl_file_mod)

        diff_output = generate_full_diff(py_orig, py_mod)

        # Should contain diff markers
        assert "---" in diff_output or "unchanged" in diff_output.lower()
