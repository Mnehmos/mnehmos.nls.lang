"""Issue #192: step numbers are node identities in the graph.

Duplicate LOGIC step numbers silently collapsed graph nodes (the second
step overwrote the first and the layering returned an empty schedule
while the emitter still returned a value).  Duplicates are now rejected
at parse time with both source locations, and the layering never drops
steps silently.
"""

from __future__ import annotations

import pytest

from nlsc.cli import main
from nlsc.parser import ParseError, parse_nl_file
from nlsc.parser_treesitter import is_available, parse_nl_file_treesitter
from nlsc.schema import ANLU, LogicStep

DUPLICATE_STEPS = """@module duplicate_step
[probe]
PURPOSE: Expose graph identity collision
LOGIC:
  1. x = 1
  1. y = x + 1
RETURNS: y
"""

VALID_STEPS = """@module valid_steps
[probe]
PURPOSE: layered
INPUTS:
  - a: number
  - b: number
LOGIC:
  1. x = a + b
  2. y = a - b
  3. z = x * y
RETURNS: z
"""


def test_duplicate_step_numbers_are_rejected_with_both_lines():
    with pytest.raises(ParseError) as excinfo:
        parse_nl_file(DUPLICATE_STEPS)
    message = str(excinfo.value)
    assert "Duplicate LOGIC step number 1" in message
    assert "line 5" in message and "line 6" in message


def test_duplicate_step_numbers_rejected_on_treesitter_path():
    if not is_available():
        pytest.skip("tree-sitter backend not installed")
    with pytest.raises(ParseError) as excinfo:
        parse_nl_file_treesitter(DUPLICATE_STEPS)
    assert "Duplicate LOGIC step number 1" in str(excinfo.value)


def test_duplicate_steps_fail_cli_verify(tmp_path, capsys):
    path = tmp_path / "dup.nl"
    path.write_text(DUPLICATE_STEPS, encoding="utf-8")
    assert main(["verify", str(path)]) == 1
    assert "Duplicate LOGIC step number 1" in capsys.readouterr().err


def test_valid_steps_layer_completely():
    anlu = parse_nl_file(VALID_STEPS).anlus[0]
    assert anlu.dependency_layers() == [[1, 2], [3]]
    assert anlu.parallel_groups() == [[1, 2], [3]]


def test_programmatic_cycle_keeps_every_step_visible():
    # A cycle cannot occur in parsed sources (dependencies point
    # backwards only), but programmatic graphs must not lose nodes.
    anlu = ANLU(
        identifier="cycle",
        purpose="p",
        returns="x",
        logic_steps=[
            LogicStep(number=1, description="x = y"),
            LogicStep(number=2, description="y = x", depends_on=[1]),
        ],
    )
    anlu.logic_steps[0].depends_on = [2]
    layers = anlu.dependency_layers()
    assert sorted(num for layer in layers for num in layer) == [1, 2]


def test_layers_preserve_every_step_exactly_once():
    anlu = parse_nl_file(VALID_STEPS).anlus[0]
    layers = anlu.dependency_layers()
    flattened = [num for layer in layers for num in layer]
    assert sorted(flattened) == [1, 2, 3]
    assert len(flattened) == len(set(flattened))
