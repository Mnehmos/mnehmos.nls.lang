"""Issue #90 — `@use` directives (Slice C) end-to-end contract tests.

Contract source: docs/design/issue-90-use-directives.md

These tests are intentionally written for TDD Red phase: they define expected
behavior for stdlib resolution and override precedence. They should FAIL on the
current implementation until Issue #90 is implemented.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


def _repo_root() -> Path:
    # tests/ is at repo_root/tests/
    return Path(__file__).resolve().parents[1]


def _pythonpath_env(*, extra_paths: Iterable[Path]) -> dict[str, str]:
    """Return env overrides ensuring `python -m nlsc` resolves to this repo."""
    existing = os.environ.get("PYTHONPATH", "")
    parts: list[str] = [str(p) for p in extra_paths]
    if existing:
        parts.append(existing)
    return {"PYTHONPATH": os.pathsep.join(parts)}


def _run_nlsc(
    argv: list[str],
    *,
    cwd: Path,
    env_overrides: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)

    return subprocess.run(
        [sys.executable, "-m", "nlsc", *argv],
        cwd=str(cwd),
        env=env,
        text=True,
        capture_output=True,
    )


@dataclass
class _BundledStdlibSandbox:
    """Creates a minimal bundled stdlib layout under `nlsc/stdlib/` if absent.

    This is a test harness for Slice C end-to-end tests.

    IMPORTANT:
    - We only *create missing* files.
    - We only *delete files we created*.

    This avoids interfering with a future committed bundled stdlib.
    """

    repo_root: Path

    created_paths: list[Path]
    manifest: dict

    @classmethod
    def ensure_minimal_math_core(cls) -> "_BundledStdlibSandbox":
        repo_root = _repo_root()
        stdlib_root = repo_root / "nlsc" / "stdlib"
        created: list[Path] = []

        stdlib_root.mkdir(parents=True, exist_ok=True)

        manifest_path = stdlib_root / "MANIFEST.json"
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        else:
            manifest = {
                "schema": 1,
                "default_major": 1,
                "versions": {"v1": {"semver": "1.0.0"}},
            }
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            created.append(manifest_path)

        default_major = int(manifest.get("default_major", 1))
        core_path = stdlib_root / f"v{default_major}" / "math" / "core.nl"
        if not core_path.exists():
            core_path.parent.mkdir(parents=True, exist_ok=True)
            core_path.write_text(
                """@module math.core\n\n# Minimal bundled stdlib placeholder for tests\n""",
                encoding="utf-8",
            )
            created.append(core_path)

        return cls(repo_root=repo_root, created_paths=created, manifest=manifest)

    @property
    def default_major(self) -> int:
        return int(self.manifest.get("default_major", 1))

    @property
    def bundled_stdlib_root(self) -> Path:
        return self.repo_root / "nlsc" / "stdlib"

    def cleanup(self) -> None:
        # Remove files we created, then prune empty dirs upward.
        for p in sorted(self.created_paths, key=lambda x: len(str(x)), reverse=True):
            try:
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink(missing_ok=True)
            except Exception:
                # Best-effort cleanup; do not mask test failures.
                pass

        # Prune newly-empty directories we might have created.
        for p in self.created_paths:
            for parent in [p.parent, *p.parents]:
                if parent == (self.repo_root / "nlsc"):
                    break
                try:
                    parent.rmdir()
                except OSError:
                    break


def test_should_resolve_bundled_stdlib_and_compile_when_use_directive_is_present(tmp_path: Path):
    """Happy path: `@use math.core` resolves bundled stdlib and compilation succeeds."""

    sandbox = _BundledStdlibSandbox.ensure_minimal_math_core()
    try:
        program = """\
@module main
@target python
@use math.core

[noop]
PURPOSE: No-op
RETURNS: 1
"""
        src = tmp_path / "main.nl"
        src.write_text(program, encoding="utf-8")

        result = _run_nlsc(
            ["--parser", "regex", "compile", str(src)],
            cwd=tmp_path,
            env_overrides=_pythonpath_env(extra_paths=[sandbox.repo_root]),
        )

        expected_rel = f"v{sandbox.default_major}/math/core.nl"
        expected_bundled = sandbox.bundled_stdlib_root / expected_rel

        assert result.returncode == 0, (
            "Expected compilation to succeed (exit 0) when bundled stdlib contains the domain. "
            f"Got exit {result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        )
        assert str(expected_bundled).replace("\\", "/") in (result.stdout + result.stderr).replace("\\", "/"), (
            "Expected output to include the resolved bundled stdlib path for `@use math.core`. "
            f"Expected to mention: {expected_bundled}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        )
    finally:
        sandbox.cleanup()


def test_should_fail_with_EUSE001_when_domain_is_missing(tmp_path: Path):
    """Error path: missing domain must raise deterministic `EUSE001` with diagnostics."""

    sandbox = _BundledStdlibSandbox.ensure_minimal_math_core()
    try:
        # Ensure the specific module is missing even if core.nl exists.
        missing_rel = f"v{sandbox.default_major}/math/missing.nl"
        missing_abs = sandbox.bundled_stdlib_root / missing_rel
        if missing_abs.exists():
            missing_abs.unlink()

        program = """\
@module main
@target python
@use math.missing

[noop]
PURPOSE: No-op
RETURNS: 1
"""
        src = tmp_path / "main.nl"
        src.write_text(program, encoding="utf-8")

        result = _run_nlsc(
            ["--parser", "regex", "compile", str(src)],
            cwd=tmp_path,
            env_overrides=_pythonpath_env(extra_paths=[sandbox.repo_root]),
        )

        assert result.returncode != 0, (
            "Expected compilation to fail (non-zero) when `@use` domain is missing. "
            f"Got exit {result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        )

        combined = (result.stdout + "\n" + result.stderr)
        assert "EUSE001" in combined, (
            "Expected missing `@use` domain error to include deterministic code `EUSE001`. "
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        )
        assert "math.missing" in combined, (
            "Expected missing domain error to include `domain=math.missing` (or equivalent). "
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        )
        assert missing_rel.replace("\\", "/") in combined.replace("\\", "/"), (
            "Expected missing domain error to include `candidate_relpath` of the attempted module. "
            f"Expected relpath: {missing_rel}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        )
        assert "attempted_roots" in combined, (
            "Expected missing domain error to include `attempted_roots` diagnostics. "
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        )
    finally:
        sandbox.cleanup()


def test_should_prefer_project_local_stdlib_override_over_bundled_when_both_exist(tmp_path: Path):
    """Precedence: `.nls/stdlib/` overrides bundled stdlib when both contain the domain."""

    sandbox = _BundledStdlibSandbox.ensure_minimal_math_core()
    try:
        default_major = sandbox.default_major

        # Project-local override root
        project_override = tmp_path / ".nls" / "stdlib" / f"v{default_major}" / "math" / "core.nl"
        project_override.parent.mkdir(parents=True, exist_ok=True)
        project_override.write_text(
            """@module math.core\n\n# Project-local override\n""",
            encoding="utf-8",
        )

        program = """\
@module main
@target python
@use math.core

[noop]
PURPOSE: No-op
RETURNS: 1
"""
        src = tmp_path / "main.nl"
        src.write_text(program, encoding="utf-8")

        result = _run_nlsc(
            ["--parser", "regex", "compile", str(src)],
            cwd=tmp_path,
            env_overrides=_pythonpath_env(extra_paths=[sandbox.repo_root]),
        )

        assert result.returncode == 0, (
            "Expected compilation to succeed when project-local stdlib override exists. "
            f"Got exit {result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        )

        combined = (result.stdout + "\n" + result.stderr).replace("\\", "/")
        expected_override = str(project_override).replace("\\", "/")
        expected_bundled = str(sandbox.bundled_stdlib_root / f"v{default_major}/math/core.nl").replace("\\", "/")

        assert expected_override in combined, (
            "Expected `@use math.core` to resolve to project-local override `.nls/stdlib/.../math/core.nl`. "
            f"Expected to mention: {expected_override}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        )
        assert expected_bundled not in combined, (
            "Expected project-local override to take precedence over bundled stdlib (bundled path should not be selected). "
            f"Bundled path unexpectedly present: {expected_bundled}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        )
    finally:
        sandbox.cleanup()


def test_should_prefer_cli_stdlib_path_over_env_and_bundled_when_all_exist(tmp_path: Path):
    """Precedence: CLI `--stdlib-path` overrides env and bundled roots."""

    sandbox = _BundledStdlibSandbox.ensure_minimal_math_core()
    try:
        default_major = sandbox.default_major

        # Env root
        env_root = tmp_path / "env-stdlib"
        env_mod = env_root / f"v{default_major}" / "math" / "core.nl"
        env_mod.parent.mkdir(parents=True, exist_ok=True)
        env_mod.write_text("@module math.core\n# Env override\n", encoding="utf-8")

        # CLI root
        cli_root = tmp_path / "cli-stdlib"
        cli_mod = cli_root / f"v{default_major}" / "math" / "core.nl"
        cli_mod.parent.mkdir(parents=True, exist_ok=True)
        cli_mod.write_text("@module math.core\n# CLI override\n", encoding="utf-8")

        program = """\
@module main
@target python
@use math.core

[noop]
PURPOSE: No-op
RETURNS: 1
"""
        src = tmp_path / "main.nl"
        src.write_text(program, encoding="utf-8")

        env = _pythonpath_env(extra_paths=[sandbox.repo_root])
        env["NLS_STDLIB_PATH"] = str(env_root)

        result = _run_nlsc(
            [
                "--parser",
                "regex",
                "compile",
                str(src),
                "--stdlib-path",
                str(cli_root),
            ],
            cwd=tmp_path,
            env_overrides=env,
        )

        assert result.returncode == 0, (
            "Expected compilation to succeed and select CLI stdlib root when provided via `--stdlib-path`. "
            f"Got exit {result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        )

        combined = (result.stdout + "\n" + result.stderr).replace("\\", "/")
        assert str(cli_mod).replace("\\", "/") in combined, (
            "Expected `@use math.core` to resolve to CLI-provided stdlib root (highest precedence in this test). "
            f"Expected to mention: {cli_mod}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        )
        assert str(env_mod).replace("\\", "/") not in combined, (
            "Expected CLI `--stdlib-path` to override env root (env path should not be selected). "
            f"Env path unexpectedly present: {env_mod}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        )
    finally:
        sandbox.cleanup()


def test_should_prefer_env_stdlib_path_over_bundled_when_both_exist_and_no_cli(tmp_path: Path):
    """Precedence: env `NLS_STDLIB_PATH` overrides bundled stdlib when CLI is not provided."""

    sandbox = _BundledStdlibSandbox.ensure_minimal_math_core()
    try:
        default_major = sandbox.default_major

        env_root = tmp_path / "env-stdlib"
        env_mod = env_root / f"v{default_major}" / "math" / "core.nl"
        env_mod.parent.mkdir(parents=True, exist_ok=True)
        env_mod.write_text("@module math.core\n# Env override\n", encoding="utf-8")

        program = """\
@module main
@target python
@use math.core

[noop]
PURPOSE: No-op
RETURNS: 1
"""
        src = tmp_path / "main.nl"
        src.write_text(program, encoding="utf-8")

        env = _pythonpath_env(extra_paths=[sandbox.repo_root])
        env["NLS_STDLIB_PATH"] = str(env_root)

        result = _run_nlsc(
            ["--parser", "regex", "compile", str(src)],
            cwd=tmp_path,
            env_overrides=env,
        )

        assert result.returncode == 0, (
            "Expected compilation to succeed and select env stdlib root when provided via `NLS_STDLIB_PATH`. "
            f"Got exit {result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        )

        combined = (result.stdout + "\n" + result.stderr).replace("\\", "/")
        assert str(env_mod).replace("\\", "/") in combined, (
            "Expected `@use math.core` to resolve to env-provided stdlib root when `NLS_STDLIB_PATH` is set. "
            f"Expected to mention: {env_mod}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        )

        bundled_mod = sandbox.bundled_stdlib_root / f"v{default_major}/math/core.nl"
        assert str(bundled_mod).replace("\\", "/") not in combined, (
            "Expected env stdlib root to take precedence over bundled stdlib (bundled path should not be selected). "
            f"Bundled path unexpectedly present: {bundled_mod}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        )
    finally:
        sandbox.cleanup()
