"""Tests for Python -> NLS -> Python roundtrip stress helpers."""

from pathlib import Path

from nlsc.roundtrip import (
    roundtrip_python_file,
    roundtrip_python_repository,
    validate_python_source_roundtrip,
)


def test_validate_python_source_roundtrip_matches_simple_behavior():
    py_source = '''\
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b
'''

    result = validate_python_source_roundtrip(
        py_source,
        "add",
        [(1.0, 2.0), (0.0, 0.0), (-5.0, 10.0)],
        module_name="arithmetic",
    )

    assert result.success
    assert result.all_match
    assert result.stage == "ok"
    assert "@module arithmetic" in result.atomized_nl
    assert "RETURNS: a + b" in result.atomized_nl


def test_validate_python_source_roundtrip_matches_variadic_behavior():
    py_source = '''\
def sum_all(*values: float) -> float:
    """Sum all values."""
    return sum(values)
'''

    result = validate_python_source_roundtrip(
        py_source,
        "sum_all",
        [(1.0, 2.0, 3.0)],
        module_name="variadics",
    )

    assert result.success
    assert result.all_match
    assert result.stage == "ok"


def test_roundtrip_python_file_writes_artifacts(tmp_path: Path):
    source_path = tmp_path / "repo" / "math_ops.py"
    source_path.parent.mkdir()
    source_path.write_text(
        '''\
def square(n: float) -> float:
    """Square a number."""
    return n * n
''',
        encoding="utf-8",
    )

    output_root = tmp_path / "converted"
    result = roundtrip_python_file(
        source_path,
        repo_root=source_path.parent,
        output_root=output_root,
        function_test_cases={"square": [(2.0,), (-3.0,), (0.5,)]},
    )

    assert result.success
    assert result.all_match
    assert (output_root / "math_ops.nl").exists()
    assert (output_root / "math_ops.roundtrip.py").exists()


def test_roundtrip_python_repository_aggregates_successes_and_failures(tmp_path: Path):
    repo_root = tmp_path / "sample_repo"
    repo_root.mkdir()
    (repo_root / "good.py").write_text(
        '''\
def double(x: float) -> float:
    """Double a number."""
    return x * 2
''',
        encoding="utf-8",
    )
    (repo_root / "weak.py").write_text(
        '''\
def sum_all(*values: float) -> float:
    """Sum all values."""
    return sum(values)
''',
        encoding="utf-8",
    )

    output_root = tmp_path / "intent_repo"
    report = roundtrip_python_repository(
        repo_root,
        output_root,
        function_test_cases_by_file={
            "good.py": {"double": [(1.0,), (4.0,)]},
            "weak.py": {"sum_all": [(1.0, 2.0, 3.0)]},
        },
    )

    assert report.total_files == 2
    assert report.succeeded_files == 2
    assert report.failed_files == 0
    assert (output_root / "good.nl").exists()
    assert (output_root / "weak.nl").exists()


def test_roundtrip_python_file_without_behavior_specs_skips_module_execution(
    tmp_path: Path,
):
    source_path = tmp_path / "repo" / "scriptish.py"
    source_path.parent.mkdir()
    source_path.write_text(
        '''\
HERE = __file__

def square(n: float) -> float:
    """Square a number."""
    return n * n
''',
        encoding="utf-8",
    )

    output_root = tmp_path / "converted"
    result = roundtrip_python_file(
        source_path,
        repo_root=source_path.parent,
        output_root=output_root,
    )

    assert result.success
    assert result.all_match
    assert result.stage == "ok"
    assert not result.errors
