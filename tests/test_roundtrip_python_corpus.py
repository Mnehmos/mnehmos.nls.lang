"""Behavioral corpus for Python -> NLS -> Python stress testing."""

import pytest

from nlsc.roundtrip import validate_python_source_roundtrip


@pytest.mark.parametrize(
    ("name", "py_source", "function_name", "test_cases", "expected_match"),
    [
        (
            "simple_arithmetic",
            '''\
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b
''',
            "add",
            [(1.0, 2.0), (-3.0, 9.0)],
            True,
        ),
        (
            "list_comprehension",
            '''\
def squares(n: int) -> list[int]:
    """Generate squares."""
    return [x * x for x in range(n)]
''',
            "squares",
            [(0,), (4,)],
            True,
        ),
        (
            "conditional_return",
            '''\
def pluralize(word: str, count: int) -> str:
    """Return singular or plural form based on count."""
    return word if count == 1 else word + "s"
''',
            "pluralize",
            [("task", 1), ("task", 3)],
            True,
        ),
        (
            "annotated_argument",
            '''\
from typing import Annotated

def main(name: Annotated[str, "user name"]) -> str:
    """Return the provided name."""
    return name
''',
            "main",
            [("Camila",), ("NLS",)],
            True,
        ),
        (
            "variadic_arguments",
            '''\
def sum_all(*values: float) -> float:
    """Sum all values."""
    return sum(values)
''',
            "sum_all",
            [(1.0, 2.0, 3.0)],
            True,
        ),
        (
            "loop_accumulation",
            '''\
def flatten_list(nested: list[list[int]]) -> list[int]:
    """Flatten a nested list by one level."""
    result = []
    for sublist in nested:
        result.extend(sublist)
    return result
''',
            "flatten_list",
            [([[1, 2], [3], []],)],
            True,
        ),
        (
            "bitwise_accumulation",
            '''\
def all_true(flags: list[bool]) -> bool:
    """Check whether all flags are true."""
    result = True
    for flag in flags:
        result &= flag
    return result
''',
            "all_true",
            [([True, True, True],), ([True, False, True],)],
            True,
        ),
        (
            "try_except_return",
            '''\
def safe_parse(text: str) -> int:
    """Parse safely."""
    try:
        return int(text)
    except ValueError:
        return 0
''',
            "safe_parse",
            [("12",), ("oops",)],
            True,
        ),
    ],
)
def test_python_roundtrip_corpus(
    name, py_source, function_name, test_cases, expected_match
):
    result = validate_python_source_roundtrip(
        py_source,
        function_name,
        test_cases,
        module_name=f"corpus-{name}",
        source_name=name,
    )

    assert result.all_match is expected_match
    if expected_match:
        assert result.success
        assert result.stage == "ok"
    else:
        assert result.errors
