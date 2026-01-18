"""
Test parity between regex and tree-sitter parsers.

Ensures that both parsers produce equivalent AST output for the same input.
"""

import pytest
from pathlib import Path

from nlsc.parser import parse_nl_file, ParseError
from nlsc.schema import NLFile


# Try to import tree-sitter parser
try:
    from nlsc.parser_treesitter import (
        parse_nl_file_treesitter,
        is_available as treesitter_available,
    )
    TREESITTER_AVAILABLE = treesitter_available()
except ImportError:
    TREESITTER_AVAILABLE = False
    parse_nl_file_treesitter = None


# Skip all tests if tree-sitter is not available
pytestmark = pytest.mark.skipif(
    not TREESITTER_AVAILABLE,
    reason="tree-sitter not available"
)


def compare_anlus(regex_file: NLFile, ts_file: NLFile) -> list[str]:
    """Compare ANLUs from both parsers, return list of differences."""
    errors = []

    if len(regex_file.anlus) != len(ts_file.anlus):
        errors.append(
            f"ANLU count mismatch: regex={len(regex_file.anlus)}, "
            f"ts={len(ts_file.anlus)}"
        )
        return errors

    for i, (ra, ta) in enumerate(zip(regex_file.anlus, ts_file.anlus)):
        prefix = f"ANLU[{i}] {ra.identifier}"

        if ra.identifier != ta.identifier:
            errors.append(f"{prefix}: identifier mismatch: {ra.identifier} vs {ta.identifier}")

        if ra.purpose != ta.purpose:
            errors.append(f"{prefix}: purpose mismatch: '{ra.purpose}' vs '{ta.purpose}'")

        if ra.returns != ta.returns:
            errors.append(f"{prefix}: returns mismatch: '{ra.returns}' vs '{ta.returns}'")

        # Compare inputs
        if len(ra.inputs) != len(ta.inputs):
            errors.append(f"{prefix}: input count mismatch: {len(ra.inputs)} vs {len(ta.inputs)}")
        else:
            for j, (ri, ti) in enumerate(zip(ra.inputs, ta.inputs)):
                if ri.name != ti.name:
                    errors.append(f"{prefix}: input[{j}].name mismatch: {ri.name} vs {ti.name}")
                if ri.type != ti.type:
                    errors.append(f"{prefix}: input[{j}].type mismatch: {ri.type} vs {ti.type}")

        # Compare guards
        if len(ra.guards) != len(ta.guards):
            errors.append(f"{prefix}: guard count mismatch: {len(ra.guards)} vs {len(ta.guards)}")
        else:
            for j, (rg, tg) in enumerate(zip(ra.guards, ta.guards)):
                if rg.condition != tg.condition:
                    errors.append(f"{prefix}: guard[{j}].condition mismatch: '{rg.condition}' vs '{tg.condition}'")
                if rg.error_type != tg.error_type:
                    errors.append(f"{prefix}: guard[{j}].error_type mismatch: {rg.error_type} vs {tg.error_type}")
                if rg.error_message != tg.error_message:
                    errors.append(f"{prefix}: guard[{j}].error_message mismatch: {rg.error_message} vs {tg.error_message}")

        # Compare logic steps
        if len(ra.logic_steps) != len(ta.logic_steps):
            errors.append(f"{prefix}: logic_step count mismatch: {len(ra.logic_steps)} vs {len(ta.logic_steps)}")
        else:
            for j, (rs, ts) in enumerate(zip(ra.logic_steps, ta.logic_steps)):
                if rs.number != ts.number:
                    errors.append(f"{prefix}: logic_step[{j}].number mismatch: {rs.number} vs {ts.number}")
                if rs.description != ts.description:
                    errors.append(f"{prefix}: logic_step[{j}].description mismatch: '{rs.description}' vs '{ts.description}'")
                if rs.assigns != ts.assigns:
                    errors.append(f"{prefix}: logic_step[{j}].assigns mismatch: {rs.assigns} vs {ts.assigns}")
                if rs.uses != ts.uses:
                    errors.append(f"{prefix}: logic_step[{j}].uses mismatch: {rs.uses} vs {ts.uses}")

        # Compare edge cases
        if len(ra.edge_cases) != len(ta.edge_cases):
            errors.append(f"{prefix}: edge_case count mismatch: {len(ra.edge_cases)} vs {len(ta.edge_cases)}")

        # Compare depends
        if ra.depends != ta.depends:
            errors.append(f"{prefix}: depends mismatch: {ra.depends} vs {ta.depends}")

    return errors


def compare_types(regex_file: NLFile, ts_file: NLFile) -> list[str]:
    """Compare type definitions from both parsers."""
    errors = []

    if len(regex_file.module.types) != len(ts_file.module.types):
        errors.append(
            f"Type count mismatch: regex={len(regex_file.module.types)}, "
            f"ts={len(ts_file.module.types)}"
        )
        return errors

    for i, (rt, tt) in enumerate(zip(regex_file.module.types, ts_file.module.types)):
        prefix = f"Type[{i}] {rt.name}"

        if rt.name != tt.name:
            errors.append(f"{prefix}: name mismatch: {rt.name} vs {tt.name}")

        if rt.base != tt.base:
            errors.append(f"{prefix}: base mismatch: {rt.base} vs {tt.base}")

        if len(rt.fields) != len(tt.fields):
            errors.append(f"{prefix}: field count mismatch: {len(rt.fields)} vs {len(tt.fields)}")
        else:
            for j, (rf, tf) in enumerate(zip(rt.fields, tt.fields)):
                if rf.name != tf.name:
                    errors.append(f"{prefix}: field[{j}].name mismatch: {rf.name} vs {tf.name}")
                if rf.type != tf.type:
                    errors.append(f"{prefix}: field[{j}].type mismatch: {rf.type} vs {tf.type}")

    return errors


def compare_tests(regex_file: NLFile, ts_file: NLFile) -> list[str]:
    """Compare test suites from both parsers."""
    errors = []

    if len(regex_file.tests) != len(ts_file.tests):
        errors.append(
            f"TestSuite count mismatch: regex={len(regex_file.tests)}, "
            f"ts={len(ts_file.tests)}"
        )
        return errors

    for i, (rt, tt) in enumerate(zip(regex_file.tests, ts_file.tests)):
        prefix = f"TestSuite[{i}] {rt.anlu_id}"

        if rt.anlu_id != tt.anlu_id:
            errors.append(f"{prefix}: anlu_id mismatch: {rt.anlu_id} vs {tt.anlu_id}")

        if len(rt.cases) != len(tt.cases):
            errors.append(f"{prefix}: case count mismatch: {len(rt.cases)} vs {len(tt.cases)}")
        else:
            for j, (rc, tc) in enumerate(zip(rt.cases, tt.cases)):
                if rc.expression != tc.expression:
                    errors.append(f"{prefix}: case[{j}].expression mismatch: '{rc.expression}' vs '{tc.expression}'")
                if rc.expected != tc.expected:
                    errors.append(f"{prefix}: case[{j}].expected mismatch: '{rc.expected}' vs '{tc.expected}'")

    return errors


def compare_properties(regex_file: NLFile, ts_file: NLFile) -> list[str]:
    """Compare property tests from both parsers."""
    errors = []

    if len(regex_file.properties) != len(ts_file.properties):
        errors.append(
            f"Property count mismatch: regex={len(regex_file.properties)}, "
            f"ts={len(ts_file.properties)}"
        )
        return errors

    for i, (rp, tp) in enumerate(zip(regex_file.properties, ts_file.properties)):
        prefix = f"Property[{i}] {rp.anlu_id}"

        if rp.anlu_id != tp.anlu_id:
            errors.append(f"{prefix}: anlu_id mismatch: {rp.anlu_id} vs {tp.anlu_id}")

        if len(rp.assertions) != len(tp.assertions):
            errors.append(f"{prefix}: assertion count mismatch: {len(rp.assertions)} vs {len(tp.assertions)}")
        else:
            for j, (ra, ta) in enumerate(zip(rp.assertions, tp.assertions)):
                if ra.expression != ta.expression:
                    errors.append(f"{prefix}: assertion[{j}].expression mismatch: '{ra.expression}' vs '{ta.expression}'")
                if ra.quantifier != ta.quantifier:
                    errors.append(f"{prefix}: assertion[{j}].quantifier mismatch: {ra.quantifier} vs {ta.quantifier}")

    return errors


def compare_invariants(regex_file: NLFile, ts_file: NLFile) -> list[str]:
    """Compare invariants from both parsers."""
    errors = []

    if len(regex_file.invariants) != len(ts_file.invariants):
        errors.append(
            f"Invariant count mismatch: regex={len(regex_file.invariants)}, "
            f"ts={len(ts_file.invariants)}"
        )
        return errors

    for i, (ri, ti) in enumerate(zip(regex_file.invariants, ts_file.invariants)):
        prefix = f"Invariant[{i}] {ri.type_name}"

        if ri.type_name != ti.type_name:
            errors.append(f"{prefix}: type_name mismatch: {ri.type_name} vs {ti.type_name}")

        if len(ri.conditions) != len(ti.conditions):
            errors.append(f"{prefix}: condition count mismatch: {len(ri.conditions)} vs {len(ti.conditions)}")
        else:
            for j, (rc, tc) in enumerate(zip(ri.conditions, ti.conditions)):
                if rc != tc:
                    errors.append(f"{prefix}: condition[{j}] mismatch: '{rc}' vs '{tc}'")

    return errors


def compare_main_block(regex_file: NLFile, ts_file: NLFile) -> list[str]:
    """Compare main block from both parsers."""
    errors = []

    if len(regex_file.main_block) != len(ts_file.main_block):
        errors.append(
            f"Main block line count mismatch: regex={len(regex_file.main_block)}, "
            f"ts={len(ts_file.main_block)}"
        )
        return errors

    for i, (rl, tl) in enumerate(zip(regex_file.main_block, ts_file.main_block)):
        if rl != tl:
            errors.append(f"Main block line[{i}] mismatch: '{rl}' vs '{tl}'")

    return errors


class TestParserParity:
    """Test that regex and tree-sitter parsers produce identical output."""

    def test_simple_anlu(self):
        """Test simple ANLU parsing."""
        source = """[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
"""
        regex_result = parse_nl_file(source)
        ts_result = parse_nl_file_treesitter(source)

        errors = compare_anlus(regex_result, ts_result)
        assert not errors, "\n".join(errors)

    def test_anlu_with_guards(self):
        """Test ANLU with guards."""
        source = '''[divide]
PURPOSE: Divide two numbers
INPUTS:
  - a: number
  - b: number
GUARDS:
  - b must not be zero -> ValueError("Division by zero")
RETURNS: a / b
'''
        regex_result = parse_nl_file(source)
        ts_result = parse_nl_file_treesitter(source)

        errors = compare_anlus(regex_result, ts_result)
        assert not errors, "\n".join(errors)

    def test_anlu_with_logic(self):
        """Test ANLU with LOGIC section."""
        source = """[calculate-total]
PURPOSE: Calculate order total with tax
INPUTS:
  - subtotal: number
  - tax_rate: number
LOGIC:
  1. tax = subtotal * tax_rate
  2. total = subtotal + tax
RETURNS: total
"""
        regex_result = parse_nl_file(source)
        ts_result = parse_nl_file_treesitter(source)

        errors = compare_anlus(regex_result, ts_result)
        assert not errors, "\n".join(errors)

    def test_directives(self):
        """Test module directives."""
        source = """@module math
@version 1.0.0
@target python

[add]
PURPOSE: Add
INPUTS:
  - a: number
RETURNS: a
"""
        regex_result = parse_nl_file(source)
        ts_result = parse_nl_file_treesitter(source)

        assert regex_result.module.name == ts_result.module.name
        assert regex_result.module.version == ts_result.module.version
        assert regex_result.module.target == ts_result.module.target

    def test_type_definitions(self):
        """Test type block parsing."""
        source = """@type Order {
  id: string
  items: list of OrderItem
  total: number
}
"""
        regex_result = parse_nl_file(source)
        ts_result = parse_nl_file_treesitter(source)

        errors = compare_types(regex_result, ts_result)
        assert not errors, "\n".join(errors)

    def test_test_blocks(self):
        """Test @test block parsing."""
        source = """[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

@test [add] {
  add(1, 2) == 3
  add(0, 0) == 0
}
"""
        regex_result = parse_nl_file(source)
        ts_result = parse_nl_file_treesitter(source)

        errors = compare_tests(regex_result, ts_result)
        assert not errors, "\n".join(errors)

    def test_edge_cases(self):
        """Test EDGE CASES section."""
        source = """[safe-divide]
PURPOSE: Divide with safe fallback
INPUTS:
  - a: number
  - b: number
  - fallback: number
EDGE CASES:
  - b is zero -> return fallback
  - result is infinity -> return fallback
RETURNS: a / b
"""
        regex_result = parse_nl_file(source)
        ts_result = parse_nl_file_treesitter(source)

        errors = compare_anlus(regex_result, ts_result)
        assert not errors, "\n".join(errors)

    def test_depends_section(self):
        """Test DEPENDS section."""
        source = """[process-order]
PURPOSE: Process customer order
INPUTS:
  - order: Order
DEPENDS: [validate-order], [calculate-total]
RETURNS: ProcessedOrder
"""
        regex_result = parse_nl_file(source)
        ts_result = parse_nl_file_treesitter(source)

        errors = compare_anlus(regex_result, ts_result)
        assert not errors, "\n".join(errors)

    def test_property_blocks(self):
        """Test @property block parsing."""
        source = """[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

@property [add] {
  add(0, x) == x  # Identity property
  add(x, y) == add(y, x)  # Commutative property
  forall n: number -> add(n, 0) == n
}
"""
        regex_result = parse_nl_file(source)
        ts_result = parse_nl_file_treesitter(source)

        errors = compare_properties(regex_result, ts_result)
        assert not errors, "\n".join(errors)
        assert len(regex_result.properties) == 1
        assert regex_result.properties[0].anlu_id == "add"
        assert len(regex_result.properties[0].assertions) == 3

    def test_invariant_blocks(self):
        """Test @invariant block parsing."""
        source = """@type Account {
  balance: number
  owner: string
}

@invariant Account {
  balance >= 0
  owner != ""
}

[deposit]
PURPOSE: Deposit money
INPUTS:
  - account: Account
  - amount: number
RETURNS: updated account
"""
        regex_result = parse_nl_file(source)
        ts_result = parse_nl_file_treesitter(source)

        errors = compare_invariants(regex_result, ts_result)
        assert not errors, "\n".join(errors)
        assert len(regex_result.invariants) == 1
        assert regex_result.invariants[0].type_name == "Account"
        assert len(regex_result.invariants[0].conditions) == 2

    def test_main_block(self):
        """Test @main block parsing."""
        source = """[greet]
PURPOSE: Print greeting
INPUTS:
  - name: string
RETURNS: greeting message

@main {
  print(greet("World"))
  process_all_items()
}
"""
        regex_result = parse_nl_file(source)
        ts_result = parse_nl_file_treesitter(source)

        errors = compare_main_block(regex_result, ts_result)
        assert not errors, "\n".join(errors)
        assert len(regex_result.main_block) == 2
        assert "greet" in regex_result.main_block[0]


class TestParserParityExamples:
    """Test parity on example files."""

    @pytest.fixture
    def examples_dir(self) -> Path:
        return Path(__file__).parent.parent / "examples"

    def test_math_example(self, examples_dir: Path):
        """Test math.nl example file."""
        math_file = examples_dir / "math.nl"
        if not math_file.exists():
            pytest.skip("math.nl not found")

        source = math_file.read_text(encoding="utf-8")
        regex_result = parse_nl_file(source)
        ts_result = parse_nl_file_treesitter(source)

        errors = []
        errors.extend(compare_anlus(regex_result, ts_result))
        errors.extend(compare_types(regex_result, ts_result))
        errors.extend(compare_tests(regex_result, ts_result))

        assert not errors, "\n".join(errors)
