"""Issue #145: the quickstart walkthrough stays true.

The guide's shipping-quote project is embedded here and exercised through
the real CLI (init, strict verify, compile both targets, test, ci) so the
documentation cannot rot.  This also pins the relative-path regression the
walkthrough exposed: ``nlsc test`` with a relative file path must run the
generated tests in the right working directory.
"""

from __future__ import annotations

import pytest

from nlsc.cli import main

WALKTHROUGH_NL = """@module shipping
@version 1.0.0
@target python

@type Parcel {
  weight_kg: number, min: 0
  declared_value: number, min: 0
}

@type Quote {
  currency: string
  base_fee: number, min: 0
  insurance: number, min: 0
  total: number, min: 0
}

[base-rate]
PURPOSE: Tiered base rate for a parcel by weight
INPUTS:
  - weight_kg: number
GUARDS:
  - weight_kg >= 0 -> ValueError("weight cannot be negative")
LOGIC:
  1. IF weight_kg <= 1 THEN 5.0 -> rate ELSE 5.0 + (weight_kg - 1) * 2.0 -> rate
RETURNS: rate

[insurance-fee]
PURPOSE: Insurance proportional to declared value
INPUTS:
  - declared_value: number
GUARDS:
  - declared_value >= 0 -> ValueError("declared value cannot be negative")
RETURNS: declared_value * 0.02

[shipping-quote]
PURPOSE: Full quote for a parcel, with an express surcharge option
INPUTS:
  - parcel: Parcel
  - express: boolean
LOGIC:
  1. base = [base-rate](parcel.weight_kg)
  2. insurance = [insurance-fee](parcel.declared_value)
  3. IF express THEN base * 1.5 -> surcharge ELSE 0 -> surcharge
  4. total = base + insurance + surcharge
RETURNS: Quote(currency = "USD", base_fee = base, insurance = insurance, total = total)
DEPENDS: [base-rate], [insurance-fee]

@test [base-rate] {
  base_rate(1) == 5
  base_rate(2) == 7
  base_rate(0.5) == 5
}

@test [shipping-quote] {
  shipping_quote(Parcel(weight_kg = 2, declared_value = 100), False).total == 9
  shipping_quote(Parcel(weight_kg = 2, declared_value = 100), True).total == 19.5
}
"""


@pytest.fixture
def project(tmp_path, monkeypatch):
    """A quickstart project laid out exactly as the guide describes."""
    (tmp_path / "src").mkdir()
    nl_path = tmp_path / "src" / "shipping.nl"
    nl_path.write_text(WALKTHROUGH_NL, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    return nl_path


def test_strict_verify_passes(project):
    assert main(["verify", "src/shipping.nl", "--strict"]) == 0


def test_compile_both_targets(project):
    assert main(["compile", "src/shipping.nl"]) == 0
    assert main(["compile", "src/shipping.nl", "-t", "typescript"]) == 0
    assert (project.parent / "shipping.py").exists()
    assert (project.parent / "shipping.ts").exists()


def test_generated_python_executes_the_documented_values(project):
    assert main(["compile", "src/shipping.nl"]) == 0
    namespace: dict = {}
    exec((project.parent / "shipping.py").read_text(encoding="utf-8"), namespace)  # noqa: S102
    assert namespace["base_rate"](2) == 7
    assert namespace["shipping_quote"](
        namespace["Parcel"](weight_kg=2, declared_value=100), False
    ).total == 9
    assert namespace["shipping_quote"](
        namespace["Parcel"](weight_kg=2, declared_value=100), True
    ).total == 19.5
    with pytest.raises(ValueError, match="weight cannot be negative"):
        namespace["base_rate"](-1)


def test_tests_run_with_relative_paths(project):
    # Regression: the temp workdir for generated tests must be absolute,
    # or pytest with cwd=tempdir cannot find a relative test path.
    assert main(["test", "src/shipping.nl"]) == 0


def test_ci_gate_passes_after_compile(project):
    assert main(["compile", "src/shipping.nl"]) == 0
    assert main(["ci", "src/shipping.nl", "--compile", "--test"]) == 0


def test_ir_shows_the_documented_structure(project):
    from nlsc.ir import module_to_canonical
    from nlsc.lowering import lower_module
    from nlsc.parser import parse_nl_file

    module = lower_module(
        parse_nl_file(WALKTHROUGH_NL, source_path=str(project))
    )
    canonical = module_to_canonical(module)
    assert "(anlu base-rate" in canonical
    assert "else" in canonical
    assert "(fail ValueError" in canonical
