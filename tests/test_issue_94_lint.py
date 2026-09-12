"""Issue #94: `nlsc lint` — semantic intent-quality rules.

One fixture per rule, plus configuration, CLI flags, and directory mode.
"""

from __future__ import annotations

import json

from nlsc.cli import main
from nlsc.lint import RULES, LintConfig, lint_module
from nlsc.parser import parse_nl_file


def _lint(source: str, tmp_path=None, config: LintConfig | None = None):
    path = None
    if tmp_path is not None:
        path = tmp_path / "probe.nl"
        path.write_text(source, encoding="utf-8")
    nl_file = parse_nl_file(source, source_path=str(path) if path else "probe.nl")
    return lint_module(nl_file, file_token=str(path or "probe.nl"), config=config)


def _codes(diagnostics):
    return [d.code for d in diagnostics]


def test_rule_registry_has_at_least_ten_rules():
    assert len(RULES) >= 10


# --------------------------------------------------------------------------
# Structural completeness
# --------------------------------------------------------------------------


def test_elint001_inputs_without_guards(tmp_path):
    diagnostics = _lint(
        """@module m
@version 1.0.0
[f]
PURPOSE: p
INPUTS:
  - a: number
RETURNS: a
""",
        tmp_path,
    )
    assert "ELINT001" in _codes(diagnostics)


def test_elint002_inputs_without_tests(tmp_path):
    source = """@module m
@version 1.0.0
[f]
PURPOSE: p
INPUTS:
  - a: number
GUARDS:
  - a > 0 -> ValueError("positive")
RETURNS: a
"""
    diagnostics = _lint(source, tmp_path)
    assert "ELINT002" in _codes(diagnostics)


def test_elint002_satisfied_by_tests(tmp_path):
    source = """@module m
@version 1.0.0
[f]
PURPOSE: p
INPUTS:
  - a: number
GUARDS:
  - a > 0 -> ValueError("positive")
RETURNS: a

@test [f] {
  f(1) == 1
}
"""
    diagnostics = _lint(source, tmp_path)
    assert "ELINT002" not in _codes(diagnostics)


def test_elint003_type_without_invariant(tmp_path):
    diagnostics = _lint(
        """@module m
@version 1.0.0
@type Point {
  x: number
}
""",
        tmp_path,
    )
    assert "ELINT003" in _codes(diagnostics)


# --------------------------------------------------------------------------
# Safety
# --------------------------------------------------------------------------


def test_elint004_division_without_zero_guard(tmp_path):
    diagnostics = _lint(
        """@module m
@version 1.0.0
[f]
PURPOSE: p
INPUTS:
  - a: number
  - b: number
RETURNS: a / b
""",
        tmp_path,
    )
    assert "ELINT004" in _codes(diagnostics)


def test_elint004_satisfied_by_divisor_guard(tmp_path):
    source = """@module m
@version 1.0.0
[f]
PURPOSE: p
INPUTS:
  - a: number
  - b: number
GUARDS:
  - b != 0 -> ZeroDivisionError("divisor must not be zero")
RETURNS: a / b
"""
    diagnostics = _lint(source, tmp_path)
    assert "ELINT004" not in _codes(diagnostics)


def test_elint005_indexing_without_length_guard(tmp_path):
    diagnostics = _lint(
        """@module m
@version 1.0.0
[f]
PURPOSE: p
INPUTS:
  - items: list of number
RETURNS: items[0]
""",
        tmp_path,
    )
    assert "ELINT005" in _codes(diagnostics)


def test_elint006_optional_arithmetic_without_nil_check(tmp_path):
    diagnostics = _lint(
        """@module m
@version 1.0.0
[f]
PURPOSE: p
INPUTS:
  - bonus: number, optional
  - base: number
RETURNS: base + bonus
""",
        tmp_path,
    )
    assert "ELINT006" in _codes(diagnostics)


def test_elint007_augmented_assignment(tmp_path):
    diagnostics = _lint(
        """@module m
@version 1.0.0
[f]
PURPOSE: p
INPUTS:
  - items: list of number
LOGIC:
  1. acc = 0
  2. acc += 1
RETURNS: acc
""",
        tmp_path,
    )
    assert "ELINT007" in _codes(diagnostics)


# --------------------------------------------------------------------------
# Hygiene and best practices
# --------------------------------------------------------------------------


def test_elint008_missing_version(tmp_path):
    diagnostics = _lint("[f]\nPURPOSE: p\nRETURNS: 1\n", tmp_path)
    assert "ELINT008" in _codes(diagnostics)


def test_elint009_long_logic(tmp_path):
    steps = "\n".join(f"  {i}. v{i} = {i}" for i in range(1, 13))
    diagnostics = _lint(
        f"""@module m
@version 1.0.0
[f]
PURPOSE: p
LOGIC:
{steps}
RETURNS: v12
""",
        tmp_path,
    )
    assert "ELINT009" in _codes(diagnostics)


def test_elint010_deep_conditional_nesting(tmp_path):
    diagnostics = _lint(
        """@module m
@version 1.0.0
[f]
PURPOSE: p
INPUTS:
  - a: boolean
  - b: boolean
  - c: boolean
LOGIC:
  1. IF a THEN IF b THEN 1 -> x ELSE 0 -> x ELSE 0 -> x
RETURNS: x
""",
        tmp_path,
    )
    assert "ELINT010" in _codes(diagnostics)


def test_elint011_input_not_referenced_by_tests(tmp_path):
    diagnostics = _lint(
        """@module m
@version 1.0.0
[f]
PURPOSE: p
INPUTS:
  - a: number
  - bonus: number
GUARDS:
  - a > 0 -> ValueError("positive")
RETURNS: a

@test [f] {
  f(2) == 2
}
""",
        tmp_path,
    )
    codes = _codes(diagnostics)
    assert "ELINT011" in codes
    message = [d for d in diagnostics if d.code == "ELINT011"][0].message
    assert "bonus" in message


def test_elint012_untyped_guard(tmp_path):
    diagnostics = _lint(
        """@module m
@version 1.0.0
[f]
PURPOSE: p
INPUTS:
  - a: number
GUARDS:
  - a > 0
RETURNS: a
""",
        tmp_path,
    )
    assert "ELINT012" in _codes(diagnostics)


def test_clean_module_has_no_warnings(tmp_path):
    diagnostics = _lint(
        """@module m
@version 1.0.0
@type Amount {
  value: number
}

@invariant Amount {
  value >= 0
}

[f]
PURPOSE: scale a validated amount
INPUTS:
  - amount: Amount
GUARDS:
  - amount.value >= 0 -> ValueError("amount must be non-negative")
RETURNS: amount.value * 2

@test [f] {
  f(Amount(value = 2)) == 4
}
""",
        tmp_path,
    )
    assert diagnostics == [], [d.message for d in diagnostics]


# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------


def test_nlslintrc_disables_rules(tmp_path):
    (tmp_path / ".nlslintrc").write_text(
        json.dumps({"disable": ["ELINT001", "ELINT002", "ELINT008", "ELINT012"]}),
        encoding="utf-8",
    )
    diagnostics = _lint(
        """[f]
PURPOSE: p
INPUTS:
  - a: number
GUARDS:
  - a > 0
RETURNS: a
""",
        tmp_path,
    )
    codes = _codes(diagnostics)
    for disabled in ("ELINT001", "ELINT002", "ELINT008", "ELINT012"):
        assert disabled not in codes


def test_nls_toml_disables_rules(tmp_path):
    (tmp_path / "nls.toml").write_text(
        "[lint]\ndisable = [\"ELINT008\"]\n", encoding="utf-8"
    )
    diagnostics = _lint("[f]\nPURPOSE: p\nRETURNS: 1\n", tmp_path)
    assert "ELINT008" not in _codes(diagnostics)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _write(tmp_path, source: str, name="probe.nl"):
    path = tmp_path / name
    path.write_text(source, encoding="utf-8")
    return path


def test_cli_lint_reports_file_line_rule(tmp_path, capsys):
    path = _write(
        tmp_path,
        """@module m
@version 1.0.0
[f]
PURPOSE: p
INPUTS:
  - a: number
RETURNS: a
""",
    )
    assert main(["lint", str(path)]) == 0
    out = capsys.readouterr().out
    assert "ELINT001" in out
    assert "probe.nl:" in out


def test_cli_lint_strict_exits_one(tmp_path, capsys):
    path = _write(tmp_path, "[f]\nPURPOSE: p\nRETURNS: 1\n")
    assert main(["lint", str(path), "--strict"]) == 1
    assert main(["lint", str(path)]) == 0


def test_cli_lint_directory_mode(tmp_path, capsys):
    _write(tmp_path, "[a]\nPURPOSE: p\nRETURNS: 1\n", "one.nl")
    (tmp_path / "sub").mkdir()
    _write(tmp_path / "sub", "[b]\nPURPOSE: p\nRETURNS: 1\n", "two.nl")
    assert main(["lint", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "2 warning(s) across 2 file(s)" in out


def test_cli_lint_json_payload(tmp_path, capsys):
    path = _write(tmp_path, "[f]\nPURPOSE: p\nRETURNS: 1\n")
    assert main(["lint", "--json", str(path)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["command"] == "lint"
    assert payload["warnings"] >= 1
    assert "ELINT008" in [d["code"] for d in payload["diagnostics"]]


def test_cli_lint_parse_failure_fails(tmp_path, capsys):
    path = _write(
        tmp_path,
        "[f]\nPURPOSE: p\nLOGIC:\n  1. x = 1\n  1. y = x + 1\nRETURNS: y\n",
    )
    assert main(["lint", str(path)]) == 1
    assert "EPARSE001" in capsys.readouterr().err


def test_cli_lint_list_rules(capsys):
    assert main(["lint", "--list-rules"]) == 0
    out = capsys.readouterr().out
    assert "ELINT001" in out and "ELINT012" in out
