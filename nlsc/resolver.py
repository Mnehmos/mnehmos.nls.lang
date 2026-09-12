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
    #
    # Reverse edges (dependency -> dependents) are built once so each node
    # is visited a constant number of times; scanning every ANLU per node
    # with dataclass equality made this quadratic in file size (#151).
    from collections import deque

    by_id = {anlu.identifier: anlu for anlu in nl_file.anlus}
    unresolved: dict[str, int] = {}
    dependents: dict[str, list[str]] = {}
    ready: deque[str] = deque()

    for anlu in nl_file.anlus:
        deps = list(dict.fromkeys(dependency_ids(anlu, allow_self=True)))
        unresolved[anlu.identifier] = len(deps)
        for dep_id in deps:
            dependents.setdefault(dep_id, []).append(anlu.identifier)
        if not deps:
            ready.append(anlu.identifier)

    resolved: set[str] = set()
    while ready:
        current_id = ready.popleft()
        if current_id in resolved:
            continue
        resolved.add(current_id)
        result.order.append(by_id[current_id])

        for dependent_id in dependents.get(current_id, ()):
            if dependent_id in resolved:
                continue
            unresolved[dependent_id] -= 1
            if unresolved[dependent_id] == 0:
                ready.append(dependent_id)

    # Check for circular dependencies (unresolved ANLUs remaining)
    unresolved_anlus = [a for a in nl_file.anlus if a.identifier not in resolved]
    for anlu in unresolved_anlus:
        result.errors.append(ResolutionError(
            anlu_id=anlu.identifier,
            message="Circular dependency detected"
        ))

    return result
