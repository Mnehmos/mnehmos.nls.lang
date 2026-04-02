"""
NLS Watch - Continuous compilation on file changes

Watches .nl files and recompiles on save.
"""

import time
import py_compile
from inspect import signature
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

from .diagnostics import (
    Diagnostic,
    dependency_error_diagnostics,
    parse_error_diagnostic,
    stdlib_use_diagnostic,
)
from .emitter import emit_python, emit_tests
from .emitter_typescript import emit_tests_typescript, emit_typescript
from .error_catalog import ETARGET001, EVALIDATE001, EWATCH002


def is_nl_file(path: Path) -> bool:
    """Check if a path is an NL source file (not a lockfile)."""
    path_str = str(path)
    if path_str.endswith(".nl.lock"):
        return False
    return path_str.endswith(".nl")


class NLWatcher:
    """
    Watches a directory for .nl file changes and triggers recompilation.

    Args:
        watch_path: Directory to watch
        debounce_ms: Debounce interval in milliseconds (default: 100)
        quiet: Suppress success messages (default: False)
        run_tests: Run tests after successful compile (default: False)
        on_compile: Callback for compilation events
    """

    def __init__(
        self,
        watch_path: Path,
        debounce_ms: int = 100,
        quiet: bool = False,
        run_tests: bool = False,
        on_compile: Optional[Callable[..., None]] = None,
    ):
        self.watch_path = Path(watch_path)
        self.debounce_ms = debounce_ms
        self.quiet = quiet
        self.run_tests = run_tests
        self.on_compile = on_compile

        # Track file modification times for debouncing
        self._last_compile: dict[Path, float] = {}
        self._running = False

    def _notify_compile(
        self,
        path: Path,
        success: bool,
        error: str | None = None,
        diagnostics: list[Diagnostic] | None = None,
    ) -> None:
        if self.on_compile is None:
            return

        callback: Callable[..., None] = self.on_compile

        if len(signature(callback).parameters) >= 4:
            callback(path, success, error, diagnostics)
        else:
            callback(path, success, error)

    def compile_file(self, path: Path) -> bool:
        """
        Compile a single .nl file.

        Args:
            path: Path to the .nl file

        Returns:
            True if compilation succeeded, False otherwise
        """
        from .parser import ParseError
        from .lockfile import generate_lockfile, write_lockfile
        from .pipeline import parse_nl_path_auto, validate_semantics
        from .stdlib_resolver import StdlibUseError

        error_msg = None
        diagnostics: list[Diagnostic] | None = None
        success = False
        output_path: Path | None = None

        try:
            # Parse
            nl_file = parse_nl_path_auto(path)

            validation = validate_semantics(nl_file, path)
            if validation.dependency_errors:
                diagnostics = dependency_error_diagnostics(
                    path, nl_file, validation.dependency_errors
                )
                error_msg = "; ".join(diagnostic.message for diagnostic in diagnostics)
                self._notify_compile(path, False, error_msg, diagnostics)
                return False

            target = nl_file.module.target or "python"
            if target == "python":
                generated_code = emit_python(nl_file, mode="mock")
                output_path = path.with_suffix(".py")
                test_code = emit_tests(nl_file)
                test_path = path.parent / f"test_{path.stem}.py"
                py_compile_required = True
            elif target == "typescript":
                generated_code = emit_typescript(nl_file)
                output_path = path.with_suffix(".ts")
                test_code = emit_tests_typescript(nl_file)
                test_path = path.parent / f"test_{path.stem}.ts"
                py_compile_required = False
            else:
                error_msg = f"Target '{target}' not yet supported"
                diagnostics = [
                    Diagnostic(
                        code=ETARGET001,
                        file=str(path),
                        line=None,
                        col=None,
                        message=error_msg,
                        hint="Select a supported target and try again.",
                    )
                ]
                self._notify_compile(path, False, error_msg, diagnostics)
                return False

            output_path.write_text(generated_code, encoding="utf-8")
            if py_compile_required:
                py_compile.compile(str(output_path), doraise=True)

            # Generate tests if present
            if nl_file.tests and test_code:
                test_path.write_text(test_code, encoding="utf-8")

            # Generate lockfile
            lock_path = path.with_suffix(".nl.lock")
            lockfile = generate_lockfile(
                nl_file,
                generated_code,
                str(output_path),
                llm_backend="mock",
                target=target,
            )
            write_lockfile(lockfile, lock_path)

            success = True

        except ParseError as e:
            diagnostics = [parse_error_diagnostic(path, e)]
            error_msg = diagnostics[0].message
        except StdlibUseError as e:
            diagnostics = [stdlib_use_diagnostic(path, e)]
            attempted = [str(p) for p in e.attempted_roots]
            error_msg = (
                f"{diagnostics[0].code} domain={e.domain} major={e.major} "
                f"candidate_relpath={e.candidate_relpath} attempted_roots={attempted}"
            )
        except py_compile.PyCompileError as e:
            output_label = (
                output_path if output_path is not None else path.with_suffix(".py")
            )
            diagnostics = [
                Diagnostic(
                    code=EVALIDATE001,
                    file=str(output_label),
                    line=None,
                    col=None,
                    message=f"py_compile validation failed for {output_label}: {e}",
                    hint="Inspect the generated output and compiler logic.",
                )
            ]
            error_msg = diagnostics[0].message
        except Exception as e:
            diagnostics = [
                Diagnostic(
                    code=EWATCH002,
                    file=str(path),
                    line=None,
                    col=None,
                    message=f"Watch runtime compile failed: {e}",
                    hint="Inspect the source file and runtime message, then save again after correcting the issue.",
                )
            ]
            error_msg = diagnostics[0].message

        self._notify_compile(path, success, error_msg, diagnostics)

        return success

    def _should_compile(self, path: Path) -> bool:
        """Check if file should be compiled (debounce check)."""
        now = time.time()
        last = self._last_compile.get(path, 0)

        if (now - last) * 1000 < self.debounce_ms:
            return False

        self._last_compile[path] = now
        return True

    def on_modified(self, path: Path) -> None:
        """Handle file modification event."""
        if not is_nl_file(path):
            return

        if not self._should_compile(path):
            return

        self.compile_file(path)

    def start(self) -> None:
        """
        Start watching for file changes.

        This is a blocking call that runs until stop() is called.
        """
        self._running = True

        # Try to use watchdog if available, otherwise fall back to polling
        try:
            self._start_watchdog()
        except ImportError:
            self._start_polling()

    def _start_watchdog(self) -> None:
        """Start watching using watchdog library."""
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEvent, FileSystemEventHandler

        watcher = self

        class NLFileHandler(FileSystemEventHandler):
            def on_modified(self, event: FileSystemEvent) -> None:
                if event.is_directory:
                    return
                if isinstance(event.src_path, bytes):
                    return
                path = Path(event.src_path)
                if is_nl_file(path):
                    watcher.on_modified(path)

        handler = NLFileHandler()
        observer = Observer()
        observer.schedule(handler, str(self.watch_path), recursive=True)
        observer.start()

        try:
            while self._running:
                time.sleep(0.1)
        finally:
            observer.stop()
            observer.join()

    def _start_polling(self) -> None:
        """Fallback polling-based watcher."""
        # Track file modification times
        file_mtimes: dict[Path, float] = {}

        # Initial scan
        for path in self.watch_path.rglob("*.nl"):
            if is_nl_file(path):
                file_mtimes[path] = path.stat().st_mtime

        while self._running:
            time.sleep(0.5)  # Poll every 500ms

            # Check for changes
            for path in self.watch_path.rglob("*.nl"):
                if not is_nl_file(path):
                    continue

                mtime = path.stat().st_mtime
                if path not in file_mtimes:
                    # New file
                    file_mtimes[path] = mtime
                    self.on_modified(path)
                elif mtime > file_mtimes[path]:
                    # Modified file
                    file_mtimes[path] = mtime
                    self.on_modified(path)

    def stop(self) -> None:
        """Stop watching for file changes."""
        self._running = False


def format_timestamp() -> str:
    """Format current time for console output."""
    return datetime.now().strftime("[%H:%M:%S]")
