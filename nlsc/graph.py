"""
Graph visualization for NLS dependencies and dataflow

Outputs:
- Mermaid: GitHub-embeddable diagrams
- DOT: Graphviz format
- ASCII: Terminal-friendly
"""

from .schema import NLFile, ANLU


def emit_mermaid(nl_file: NLFile, direction: str = "LR") -> str:
    """
    Generate Mermaid diagram for inter-ANLU dependencies.

    Args:
        nl_file: Parsed NL file
        direction: Graph direction (LR, TD, BT, RL)

    Returns:
        Mermaid diagram string
    """
    lines = [f"graph {direction}"]

    # Build dependency map
    edges = []
    for anlu in nl_file.anlus:
        # Add node
        node_id = _mermaid_id(anlu.identifier)
        lines.append(f"    {node_id}[{anlu.identifier}]")

        # Add edges from dependencies
        for dep in anlu.depends:
            dep_id = dep.strip("[]")
            edges.append((dep_id, anlu.identifier))

    # Add edges
    for from_id, to_id in edges:
        from_node = _mermaid_id(from_id)
        to_node = _mermaid_id(to_id)
        lines.append(f"    {from_node} --> {to_node}")

    return "\n".join(lines)


def emit_dot(nl_file: NLFile) -> str:
    """
    Generate Graphviz DOT format for inter-ANLU dependencies.

    Args:
        nl_file: Parsed NL file

    Returns:
        DOT format string
    """
    lines = ["digraph NLSDependencies {"]
    lines.append("    rankdir=LR;")
    lines.append("    node [shape=box, style=rounded];")

    # Add nodes with labels
    for anlu in nl_file.anlus:
        node_id = _dot_id(anlu.identifier)
        label = anlu.identifier
        purpose_short = anlu.purpose[:30] + "..." if len(anlu.purpose) > 30 else anlu.purpose
        lines.append(f'    {node_id} [label="{label}\\n{purpose_short}"];')

    # Add edges
    for anlu in nl_file.anlus:
        to_node = _dot_id(anlu.identifier)
        for dep in anlu.depends:
            dep_id = dep.strip("[]")
            from_node = _dot_id(dep_id)
            lines.append(f"    {from_node} -> {to_node};")

    lines.append("}")
    return "\n".join(lines)


def emit_ascii(nl_file: NLFile) -> str:
    """
    Generate ASCII diagram for terminal display.

    Args:
        nl_file: Parsed NL file

    Returns:
        ASCII art string
    """
    lines = []
    lines.append("=" * 50)
    lines.append("ANLU Dependency Graph")
    lines.append("=" * 50)

    if not nl_file.anlus:
        lines.append("(no ANLUs)")
        return "\n".join(lines)

    # Group by dependency level
    levels = _compute_levels(nl_file)

    for level, anlus in sorted(levels.items()):
        lines.append(f"\nLevel {level}:")
        for anlu_id in anlus:
            anlu = nl_file.get_anlu(anlu_id)
            if anlu:
                deps = ", ".join(d.strip("[]") for d in anlu.depends) or "(none)"
                lines.append(f"  [{anlu_id}]")
                lines.append(f"    Purpose: {anlu.purpose[:40]}...")
                lines.append(f"    Depends: {deps}")

    lines.append("\n" + "=" * 50)
    return "\n".join(lines)


def emit_dataflow_mermaid(anlu: ANLU) -> str:
    """
    Generate Mermaid diagram for intra-ANLU dataflow.

    Args:
        anlu: ANLU with logic_steps

    Returns:
        Mermaid diagram string
    """
    lines = ["graph TD"]

    if not anlu.logic_steps:
        lines.append("    empty[No LOGIC steps]")
        return "\n".join(lines)

    # Add step nodes
    for step in anlu.logic_steps:
        node_id = f"step{step.number}"
        assigns_str = ", ".join(step.assigns) if step.assigns else "..."
        step.description[:25] if len(step.description) > 25 else step.description
        label = f"Step {step.number}: {assigns_str}"
        lines.append(f'    {node_id}["{label}"]')

    # Add edges based on dependencies
    for step in anlu.logic_steps:
        to_node = f"step{step.number}"
        for dep_num in step.depends_on:
            from_node = f"step{dep_num}"
            lines.append(f"    {from_node} --> {to_node}")

    return "\n".join(lines)


def emit_dataflow_ascii(anlu: ANLU) -> str:
    """
    Generate ASCII diagram for intra-ANLU dataflow.

    Args:
        anlu: ANLU with logic_steps

    Returns:
        ASCII art string
    """
    lines = []
    lines.append(f"Dataflow: {anlu.identifier}")
    lines.append("-" * 40)

    if not anlu.logic_steps:
        lines.append("(no LOGIC steps)")
        return "\n".join(lines)

    # Get parallel groups
    groups = anlu.parallel_groups()

    for i, group in enumerate(groups):
        lines.append(f"\nPhase {i + 1} (parallel):")
        for step_num in group:
            step = next((s for s in anlu.logic_steps if s.number == step_num), None)
            if step:
                assigns = ", ".join(step.assigns) if step.assigns else "-"
                uses = ", ".join(step.uses) if step.uses else "-"
                lines.append(f"  Step {step.number}: {step.description[:30]}")
                lines.append(f"    Assigns: {assigns}")
                lines.append(f"    Uses: {uses}")

    return "\n".join(lines)


def emit_fsm_mermaid(anlu: ANLU) -> str:
    """
    Generate Mermaid stateDiagram for FSM-style LOGIC steps.

    Args:
        anlu: ANLU with state-named logic_steps

    Returns:
        Mermaid stateDiagram string
    """
    states = anlu.fsm_states()

    if not states:
        # Fall back to regular graph if no states
        return emit_dataflow_mermaid(anlu)

    lines = ["stateDiagram-v2"]

    # Add state definitions
    for state in states:
        lines.append(f"    {state}")

    # Add transitions
    transitions = anlu.fsm_transitions()
    for from_state, to_state in transitions:
        lines.append(f"    {from_state} --> {to_state}")

    # If no transitions but has states, show linear flow
    if not transitions and len(states) > 1:
        for i in range(len(states) - 1):
            lines.append(f"    {states[i]} --> {states[i + 1]}")

    return "\n".join(lines)


# Helper functions

def _mermaid_id(identifier: str) -> str:
    """Convert identifier to valid Mermaid node ID"""
    return identifier.replace("-", "_").replace(".", "_")


def _dot_id(identifier: str) -> str:
    """Convert identifier to valid DOT node ID"""
    return identifier.replace("-", "_").replace(".", "_")


def _compute_levels(nl_file: NLFile) -> dict[int, list[str]]:
    """
    Compute dependency levels for topological layout.
    Level 0 = no dependencies, Level N = max dependency depth
    """
    levels: dict[int, list[str]] = {}
    computed: dict[str, int] = {}

    def get_level(anlu_id: str, visited: set) -> int:
        if anlu_id in computed:
            return computed[anlu_id]

        if anlu_id in visited:
            # Circular dependency - break cycle
            return 0

        visited.add(anlu_id)
        anlu = nl_file.get_anlu(anlu_id)

        if not anlu or not anlu.depends:
            computed[anlu_id] = 0
            return 0

        max_dep_level = 0
        for dep in anlu.depends:
            dep_id = dep.strip("[]")
            dep_level = get_level(dep_id, visited.copy())
            max_dep_level = max(max_dep_level, dep_level + 1)

        computed[anlu_id] = max_dep_level
        return max_dep_level

    for anlu in nl_file.anlus:
        level = get_level(anlu.identifier, set())
        if level not in levels:
            levels[level] = []
        levels[level].append(anlu.identifier)

    return levels
