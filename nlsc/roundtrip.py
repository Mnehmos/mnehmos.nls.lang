"""
NLS Round-trip Validation - Prove behavioral equivalence

Validates that atomize(compile(x)) ≈ x for behavioral equivalence.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .parser import parse_nl_file
from .emitter import emit_python
from .atomize import atomize_to_nl


@dataclass
class RoundTripResult:
    """Result of a round-trip validation"""

    success: bool
    all_match: bool
    original_results: list[Any] = field(default_factory=list)
    roundtrip_results: list[Any] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class PythonSourceRoundTripResult:
    """Result of Python -> NLS -> Python validation."""

    success: bool
    all_match: bool
    stage: str
    source_name: str
    atomized_nl: str = ""
    regenerated_python: str = ""
    original_results: list[Any] = field(default_factory=list)
    roundtrip_results: list[Any] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class RepositoryRoundTripReport:
    """Aggregate report for repository-scale roundtrip runs."""

    repo_root: str
    output_root: str
    file_results: list[PythonSourceRoundTripResult] = field(default_factory=list)

    @property
    def total_files(self) -> int:
        return len(self.file_results)

    @property
    def succeeded_files(self) -> int:
        return sum(
            1 for result in self.file_results if result.success and result.all_match
        )

    @property
    def unsupported_files(self) -> int:
        return sum(
            1 for result in self.file_results if result.stage == "unsupported_source"
        )

    @property
    def failed_files(self) -> int:
        return self.total_files - self.succeeded_files - self.unsupported_files


def validate_roundtrip(
    nl_source: str,
    function_name: str,
    test_cases: list[tuple],
    module_name: str = "roundtrip_test",
) -> RoundTripResult:
    """
    Validate that a function round-trips correctly.

    Args:
        nl_source: Original NL source code
        function_name: Name of function to test (snake_case)
        test_cases: List of argument tuples to test with
        module_name: Module name for atomization

    Returns:
        RoundTripResult with validation details
    """
    result = RoundTripResult(success=True, all_match=True)

    try:
        # First compile: NL -> Python
        nl_file = parse_nl_file(nl_source)
        py_code = emit_python(nl_file)

        # Execute original
        ns1: dict[str, Any] = {}
        exec(py_code, ns1)

        if function_name not in ns1:
            result.success = False
            result.errors.append(
                f"Function '{function_name}' not found in original code"
            )
            return result

        # Atomize: Python -> NL
        regenerated_nl = atomize_to_nl(py_code, module_name=module_name)

        # Second compile: NL -> Python
        nl_file2 = parse_nl_file(regenerated_nl)
        py_code2 = emit_python(nl_file2)

        # Execute regenerated
        ns2: dict[str, Any] = {}
        exec(py_code2, ns2)

        if function_name not in ns2:
            result.success = False
            result.errors.append(
                f"Function '{function_name}' not found in round-tripped code"
            )
            return result

        # Compare behavior for each test case
        for args in test_cases:
            try:
                original_result = ns1[function_name](*args)
                result.original_results.append(original_result)
            except Exception as e:
                result.success = False
                result.errors.append(f"Original failed with args {args}: {e}")
                result.original_results.append(None)
                continue

            try:
                roundtrip_result = ns2[function_name](*args)
                result.roundtrip_results.append(roundtrip_result)
            except Exception as e:
                result.success = False
                result.all_match = False
                result.errors.append(f"Round-trip failed with args {args}: {e}")
                result.roundtrip_results.append(None)
                continue

            if original_result != roundtrip_result:
                result.all_match = False
                result.errors.append(
                    f"Mismatch for args {args}: "
                    f"original={original_result}, roundtrip={roundtrip_result}"
                )

    except Exception as e:
        result.success = False
        result.errors.append(f"Round-trip validation failed: {e}")

    return result


def validate_file_roundtrip(
    nl_source: str, test_specs: dict[str, list[tuple]]
) -> dict[str, RoundTripResult]:
    """
    Validate round-trip for multiple functions in a file.

    Args:
        nl_source: Original NL source code
        test_specs: Dict mapping function names to test cases

    Returns:
        Dict mapping function names to RoundTripResult
    """
    results = {}
    for func_name, test_cases in test_specs.items():
        results[func_name] = validate_roundtrip(nl_source, func_name, test_cases)
    return results


def validate_python_source_roundtrip(
    py_source: str,
    function_name: str,
    test_cases: list[tuple],
    module_name: str = "roundtrip_test",
    source_name: str = "<memory>",
) -> PythonSourceRoundTripResult:
    """Validate behavioral roundtrip starting from Python source."""
    result = PythonSourceRoundTripResult(
        success=False,
        all_match=False,
        stage="original",
        source_name=source_name,
    )

    try:
        ns1: dict[str, Any] = {}
        exec(py_source, ns1)
    except Exception as exc:
        result.errors.append(f"Original execution failed: {exc}")
        return result

    if function_name not in ns1:
        result.errors.append(f"Function '{function_name}' not found in original source")
        return result

    try:
        atomized_nl = atomize_to_nl(py_source, module_name=module_name)
        result.atomized_nl = atomized_nl
        result.stage = "parse"
        nl_file = parse_nl_file(atomized_nl)
    except Exception as exc:
        result.errors.append(f"Atomize/parse failed: {exc}")
        return result

    try:
        regenerated_python = emit_python(nl_file)
        result.regenerated_python = regenerated_python
        result.stage = "roundtrip"
        ns2: dict[str, Any] = {}
        exec(regenerated_python, ns2)
    except Exception as exc:
        result.errors.append(f"Emit/roundtrip execution failed: {exc}")
        return result

    if function_name not in ns2:
        result.errors.append(
            f"Function '{function_name}' not found in round-tripped source"
        )
        return result

    result.stage = "behavior"
    result.success = True
    result.all_match = True

    for args in test_cases:
        try:
            original_value = ns1[function_name](*args)
            result.original_results.append(original_value)
        except Exception as exc:
            result.success = False
            result.all_match = False
            result.errors.append(f"Original failed with args {args}: {exc}")
            result.original_results.append(None)
            continue

        try:
            roundtrip_value = ns2[function_name](*args)
            result.roundtrip_results.append(roundtrip_value)
        except Exception as exc:
            result.success = False
            result.all_match = False
            result.errors.append(f"Round-trip failed with args {args}: {exc}")
            result.roundtrip_results.append(None)
            continue

        if original_value != roundtrip_value:
            result.all_match = False
            result.errors.append(
                f"Mismatch for args {args}: original={original_value}, roundtrip={roundtrip_value}"
            )

    result.stage = "ok" if result.all_match else "behavior"
    return result


def validate_python_structure_roundtrip(
    py_source: str,
    module_name: str = "roundtrip_test",
    source_name: str = "<memory>",
) -> PythonSourceRoundTripResult:
    """Validate atomize -> parse -> emit without executing the module."""
    result = PythonSourceRoundTripResult(
        success=False,
        all_match=False,
        stage="atomize",
        source_name=source_name,
    )

    try:
        atomized_nl = atomize_to_nl(py_source, module_name=module_name)
        result.atomized_nl = atomized_nl
        result.stage = "parse"
        nl_file = parse_nl_file(atomized_nl)
        result.regenerated_python = emit_python(nl_file)
    except SyntaxError as exc:
        result.stage = "unsupported_source"
        result.errors.append(f"Unsupported source syntax: {exc}")
        return result
    except Exception as exc:
        result.errors.append(f"Structural round-trip failed: {exc}")
        return result

    result.success = True
    result.all_match = True
    result.stage = "ok"
    return result


def roundtrip_python_file(
    source_path: Path,
    *,
    repo_root: Path | None = None,
    output_root: Path | None = None,
    function_test_cases: dict[str, list[tuple]] | None = None,
) -> PythonSourceRoundTripResult:
    """Run Python -> NLS -> Python validation for one file and write artifacts."""
    source_path = Path(source_path)
    py_source = source_path.read_text(encoding="utf-8")
    module_name = source_path.stem.replace("_", "-")

    if function_test_cases:
        first_function = next(iter(function_test_cases))
        result = validate_python_source_roundtrip(
            py_source,
            first_function,
            function_test_cases[first_function],
            module_name=module_name,
            source_name=str(source_path),
        )
        for function_name, test_cases in list(function_test_cases.items())[1:]:
            extra = validate_python_source_roundtrip(
                py_source,
                function_name,
                test_cases,
                module_name=module_name,
                source_name=str(source_path),
            )
            result.success = result.success and extra.success
            result.all_match = result.all_match and extra.all_match
            result.original_results.extend(extra.original_results)
            result.roundtrip_results.extend(extra.roundtrip_results)
            result.errors.extend(extra.errors)
            if extra.atomized_nl:
                result.atomized_nl = extra.atomized_nl
            if extra.regenerated_python:
                result.regenerated_python = extra.regenerated_python
            if extra.stage != "ok":
                result.stage = extra.stage
    else:
        result = validate_python_structure_roundtrip(
            py_source,
            module_name=module_name,
            source_name=str(source_path),
        )

    if output_root:
        root = Path(repo_root) if repo_root else source_path.parent
        relative = source_path.relative_to(root)
        nl_output_path = Path(output_root) / relative.with_suffix(".nl")
        py_output_path = Path(output_root) / relative.with_suffix(".roundtrip.py")
        nl_output_path.parent.mkdir(parents=True, exist_ok=True)
        nl_output_path.write_text(result.atomized_nl, encoding="utf-8")
        py_output_path.write_text(result.regenerated_python, encoding="utf-8")

    return result


def roundtrip_python_repository(
    repo_root: Path,
    output_root: Path,
    *,
    function_test_cases_by_file: dict[str, dict[str, list[tuple]]] | None = None,
    max_files: int | None = None,
) -> RepositoryRoundTripReport:
    """Run the Python -> NLS -> Python loop across a repository tree."""
    repo_root = Path(repo_root)
    output_root = Path(output_root)
    report = RepositoryRoundTripReport(
        repo_root=str(repo_root),
        output_root=str(output_root),
    )

    excluded_dirs = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
    }
    files = []
    for path in repo_root.rglob("*.py"):
        if any(part in excluded_dirs for part in path.parts):
            continue
        files.append(path)

    files.sort()
    if max_files is not None:
        files = files[:max_files]

    for path in files:
        test_cases = None
        if function_test_cases_by_file:
            key = str(path.relative_to(repo_root)).replace("\\", "/")
            test_cases = function_test_cases_by_file.get(
                key
            ) or function_test_cases_by_file.get(path.name)
        report.file_results.append(
            roundtrip_python_file(
                path,
                repo_root=repo_root,
                output_root=output_root,
                function_test_cases=test_cases,
            )
        )

    return report
