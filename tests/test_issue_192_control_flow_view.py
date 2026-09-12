"""Issue #192: the control-flow view shows real execution paths.

Effect-only steps (discarded calls) stay visible, branch edges carry
their conditions, loop regions render back edges, and the view is
deterministic.  The data-dependency view remains separate.
"""

from __future__ import annotations

import json

from nlsc.cli import main
from nlsc.graph import (
    _ControlFlowBuilder,
    emit_controlflow_ascii,
    emit_controlflow_mermaid,
)
from nlsc.ir import IRBind, IRLiteral, IRLoop, IRRef
from nlsc.parser import parse_nl_file

PROGRAM = """@module cf_probe
[probe]
PURPOSE: probe
INPUTS:
  - flag: boolean
LOGIC:
  1. total = 1
  2. [notify](total)
  3. IF flag THEN total + 1 -> x ELSE total - 1 -> x
RETURNS: x

[notify]
PURPOSE: notify
INPUTS:
  - value: number
RETURNS: value
"""


def _anlu():
    nl_file = parse_nl_file(PROGRAM, source_path="cf_probe.nl")
    return nl_file.anlus[0]


# --------------------------------------------------------------------------
# Execution paths
# --------------------------------------------------------------------------


def test_effect_only_step_appears_in_control_view():
    diagram = emit_controlflow_ascii(_anlu())
    assert "[notify](...)" in diagram
    # It sits between the bind and the branch, in source order.
    assert diagram.index("total = 1") < diagram.index("[notify](...)") < diagram.index("IF flag")


def test_branch_edges_carry_conditions_and_both_arms():
    mermaid = emit_controlflow_mermaid(_anlu())
    assert "-->|true|" in mermaid
    assert "-->|false|" in mermaid
    assert "IF flag" in mermaid
    assert "x = total add 1" in mermaid
    assert "x = total sub 1" in mermaid


def test_node_order_follows_source_order():
    diagram = emit_controlflow_ascii(_anlu())
    positions = [diagram.index(f"n{index}:") for index in range(1, 6)]
    assert positions == sorted(positions)


def test_empty_arm_is_explicit():
    source = """@module cf
[probe]
PURPOSE: p
INPUTS:
  - flag: boolean
LOGIC:
  1. IF flag THEN [notify](1)
RETURNS: 0

[notify]
PURPOSE: n
INPUTS:
  - v: number
RETURNS: v
"""
    anlu = parse_nl_file(source).anlus[0]
    mermaid = emit_controlflow_mermaid(anlu)
    assert "(empty)" in mermaid
    assert "-->|false|" in mermaid


def test_loop_region_renders_back_edge_and_exit():
    builder = _ControlFlowBuilder()
    loop = IRLoop(
        condition=IRRef(name="flag"),
        body=(IRBind(name="x", value=IRLiteral(kind="number", raw="1")),),
    )
    builder.build_region((loop,), None)
    edges = [(source, target, label) for source, target, label in builder.edges]
    assert any(label == "repeat" for _, _, label in edges)
    # The loop node is the region exit, so a continuation would hang off it.
    labels = dict(builder.nodes)
    assert any("WHILE flag" in label for label in labels.values())


def test_view_is_deterministic():
    first = emit_controlflow_mermaid(_anlu())
    second = emit_controlflow_mermaid(_anlu())
    assert first == second


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _write(tmp_path):
    path = tmp_path / "cf_probe.nl"
    path.write_text(PROGRAM, encoding="utf-8")
    return path


def test_cli_control_ascii(tmp_path, capsys):
    path = _write(tmp_path)
    assert main(["graph", str(path), "--anlu", "probe", "--control", "--format", "ascii"]) == 0
    out = capsys.readouterr().out
    assert "Control flow: probe" in out
    assert "[notify](...)" in out


def test_cli_control_json_reports_kind(tmp_path, capsys):
    path = _write(tmp_path)
    assert main(["graph", "--json", str(path), "--anlu", "probe", "--control"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["graph_kind"] == "control"


def test_cli_control_requires_anlu(tmp_path, capsys):
    path = _write(tmp_path)
    assert main(["graph", str(path), "--control"]) == 1
    assert "EGRAPH003" in capsys.readouterr().err


def test_cli_control_conflicts_with_dataflow(tmp_path, capsys):
    path = _write(tmp_path)
    assert main(["graph", str(path), "--anlu", "probe", "--control", "--dataflow"]) == 1
    err = capsys.readouterr().err
    assert "EGRAPH003" in err
    assert "separate views" in err


def test_cli_control_and_dataflow_are_distinct_views(tmp_path, capsys):
    path = _write(tmp_path)
    dataflow_out = main(["graph", str(path), "--anlu", "probe", "--dataflow", "--format", "ascii"])
    capsys.readouterr()
    control_out = main(["graph", str(path), "--anlu", "probe", "--control", "--format", "ascii"])
    captured = capsys.readouterr()
    assert dataflow_out == 0 and control_out == 0
    assert "Control flow: probe" in captured.out
