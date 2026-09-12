"""Package model: versioned dependency resolution (Issue #146).

Slice 1 scope: a project manifest (``nls.pkg.json``) declaring local
path dependencies with semver constraints, resolution into package roots
that ``@use`` can search, and a project lock (``nls.pkg.lock``) capturing
each dependency's version and content hash.

Everything is offline and deterministic: sources are local directories,
hashes are content hashes over the package's ``.nl`` files, and no
network, registry, or publish path is involved (that is #27).
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from .error_catalog import EPKG001, EPKG002, EPKG003

MANIFEST_NAME = "nls.pkg.json"
LOCK_NAME = "nls.pkg.lock"
MANIFEST_SCHEMA = "nls.pkg/1"

_PACKAGE_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*$")
_SEMVER = re.compile(r"^(?P<major>\d+)(?:\.(?P<minor>\d+))?(?:\.(?P<patch>\d+))?$")


class PackageError(Exception):
    """A manifest, dependency, or lockfile problem with a stable code."""

    def __init__(self, *, code: str, message: str, hint: str) -> None:
        self.code = code
        self.message = message
        self.hint = hint
        super().__init__(message)


@dataclass(frozen=True)
class PackageDependency:
    """One declared dependency: a local package root and a version range."""

    name: str
    path: str
    version: str = "*"


@dataclass(frozen=True)
class PackageManifest:
    name: str
    version: str
    dependencies: dict[str, PackageDependency] = field(default_factory=dict)


@dataclass(frozen=True)
class ResolvedPackage:
    """A dependency resolved to a concrete directory and content hash.

    ``declared_path`` is the manifest's relative path (what the lock
    records — absolute paths would leak machine layout and churn the lock);
    ``root`` is the resolved absolute directory.
    """

    name: str
    version: str | None
    root: Path
    declared_path: str
    content_hash: str


def find_manifest(project_dir: Path) -> Path | None:
    candidate = Path(project_dir) / MANIFEST_NAME
    return candidate if candidate.is_file() else None


def find_project_root(start: Path) -> Path | None:
    """Nearest ancestor directory containing ``nls.pkg.json``."""
    current = Path(start).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / MANIFEST_NAME).is_file():
            return candidate
    return None


def _manifest_error(message: str, hint: str) -> PackageError:
    return PackageError(code=EPKG001, message=message, hint=hint)


def load_manifest(project_dir: Path) -> PackageManifest:
    """Load and validate ``nls.pkg.json`` from a project directory."""
    manifest_path = find_manifest(project_dir)
    if manifest_path is None:
        raise _manifest_error(
            f"No package manifest found: {Path(project_dir) / MANIFEST_NAME}",
            f"Create {MANIFEST_NAME} at the project root, or run `nlsc install` "
            "in a project that has one.",
        )
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise _manifest_error(
            f"Could not read {manifest_path}: {exc}",
            "Fix the JSON syntax and rerun `nlsc install`.",
        ) from exc

    if not isinstance(data, dict):
        raise _manifest_error(
            f"{manifest_path} must contain a JSON object",
            f"Use the {MANIFEST_SCHEMA} shape with name, version, and dependencies.",
        )

    schema = data.get("schema")
    if schema not in (None, MANIFEST_SCHEMA):
        raise _manifest_error(
            f"Unsupported manifest schema {schema!r} in {manifest_path}",
            f"Set \"schema\": \"{MANIFEST_SCHEMA}\".",
        )

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        raise _manifest_error(
            f"{manifest_path} is missing a package \"name\"",
            "Declare the package name, e.g. \"name\": \"acme.project\".",
        )

    version = data.get("version", "0.0.0")
    if not isinstance(version, str) or _SEMVER.match(version) is None:
        raise _manifest_error(
            f"Invalid package version {version!r} in {manifest_path}",
            "Use a MAJOR or MAJOR.MINOR.PATCH version string.",
        )

    raw_dependencies = data.get("dependencies", {})
    if not isinstance(raw_dependencies, dict):
        raise _manifest_error(
            f"\"dependencies\" in {manifest_path} must be an object",
            "Map package names to {\"path\": ..., \"version\": ...} entries.",
        )

    dependencies: dict[str, PackageDependency] = {}
    for dep_name, spec in raw_dependencies.items():
        if not isinstance(dep_name, str) or _PACKAGE_NAME.match(dep_name) is None:
            raise _manifest_error(
                f"Invalid dependency name {dep_name!r} in {manifest_path}",
                "Use a dotted identifier such as \"acme.payments\".",
            )
        if not isinstance(spec, dict) or not isinstance(spec.get("path"), str):
            raise _manifest_error(
                f"Dependency {dep_name!r} needs a \"path\" entry",
                "Local path dependencies are the supported source in this release.",
            )
        dep_path = spec["path"].strip()
        if not dep_path:
            raise _manifest_error(
                f"Dependency {dep_name!r} has an empty \"path\"",
                "Point the dependency at its directory, e.g. \"vendor/payments\".",
            )
        if Path(dep_path).is_absolute():
            raise _manifest_error(
                f"Dependency {dep_name!r} uses an absolute path",
                "Use a path relative to the manifest so the lock stays portable.",
            )
        constraint = spec.get("version", "*")
        if not isinstance(constraint, str):
            raise _manifest_error(
                f"Dependency {dep_name!r} has a non-string version",
                "Use a semver range such as \"^1.2.0\", \"~1.2.0\", \"1.2.0\", or \"*\".",
            )
        if not _is_valid_constraint(constraint):
            raise _manifest_error(
                f"Dependency {dep_name!r} has an unsupported version constraint "
                f"{constraint!r}",
                "Supported forms: \"*\", \"1.2.3\", \"^1.2.0\", \"~1.2.0\".",
            )
        dependencies[dep_name] = PackageDependency(
            name=dep_name, path=dep_path, version=constraint
        )

    return PackageManifest(name=name, version=version, dependencies=dependencies)


def _parse_version(text: str) -> tuple[int, int, int] | None:
    match = _SEMVER.match(text.strip())
    if match is None:
        return None
    return (
        int(match.group("major")),
        int(match.group("minor") or 0),
        int(match.group("patch") or 0),
    )


def _is_valid_constraint(constraint: str) -> bool:
    constraint = constraint.strip()
    if constraint in ("", "*"):
        return True
    if constraint[:1] in ("^", "~"):
        return _parse_version(constraint[1:]) is not None
    return _parse_version(constraint) is not None


def version_satisfies(version: str, constraint: str) -> bool:
    """Match a concrete version against ``*``, exact, caret, or tilde range."""
    parsed = _parse_version(version)
    if parsed is None:
        return False
    constraint = constraint.strip()
    if constraint in ("", "*"):
        return True
    if constraint.startswith("^"):
        base = _parse_version(constraint[1:])
        if base is None:
            return False
        # Caret: compatible with the leftmost non-zero component.
        if parsed < base:
            return False
        if base[0] > 0:
            return parsed[0] == base[0]
        if base[1] > 0:
            return parsed[0] == 0 and parsed[1] == base[1]
        return parsed[0] == 0 and parsed[1] == 0 and parsed[2] == base[2]
    if constraint.startswith("~"):
        base = _parse_version(constraint[1:])
        if base is None:
            return False
        return parsed >= base and parsed[0] == base[0] and parsed[1] == base[1]
    exact = _parse_version(constraint)
    if exact is not None:
        return parsed == exact
    return False


def package_content_hash(root: Path) -> str:
    """Content hash over a package's ``.nl`` files (order-independent)."""
    digest = hashlib.sha256()
    files = sorted(
        path for path in Path(root).rglob("*.nl") if path.is_file()
    )
    for path in files:
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        try:
            digest.update(path.read_bytes())
        except OSError:
            digest.update(b"<unreadable>")
        digest.update(b"\0")
    return "sha256:" + digest.hexdigest()[:12]


def _package_version(root: Path) -> str | None:
    """Read the dependency's own manifest version when it has one."""
    manifest_path = Path(root) / MANIFEST_NAME
    if not manifest_path.is_file():
        return None
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    version = data.get("version")
    return version if isinstance(version, str) else None


def resolve_dependencies(project_dir: Path, manifest: PackageManifest) -> list[ResolvedPackage]:
    """Resolve every dependency to a concrete root, version, and hash."""
    project_dir = Path(project_dir)
    resolved: list[ResolvedPackage] = []
    for dependency in manifest.dependencies.values():
        root = (project_dir / dependency.path).resolve()
        if not root.is_dir():
            raise PackageError(
                code=EPKG002,
                message=(
                    f"Dependency '{dependency.name}' path does not exist: "
                    f"{dependency.path}"
                ),
                hint=(
                    "Fix the \"path\" entry in the manifest, or clone/check out "
                    "the dependency directory."
                ),
            )
        version = _package_version(root)
        if version is not None and not version_satisfies(version, dependency.version):
            raise PackageError(
                code=EPKG003,
                message=(
                    f"Dependency '{dependency.name}' version {version} does not "
                    f"satisfy {dependency.version}"
                ),
                hint=(
                    "Update the dependency's version or relax the manifest's "
                    "constraint."
                ),
            )
        resolved.append(
            ResolvedPackage(
                name=dependency.name,
                version=version,
                root=root,
                declared_path=dependency.path,
                content_hash=package_content_hash(root),
            )
        )
    return resolved


def package_search_roots(project_dir: Path) -> list[tuple[str, Path]]:
    """(package name, root) pairs from the manifest, for ``@use`` search.

    Returns an empty list when the project has no manifest: packages are
    opt-in and never break projects that do not use them.
    """
    project_dir = Path(project_dir)
    if find_manifest(project_dir) is None:
        return []
    try:
        manifest = load_manifest(project_dir)
    except PackageError:
        # Compilation is not the place to report manifest problems: a
        # broken manifest must not crash `nlsc compile` with a traceback.
        # `nlsc install` reports it as EPKG001.
        return []
    roots: list[tuple[str, Path]] = []
    for dependency in manifest.dependencies.values():
        root = (project_dir / dependency.path).resolve()
        if root.is_dir():
            roots.append((dependency.name, root))
    return roots


def matching_package_root(
    domain: str, package_roots: list[tuple[str, Path]]
) -> tuple[str, Path, str] | None:
    """Longest-prefix package match for a dotted ``@use`` domain.

    ``@use acme.payments.charge`` with dependency ``acme.payments`` yields
    ``(package name, root, remainder "charge")``.
    """
    best: tuple[str, Path, str] | None = None
    for name, root in package_roots:
        if domain == name:
            remainder = ""
        elif domain.startswith(name + "."):
            remainder = domain[len(name) + 1 :]
        else:
            continue
        if best is None or len(name) > len(best[0]):
            best = (name, root, remainder)
    return best


def write_package_lock(
    path: Path, manifest: PackageManifest, resolved: list[ResolvedPackage]
) -> None:
    lines = [
        "# DO NOT EDIT - Generated by nlsc",
        "",
        f"schema: {MANIFEST_SCHEMA}",
        f"package: {manifest.name}",
        f"version: {manifest.version}",
        "",
        "dependencies:",
    ]
    for package in sorted(resolved, key=lambda item: item.name):
        lines.append(f"  {package.name}:")
        lines.append(f"    version: {package.version or 'unknown'}")
        lines.append(f"    path: {package.declared_path}")
        lines.append(f"    hash: {package.content_hash}")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def read_package_lock(path: Path) -> dict[str, dict[str, str]]:
    """Parse a package lock into ``{name: {version, path, hash}}``."""
    path = Path(path)
    if not path.is_file():
        return {}
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {}
    entries: dict[str, dict[str, str]] = {}
    current: str | None = None
    in_dependencies = False
    for raw in content.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("dependencies:"):
            in_dependencies = True
            continue
        if not in_dependencies:
            continue
        if raw.startswith("  ") and not raw.startswith("    "):
            current = raw.strip().rstrip(":")
            entries[current] = {}
            continue
        if raw.startswith("    ") and current is not None:
            key, _, value = raw.strip().partition(": ")
            entries[current][key] = value
    return entries


def verify_package_lock(
    path: Path, project_dir: Path, manifest: PackageManifest
) -> list[str]:
    """Report lockfile drift: missing packages, changed hashes, or versions.

    Re-resolves the manifest so on-disk changes are detected; comparing a
    previously resolved list would always match the lock.
    """
    resolved = resolve_dependencies(project_dir, manifest)
    recorded = read_package_lock(path)
    errors: list[str] = []
    for package in resolved:
        entry = recorded.get(package.name)
        if entry is None:
            errors.append(f"Dependency {package.name} not in lockfile")
            continue
        if entry.get("hash") != package.content_hash:
            errors.append(f"Dependency {package.name} content changed since lock")
        if entry.get("path") and entry.get("path") != package.declared_path:
            errors.append(
                f"Dependency {package.name} path changed since lock "
                f"({entry.get('path')} -> {package.declared_path})"
            )
        if (entry.get("version") or "unknown") != (package.version or "unknown"):
            errors.append(
                f"Dependency {package.name} version changed since lock "
                f"({entry.get('version')} -> {package.version or 'unknown'})"
            )
    for name in recorded:
        if name not in {package.name for package in resolved}:
            errors.append(f"Dependency {name} in lockfile but not in manifest")
    return errors
