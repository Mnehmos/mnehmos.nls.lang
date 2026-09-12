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

# Backend semantics/capability version per target.  Bump when emitted
# behavior or the runtime contract changes (new helpers, different error
# identities, changed truthiness/equality semantics, capability flips):
# lockfile identity includes this marker, so stale artifacts are detected
# instead of trusted (#202).
EMITTER_SEMANTICS_VERSION: dict[str, str] = {
    "python": "py-1",
    "typescript": "ts-2",
}


def emitter_semantics_version(target: str) -> str:
    return EMITTER_SEMANTICS_VERSION.get(target, "unknown")


# feature name -> supported by target
TARGET_CAPABILITIES: dict[str, dict[str, bool]] = {
    "python": {
        "literal_blocks": True,
        "main_block": True,
        "property_tests": True,
        "loop_steps": True,
    },
    "typescript": {
        "literal_blocks": False,
        "main_block": False,
        "property_tests": False,
        "loop_steps": False,
    },
}

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
    capabilities = TARGET_CAPABILITIES.get(target, {})
    gaps: list[CapabilityGap] = []
    for feature, supported in capabilities.items():
        if not supported and _file_uses_feature(nl_file, feature):
            # Dropped program content is fatal; dropped test coverage is
            # strict-only.
            fatal = feature in ("literal_blocks", "main_block", "loop_steps")
            gaps.append(CapabilityGap(feature=feature, fatal=fatal))
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
