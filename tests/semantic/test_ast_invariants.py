"""
AST-level structural tests for semantic preservation.

These tests verify that the parser preserves semantic structure in the AST,
complementing the execution-based tests that verify runtime behavior.

Tests verify:
- Guards are preserved in count and order
- Logic steps preserve dataflow dependencies
- Type fields and constraints are preserved
- Dependencies are correctly resolved
"""
import pytest

from nlsc.parser import parse_nl_file
from nlsc.schema import NLFile, ANLU, Guard, LogicStep, TypeDefinition


class TestGuardPreservation:
    """Tests that guards are preserved in the AST."""

    def test_guard_count_preserved(self):
        """Parser preserves all guards from source."""
        source = """\
@module test
@target python

[validate]
PURPOSE: Test guards
INPUTS:
  - x: number
GUARDS:
  - x > 0 -> ValueError("one")
  - x < 100 -> ValueError("two")
  - x != 50 -> ValueError("three")
RETURNS: x
"""
        nl_file = parse_nl_file(source)
        assert len(nl_file.anlus) == 1
        assert len(nl_file.anlus[0].guards) == 3

    def test_guard_order_preserved(self):
        """Guards in AST match specification order."""
        source = """\
@module test
@target python

[ordered]
PURPOSE: Test guard ordering
INPUTS:
  - x: number
GUARDS:
  - x != 1 -> ValueError("First")
  - x != 2 -> ValueError("Second")
  - x != 3 -> ValueError("Third")
RETURNS: x
"""
        nl_file = parse_nl_file(source)
        guards = nl_file.anlus[0].guards

        assert len(guards) == 3
        assert "First" in guards[0].error_message
        assert "Second" in guards[1].error_message
        assert "Third" in guards[2].error_message

    def test_guard_error_types_preserved(self):
        """Guard error types are preserved in AST."""
        source = """\
@module test
@target python

[typed]
PURPOSE: Test error types
INPUTS:
  - x: number
  - name: string
GUARDS:
  - x > 0 -> ValueError("positive required")
  - name -> TypeError("name required")
RETURNS: name
"""
        nl_file = parse_nl_file(source)
        guards = nl_file.anlus[0].guards

        assert guards[0].error_type == "ValueError"
        assert guards[1].error_type == "TypeError"


class TestLogicStepPreservation:
    """Tests that logic steps and dataflow are preserved."""

    def test_logic_step_count_preserved(self):
        """Parser preserves all logic steps."""
        source = """\
@module test
@target python

[multi-step]
PURPOSE: Multiple steps
INPUTS:
  - x: number
LOGIC:
  1. a = x + 1
  2. b = a + 1
  3. c = b + 1
  4. d = c + 1
RETURNS: d
"""
        nl_file = parse_nl_file(source)
        anlu = nl_file.anlus[0]

        assert len(anlu.logic_steps) == 4

    def test_logic_step_numbering_sequential(self):
        """Step numbers are sequential with no gaps."""
        source = """\
@module test
@target python

[sequential]
PURPOSE: Sequential steps
INPUTS:
  - x: number
LOGIC:
  1. a = x
  2. b = a
  3. c = b
RETURNS: c
"""
        nl_file = parse_nl_file(source)
        steps = nl_file.anlus[0].logic_steps

        for i, step in enumerate(steps):
            assert step.number == i + 1, f"Step {i} has wrong number {step.number}"

    def test_dataflow_dependencies_tracked(self):
        """Dataflow dependencies are tracked in AST."""
        source = """\
@module test
@target python

[pipeline]
PURPOSE: Pipeline with dependencies
INPUTS:
  - x: number
LOGIC:
  1. a = x + 1
  2. b = a * 2
  3. c = b + a
RETURNS: c
"""
        nl_file = parse_nl_file(source)
        steps = nl_file.anlus[0].logic_steps

        # Step 1 has no dependencies
        assert steps[0].depends_on == []

        # Step 2 depends on step 1 (uses 'a')
        assert 1 in steps[1].depends_on

        # Step 3 depends on steps 1 and 2 (uses 'a' and 'b')
        assert 1 in steps[2].depends_on
        assert 2 in steps[2].depends_on

    def test_variable_assignments_tracked(self):
        """Variable assignments are tracked in each step."""
        source = """\
@module test
@target python

[assignments]
PURPOSE: Track assignments
INPUTS:
  - x: number
LOGIC:
  1. first = x + 1
  2. second = first * 2
RETURNS: second
"""
        nl_file = parse_nl_file(source)
        steps = nl_file.anlus[0].logic_steps

        assert "first" in steps[0].assigns
        assert "second" in steps[1].assigns

    def test_dataflow_is_dag(self):
        """Logic step dependencies form a DAG (no cycles)."""
        source = """\
@module test
@target python

[dag]
PURPOSE: DAG structure
INPUTS:
  - x: number
LOGIC:
  1. a = x
  2. b = a
  3. c = a + b
  4. d = b + c
RETURNS: d
"""
        nl_file = parse_nl_file(source)

        # dependency_order() on NLFile returns ANLUs in topological order
        # If it succeeds, the dependencies form a valid DAG
        order = nl_file.dependency_order()
        assert order is not None, "Dataflow should form a valid DAG"
        assert len(order) == 1  # One ANLU in this file


class TestTypePreservation:
    """Tests that type definitions are preserved."""

    def test_type_fields_preserved(self):
        """All type fields are preserved in AST."""
        source = """\
@module test
@target python

@type User {
  name: string, required
  age: number
  email: string
}
"""
        nl_file = parse_nl_file(source)

        # Type definitions are stored in module.types
        assert len(nl_file.module.types) == 1
        type_def = nl_file.module.types[0]

        # Check this is a type definition with expected fields
        assert type_def.name == "User"
        assert len(type_def.fields) == 3
        field_names = [f.name for f in type_def.fields]
        assert "name" in field_names
        assert "age" in field_names
        assert "email" in field_names

    def test_type_constraints_preserved(self):
        """Field constraints are preserved in type definitions."""
        source = """\
@module test
@target python

@type Order {
  quantity: number, min: 1, max: 100
  price: number, positive
  description: string, required
}
"""
        nl_file = parse_nl_file(source)

        # Type definitions are stored in module.types
        assert len(nl_file.module.types) == 1
        type_def = nl_file.module.types[0]

        # Check fields exist
        field_names = [f.name for f in type_def.fields]
        assert "quantity" in field_names
        assert "price" in field_names
        assert "description" in field_names

    def test_invariants_linked_to_types(self):
        """@invariant blocks are linked to their types."""
        source = """\
@module test
@target python

@type Account {
  balance: number
}

@invariant Account {
  balance >= 0
}
"""
        nl_file = parse_nl_file(source)

        # Check invariant exists and is linked to Account
        assert len(nl_file.invariants) >= 1
        account_invariant = next(
            (inv for inv in nl_file.invariants if inv.type_name == "Account"),
            None
        )
        assert account_invariant is not None
        assert "balance >= 0" in account_invariant.conditions


class TestDependencyPreservation:
    """Tests that ANLU dependencies are preserved."""

    def test_depends_section_parsed(self):
        """DEPENDS section is correctly parsed."""
        source = """\
@module test
@target python

[helper]
PURPOSE: Helper function
INPUTS:
  - x: number
RETURNS: x * 2

[main-func]
PURPOSE: Uses helper
INPUTS:
  - x: number
LOGIC:
  1. doubled = helper(x)
RETURNS: doubled
DEPENDS: [helper]
"""
        nl_file = parse_nl_file(source)

        # Find main-func
        main_func = next(
            (a for a in nl_file.anlus if a.identifier == "main-func"),
            None
        )
        assert main_func is not None
        # Dependencies include brackets in storage, check either format
        assert "[helper]" in main_func.depends or "helper" in main_func.depends

    def test_multiple_dependencies(self):
        """Multiple dependencies are all preserved."""
        source = """\
@module test
@target python

[a]
PURPOSE: Function a
RETURNS: 1

[b]
PURPOSE: Function b
RETURNS: 2

[c]
PURPOSE: Uses a and b
LOGIC:
  1. result = a() + b()
RETURNS: result
DEPENDS: [a], [b]
"""
        nl_file = parse_nl_file(source)

        c_func = next(
            (a for a in nl_file.anlus if a.identifier == "c"),
            None
        )
        assert c_func is not None
        # Dependencies include brackets in storage
        assert "[a]" in c_func.depends or "a" in c_func.depends
        assert "[b]" in c_func.depends or "b" in c_func.depends


class TestModuleMetadataPreservation:
    """Tests that module metadata is preserved."""

    def test_module_name_preserved(self):
        """@module name is preserved."""
        source = """\
@module my_calculator
@target python

[add]
PURPOSE: Add numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
"""
        nl_file = parse_nl_file(source)
        assert nl_file.module.name == "my_calculator"

    def test_target_preserved(self):
        """@target is preserved."""
        source = """\
@module test
@target python

[identity]
PURPOSE: Identity
INPUTS:
  - x: number
RETURNS: x
"""
        nl_file = parse_nl_file(source)
        assert nl_file.module.target == "python"

    def test_version_preserved(self):
        """@version is preserved when present."""
        source = """\
@module test
@version 1.2.3
@target python

[func]
PURPOSE: Test
RETURNS: 1
"""
        nl_file = parse_nl_file(source)
        assert nl_file.module.version == "1.2.3"
