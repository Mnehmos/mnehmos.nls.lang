"""
Shared fixtures for semantic tests.

The runner fixture is parameterized over every supported target (#202):
Python and TypeScript (Node execution).  TypeScript skips when no Node
runtime is available unless NLSC_REQUIRE_TS=1, which turns a missing
toolchain into a failure so CI gates on it.
"""
import os

import pytest

from .runners import PythonRunner, TypeScriptRunner, node_available


def _typescript_runner() -> TypeScriptRunner:
    if not node_available():
        if os.environ.get("NLSC_REQUIRE_TS") == "1":
            pytest.fail("NLSC_REQUIRE_TS=1 but Node.js is not available")
        pytest.skip("Node.js runtime not available for the TypeScript runner")
    return TypeScriptRunner()


@pytest.fixture(params=["python", "typescript"])
def runner(request):
    """Provide a target runner for semantic tests."""
    if request.param == "typescript":
        return _typescript_runner()
    return PythonRunner()


@pytest.fixture
def python_runner() -> PythonRunner:
    """Python-only runner for behavior the TS backend does not emit yet
    (constructor constraint/invariant checks are Python-only until the
    #202 backend migration adds executable TS checks)."""
    return PythonRunner()
