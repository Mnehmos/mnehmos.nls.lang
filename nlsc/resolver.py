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

    # Check for missing dependencies
    for anlu in nl_file.anlus:
        for dep in anlu.depends:
            # Strip brackets if present [dep-name] -> dep-name
            dep_id = dep.strip("[]")
            # Skip "none" as it's a placeholder meaning no dependencies
            if dep_id.lower() == "none":
                continue
            if dep_id not in anlu_map:
                result.errors.append(ResolutionError(
                    anlu_id=anlu.identifier,
                    message=f"Missing dependency: {dep_id}",
                    missing_dep=dep_id
                ))

    if result.errors:
        return result

    # Topological sort using Kahn's algorithm
    # Count incoming edges (dependencies pointing to each node)
    {anlu.identifier: 0 for anlu in nl_file.anlus}

    for anlu in nl_file.anlus:
        for dep in anlu.depends:
            dep_id = dep.strip("[]")
            # The current ANLU depends on dep_id, so current has in_degree from dep
            # But we want to track: who depends on me?
            pass

    # Helper to filter out "none" placeholder from dependencies
    def real_deps(anlu: ANLU) -> list[str]:
        return [d for d in anlu.depends if d.strip("[]").lower() != "none"]

    # Actually, let's track: for each ANLU, how many unresolved deps does it have?
    unresolved = {anlu.identifier: len(real_deps(anlu)) for anlu in nl_file.anlus}

    # Start with ANLUs that have no dependencies
    ready = [anlu for anlu in nl_file.anlus if not real_deps(anlu)]
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
            for dep in anlu.depends:
                dep_id = dep.strip("[]")
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
