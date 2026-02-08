"""Regression tests for Issue #125: version must have a single source of truth.

Contracts:
- nlsc.__version__ must match pyproject.toml [project].version
- CLI `--version` must report the same version
- LSP server version must not be hard-coded stale
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path


def _project_version_from_pyproject() -> str:
    """Read the canonical project version from pyproject.toml."""
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    try:
        import tomllib  # py311+
    except ModuleNotFoundError as e:  # pragma: no cover
        raise AssertionError("Python 3.11+ is required for tomllib-based parsing") from e

    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    try:
        return data["project"]["version"]
    except KeyError as e:  # pragma: no cover
        raise AssertionError(
            "pyproject.toml must contain [project].version so tests can validate version consistency"
        ) from e


def _lsp_server_version_argument_expression() -> ast.expr | None:
    """Return the AST expression used for LanguageServer(super) version=... in NLSLanguageServer.__init__.

    If the call can't be found, return None so the test can fail with a clear message.
    """
    server_path = Path(__file__).resolve().parents[1] / "nlsc" / "lsp" / "server.py"
    module = ast.parse(server_path.read_text(encoding="utf-8"))

    for node in ast.walk(module):
        # Find: class NLSLanguageServer(LanguageServer):
        if not isinstance(node, ast.ClassDef) or node.name != "NLSLanguageServer":
            continue

        for body_item in node.body:
            if not isinstance(body_item, ast.FunctionDef) or body_item.name != "__init__":
                continue

            for stmt in ast.walk(body_item):
                # Find a call expression for super().__init__(..., version=...)
                if not isinstance(stmt, ast.Call):
                    continue
                if not isinstance(stmt.func, ast.Attribute):
                    continue
                if stmt.func.attr != "__init__":
                    continue
                if not isinstance(stmt.func.value, ast.Call):
                    continue
                if not isinstance(stmt.func.value.func, ast.Name):
                    continue
                if stmt.func.value.func.id != "super":
                    continue

                for kw in stmt.keywords:
                    if kw.arg == "version":
                        return kw.value

    return None


def test_package_version_should_match_pyproject_version():
    """nlsc.__version__ should match pyproject.toml [project].version."""
    expected = _project_version_from_pyproject()

    import nlsc

    actual = nlsc.__version__
    assert (
        actual == expected
    ), f"Version mismatch: nlsc.__version__={actual!r} but pyproject.toml [project].version={expected!r}"


def test_cli_dash_dash_version_should_report_pyproject_version():
    """`python -m nlsc --version` should report the same version as pyproject.toml."""
    expected = _project_version_from_pyproject()

    result = subprocess.run(
        [sys.executable, "-m", "nlsc", "--version"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        "Expected `python -m nlsc --version` to exit 0, "
        f"got {result.returncode}. stderr was: {result.stderr!r}"
    )

    stdout = (result.stdout or "").strip()
    assert expected in stdout, (
        "Expected CLI --version output to include the canonical project version from pyproject.toml. "
        f"Expected version {expected!r} to be in stdout, got stdout={stdout!r}"
    )


def test_lsp_server_version_should_not_be_hardcoded_stale():
    """LSP server version should not be a stale hard-coded string literal."""
    expected = _project_version_from_pyproject()

    version_expr = _lsp_server_version_argument_expression()
    assert version_expr is not None, (
        "Expected to find a super().__init__(..., version=...) call in NLSLanguageServer.__init__ "
        "so the test can validate version consistency."
    )

    # If it's a constant string, it MUST match the canonical project version.
    if isinstance(version_expr, ast.Constant) and isinstance(version_expr.value, str):
        assert version_expr.value == expected, (
            "LSP server version is hard-coded and stale. "
            f"Found version={version_expr.value!r} in nlsc/lsp/server.py but expected {expected!r} from pyproject.toml. "
            "Version must be sourced from a single location."
        )
    else:
        # Non-literal is acceptable (e.g., nlsc.__version__ or importlib.metadata.version()).
        assert True

