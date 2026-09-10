"""Issue #199: checked parallel eligibility over effect/alias/failure contracts.

``parallel_groups`` claimed concurrency from data dependencies alone.
These fixtures pin the conservative eligibility analysis and the
truthful graph output.
"""

from __future__ import annotations

from nlsc.graph import emit_dataflow_ascii
from nlsc.parallel import analyze_parallel_eligibility
from nlsc.parser import parse_nl_file

SHARED_LIST_WRITES = """@module shared_effect
[probe]
PURPOSE: Two writes to one list
INPUTS:
  - items: list of number
LOGIC:
  1. items.append(1) -> first
  2. items.append(2) -> second
RETURNS: items
"""

ALIASED_INPUT_WRITES = """@module aliased
[probe]
PURPOSE: appends to two possibly-aliased inputs
INPUTS:
  - left: list of number
  - right: list of number
LOGIC:
  1. left.append(1) -> a
  2. right.append(2) -> b
RETURNS: a
"""

PURE_JOIN = """@module pure_join
[calc]
PURPOSE: two producers one join
INPUTS:
  - a: number
  - b: number
LOGIC:
  1. x = a + b
  2. y = a - b
  3. z = x * y
RETURNS: z
"""

FOREIGN_CALL_PAIR = """@module foreign_pair
[probe]
PURPOSE: two foreign calls
INPUTS:
  - a: string
  - b: string
LOGIC:
  1. log_event(a) -> first
  2. log_event(b) -> second
RETURNS: first
"""

FAILING_THEN_WRITER = """@module fail_order
[probe]
PURPOSE: a failing step before an effectful step
INPUTS:
  - a: number
  - b: number
  - c: string
LOGIC:
  1. q = a / b
  2. log_event(c)
RETURNS: q
"""

GUARDED_EFFECTS = """@module guarded_effects
[charge]
PURPOSE: charge with guards
INPUTS:
  - amount: number
GUARDS:
  - amount > 0 -> ValueError("positive amounts only")
LOGIC:
  1. x = amount * 2
  2. y = amount / 2
RETURNS: x
"""


def _report(source: str, index: int = 0):
    nl_file = parse_nl_file(source)
    return analyze_parallel_eligibility(nl_file.anlus[index])


def _pair_reasons(report, layer_index: int):
    layer = report.layers[layer_index]
    assert layer.pairs
    return layer.pairs[0].reasons


# --------------------------------------------------------------------------
# Never certified: shared resources, aliases, unknown effects
# --------------------------------------------------------------------------


def test_two_writes_to_one_list_are_never_certified():
    report = _report(SHARED_LIST_WRITES)
    layer = report.layers[0]
    assert layer.steps == (1, 2)
    assert not layer.eligible
    reasons = " ; ".join(_pair_reasons(report, 0))
    assert "write/write overlap on items" in reasons


def test_writes_through_distinct_inputs_could_alias_and_are_blocked():
    report = _report(ALIASED_INPUT_WRITES)
    assert not report.layers[0].eligible
    reasons = " ; ".join(_pair_reasons(report, 0))
    assert "possible aliasing" in reasons


def test_unknown_foreign_calls_cannot_be_certified():
    report = _report(FOREIGN_CALL_PAIR)
    assert not report.layers[0].eligible
    reasons = " ; ".join(_pair_reasons(report, 0))
    assert "unresolved" in reasons


# --------------------------------------------------------------------------
# Eligible: pure, total, provably disjoint
# --------------------------------------------------------------------------


def test_pure_two_producers_one_join_is_eligible():
    report = _report(PURE_JOIN)
    assert [list(layer.steps) for layer in report.layers] == [[1, 2], [3]]
    assert report.layers[0].eligible
    assert _pair_reasons(report, 0)[0] == "disjoint fresh bindings"
    assert report.layers[1].eligible


# --------------------------------------------------------------------------
# Failure ordering
# --------------------------------------------------------------------------


def test_failing_step_before_effectful_step_is_not_reordered():
    report = _report(FAILING_THEN_WRITER)
    assert not report.layers[0].eligible
    reasons = " ; ".join(_pair_reasons(report, 0))
    assert "may fail before step 2's effects" in reasons


def test_guards_are_recorded_as_premises():
    report = _report(GUARDED_EFFECTS)
    assert any("guards execute first" in premise for premise in report.premises)


# --------------------------------------------------------------------------
# Report integrity and determinism
# --------------------------------------------------------------------------


def test_every_step_appears_exactly_once():
    report = _report(SHARED_LIST_WRITES)
    assert report.all_steps == (1, 2)
    report_join = _report(PURE_JOIN)
    assert report_join.all_steps == (1, 2, 3)


def test_analysis_is_deterministic():
    first = _report(PURE_JOIN)
    second = _report(PURE_JOIN)
    assert first == second


def test_dependency_layers_matches_legacy_alias():
    nl_file = parse_nl_file(PURE_JOIN)
    anlu = nl_file.anlus[0]
    assert anlu.parallel_groups() == anlu.dependency_layers()


# --------------------------------------------------------------------------
# Truthful graph output
# --------------------------------------------------------------------------


def test_graph_ascii_labels_blocked_layers_sequential():
    nl_file = parse_nl_file(SHARED_LIST_WRITES)
    diagram = emit_dataflow_ascii(nl_file.anlus[0])
    assert "(parallel)" not in diagram
    assert "Layer 1 (sequential required" in diagram
    assert "write/write overlap on items" in diagram


def test_graph_ascii_labels_certified_layers_eligible():
    nl_file = parse_nl_file(PURE_JOIN)
    diagram = emit_dataflow_ascii(nl_file.anlus[0])
    assert "Layer 1 (parallel-eligible)" in diagram
    assert "Layer 2" in diagram
