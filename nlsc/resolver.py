"""
NLS Resolver - Dependency resolution for ANLUs

Validates and orders ANLUs based on their dependency graph.
"""

from dataclasses import dataclass
from typing import Optional

from .schema import NLFile, ANLU


@dataclass
class ResolutionError:
    """Error during dependency resolution"""
    anlu_id: str
    message: str
    missing_dep: Optional[str] = None


class ResolverResult:
    """Result of dependency resolution"""

    def __init__(self) -> None:
        self.order: list[ANLU] = []
        self.errors: list[ResolutionError] = []

    @property
    def success(self) -> bool:
        return len(self.errors) == 0

    def __repr__(self) -> str:
        if self.success:
            return f"ResolverResult(ok, order=[{', '.join(a.identifier for a in self.order)}])"
        else:
            return f"ResolverResult(errors={len(self.errors)})"


def resolve_dependencies(nl_file: NLFile) -> ResolverResult:
    """
    Resolve ANLU dependencies and return compilation order.

    Uses topological sort to order ANLUs so dependencies come first.
    Detects:
    - Missing dependencies
    - Circular dependencies

    Args:
        nl_file: Parsed NLFile with ANLUs

    Returns:
        ResolverResult with ordered ANLUs or errors
    """
    result = ResolverResult()

    # Build lookup map
    anlu_map = {anlu.identifier: anlu for anlu in nl_file.anlus}

    def dependency_ids(anlu: ANLU, *, allow_self: bool) -> list[str]:
        """Return normalized dependency IDs, excluding placeholder dependencies."""
        deps: list[str] = []
        for dep in anlu.depends:
            dep_id = dep.strip("[]")
            if dep_id.lower() == "none":
                continue
            if allow_self and dep_id == anlu.identifier:
                continue
            deps.append(dep_id)
        return deps

    # Check for missing dependencies
    for anlu in nl_file.anlus:
        for dep_id in dependency_ids(anlu, allow_self=False):
            if dep_id not in anlu_map:
                result.errors.append(ResolutionError(
                    anlu_id=anlu.identifier,
                    message=f"Missing dependency: {dep_id}",
                    missing_dep=dep_id
                ))

    if result.errors:
        return result

    # Topological sort using unresolved dependency counts per ANLU.
    # Self-recursive dependencies are treated as valid declarations, not cycles.
    unresolved = {
        anlu.identifier: len(dependency_ids(anlu, allow_self=True))
        for anlu in nl_file.anlus
    }

    # Start with ANLUs that have no dependencies
    ready = [anlu for anlu in nl_file.anlus if not dependency_ids(anlu, allow_self=True)]
    resolved = set()

    while ready:
        # Take next ready ANLU
        current = ready.pop(0)
        result.order.append(current)
        resolved.add(current.identifier)

        # Update dependents
        for anlu in nl_file.anlus:
            if anlu.identifier in resolved:
                continue

            # Check if this ANLU depends on current
            for dep_id in dependency_ids(anlu, allow_self=True):
                if dep_id == current.identifier:
                    unresolved[anlu.identifier] -= 1

            # If all deps resolved, add to ready
            if unresolved[anlu.identifier] == 0 and anlu.identifier not in resolved:
                if anlu not in ready:
                    ready.append(anlu)

    # Check for circular dependencies (unresolved ANLUs remaining)
    unresolved_anlus = [a for a in nl_file.anlus if a.identifier not in resolved]
    for anlu in unresolved_anlus:
        result.errors.append(ResolutionError(
            anlu_id=anlu.identifier,
            message="Circular dependency detected"
        ))

    return result
