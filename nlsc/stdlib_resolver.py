"""Issue #90: resolve `@use <domain>` directives against a versioned stdlib.

Slice C contract highlights (see docs/design/issue-90-use-directives.md):

* Supports `@use math.core` and `@use v1.math.core`
* Resolves to a single `.nl` source file inside a stdlib root
* Root precedence (highest first):
  1) Project-local `.nls/stdlib`
  2) CLI `--stdlib-path` (repeatable; earlier flags higher precedence)
  3) Env `NLS_STDLIB_PATH` (path-list; left-to-right precedence)
  4) Bundled `nlsc/stdlib`

This module intentionally keeps the error surface stable for tests:
* `EUSE001` Missing domain (also used for invalid domain tokens in Slice C)
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path


ENV_STDLIB_PATH = "NLS_STDLIB_PATH"
PROJECT_STDLIB_REL = Path(".nls") / "stdlib"

_DOMAIN_TOKEN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*$")
_USE_SPEC = re.compile(r"^v(?P<major>\d+)\.(?P<domain>.+)$")


@dataclass(frozen=True)
class ResolvedUse:
    domain: str
    major: int
    candidate_relpath: str
    path: Path


class StdlibUseError(RuntimeError):
    def __init__(
        self,
        *,
        code: str,
        domain: str,
        major: int,
        candidate_relpath: str,
        attempted_roots: list[Path],
        message: str,
    ) -> None:
        self.code = code
        self.domain = domain
        self.major = major
        self.candidate_relpath = candidate_relpath
        self.attempted_roots = attempted_roots
        super().__init__(message)


def bundled_stdlib_root() -> Path:
    return Path(__file__).resolve().parent / "stdlib"


def bundled_default_major(*, root: Path) -> int:
    manifest_path = root / "MANIFEST.json"
    if not manifest_path.exists():
        return 1
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        return int(data.get("default_major", 1))
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return 1


def parse_use_spec(spec: str, *, default_major: int) -> tuple[int, str]:
    raw = (spec or "").strip()
    m = _USE_SPEC.match(raw)
    if m:
        return int(m.group("major")), m.group("domain")
    return int(default_major), raw


def domain_to_relpath(*, major: int, domain: str) -> str:
    return f"v{major}/" + domain.replace(".", "/") + ".nl"


def _missing_domain_error(
    *,
    domain_spec: str,
    domain: str,
    major: int,
    roots: list[Path],
) -> StdlibUseError:
    candidate_rel = domain_to_relpath(major=major, domain=domain)
    # NOTE: tests assert for stable code + candidate_relpath + attempted_roots.
    return StdlibUseError(
        code="EUSE001",
        domain=domain or domain_spec,
        major=major,
        candidate_relpath=candidate_rel,
        attempted_roots=roots,
        message=f"Missing stdlib domain: {domain_spec}",
    )


def stdlib_search_roots(
    *,
    cwd: Path,
    cli_roots: list[Path] | None = None,
    env_var: str = ENV_STDLIB_PATH,
    include_project: bool = True,
    bundled_root: Path | None = None,
) -> list[Path]:
    roots: list[Path] = []

    # 1) Project-local override root (highest precedence)
    if include_project:
        roots.append(Path(cwd) / PROJECT_STDLIB_REL)

    # 2) CLI roots (repeatable; left-to-right precedence)
    for r in (cli_roots or []):
        roots.append(Path(r))

    # 3) Env roots (path list; left-to-right precedence)
    env_val = os.environ.get(env_var, "")
    if env_val:
        for part in env_val.split(os.pathsep):
            part = part.strip()
            if part:
                roots.append(Path(part))

    # 4) Bundled (lowest precedence)
    roots.append(bundled_root or bundled_stdlib_root())

    # Ignore missing roots (Slice C)
    return [r for r in roots if r.exists() and r.is_dir()]


def resolve_use(
    *,
    domain_spec: str,
    roots: list[Path],
    default_major: int,
) -> ResolvedUse:
    major, domain = parse_use_spec(domain_spec, default_major=default_major)

    if not domain or not _DOMAIN_TOKEN.match(domain):
        # Treat invalid domains as missing for Slice C.
        raise _missing_domain_error(domain_spec=domain_spec, domain=domain or "", major=major, roots=roots)

    candidate_rel = domain_to_relpath(major=major, domain=domain)
    attempted: list[Path] = []
    for root in roots:
        attempted.append(root)
        candidate = root / candidate_rel
        if candidate.exists() and candidate.is_file():
            return ResolvedUse(domain=domain, major=major, candidate_relpath=candidate_rel, path=candidate)

    raise _missing_domain_error(domain_spec=domain_spec, domain=domain, major=major, roots=attempted)

