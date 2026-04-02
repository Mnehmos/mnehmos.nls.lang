"""Tests for TypeScript CLI compilation."""

from argparse import Namespace
from pathlib import Path

from nlsc import cli
from nlsc.lockfile import read_lockfile


def test_cmd_compile_uses_source_target_typescript(tmp_path: Path):
    source_path = tmp_path / "sorting.nl"
    source_path.write_text(
        """\
@module sorting
@target typescript

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

@test [add] {
  add(2, 3) == 5
}
""",
        encoding="utf-8",
    )

    args = Namespace(
        file=str(source_path),
        target=None,
        output=None,
        stdlib_path=[],
    )

    exit_code = cli.cmd_compile(args)

    assert exit_code == 0
    assert (tmp_path / "sorting.ts").exists()
    assert (tmp_path / "test_sorting.ts").exists()

    lockfile = read_lockfile(tmp_path / "sorting.nl.lock")
    assert lockfile is not None
    assert "typescript" in lockfile.targets
    assert lockfile.targets["typescript"].file.endswith("sorting.ts")
