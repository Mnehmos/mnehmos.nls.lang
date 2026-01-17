"""
NLS Round-trip Validation - Prove behavioral equivalence

Validates that atomize(compile(x)) ≈ x for behavioral equivalence.
"""

from dataclasses import dataclass, field
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


def validate_roundtrip(
    nl_source: str,
    function_name: str,
    test_cases: list[tuple],
    module_name: str = "roundtrip_test"
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
        ns1 = {}
        exec(py_code, ns1)

        if function_name not in ns1:
            result.success = False
            result.errors.append(f"Function '{function_name}' not found in original code")
            return result

        # Atomize: Python -> NL
        regenerated_nl = atomize_to_nl(py_code, module_name=module_name)

        # Second compile: NL -> Python
        nl_file2 = parse_nl_file(regenerated_nl)
        py_code2 = emit_python(nl_file2)

        # Execute regenerated
        ns2 = {}
        exec(py_code2, ns2)

        if function_name not in ns2:
            result.success = False
            result.errors.append(f"Function '{function_name}' not found in round-tripped code")
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


def validate_file_roundtrip(nl_source: str, test_specs: dict[str, list[tuple]]) -> dict[str, RoundTripResult]:
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
