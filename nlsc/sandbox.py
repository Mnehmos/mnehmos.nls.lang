"""Best-effort runtime sandbox for ``nlsc run --sandbox`` (Issue #150).

Honest framing: this is **defense in depth, not a security boundary**.
It runs generated Python in an isolated interpreter (``-I``: no
environment variables, no user site-packages on the path) with an audit
hook that blocks a curated set of dangerous operations.  Audit hooks are
installed before user code is imported and cannot be removed, but a
determined attacker can still escape through native extensions or
reflection.

For untrusted input, use an OS-level boundary (container, VM, seccomp,
Windows Sandbox) as described in ``docs/security.md``.

Denied:
- process execution (``os.system``, ``subprocess.Popen``, ``os.exec*``);
- network access (socket connect/bind/getaddrinfo, urllib, http.client,
  ftplib);
- native interop (``ctypes.dlopen``/``dlsym``);
- filesystem mutation (write-mode ``open``, ``os.remove``/``rename``/
  ``mkdir``/``rmdir``, ``shutil.rmtree``, ``os.chmod``/``chown``), except
  writes inside the run's own temporary directory;
- GUI/browser launching (``webbrowser.open``).

Read-only file access is permitted.
"""

from __future__ import annotations

import sys
from pathlib import Path

DEFAULT_SANDBOX_TIMEOUT_SECONDS = 30

# Audit events denied outright (exact names, per sys.addaudithook).
DENIED_AUDIT_EVENTS = (
    "os.system",
    "os.exec",
    "os.posix_spawn",
    "os.spawn",
    "subprocess.Popen",
    "socket.connect",
    "socket.bind",
    "socket.getaddrinfo",
    "socket.gethostbyname",
    "socket.sendto",
    "urllib.Request",
    "http.client.connect",
    "ftplib.connect",
    "smtplib.connect",
    "ctypes.dlopen",
    "ctypes.dlsym",
    "ctypes.dlsym/handle",
    "os.remove",
    "os.rename",
    "os.replace",
    "os.mkdir",
    "os.rmdir",
    "os.chmod",
    "os.chown",
    "os.truncate",
    "shutil.rmtree",
    "shutil.copyfile",
    "shutil.move",
    "webbrowser.open",
)

_WRITE_FLAG_BITS = 0  # resolved inside the runner via os flags


def sandbox_runner_source(
    *,
    temp_dir: str,
    source_root: str,
    module_name: str,
    module_path: str,
    entry_point: str | None,
) -> str:
    """Source of the sandboxed runner written into the run directory."""
    denied = repr(list(DENIED_AUDIT_EVENTS))
    if entry_point:
        invocation_code = (
            f"from {module_name} import {entry_point}\n{entry_point}()"
        )
    else:
        invocation_code = (
            "import runpy\n"
            f"runpy.run_path({module_path!r}, run_name='__main__')"
        )
    return f'''"""Generated sandbox runner (nlsc run --sandbox)."""
import os
import sys

_TEMP_DIR = os.path.realpath({temp_dir!r})
_DENIED_EVENTS = {denied}
_DENIED_PREFIXES = ("os.exec", "os.spawn", "socket.", "ctypes.", "shutil.")
_WRITE_MODES = ("w", "a", "x", "+")
_WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC


def _is_denied(event, args):
    if event in _DENIED_EVENTS:
        return True
    for prefix in _DENIED_PREFIXES:
        if event.startswith(prefix):
            return True
    if event == "open":
        path, mode, flags = args
        wants_write = any(ch in (mode or "") for ch in _WRITE_MODES)
        if isinstance(flags, int) and flags & _WRITE_FLAGS:
            wants_write = True
        if wants_write:
            try:
                resolved = os.path.realpath(os.fspath(path))
            except TypeError:
                return True
            return not resolved.startswith(_TEMP_DIR)
    return False


def _hook(event, args):
    if _is_denied(event, args):
        raise PermissionError(
            "sandbox: blocked '{{}}' (run without --sandbox or use an OS-level "
            "boundary for untrusted code)".format(event)
        )


sys.addaudithook(_hook)

sys.path.insert(0, {source_root!r})
sys.path.insert(0, {temp_dir!r})

{invocation_code}
'''


def write_sandbox_runner(
    temp_dir: Path,
    *,
    source_root: Path,
    module_name: str,
    module_path: Path,
    entry_point: str | None,
) -> Path:
    """Write the runner script and return its path."""
    runner_path = temp_dir / "_nlsc_sandbox.py"
    runner_path.write_text(
        sandbox_runner_source(
            temp_dir=str(temp_dir.resolve()),
            source_root=str(source_root.resolve()),
            module_name=module_name,
            module_path=str(module_path.resolve()),
            entry_point=entry_point,
        ),
        encoding="utf-8",
    )
    return runner_path


def sandbox_command(runner_path: Path) -> list[str]:
    """Isolated interpreter invocation for the sandbox runner."""
    # -I: isolated mode (no PYTHONPATH, no user site-packages, cwd off
    # sys.path); the runner inserts the needed paths itself.
    return [sys.executable, "-I", str(runner_path)]


def sandbox_env() -> dict[str, str]:
    """Curated environment for sandboxed runs."""
    env = {
        "PATH": "",
        "PYTHONIOENCODING": "utf-8",
    }
    if sys.platform == "win32":
        # Python needs SystemRoot for its own startup on Windows.
        system_root = __import__("os").environ.get("SystemRoot")
        if system_root:
            env["SystemRoot"] = system_root
    return env
