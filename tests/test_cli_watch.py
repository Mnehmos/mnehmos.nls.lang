"""Tests for nlsc watch command - Issue #14"""

import json
import py_compile
import pytest
import time
from pathlib import Path
from argparse import Namespace
from unittest.mock import patch

from nlsc.diagnostics import Diagnostic

from nlsc.cli import cmd_watch


class TestWatchCommand:
    """Tests for nlsc watch CLI command"""

    def test_cmd_watch_exists(self):
        """cmd_watch function should exist"""
        assert callable(cmd_watch)

    def test_watch_directory_not_found(self):
        """nlsc watch should error on missing directory"""
        args = Namespace(dir="nonexistent_dir", test=False, quiet=False, debounce=100)
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

        def on_compile(path, success, error=None, diagnostics=None):
            compiled_files.append((path, success, error, diagnostics))

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
        assert compiled_files[0][3] is None

    def test_compile_with_error(self, tmp_path):
        """Watcher should report compilation errors"""
        from nlsc.watch import NLWatcher

        compiled_files = []

        def on_compile(path, success, error=None, diagnostics=None):
            compiled_files.append((path, success, error, diagnostics))

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
        assert [d.code for d in compiled_files[0][3]] == ["E_RESOLUTION"]

    def test_compile_reports_parse_error_diagnostics(self, tmp_path):
        """Watcher should surface structured parse diagnostics for runtime failures."""
        from nlsc.watch import NLWatcher

        compiled_files = []

        def on_compile(path, success, error=None, diagnostics=None):
            compiled_files.append((path, success, error, diagnostics))

        watcher = NLWatcher(tmp_path, on_compile=on_compile)

        nl_file = tmp_path / "broken.nl"
        nl_file.write_text(
            """\
@module broken
@target python

[main]
PURPOSE: Broken
LOGIC:
  first step is not numbered
RETURNS: void
"""
        )

        watcher.compile_file(nl_file)

        assert len(compiled_files) == 1
        assert compiled_files[0][1] is False
        assert compiled_files[0][3] is not None
        assert [d.code for d in compiled_files[0][3]] == ["EPARSE001"]
        assert compiled_files[0][3][0].line == 7
        assert "Invalid LOGIC step format" in compiled_files[0][2]

    def test_compile_reports_stdlib_use_errors(self, tmp_path):
        """Watcher should surface @use resolution failures from shared validation."""
        from nlsc.watch import NLWatcher

        compiled_files = []

        def on_compile(path, success, error=None, diagnostics=None):
            compiled_files.append((path, success, error, diagnostics))

        watcher = NLWatcher(tmp_path, on_compile=on_compile)

        nl_file = tmp_path / "missing_use.nl"
        nl_file.write_text("""\
@module missing-use
@target python
@use math.missing

[calc]
PURPOSE: Return zero
RETURNS: 0
""")

        watcher.compile_file(nl_file)

        assert len(compiled_files) == 1
        assert compiled_files[0][1] is False
        assert "EUSE001" in compiled_files[0][2]
        assert "math" in compiled_files[0][2]
        assert [d.code for d in compiled_files[0][3]] == ["EUSE001"]

    def test_compile_reports_unsupported_target_diagnostic(self, tmp_path):
        """Watcher should reuse ETARGET001 for unsupported runtime targets."""
        from nlsc.watch import NLWatcher

        compiled_files = []

        def on_compile(path, success, error=None, diagnostics=None):
            compiled_files.append((path, success, error, diagnostics))

        watcher = NLWatcher(tmp_path, on_compile=on_compile)

        nl_file = tmp_path / "unsupported_target.nl"
        nl_file.write_text(
            """\
@module unsupported-target
@target ruby

[main]
PURPOSE: Unsupported target
RETURNS: 1
"""
        )

        watcher.compile_file(nl_file)

        assert len(compiled_files) == 1
        assert compiled_files[0][1] is False
        assert compiled_files[0][3] is not None
        assert [d.code for d in compiled_files[0][3]] == ["ETARGET001"]
        assert compiled_files[0][3][0].file == str(nl_file)

    def test_compile_reports_validation_diagnostic(self, tmp_path):
        """Watcher should reuse EVALIDATE001 for post-emit validation failures."""
        from nlsc.watch import NLWatcher

        compiled_files = []

        def on_compile(path, success, error=None, diagnostics=None):
            compiled_files.append((path, success, error, diagnostics))

        watcher = NLWatcher(tmp_path, on_compile=on_compile)

        nl_file = tmp_path / "validation.nl"
        nl_file.write_text(
            """\
@module validation
@target python

[main]
PURPOSE: Validation failure
RETURNS: 1
"""
        )

        compile_error = py_compile.PyCompileError(
            SyntaxError,
            SyntaxError("invalid generated code"),
            str(nl_file.with_suffix(".py")),
        )
        with patch("nlsc.watch.py_compile.compile", side_effect=compile_error):
            watcher.compile_file(nl_file)

        assert len(compiled_files) == 1
        assert compiled_files[0][1] is False
        assert compiled_files[0][3] is not None
        assert [d.code for d in compiled_files[0][3]] == ["EVALIDATE001"]
        assert compiled_files[0][3][0].file == str(nl_file.with_suffix(".py"))

    def test_compile_reports_watch_runtime_fallback_diagnostic(self, tmp_path):
        """Watcher should use EWATCH002 for unexpected runtime compile failures."""
        from nlsc.watch import NLWatcher

        compiled_files = []

        def on_compile(path, success, error=None, diagnostics=None):
            compiled_files.append((path, success, error, diagnostics))

        watcher = NLWatcher(tmp_path, on_compile=on_compile)

        nl_file = tmp_path / "fallback.nl"
        nl_file.write_text(
            """\
@module fallback
@target python

[main]
PURPOSE: Fallback failure
RETURNS: 1
"""
        )

        with patch("pathlib.Path.write_text", side_effect=OSError("disk is full")):
            watcher.compile_file(nl_file)

        assert len(compiled_files) == 1
        assert compiled_files[0][1] is False
        assert compiled_files[0][3] is not None
        assert [d.code for d in compiled_files[0][3]] == ["EWATCH002"]
        assert "disk is full" in compiled_files[0][2]

    def test_cmd_watch_json_emits_runtime_compile_diagnostic_after_startup(
        self, tmp_path, capsys
    ):
        """watch --json should emit structured runtime diagnostics from compile callbacks."""

        args = Namespace(
            dir=str(tmp_path),
            test=False,
            quiet=False,
            debounce=100,
            json=True,
        )

        runtime_diagnostic = Diagnostic(
            code="EPARSE001",
            file=str(tmp_path / "broken.nl"),
            line=7,
            col=None,
            message="Invalid LOGIC step format; expected numbered step like '1. ...'",
            hint="Rewrite the line as a numbered LOGIC step like '1. ...'.",
        )

        def fake_start(self):
            assert self.on_compile is not None
            self.on_compile(
                tmp_path / "broken.nl",
                False,
                runtime_diagnostic.message,
                [runtime_diagnostic],
            )

        with patch("nlsc.cli.NLWatcher.start", new=fake_start):
            result = cmd_watch(args)

        captured = capsys.readouterr()

        assert result == 0
        assert f"Watching {tmp_path.absolute()} for .nl changes..." in captured.out
        payload = json.loads(captured.out[captured.out.index("{") :])
        assert payload["command"] == "watch"
        assert payload["event"] == "compile"
        assert payload["phase"] == "runtime"
        assert payload["ok"] is False
        assert payload["diagnostics"] == [runtime_diagnostic.to_dict()]


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
