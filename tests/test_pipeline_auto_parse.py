"""Regression tests for automatic parser fallback."""

from pathlib import Path

from nlsc.emitter import emit_python
from nlsc.pipeline import parse_nl_path_auto


SOURCE_WITH_OUTPUT_BINDINGS_AND_TESTS = """\
@module sorting
@target python

[quick-sort]
PURPOSE: Sort a list of numbers using the quicksort algorithm
INPUTS:
  - items: list of number
EDGE CASES:
  - len(items) < 2 -> return items
LOGIC:
  1. items[0] -> pivot
  2. [x for x in items if x < pivot] -> lesser
  3. [x for x in items if x == pivot] -> equal
  4. [x for x in items if x > pivot] -> greater
  5. [quick-sort](lesser) -> sorted_lesser
  6. [quick-sort](greater) -> sorted_greater
RETURNS: sorted_lesser + equal + sorted_greater

@test [quick-sort] {
  quick_sort([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]
}
"""


def test_parse_nl_path_auto_falls_back_when_tree_sitter_drops_output_bindings(
    tmp_path: Path,
):
    source_path = tmp_path / "sorting.nl"
    source_path.write_text(SOURCE_WITH_OUTPUT_BINDINGS_AND_TESTS, encoding="utf-8")

    nl_file = parse_nl_path_auto(source_path)
    anlu = nl_file.anlus[0]

    assert len(nl_file.tests) == 1
    assert anlu.logic_steps[0].output_binding == "pivot"
    assert anlu.logic_steps[-1].output_binding == "sorted_greater"

    code = emit_python(nl_file)
    namespace = {}
    exec(code, namespace)

    assert namespace["quick_sort"]([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]
