#!/usr/bin/env python3
"""Isolated NLS workspace bootstrap and health checks (Issue #224).

Executes the workspace contract declared in ``.mnehmos/tool.json``:
create a virtualenv, install ``nlsc`` (from PyPI or from a built wheel),
write a sample specification, and run validation/tests/compilation
against it.  Every action prints a JSON report so a distribution
dashboard can consume results without parsing prose.

Usage:
    python scripts/nls_workspace.py bootstrap [--root DIR] [--install-from PATH]
    python scripts/nls_workspace.py health --json
    python scripts/nls_workspace.py verify|test|compile-sample --json

Actions are deterministic: the same root, interpreter, and install
source produce the same workspace layout and the same sample spec.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import sysconfig
from importlib import metadata
from pathlib import Path

DEFAULT_ROOT = Path(".nls-workspace")
SAMPLE_SOURCE = """@module demo
@version 1.0.0
@target python

@type Range {
  low: number
  high: number
}

@invariant Range {
  low <= high
}

[clamp]
PURPOSE: Clamp a value into a closed range
INPUTS:
  - value: number
  - bounds: Range
GUARDS:
  - bounds.low <= bounds.high -> ValueError("range bounds are inverted")
LOGIC:
  1. floored = max(value, bounds.low)
  2. IF floored > bounds.high THEN bounds.high -> result ELSE floored -> result
RETURNS: result

@test [clamp] {
  clamp(5, Range(low = 0, high = 10)) == 5
  clamp(-3, Range(low = 0, high = 10)) == 0
}
"""


def venv_python(venv_dir: Path) -> Path:
    """Interpreter inside a virtualenv, per platform layout."""
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def _report(action: str, ok: bool, **extra: object) -> int:
    payload = {
        "action": action,
        "ok": ok,
        "platform": platform.system(),
        "python": sys.version.split()[0],
    }
    payload.update(extra)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if ok else 1


def _run(argv: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(argv, capture_output=True, text=True, **kwargs)


def bootstrap(root: Path, install_from: str | None, no_venv: bool = False) -> int:
    """Create the venv, install nlsc, and write the sample spec."""
    venv_dir = root / "venv"
    sample_dir = root / "sample" / "src"
    sample_dir.mkdir(parents=True, exist_ok=True)
    sample_path = sample_dir / "demo.nl"
    sample_path.write_text(SAMPLE_SOURCE, encoding="utf-8")

    if no_venv:
        version = _run([sys.executable, "-m", "nlsc", "--version"])
        return _report(
            "bootstrap",
            version.returncode == 0,
            root=str(root),
            venv=None,
            install_from="current-interpreter",
            nlsc_version=version.stdout.strip(),
            sample=str(sample_path),
        )

    if not venv_python(venv_dir).exists():
        created = _run([sys.executable, "-m", "venv", str(venv_dir)])
        if created.returncode != 0:
            return _report(
                "bootstrap", False, stage="venv", stderr=created.stderr.strip()
            )
    python = str(venv_python(venv_dir))

    upgrade = _run([python, "-m", "pip", "install", "--upgrade", "pip", "--quiet"])
    if upgrade.returncode != 0:
        return _report(
            "bootstrap", False, stage="pip", stderr=upgrade.stderr.strip()
        )

    install_target = install_from or "nlsc"
    # pytest is the workspace's test runner: the `test` action executes
    # generated @test specifications through it.
    installed = _run(
        [python, "-m", "pip", "install", "--quiet", install_target, "pytest"]
    )
    if installed.returncode != 0:
        return _report(
            "bootstrap",
            False,
            stage="install",
            install_from=install_target,
            stderr=installed.stderr.strip()[-500:],
        )

    version = _run([python, "-m", "nlsc", "--version"])
    return _report(
        "bootstrap",
        version.returncode == 0,
        root=str(root),
        venv=python,
        install_from=install_target,
        nlsc_version=version.stdout.strip(),
        sample=str(sample_path),
    )


def _workspace_interpreter(root: Path) -> str:
    """The venv interpreter when present, else the running interpreter."""
    candidate = venv_python(root / "venv")
    return str(candidate) if candidate.exists() else sys.executable


def health(root: Path) -> int:
    """Report workspace and toolchain health."""
    interpreter = _workspace_interpreter(root)
    version = _run([interpreter, "-m", "nlsc", "--version"])
    package_version = None
    try:
        package_version = metadata.version("nlsc")
    except metadata.PackageNotFoundError:
        pass
    sample = root / "sample" / "src" / "demo.nl"
    return _report(
        "health",
        version.returncode == 0,
        interpreter=interpreter,
        venv_exists=(root / "venv").exists(),
        package_version=package_version,
        nlsc_version=version.stdout.strip() or version.stderr.strip(),
        sample_exists=sample.exists(),
        python_requirement=">=3.11",
        current_python_ok=sys.version_info >= (3, 11),
        purelib=sysconfig.get_paths()["purelib"],
    )


def _parse_last_json(text: str) -> dict:
    """Last complete JSON object in mixed output.

    `nlsc ci --test --json` streams the pytest subprocess's own JSON before
    the ci payload, so the first parsable document is not always the one
    that matters.
    """
    for index in range(len(text) - 1, -1, -1):
        if text[index] != "{":
            continue
        try:
            candidate = json.loads(text[index:])
        except ValueError:
            continue
        if isinstance(candidate, dict):
            return candidate
    return {}


def _run_nlsc(root: Path, args: list[str]) -> int:
    interpreter = _workspace_interpreter(root)
    result = _run([interpreter, "-m", "nlsc", *args, "--json"])
    payload = _parse_last_json(result.stdout)
    if not payload:
        payload = {
            "stdout": result.stdout.strip()[-500:],
            "stderr": result.stderr.strip()[-500:],
        }
    return _report(
        args[0],
        result.returncode == 0,
        nlsc=payload,
        exit_code=result.returncode,
    )


def verify(root: Path) -> int:
    return _run_nlsc(root, ["verify", "--strict", str(root / "sample" / "src" / "demo.nl")])


def run_tests(root: Path) -> int:
    """Compile (to create the lockfile) then run the CI gate with tests."""
    sample = root / "sample" / "src" / "demo.nl"
    output = root / "sample" / "build"
    output.mkdir(parents=True, exist_ok=True)
    interpreter = _workspace_interpreter(root)
    compile_result = subprocess.run(
        [interpreter, "-m", "nlsc", "compile", str(sample), "-o", str(output / "demo.py")],
        capture_output=True,
        text=True,
    )
    if compile_result.returncode != 0:
        return _report(
            "test",
            False,
            stage="compile",
            stderr=compile_result.stderr.strip()[-300:],
        )
    return _run_nlsc(root, ["ci", "--test", str(sample)])


def compile_sample(root: Path) -> int:
    sample = root / "sample" / "src" / "demo.nl"
    output = root / "sample" / "build"
    output.mkdir(parents=True, exist_ok=True)
    interpreter = _workspace_interpreter(root)
    code = subprocess.run(
        [interpreter, "-m", "nlsc", "compile", str(sample), "-o", str(output / "demo.py")],
        capture_output=True,
        text=True,
    )
    produced = (output / "demo.py").exists()
    return _report(
        "compile-sample",
        code.returncode == 0 and produced,
        output=str(output / "demo.py"),
        produced=produced,
        stderr=code.stderr.strip()[-300:],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["bootstrap", "health", "verify", "test", "compile-sample"])
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help="Workspace root directory")
    parser.add_argument(
        "--install-from",
        default=None,
        help="Install target for bootstrap: PyPI spec (default 'nlsc') or a wheel/sdist path",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Accepted for contract compatibility; every action already prints JSON.",
    )
    parser.add_argument(
        "--no-venv",
        action="store_true",
        help="Write the sample only; use the running interpreter (for dashboards "
        "that manage their own environment).",
    )
    args = parser.parse_args()
    root = Path(args.root)

    if args.action == "bootstrap":
        return bootstrap(root, args.install_from, no_venv=args.no_venv)
    if args.action == "health":
        return health(root)
    if args.action == "verify":
        return verify(root)
    if args.action == "test":
        return run_tests(root)
    return compile_sample(root)


if __name__ == "__main__":
    raise SystemExit(main())
