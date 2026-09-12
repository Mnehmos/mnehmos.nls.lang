"""
Shared fixtures for semantic tests.

The runner fixture is parameterized over every supported target (#202):
Python and TypeScript (Node execution).  TypeScript skips when no Node
runtime is available unless NLSC_REQUIRE_TS=1, which turns a missing
toolchain into a failure so CI gates on it.  That rule lives in
``runners.require_typescript_runner`` so fixtures and tests that build a
runner directly cannot drift apart.
"""
import pytest

from .runners import PythonRunner, require_typescript_runner


@pytest.fixture(params=["python", "typescript"])
def runner(request):
    """Provide a target runner for semantic tests."""
    if request.param == "typescript":
        return require_typescript_runner()
    return PythonRunner()
