"""Tests for dependency graph visualization - Issue #4"""

import pytest
from nlsc.parser import parse_nl_file
from nlsc.graph import (
    emit_mermaid,
    emit_dot,
    emit_ascii,
    emit_dataflow_mermaid,
    emit_dataflow_ascii,
)


class TestMermaidOutput:
    """Tests for Mermaid diagram generation"""

    def test_emit_mermaid_simple(self):
        """Generate Mermaid for ANLU dependencies"""
        source = """\
@module test
@target python

[validate-input]
PURPOSE: Validate user input
INPUTS:
  - data: string
RETURNS: boolean

[calculate-tax]
PURPOSE: Calculate tax
DEPENDS: [validate-input]
INPUTS:
  - amount: number
RETURNS: number

[finalize-order]
PURPOSE: Finalize order
DEPENDS: [calculate-tax]
INPUTS:
  - order: Order
RETURNS: Order
"""
        result = parse_nl_file(source)
        mermaid = emit_mermaid(result)

        assert "graph LR" in mermaid or "graph TD" in mermaid
        assert "validate-input" in mermaid
        assert "calculate-tax" in mermaid
        assert "finalize-order" in mermaid
        # Check edges exist
        assert "-->" in mermaid

    def test_emit_mermaid_no_deps(self):
        """Independent ANLUs should be listed without edges"""
        source = """\
@module test
@target python

[add]
PURPOSE: Add numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

[multiply]
PURPOSE: Multiply numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a * b
"""
        result = parse_nl_file(source)
        mermaid = emit_mermaid(result)

        assert "add" in mermaid
        assert "multiply" in mermaid
        # No dependencies, so no edges between them
        lines = [l.strip() for l in mermaid.split("\n") if "-->" in l]
        assert len(lines) == 0


class TestDotOutput:
    """Tests for Graphviz DOT format"""

    def test_emit_dot_basic(self):
        """Generate DOT for ANLU dependencies"""
        source = """\
@module test
@target python

[step-a]
PURPOSE: Step A
RETURNS: void

[step-b]
PURPOSE: Step B
DEPENDS: [step-a]
RETURNS: void
"""
        result = parse_nl_file(source)
        dot = emit_dot(result)

        assert "digraph" in dot
        assert "step_a" in dot or "step-a" in dot  # DOT may use underscores
        assert "step_b" in dot or "step-b" in dot
        assert "->" in dot

    def test_emit_dot_with_labels(self):
        """DOT nodes should have labels"""
        source = """\
@module test
@target python

[process-data]
PURPOSE: Process incoming data
RETURNS: ProcessedData
"""
        result = parse_nl_file(source)
        dot = emit_dot(result)

        assert "label" in dot


class TestAsciiOutput:
    """Tests for ASCII terminal-friendly output"""

    def test_emit_ascii_simple(self):
        """Generate ASCII representation"""
        source = """\
@module test
@target python

[start]
PURPOSE: Start process
RETURNS: void

[middle]
PURPOSE: Middle step
DEPENDS: [start]
RETURNS: void

[end]
PURPOSE: End process
DEPENDS: [middle]
RETURNS: void
"""
        result = parse_nl_file(source)
        ascii_out = emit_ascii(result)

        # Should show some visual structure
        assert "start" in ascii_out
        assert "middle" in ascii_out
        assert "end" in ascii_out


class TestDataflowVisualization:
    """Tests for intra-function dataflow graphs"""

    def test_emit_dataflow_mermaid(self):
        """Generate Mermaid for LOGIC step dataflow"""
        source = """\
@module test
@target python

[pipeline]
PURPOSE: Data pipeline
INPUTS:
  - x: number
LOGIC:
  1. a = x + 1
  2. b = x * 2
  3. c = a + b
RETURNS: c
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        mermaid = emit_dataflow_mermaid(anlu)

        assert "graph" in mermaid
        # Should show step nodes
        assert "step1" in mermaid or "Step 1" in mermaid or "1" in mermaid
        # Should show dataflow edges
        assert "-->" in mermaid

    def test_emit_dataflow_ascii(self):
        """Generate ASCII for LOGIC step dataflow"""
        source = """\
@module test
@target python

[flow]
PURPOSE: Data flow
INPUTS:
  - x: number
LOGIC:
  1. a = x + 1
  2. b = a * 2
RETURNS: b
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        ascii_out = emit_dataflow_ascii(anlu)

        # Should show steps and flow
        assert "a" in ascii_out or "Step" in ascii_out


class TestFSMVisualization:
    """Tests for FSM state machine diagrams"""

    def test_emit_fsm_mermaid(self):
        """Generate Mermaid stateDiagram for FSM steps"""
        source = """\
@module test
@target python

[workflow]
PURPOSE: State machine workflow
INPUTS:
  - request: Request
LOGIC:
  1. [init] Initialize process → data
  2. [validate] Validate data → result
  3. [complete] Finalize result
RETURNS: Response
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]

        # FSM should be rendered as stateDiagram
        from nlsc.graph import emit_fsm_mermaid
        mermaid = emit_fsm_mermaid(anlu)

        assert "stateDiagram" in mermaid or "graph" in mermaid
        assert "init" in mermaid
        assert "validate" in mermaid
        assert "complete" in mermaid


class TestEdgeCases:
    """Tests for edge cases and error handling"""

    def test_empty_file(self):
        """Handle file with no ANLUs"""
        source = """\
@module test
@target python
"""
        result = parse_nl_file(source)
        mermaid = emit_mermaid(result)

        # Should produce valid but empty graph
        assert "graph" in mermaid

    def test_circular_deps_handled(self):
        """Circular dependencies should not crash"""
        source = """\
@module test
@target python

[a]
PURPOSE: A
DEPENDS: [b]
RETURNS: void

[b]
PURPOSE: B
DEPENDS: [a]
RETURNS: void
"""
        result = parse_nl_file(source)
        # Should not raise
        mermaid = emit_mermaid(result)
        assert "a" in mermaid
        assert "b" in mermaid
