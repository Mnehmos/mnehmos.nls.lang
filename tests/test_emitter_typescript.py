"""Tests for the TypeScript emitter."""

from nlsc.parser import parse_nl_file
from nlsc.emitter_typescript import emit_tests_typescript, emit_typescript


def test_emit_typescript_math_functions():
    source = """\
@module math
@target typescript

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

[multiply]
PURPOSE: Multiply two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a × b
"""
    nl_file = parse_nl_file(source, source_path="math.nl")

    code = emit_typescript(nl_file)

    assert "export function add(a: number, b: number): number {" in code
    assert "return a + b;" in code
    assert "export function multiply(a: number, b: number): number {" in code
    assert "return a * b;" in code


def test_emit_typescript_quicksort_logic():
    source = """\
@module sorting
@target typescript

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
    nl_file = parse_nl_file(source, source_path="sorting.nl")

    code = emit_typescript(nl_file)
    test_code = emit_tests_typescript(nl_file)

    assert test_code is not None
    assert "export function quick_sort(items: number[]): number[] {" in code
    assert "if (items.length < 2) {" in code
    assert "const lesser = items.filter((x) => x < pivot);" in code
    assert "const equal = items.filter((x) => x === pivot);" in code
    assert "return [...sorted_lesser, ...equal, ...sorted_greater];" in code
    assert 'import assert from "node:assert/strict";' in test_code
    assert (
        "assert.deepStrictEqual(quick_sort([3, 1, 4, 1, 5]), [1, 1, 3, 4, 5]);"
        in test_code
    )
