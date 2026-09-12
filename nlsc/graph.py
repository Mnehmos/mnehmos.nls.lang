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

    # Data-dependency layers with checked parallel eligibility (#199):
    # a layer is only labeled parallel-eligible when effect, alias, and
    # failure constraints certify its steps independent.
    from .parallel import analyze_parallel_eligibility

    report = analyze_parallel_eligibility(anlu)

    for i, layer in enumerate(report.layers):
        if len(layer.steps) > 1 and layer.eligible:
            heading = f"Layer {i + 1} (parallel-eligible)"
        elif len(layer.steps) > 1:
            heading = f"Layer {i + 1} (sequential required)"
        else:
            heading = f"Layer {i + 1}"
        lines.append(f"\n{heading}:")
        for note in layer.notes:
            lines.append(f"  blocked: {note}")
        for step_num in layer.steps:
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




# ---------------------------------------------------------------------------
# Control-flow view (Issue #192)
#
# The data-dependency view answers "which values feed which"; this view
# answers "what actually executes, in what order, under which
# conditions".  It walks the lowered IR regions, so effect-only steps
# (discarded calls) appear as nodes, branch edges carry their
# conditions, and loop regions render back edges without pretending the
# value graph is cyclic.
# ---------------------------------------------------------------------------


def _expr_summary(expr: object) -> str:
    """Compact one-line summary of an IR expression."""
    from .ir import (
        IRBinary,
        IRCall,
        IRFieldAccess,
        IRIndexAccess,
        IRList,
        IRLiteral,
        IRMethodCall,
        IRRef,
        IRUnary,
    )

    if expr is None:
        return "..."
    if isinstance(expr, IRLiteral):
        return expr.raw
    if isinstance(expr, IRRef):
        return expr.name
    if isinstance(expr, IRFieldAccess):
        return f"{_expr_summary(expr.base)}.{expr.field_name}"
    if isinstance(expr, IRIndexAccess):
        return f"{_expr_summary(expr.base)}[{_expr_summary(expr.index)}]"
    if isinstance(expr, IRList):
        return "[" + ", ".join(_expr_summary(item) for item in expr.items) + "]"
    if isinstance(expr, IRUnary):
        operator = "not " if expr.op == "not" else "-"
        return f"{operator}{_expr_summary(expr.operand)}"
    if isinstance(expr, IRBinary):
        return f"{_expr_summary(expr.left)} {expr.op} {_expr_summary(expr.right)}"
    if isinstance(expr, IRCall):
        target = f"[{expr.target}]" if expr.anlu else expr.target
        return f"{target}(...)"
    if isinstance(expr, IRMethodCall):
        return f"{_expr_summary(expr.base)}.{expr.method}(...)"
    return type(expr).__name__


def _stmt_summary(stmt: object) -> str:
    """One-line label for a statement, prefixed with its LOGIC step."""
    from .ir import IRBind, IRBranch, IRDiscard, IRGuard, IRLoop, IRNote, ForeignStmt

    span = getattr(stmt, "span", None)
    step = span.step if span else None
    prefix = f"{step}: " if step else ""
    if isinstance(stmt, IRBind):
        return f"{prefix}{stmt.name} = {_expr_summary(stmt.value)}"
    if isinstance(stmt, IRDiscard):
        return f"{prefix}{_expr_summary(stmt.value)}"
    if isinstance(stmt, IRBranch):
        return f"{prefix}IF {_expr_summary(stmt.condition)}"
    if isinstance(stmt, IRGuard):
        return f"{prefix}GUARD {_expr_summary(stmt.condition)}"
    if isinstance(stmt, IRLoop):
        return f"{prefix}WHILE {_expr_summary(stmt.condition)}"
    if isinstance(stmt, IRNote):
        return f"{prefix}note: {stmt.text[:48]}"
    if isinstance(stmt, ForeignStmt):
        return f"{prefix}foreign {stmt.reason}: {stmt.raw[:40]}"
    return f"{prefix}{type(stmt).__name__}"


class _ControlFlowBuilder:
    """Builds nodes and labeled edges from IR statement regions."""

    def __init__(self) -> None:
        self.nodes: list[tuple[str, str]] = []
        self.edges: list[tuple[str, str, str | None]] = []

    def add_node(self, label: str) -> str:
        node_id = f"n{len(self.nodes) + 1}"
        self.nodes.append((node_id, label))
        return node_id

    def add_edge(self, source: str, target: str, label: str | None = None) -> None:
        self.edges.append((source, target, label))

    def build_region(
        self, statements: tuple, entry: str | None, entry_label: str | None = None
    ) -> list[str]:
        """Wire a statement region; returns its exit node ids."""
        from .ir import IRBranch, IRLoop

        previous: list[str] = [entry] if entry else []
        pending_label: str | None = entry_label
        for stmt in statements:
            if isinstance(stmt, IRBranch):
                condition = self.add_node(_stmt_summary(stmt))
                self._connect(previous, condition, pending_label)
                then_exits = self._build_arm(stmt.then_body, condition, "true")
                else_exits = self._build_arm(stmt.otherwise, condition, "false")
                previous = then_exits + else_exits
                pending_label = None
                continue
            if isinstance(stmt, IRLoop):
                loop = self.add_node(_stmt_summary(stmt))
                self._connect(previous, loop, pending_label)
                body_exits = self._build_arm(stmt.body, loop, None)
                for exit_node in body_exits:
                    self.add_edge(exit_node, loop, "repeat")
                previous = [loop]
                pending_label = "exit"
                continue
            node = self.add_node(_stmt_summary(stmt))
            self._connect(previous, node, pending_label)
            previous = [node]
            pending_label = None
        return previous

    def _connect(
        self, parents: list[str], node: str, label: str | None
    ) -> None:
        for index, parent in enumerate(parents):
            # The label belongs to the first incoming edge only.
            self.add_edge(parent, node, label if index == 0 else None)

    def _build_arm(self, body: tuple, condition: str, label: str | None) -> list[str]:
        if not body:
            empty = self.add_node("(empty)")
            self.add_edge(condition, empty, label)
            return [empty]
        first = self.add_node(_stmt_summary(body[0]))
        self.add_edge(condition, first, label)
        if len(body) == 1:
            return [first]
        rest_exits = self.build_region(body[1:], first)
        return rest_exits or [first]


def _build_control_flow(anlu: ANLU) -> _ControlFlowBuilder:
    from .lowering import lower_anlu

    operation, _diagnostics = lower_anlu(anlu, set())
    builder = _ControlFlowBuilder()
    builder.build_region(operation.body, None)
    return builder


def _mermaid_label(text: str) -> str:
    return text.replace('"', "'")


def emit_controlflow_mermaid(anlu: ANLU) -> str:
    """Mermaid flowchart of the operation's execution paths."""
    builder = _build_control_flow(anlu)
    lines = ["graph TD"]
    if not builder.nodes:
        lines.append("    empty[No executable statements]")
        return "\n".join(lines)
    for node_id, label in builder.nodes:
        lines.append(f'    {node_id}["{_mermaid_label(label)}"]')
    for source, target, edge_label in builder.edges:
        if edge_label:
            lines.append(f"    {source} -->|{edge_label}| {target}")
        else:
            lines.append(f"    {source} --> {target}")
    return "\n".join(lines)


def emit_controlflow_ascii(anlu: ANLU) -> str:
    """ASCII listing of nodes with their labeled outgoing edges."""
    builder = _build_control_flow(anlu)
    lines = [f"Control flow: {anlu.identifier}", "-" * 40]
    if not builder.nodes:
        lines.append("(no executable statements)")
        return "\n".join(lines)
    outgoing: dict[str, list[tuple[str, str | None]]] = {}
    for source, target, label in builder.edges:
        outgoing.setdefault(source, []).append((target, label))
    labels = dict(builder.nodes)
    for node_id, label in builder.nodes:
        lines.append(f"  {node_id}: {label}")
        for target, edge_label in outgoing.get(node_id, []):
            arrow = f"--{edge_label}-->" if edge_label else "-->"
            lines.append(f"      {arrow} {target}: {labels[target]}")
    return "\n".join(lines)
