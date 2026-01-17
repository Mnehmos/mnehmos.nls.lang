"""Tests for nlsc test command - Issue #13"""

import pytest
import tempfile
from pathlib import Path
from nlsc.cli import cmd_test
from argparse import Namespace


class TestNlscTestCommand:
    """Tests for the nlsc test command"""

    def test_cmd_test_exists(self):
        """cmd_test function should exist"""
        assert callable(cmd_test)

    def test_cmd_test_runs_test_blocks(self, tmp_path):
        """nlsc test should execute @test blocks"""
        # Create a simple .nl file with tests
        # Note: Don't use "math" as module name - it shadows Python's math module
        nl_file = tmp_path / "calculator.nl"
        nl_file.write_text("""\
@module calculator
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

@test [add] {
  add(2, 3) == 5
  add(-1, 1) == 0
}
""")

        args = Namespace(file=str(nl_file), verbose=False)
        result = cmd_test(args)

        # Should pass (exit code 0)
        assert result == 0

    def test_cmd_test_reports_failures(self, tmp_path):
        """nlsc test should report failing tests"""
        nl_file = tmp_path / "broken.nl"
        nl_file.write_text("""\
@module broken
@target python

[always-one]
PURPOSE: Always returns 1
INPUTS:
  - x: number
RETURNS: 1

@test [always-one] {
  always_one(5) == 5
}
""")

        args = Namespace(file=str(nl_file), verbose=False)
        result = cmd_test(args)

        # Should fail (non-zero exit code)
        assert result != 0

    def test_cmd_test_no_tests_returns_success(self, tmp_path):
        """nlsc test with no @test blocks should succeed"""
        nl_file = tmp_path / "notests.nl"
        nl_file.write_text("""\
@module notests
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
""")

        args = Namespace(file=str(nl_file), verbose=False)
        result = cmd_test(args)

        # No tests = success with message
        assert result == 0

    def test_cmd_test_file_not_found(self):
        """nlsc test should error on missing file"""
        args = Namespace(file="nonexistent.nl", verbose=False)
        result = cmd_test(args)

        assert result == 1


class TestTestBlockParsing:
    """Tests for @test block parsing"""

    def test_parse_test_block(self):
        """Parser should extract @test blocks"""
        from nlsc.parser import parse_nl_file

        source = """\
@module test
@target python

[add]
PURPOSE: Add numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

@test [add] {
  add(1, 2) == 3
  add(0, 0) == 0
}
"""
        result = parse_nl_file(source)

        assert len(result.tests) == 1
        assert result.tests[0].anlu_id == "add"
        assert len(result.tests[0].cases) == 2

    def test_parse_multiple_test_blocks(self):
        """Parser should handle multiple @test blocks"""
        from nlsc.parser import parse_nl_file

        source = """\
@module test
@target python

[add]
PURPOSE: Add
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

[multiply]
PURPOSE: Multiply
INPUTS:
  - a: number
  - b: number
RETURNS: a * b

@test [add] {
  add(1, 2) == 3
}

@test [multiply] {
  multiply(2, 3) == 6
}
"""
        result = parse_nl_file(source)

        assert len(result.tests) == 2
        assert result.tests[0].anlu_id == "add"
        assert result.tests[1].anlu_id == "multiply"
