"""Tests for FSM-style state names in LOGIC steps - Issue #3"""

import pytest
from nlsc.parser import parse_nl_file
from nlsc.schema import LogicStep


class TestStateNameParsing:
    """Tests for [state_name] prefix in LOGIC steps"""

    def test_parse_state_name(self):
        """Parse [state_name] prefix from LOGIC step"""
        source = """\
@module test
@target python

[process-order]
PURPOSE: Process an order
INPUTS:
  - order: Order
LOGIC:
  1. [validate] Check order items are in stock
  2. [charge] Process payment
  3. [fulfill] Ship the order
RETURNS: ProcessResult
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]
        assert len(anlu.logic_steps) == 3

        assert anlu.logic_steps[0].state_name == "validate"
        assert anlu.logic_steps[1].state_name == "charge"
        assert anlu.logic_steps[2].state_name == "fulfill"

    def test_state_name_optional(self):
        """Steps without [state_name] should have None"""
        source = """\
@module test
@target python

[simple]
PURPOSE: Simple operation
INPUTS:
  - x: number
LOGIC:
  1. Calculate result
  2. [save] Store in database
RETURNS: result
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]

        assert anlu.logic_steps[0].state_name is None
        assert anlu.logic_steps[1].state_name == "save"


class TestOutputBinding:
    """Tests for → variable output binding"""

    def test_parse_output_binding(self):
        """Parse → variable syntax"""
        source = """\
@module test
@target python

[pipeline]
PURPOSE: Multi-step pipeline
INPUTS:
  - data: Data
LOGIC:
  1. [validate] Validate input → valid_data
  2. [transform] Transform valid_data → result
RETURNS: result
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]

        assert anlu.logic_steps[0].output_binding == "valid_data"
        assert anlu.logic_steps[1].output_binding == "result"

    def test_output_binding_with_arrow_text(self):
        """Parse with ASCII arrow ->"""
        source = """\
@module test
@target python

[flow]
PURPOSE: Data flow
INPUTS:
  - x: number
LOGIC:
  1. Calculate value -> result
RETURNS: result
"""
        result = parse_nl_file(source)
        step = result.anlus[0].logic_steps[0]
        assert step.output_binding == "result"

    def test_no_output_binding(self):
        """Steps without → should have None output_binding"""
        source = """\
@module test
@target python

[simple]
PURPOSE: Simple
INPUTS:
  - x: number
LOGIC:
  1. Do something
RETURNS: x
"""
        result = parse_nl_file(source)
        assert result.anlus[0].logic_steps[0].output_binding is None


class TestConditionalTransitions:
    """Tests for IF condition THEN syntax"""

    def test_parse_if_then(self):
        """Parse IF condition THEN action"""
        source = """\
@module test
@target python

[branching]
PURPOSE: Conditional logic
INPUTS:
  - payment: Payment
LOGIC:
  1. [check] Verify payment → payment_result
  2. [ship] IF payment_result.success THEN ship order
  3. [refund] IF NOT payment_result.success THEN refund customer
RETURNS: OrderResult
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]

        step2 = anlu.logic_steps[1]
        assert step2.condition == "payment_result.success"
        assert step2.is_conditional

        step3 = anlu.logic_steps[2]
        assert step3.condition == "NOT payment_result.success"
        assert step3.is_conditional

    def test_non_conditional_step(self):
        """Steps without IF should not be conditional"""
        source = """\
@module test
@target python

[simple]
PURPOSE: Simple
INPUTS:
  - x: number
LOGIC:
  1. Calculate result
RETURNS: result
"""
        result = parse_nl_file(source)
        step = result.anlus[0].logic_steps[0]
        assert step.condition is None
        assert not step.is_conditional


class TestFSMGraph:
    """Tests for FSM graph construction"""

    def test_get_fsm_states(self):
        """Extract FSM states from LOGIC steps"""
        source = """\
@module test
@target python

[workflow]
PURPOSE: Multi-step workflow
INPUTS:
  - request: Request
LOGIC:
  1. [init] Initialize process
  2. [validate] Validate request
  3. [process] Process request
  4. [complete] Mark as complete
RETURNS: Response
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]

        states = anlu.fsm_states()
        assert states == ["init", "validate", "process", "complete"]

    def test_fsm_transitions(self):
        """Build transitions from state dependencies"""
        source = """\
@module test
@target python

[flow]
PURPOSE: State flow
INPUTS:
  - x: number
LOGIC:
  1. [start] a = x + 1
  2. [middle] b = a * 2
  3. [end] result = b + 10
RETURNS: result
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]

        transitions = anlu.fsm_transitions()
        # start -> middle (because middle uses 'a' from start)
        # middle -> end (because end uses 'b' from middle)
        assert ("start", "middle") in transitions
        assert ("middle", "end") in transitions


class TestCombinedFeatures:
    """Tests for combined state names, output bindings, and conditions"""

    def test_full_fsm_step(self):
        """Parse step with all FSM features"""
        source = """\
@module test
@target python

[full-workflow]
PURPOSE: Complete workflow
INPUTS:
  - order: Order
LOGIC:
  1. [validate] Check order validity → validation_result
  2. [charge] IF validation_result.valid THEN process payment → payment
  3. [ship] IF payment.success THEN ship order → tracking
RETURNS: OrderResult
"""
        result = parse_nl_file(source)
        anlu = result.anlus[0]

        step1 = anlu.logic_steps[0]
        assert step1.state_name == "validate"
        assert step1.output_binding == "validation_result"
        assert not step1.is_conditional

        step2 = anlu.logic_steps[1]
        assert step2.state_name == "charge"
        assert step2.output_binding == "payment"
        assert step2.condition == "validation_result.valid"
        assert step2.is_conditional

        step3 = anlu.logic_steps[2]
        assert step3.state_name == "ship"
        assert step3.output_binding == "tracking"
        assert step3.condition == "payment.success"
