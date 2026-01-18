"""
Shared fixtures for semantic tests.
"""
import pytest

from .runners import PythonRunner


@pytest.fixture
def runner() -> PythonRunner:
    """Provide a PythonRunner instance for semantic tests."""
    return PythonRunner()
