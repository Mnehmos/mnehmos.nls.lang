"""Target capability matrix (Issue #202).

Emitting to a target that cannot represent some content must produce an
explicit diagnostic — never silently incomplete output.  Two severities:

- **fatal**: the emitted program would be wrong or broken (a ``@literal
  python`` block dropped from TypeScript leaves calls to undefined
  functions; a dropped ``@main`` block loses the entry point);
- **strict-only**: the program is correct but an artifact silently loses
  coverage (``@property`` specifications are not emitted for TypeScript
  test files yet).

The matrix is deliberately small and explicit: adding support to a backend
means flipping an entry here, not quietly changing output.
"""

from __future__ import annotations

from dataclasses import dataclass

from .diagnostics import Diagnostic
from .error_catalog import ETARGET002
from .schema import NLFile

# Per-target data (capabilities, fatal classification, semantics markers)
# is owned by the target registry (#147): plugins register targets without
# editing this module. These are compatibility views over the registry;
# bump a marker when emitted behavior or the runtime contract changes
# (new helpers, different error identities, capability flips) — lockfile
# identity includes the marker, so stale artifacts are detected instead
# of trusted (#202). Marker history: py-2 coded guards carry `.code`;
# py-3 IR-rendered checked bodies with canonical record kwargs;
# ts-2 loop-step capability gap plus branch-joined `let` hoisting.
from .targets import TARGET_REGISTRY, ensure_plugins_loaded

# Discover installed plugins before snapshotting, so these views are
# deterministic rather than depending on which API was called first.
# They remain snapshots: runtime registrations are seen by the gates
# (which read the registry live), not by these dicts.
ensure_plugins_loaded()

TARGET_CAPABILITIES: dict[str, dict[str, bool]] = {
    name: dict(entry.capabilities) for name, entry in TARGET_REGISTRY.items()
}

EMITTER_SEMANTICS_VERSION: dict[str, str] = {
    name: entry.semantics_version for name, entry in TARGET_REGISTRY.items()
}


def emitter_semantics_version(target: str) -> str:
    from .targets import get_target

    entry = get_target(target)
    return entry.semantics_version if entry else "unknown"

_FEATURE_DESCRIPTIONS = {
    "literal_blocks": "@literal blocks",
    "main_block": "@main block",
    "property_tests": "@property specifications",
    "loop_steps": "FOR each LOGIC loop steps",
}


@dataclass(frozen=True)
class CapabilityGap:
    """One unsupported feature on a target."""

    feature: str
    fatal: bool

    @property
    def description(self) -> str:
        return _FEATURE_DESCRIPTIONS.get(self.feature, self.feature)


def _file_uses_feature(nl_file: NLFile, feature: str) -> bool:
    if feature == "literal_blocks":
        return bool(nl_file.literals)
    if feature == "main_block":
        return bool(nl_file.main_block)
    if feature == "property_tests":
        return bool(nl_file.properties)
    if feature == "loop_steps":
        return nl_file.uses_for_each_loops()
    return False


def capability_gaps(nl_file: NLFile, target: str) -> list[CapabilityGap]:
    """Unsupported features used by this file on the selected target."""
    from .targets import get_target

    entry = get_target(target)
    if entry is None:
        return []
    gaps: list[CapabilityGap] = []
    for feature, supported in entry.capabilities.items():
        if not supported and _file_uses_feature(nl_file, feature):
            # Fatal classification comes from the registry entry: dropped
            # program content breaks the artifact; dropped test coverage
            # is strict-only.
            gaps.append(
                CapabilityGap(
                    feature=feature,
                    fatal=feature in entry.fatal_capabilities,
                )
            )
    return gaps


def capability_diagnostics(
    nl_file: NLFile, target: str, *, file_token: str = "<source>"
) -> tuple[list[Diagnostic], list[Diagnostic]]:
    """Return (fatal, strict_only) capability diagnostics for a target."""
    fatal: list[Diagnostic] = []
    warnings: list[Diagnostic] = []
    for gap in capability_gaps(nl_file, target):
        diagnostic = Diagnostic(
            code=ETARGET002,
            file=file_token,
            line=None,
            col=None,
            message=(
                f"target '{target}' does not support {gap.description}; "
                "emitting it would produce an incomplete or invalid artifact"
            ),
            hint=(
                f"Compile with the target that supports {gap.description}, or "
                "move the content into supported constructs."
            ),
        )
        (fatal if gap.fatal else warnings).append(diagnostic)
    return fatal, warnings
