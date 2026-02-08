"""Regression tests for Issue #123: allow self-recursive dependencies while rejecting true cycles."""

from nlsc.emitter import emit_python
from nlsc.parser import parse_nl_file
from nlsc.resolver import resolve_dependencies


def test_should_resolve_and_emit_when_anlu_depends_on_itself_for_recursion():
    """A self-recursive ANLU should be valid and emit code without circular-dependency failure."""
    source = """\
@module issue123
@target python

[factorial]
PURPOSE: Compute factorial recursively
INPUTS:
  • n: number
DEPENDS: [factorial]
RETURNS: 1 if n <= 1 else n * factorial(n - 1)
"""

    parsed = parse_nl_file(source)
    result = resolve_dependencies(parsed)

    assert result.success, (
        "Self-recursive dependency [factorial] -> [factorial] must be accepted; "
        "resolver currently rejects it as a circular dependency."
    )
    assert not any(err.anlu_id == "factorial" for err in result.errors), (
        "Self-recursive factorial must not be reported as dependency-resolution error."
    )

    python_code = emit_python(parsed, mode="mock")
    assert "def factorial(" in python_code, (
        "Emitter should still generate factorial function when self-recursion is declared in DEPENDS."
    )


def test_should_reject_true_cycle_when_two_nodes_depend_on_each_other():
    """A true multi-node cycle (A -> B -> A) must remain rejected."""
    source = """\
@module issue123
@target python

[a]
PURPOSE: A
DEPENDS: [b]
RETURNS: 1

[b]
PURPOSE: B
DEPENDS: [a]
RETURNS: 2
"""

    parsed = parse_nl_file(source)
    result = resolve_dependencies(parsed)

    assert not result.success, "True multi-node cycle must still fail dependency resolution."
    error_ids = {err.anlu_id for err in result.errors}
    assert error_ids == {"a", "b"}, (
        "Resolver must report both nodes participating in A->B->A cycle."
    )
    assert all("Circular dependency" in err.message for err in result.errors), (
        "Cycle errors should explicitly communicate circular dependency detection."
    )


def test_should_distinguish_self_recursion_from_true_cycle_when_both_exist():
    """Mixed graph should only fail on the true cycle; self-recursive node should remain valid."""
    source = """\
@module issue123
@target python

[factorial]
PURPOSE: Compute factorial recursively
INPUTS:
  • n: number
DEPENDS: [factorial]
RETURNS: 1 if n <= 1 else n * factorial(n - 1)

[a]
PURPOSE: A
DEPENDS: [b]
RETURNS: 1

[b]
PURPOSE: B
DEPENDS: [a]
RETURNS: 2
"""

    parsed = parse_nl_file(source)
    result = resolve_dependencies(parsed)

    assert not result.success, "Mixed graph with A->B->A should still fail because of true cycle."

    error_ids = {err.anlu_id for err in result.errors}
    assert error_ids == {"a", "b"}, (
        "Resolver must distinguish self-recursion from true cycles: only A and B should fail, "
        "while factorial self-recursion should be accepted."
    )
    assert "factorial" not in error_ids, (
        "Self-recursive factorial should not be labeled circular when true cycle exists elsewhere."
    )

