"""Cross-platform CLI regressions for issue #140."""

from __future__ import annotations

import subprocess
import sys
from argparse import Namespace
from pathlib import Path

from nlsc import cli
from nlsc.pipeline import create_temp_workdir


SIMPLE_PROGRAM = """\
@module hello-world
@target python

[main]
PURPOSE: Print hello
LOGIC:
  1. Print "Hello from NLS"
RETURNS: void
"""


TEST_PROGRAM = """\
@module calculator
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

@test [add] {
  add(2, 3) == 5
}
"""


def test_cmd_compile_handles_source_path_with_spaces(tmp_path: Path) -> None:
    source_dir = tmp_path / "dir with spaces"
    source_dir.mkdir()
    source_path = source_dir / "hello world.nl"
    source_path.write_text(SIMPLE_PROGRAM, encoding="utf-8")

    args = Namespace(file=str(source_path), target=None, output=None, stdlib_path=[])

    exit_code = cli.cmd_compile(args)

    assert exit_code == 0
    assert (source_dir / "hello world.py").exists()
    assert (source_dir / "hello world.nl.lock").exists()


def test_cli_run_handles_source_path_with_spaces(tmp_path: Path) -> None:
    source_dir = tmp_path / "dir with spaces"
    source_dir.mkdir()
    source_path = source_dir / "hello world.nl"
    source_path.write_text(SIMPLE_PROGRAM, encoding="utf-8")
    keep_dir = tmp_path / "keep dir"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "nlsc",
            "run",
            str(source_path),
            "--keep",
            str(keep_dir),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert (keep_dir / "hello_world.py").exists()


def test_cmd_test_handles_source_path_with_spaces(tmp_path: Path) -> None:
    source_dir = tmp_path / "dir with spaces"
    source_dir.mkdir()
    source_path = source_dir / "calculator spec.nl"
    source_path.write_text(TEST_PROGRAM, encoding="utf-8")

    args = Namespace(file=str(source_path), verbose=False, case=None)

    exit_code = cli.cmd_test(args)

    assert exit_code == 0


def test_create_temp_workdir_falls_back_when_preferred_root_is_unusable(
    tmp_path: Path, monkeypatch
) -> None:
    unusable_root = tmp_path / "not-a-directory"
    unusable_root.write_text("blocking file", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    temp_dir = create_temp_workdir("nlsc_test_", preferred_root=unusable_root)
    try:
        assert temp_dir.exists()
        assert temp_dir.is_dir()
        assert unusable_root not in temp_dir.parents
    finally:
        temp_dir.rmdir()
