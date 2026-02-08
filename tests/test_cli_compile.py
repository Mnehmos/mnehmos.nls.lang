"""Tests for nlsc compile command error handling."""

import subprocess
import sys
from pathlib import Path


class TestCompileCommand:
    """Compile command behavior tests."""

    def test_compile_emitter_error_is_reported_cleanly(self, tmp_path):
        """Compile should fail gracefully when emitted Python is invalid."""
        nl_file = tmp_path / "bad_guard.nl"
        nl_file.write_text("""\
@module bad_guard
@target python

[divide]
PURPOSE: Divide safely
INPUTS:
  - numerator: number
  - divisor: number
GUARDS:
  - divisor must not be zero -> ValueError("Cannot divide by zero")
LOGIC:
  1. result = numerator / divisor
RETURNS: result
""")

        result = subprocess.run(
            [sys.executable, "-m", "nlsc", "compile", str(nl_file)],
            capture_output=True,
            text=True,
        )

        # Note: python -m nlsc currently does not propagate main() return code.
        assert "Emitter error:" in result.stderr
        assert "Traceback" not in result.stderr
