"""Issue #150: `nlsc run --sandbox` blocks dangerous operations.

The sandbox is defense in depth, not a security boundary; these tests pin
the behavior it promises: process execution, networking, and writes
outside the run directory are blocked, reads and pure computation work,
and a wall-clock timeout applies.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from nlsc.cli import main

EVIL_TEMPLATE = '''@module sandbox_probe
@literal python {{
import {import_line}

def poke():
{body}
}}

[poke-it]
PURPOSE: run the probe
LOGIC:
  1. poke()
RETURNS: 0

@main {{
  poke-it()
}}
'''

PURE = """@module sandbox_pure
@main {
  PRINT 6 * 7
}
"""


def _write(tmp_path, source: str, name="probe.nl"):
    path = tmp_path / name
    path.write_text(source, encoding="utf-8")
    return path


def _evil(tmp_path, import_line: str, body: str):
    return _write(
        tmp_path,
        EVIL_TEMPLATE.format(import_line=import_line, body=body),
        "evil.nl",
    )


# --------------------------------------------------------------------------
# Blocked operations
# --------------------------------------------------------------------------


def test_sandbox_blocks_process_execution(tmp_path, capsys):
    path = _evil(tmp_path, "os", "    os.system('echo pwned')")
    assert main(["run", str(path), "--sandbox"]) == 1
    captured = capsys.readouterr()
    assert "sandbox: blocked" in captured.err
    assert "os.system" in captured.err
    # The traceback echoes the source line, but the command never ran:
    # nothing reached stdout.
    assert "pwned" not in captured.out


def test_sandbox_blocks_subprocess(tmp_path, capsys):
    path = _evil(
        tmp_path,
        "subprocess",
        "    subprocess.run(['echo', 'pwned'])",
    )
    assert main(["run", str(path), "--sandbox"]) == 1
    assert "sandbox: blocked" in capsys.readouterr().err


def test_sandbox_blocks_network(tmp_path, capsys):
    path = _evil(
        tmp_path,
        "socket",
        "    s = socket.socket()\n    s.connect(('127.0.0.1', 9))",
    )
    assert main(["run", str(path), "--sandbox"]) == 1
    assert "sandbox: blocked" in capsys.readouterr().err


def test_sandbox_blocks_writes_outside_run_directory(tmp_path, capsys):
    target = (tmp_path / "outside.txt").resolve()
    path = _evil(
        tmp_path,
        "pathlib",
        f"    pathlib.Path(r'{target}').write_text('x')",
    )
    assert main(["run", str(path), "--sandbox"]) == 1
    assert "sandbox: blocked" in capsys.readouterr().err
    assert not target.exists()


# --------------------------------------------------------------------------
# Allowed operations
# --------------------------------------------------------------------------


def test_sandbox_allows_pure_computation(tmp_path, capsys):
    path = _write(tmp_path, PURE, "pure.nl")
    assert main(["run", str(path), "--sandbox"]) == 0
    assert "42" in capsys.readouterr().out


def test_sandbox_allows_reads(tmp_path, capsys):
    readable = (tmp_path / "data.txt").resolve()
    readable.write_text("hello", encoding="utf-8")
    path = _evil(
        tmp_path,
        "pathlib",
        f"    print(pathlib.Path(r'{readable}').read_text())",
    )
    assert main(["run", str(path), "--sandbox"]) == 0
    assert "hello" in capsys.readouterr().out


def test_plain_run_is_unaffected(tmp_path, capsys):
    path = _evil(tmp_path, "os", "    os.system('echo untouched')")
    assert main(["run", str(path)]) == 0
    assert "untouched" in capsys.readouterr().out


# --------------------------------------------------------------------------
# Timeout
# --------------------------------------------------------------------------


def test_sandbox_timeout_is_enforced(tmp_path, capsys):
    path = _evil(tmp_path, "time", "    time.sleep(30)")
    assert main(["run", str(path), "--sandbox", "--timeout", "2"]) == 1
    assert "sandbox timeout exceeded" in capsys.readouterr().err


def test_sandbox_violation_json_payload(tmp_path, capsys):
    import json

    path = _evil(tmp_path, "os", "    os.system('echo pwned')")
    assert main(["run", "--json", str(path), "--sandbox"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is False
