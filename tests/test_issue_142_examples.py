"""Issue #142: the feature example corpus is a live regression suite.

Every ``examples/features/*.nl`` file must pass strict verification, run
its committed lockfile through the CI gate (proving the lock is current
and the tests pass), and execute its ``@main`` block.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from nlsc.cli import main

FEATURES_DIR = Path(__file__).resolve().parent.parent / "examples" / "features"
EXAMPLE_FILES = sorted(FEATURES_DIR.glob("*.nl"))

EXPECTED_COUNT = 14


def test_corpus_has_the_documented_files():
    assert len(EXAMPLE_FILES) == EXPECTED_COUNT, [p.name for p in EXAMPLE_FILES]


@pytest.mark.parametrize("path", EXAMPLE_FILES, ids=lambda p: p.stem)
def test_example_passes_strict_verification(path):
    assert main(["verify", str(path), "--strict"]) == 0


@pytest.mark.parametrize("path", EXAMPLE_FILES, ids=lambda p: p.stem)
def test_example_ci_gate_with_tests(path):
    # ci verifies the committed lockfile is current and never rewrites it;
    # --test runs the example's @test specifications.
    assert main(["ci", str(path), "--test"]) == 0


def test_stdlib_shadowing_module_names_warn():
    from nlsc.parser import parse_nl_file
    from nlsc.typecheck import check_module

    source = "@module json\n[noop]\nPURPOSE: p\nRETURNS: 1\n"
    result = check_module(parse_nl_file(source, source_path="json.nl"))
    assert "ESEM013" in [d.code for d in result.warnings]
    assert not result.errors


@pytest.mark.parametrize("path", EXAMPLE_FILES, ids=lambda p: p.stem)
def test_example_runs_its_main_block(path):
    text = path.read_text(encoding="utf-8")
    if "@main" not in text:
        pytest.skip("no @main block")
    assert main(["run", str(path)]) == 0
