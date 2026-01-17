"""Tests for nlsc watch command - Issue #14"""

import pytest
import time
from pathlib import Path
from argparse import Namespace
from unittest.mock import patch, MagicMock

from nlsc.cli import cmd_watch


class TestWatchCommand:
    """Tests for nlsc watch CLI command"""

    def test_cmd_watch_exists(self):
        """cmd_watch function should exist"""
        assert callable(cmd_watch)

    def test_watch_directory_not_found(self):
        """nlsc watch should error on missing directory"""
        args = Namespace(
            dir="nonexistent_dir",
            test=False,
            quiet=False,
            debounce=100
        )
        result = cmd_watch(args)
        assert result == 1


class TestWatchModule:
    """Tests for watch module functionality"""

    def test_watcher_module_exists(self):
        """Watcher module should exist"""
        from nlsc import watch
        assert hasattr(watch, "NLWatcher")

    def test_watcher_initialization(self, tmp_path):
        """Watcher should initialize with path"""
        from nlsc.watch import NLWatcher

        watcher = NLWatcher(tmp_path)
        assert watcher.watch_path == tmp_path

    def test_debounce_default(self, tmp_path):
        """Watcher should have default debounce"""
        from nlsc.watch import NLWatcher

        watcher = NLWatcher(tmp_path)
        assert watcher.debounce_ms > 0

    def test_debounce_custom(self, tmp_path):
        """Watcher should accept custom debounce"""
        from nlsc.watch import NLWatcher

        watcher = NLWatcher(tmp_path, debounce_ms=200)
        assert watcher.debounce_ms == 200


class TestFileDetection:
    """Tests for detecting .nl file changes"""

    def test_detects_nl_files(self, tmp_path):
        """Watcher should detect .nl files"""
        from nlsc.watch import is_nl_file

        assert is_nl_file(Path("test.nl"))
        assert is_nl_file(Path("src/math.nl"))
        assert not is_nl_file(Path("test.py"))
        assert not is_nl_file(Path("test.txt"))

    def test_ignores_lockfiles(self, tmp_path):
        """Watcher should ignore .nl.lock files"""
        from nlsc.watch import is_nl_file

        assert not is_nl_file(Path("test.nl.lock"))
        assert not is_nl_file(Path("src/math.nl.lock"))


class TestCompileOnChange:
    """Tests for compilation on file change"""

    def test_compile_callback(self, tmp_path):
        """Watcher should call compile on change"""
        from nlsc.watch import NLWatcher

        compiled_files = []

        def on_compile(path, success, error=None):
            compiled_files.append((path, success))

        watcher = NLWatcher(tmp_path, on_compile=on_compile)

        # Create a test file
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

        # Trigger compilation manually
        watcher.compile_file(nl_file)

        assert len(compiled_files) == 1
        assert compiled_files[0][0] == nl_file
        assert compiled_files[0][1] is True  # Success

    def test_compile_with_error(self, tmp_path):
        """Watcher should report compilation errors"""
        from nlsc.watch import NLWatcher

        compiled_files = []

        def on_compile(path, success, error=None):
            compiled_files.append((path, success, error))

        watcher = NLWatcher(tmp_path, on_compile=on_compile)

        # Create file with unresolvable dependency
        nl_file = tmp_path / "invalid.nl"
        nl_file.write_text("""\
@module test
@target python

[broken]
PURPOSE: Test with missing dependency
INPUTS:
  - a: number
DEPENDS: [nonexistent_function]
RETURNS: a
""")

        watcher.compile_file(nl_file)

        assert len(compiled_files) == 1
        assert compiled_files[0][1] is False  # Failed
        assert "nonexistent_function" in compiled_files[0][2]  # Error message


class TestQuietMode:
    """Tests for quiet mode"""

    def test_quiet_suppresses_success(self, tmp_path):
        """Quiet mode should suppress success messages"""
        from nlsc.watch import NLWatcher

        watcher = NLWatcher(tmp_path, quiet=True)
        assert watcher.quiet is True


class TestTestAfterCompile:
    """Tests for running tests after compile"""

    def test_test_flag(self, tmp_path):
        """--test flag should enable test running"""
        from nlsc.watch import NLWatcher

        watcher = NLWatcher(tmp_path, run_tests=True)
        assert watcher.run_tests is True
