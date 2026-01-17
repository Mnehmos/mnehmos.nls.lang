"""Tests for dataflow extraction from LOGIC steps - Issue #2"""

import pytest
from nlsc.parser import parse_nl_file
from nlsc.schema import LogicStep


class TestLogicStepParsing:
    """Tests for parsing LOGIC steps with variable assignments"""

    def test_parse_simple_assignment(self):
        """Parse LOGIC step with simple assignment"""
        source = """\
@module test
@target python

[calculate-tax]
PURPOSE: Calculate tax amount
INPUTS:
  - income: number
  - rate: number
LOGIC:
  1. tax = income * rate
RETURNS: tax
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        assert len(anlu.logic_steps) == 1
        step = anlu.logic_steps[0]
        assert step.number == 1
        assert "tax" in step.assigns
        assert "income" in step.uses
        assert "rate" in step.uses

    def test_parse_multiple_assignments(self):
        """Parse multiple LOGIC steps with dependencies"""
        source = """\
@module test
@target python

[calculate-final-tax]
PURPOSE: Calculate final tax with deductions
INPUTS:
  - income: number
  - deductions: list of number
LOGIC:
  1. base_tax = income * 0.25
  2. total_deductions = sum(deductions)
  3. final_tax = base_tax - total_deductions
RETURNS: final_tax
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        assert len(anlu.logic_steps) == 3

        step1 = anlu.logic_steps[0]
        assert step1.assigns == ["base_tax"]
        assert "income" in step1.uses

        step2 = anlu.logic_steps[1]
        assert step2.assigns == ["total_deductions"]
        assert "deductions" in step2.uses

        step3 = anlu.logic_steps[2]
        assert step3.assigns == ["final_tax"]
        assert "base_tax" in step3.uses
        assert "total_deductions" in step3.uses

    def test_step_dependencies(self):
        """Steps should track which previous steps they depend on"""
        source = """\
@module test
@target python

[pipeline]
PURPOSE: Multi-step pipeline
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

        step1 = anlu.logic_steps[0]  # a = x + 1
        step2 = anlu.logic_steps[1]  # b = x * 2
        step3 = anlu.logic_steps[2]  # c = a + b

        # Step 1 and 2 have no dependencies on other steps
        assert step1.depends_on == []
        assert step2.depends_on == []

        # Step 3 depends on steps 1 and 2
        assert 1 in step3.depends_on
        assert 2 in step3.depends_on


class TestLogicStepDataclass:
    """Tests for LogicStep dataclass"""

    def test_logic_step_creation(self):
        """LogicStep should be creatable with all fields"""
        step = LogicStep(
            number=1,
            description="Calculate base tax",
            assigns=["base_tax"],
            uses=["income", "rate"],
            depends_on=[]
        )
        assert step.number == 1
        assert step.description == "Calculate base tax"
        assert step.assigns == ["base_tax"]
        assert step.uses == ["income", "rate"]
        assert step.depends_on == []

    def test_logic_step_is_independent(self):
        """LogicStep with no depends_on is independent"""
        step = LogicStep(
            number=1,
            description="First step",
            assigns=["a"],
            uses=["x"],
            depends_on=[]
        )
        assert step.is_independent

    def test_logic_step_is_not_independent(self):
        """LogicStep with depends_on is not independent"""
        step = LogicStep(
            number=3,
            description="Third step",
            assigns=["c"],
            uses=["a", "b"],
            depends_on=[1, 2]
        )
        assert not step.is_independent


class TestParallelizationDetection:
    """Tests for detecting parallelizable steps"""

    def test_detect_parallel_steps(self):
        """Steps with no inter-dependencies can run in parallel"""
        source = """\
@module test
@target python

[parallel-ops]
PURPOSE: Operations that can run in parallel
INPUTS:
  - x: number
  - y: number
LOGIC:
  1. a = x * 2
  2. b = y * 3
  3. result = a + b
RETURNS: result
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]

        # Get parallelizable groups
        groups = anlu.parallel_groups()

        # Steps 1 and 2 can run in parallel (both independent)
        # Step 3 must wait for both
        assert len(groups) == 2
        assert {1, 2} in [set(g) for g in groups]
        assert {3} in [set(g) for g in groups]


class TestExpressionParsing:
    """Tests for parsing variable references in expressions"""

    def test_parse_arithmetic_expression(self):
        """Parse variables from arithmetic expressions"""
        source = """\
@module test
@target python

[math]
PURPOSE: Math operations
INPUTS:
  - a: number
  - b: number
  - c: number
LOGIC:
  1. result = a + b * c - 10
RETURNS: result
"""
        result = parse_nl_file(source)
        step = result.anlus[0].logic_steps[0]
        assert "a" in step.uses
        assert "b" in step.uses
        assert "c" in step.uses
        # Literals should not be in uses
        assert "10" not in step.uses

    def test_parse_function_call_args(self):
        """Parse variables from function call arguments"""
        source = """\
@module test
@target python

[with-functions]
PURPOSE: Use function calls
INPUTS:
  - items: list of number
  - factor: number
LOGIC:
  1. total = sum(items)
  2. scaled = total * factor
RETURNS: scaled
"""
        result = parse_nl_file(source)
        step1 = result.anlus[0].logic_steps[0]
        assert "items" in step1.uses

        step2 = result.anlus[0].logic_steps[1]
        assert "total" in step2.uses
        assert "factor" in step2.uses


class TestBackwardsCompatibility:
    """Ensure old-style LOGIC still works"""

    def test_plain_logic_still_works(self):
        """LOGIC without assignments should still parse"""
        source = """\
@module test
@target python

[simple]
PURPOSE: Simple operation
INPUTS:
  - a: number
  - b: number
LOGIC:
  1. Add a and b together
  2. Return the result
RETURNS: a + b
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        # Plain LOGIC should still be in .logic list
        assert len(anlu.logic) == 2
        assert "Add a and b" in anlu.logic[0]
