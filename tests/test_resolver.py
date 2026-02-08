"""Tests for dependency resolution behavior."""

from nlsc.parser import parse_nl_file
from nlsc.resolver import resolve_dependencies


class TestResolverDependencies:
    """Resolver correctness tests."""

    def test_self_dependency_allowed_for_recursion(self):
        source = """\
@module test
@target python

[factorial]
PURPOSE: Compute factorial
INPUTS:
  - n: integer
DEPENDS: [factorial]
RETURNS: 1
"""
        nl_file = parse_nl_file(source)
        result = resolve_dependencies(nl_file)

        assert result.success is True
        assert [a.identifier for a in result.order] == ["factorial"]

    def test_cycle_between_two_anlus_is_still_error(self):
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
        nl_file = parse_nl_file(source)
        result = resolve_dependencies(nl_file)

        assert result.success is False
        assert any("Circular dependency detected" in e.message for e in result.errors)

    def test_missing_dependency_reports_error(self):
        source = """\
@module test
@target python

[a]
PURPOSE: A
DEPENDS: [missing]
RETURNS: void
"""
        nl_file = parse_nl_file(source)
        result = resolve_dependencies(nl_file)

        assert result.success is False
        assert any(e.missing_dep == "missing" for e in result.errors)
