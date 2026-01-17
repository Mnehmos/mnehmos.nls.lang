"""
NLS Watch - Continuous compilation on file changes

Watches .nl files and recompiles on save.
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional


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
        on_compile: Optional[Callable[[Path, bool, Optional[str]], None]] = None,
    ):
        self.watch_path = Path(watch_path)
        self.debounce_ms = debounce_ms
        self.quiet = quiet
        self.run_tests = run_tests
        self.on_compile = on_compile

        # Track file modification times for debouncing
        self._last_compile: dict[Path, float] = {}
        self._running = False

    def compile_file(self, path: Path) -> bool:
        """
        Compile a single .nl file.

        Args:
            path: Path to the .nl file

        Returns:
            True if compilation succeeded, False otherwise
        """
        from .parser import parse_nl_path, ParseError
        from .resolver import resolve_dependencies
        from .emitter import emit_python, emit_tests
        from .lockfile import generate_lockfile, write_lockfile

        error_msg = None
        success = False

        try:
            # Parse
            nl_file = parse_nl_path(path)

            # Resolve
            result = resolve_dependencies(nl_file)
            if not result.success:
                error_msg = "; ".join(f"{e.anlu_id}: {e.message}" for e in result.errors)
                if self.on_compile:
                    self.on_compile(path, False, error_msg)
                return False

            # Emit Python
            python_code = emit_python(nl_file, mode="mock")
            output_path = path.with_suffix(".py")
            output_path.write_text(python_code, encoding="utf-8")

            # Generate tests if present
            if nl_file.tests:
                test_code = emit_tests(nl_file)
                if test_code:
                    test_path = path.parent / f"test_{path.stem}.py"
                    test_path.write_text(test_code, encoding="utf-8")

            # Generate lockfile
            lock_path = path.with_suffix(".nl.lock")
            lockfile = generate_lockfile(
                nl_file,
                python_code,
                str(output_path),
                llm_backend="mock"
            )
            write_lockfile(lockfile, lock_path)

            success = True

        except ParseError as e:
            error_msg = f"Parse error: {e}"
        except Exception as e:
            error_msg = f"Error: {e}"

        if self.on_compile:
            self.on_compile(path, success, error_msg)

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
        from watchdog.events import FileSystemEventHandler, FileModifiedEvent

        watcher = self

        class NLFileHandler(FileSystemEventHandler):
            def on_modified(self, event: FileModifiedEvent) -> None:
                if event.is_directory:
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
