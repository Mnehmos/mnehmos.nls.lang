"""Issue #201 PR 1: checked Retry and Timeout policies.

Surface + IR + checker only: policies are validated and recorded, but no
emitter produces them yet, so both targets refuse with `ETARGET002`
rather than silently dropping the policy.  Static guarantees are about
the declared policy shape; they say nothing about the provider honoring
the idempotency key.
"""

from __future__ import annotations

import json

import pytest

from nlsc.cli import main
from nlsc.parser import parse_nl_file

BASE = """@module retry_probe
[transfer]
PURPOSE: transfer funds
INPUTS:
  - order_id: string
  - amount: number
  - ledger: list of number
GUARDS:
  - amount > 0 -> NetworkError("amount must be positive")
EFFECTS: unknown
LOGIC:
  1. ledger.append(amount)
  2. receipt = amount
RETURNS: receipt
"""

RETRY_OK = """@module retry_ok
[transfer]
PURPOSE: transfer funds
INPUTS:
  - order_id: string
  - amount: number
  - ledger: list of number
GUARDS:
  - amount > 0 -> NetworkError("amount must be positive")
RETRY:
  - up to 3 attempts on NetworkError
  - idempotency key: order_id
TIMEOUT:
  - after 5000ms -> cancel-and-reconcile
EFFECTS: unknown
LOGIC:
  1. ledger.append(amount)
  2. receipt = amount
RETURNS: receipt
"""

NO_BUDGET = RETRY_OK.replace("  - up to 3 attempts on NetworkError\n", "")
ZERO_BUDGET = RETRY_OK.replace("up to 3 attempts", "up to 0 attempts")
# A fixture whose failure set is fully known (a guard-raised error only),
# so an unprovable retry identity is provably absent.
IDENTITY_BASE = """@module identity_probe
[transfer]
PURPOSE: transfer funds
INPUTS:
  - order_id: string
  - amount: number
GUARDS:
  - amount > 0 -> NetworkError("amount must be positive")
RETRY:
  - up to 3 attempts on TimeoutError
EFFECTS: pure
LOGIC:
  1. receipt = amount
RETURNS: receipt
"""

UNKNOWN_IDENTITY = IDENTITY_BASE
KEY_NOT_PARAM = RETRY_OK.replace(
    "idempotency key: order_id", "idempotency key: receipt"
)
NO_TIMEOUT_OUTCOME = RETRY_OK.replace(
    "  - after 5000ms -> cancel-and-reconcile\n", ""
)
NO_KEY = RETRY_OK.replace("  - idempotency key: order_id\n", "")


def _write(tmp_path, source: str):
    path = tmp_path / "probe.nl"
    path.write_text(source, encoding="utf-8")
    return path


def _diagnostics(tmp_path, capsys, source: str, command: str = "verify"):
    path = _write(tmp_path, source)
    exit_code = main([command, "--json", str(path)])
    payload = json.loads(capsys.readouterr().out)
    return exit_code, [d["code"] for d in payload["diagnostics"]]


# --------------------------------------------------------------------------
# Surface and IR
# --------------------------------------------------------------------------


def test_policy_sections_parse():
    anlu = parse_nl_file(RETRY_OK, source_path="p.nl").anlus[0]
    assert anlu.retry is not None
    assert anlu.retry.attempts == 3
    assert anlu.retry.error_types == ["NetworkError"]
    assert anlu.retry.idempotency_key == "order_id"
    assert anlu.timeout is not None
    assert anlu.timeout.after_ms == 5000
    assert anlu.timeout.outcome == "cancel-and-reconcile"


def test_policy_parses_through_the_auto_backend(tmp_path):
    from nlsc.pipeline import parse_nl_path_auto

    path = _write(tmp_path, RETRY_OK)
    parsed = parse_nl_path_auto(path)
    assert parsed.anlus[0].retry is not None
    assert parsed.anlus[0].timeout is not None


def test_invalid_retry_bullet_is_a_parse_error(tmp_path, capsys):
    source = RETRY_OK.replace(
        "  - idempotency key: order_id", "  - key is order_id"
    )
    path = _write(tmp_path, source)
    assert main(["verify", str(path)]) == 1
    assert "Invalid RETRY bullet" in capsys.readouterr().err


def test_policies_render_in_canonical_ir(tmp_path, capsys):
    path = _write(tmp_path, RETRY_OK)
    assert main(["ir", str(path)]) == 0
    out = capsys.readouterr().out
    assert "(retry attempts=3 on=NetworkError key=order_id)" in out
    assert "(timeout after=5000ms outcome=cancel-and-reconcile)" in out


# --------------------------------------------------------------------------
# Checker
# --------------------------------------------------------------------------


def test_valid_policy_passes_the_gate(tmp_path, capsys):
    exit_code, codes = _diagnostics(tmp_path, capsys, RETRY_OK)
    assert exit_code == 0
    assert codes == []


def test_missing_budget_is_esem018(tmp_path, capsys):
    exit_code, codes = _diagnostics(tmp_path, capsys, NO_BUDGET)
    assert exit_code == 1
    assert "ESEM018" in codes


def test_zero_budget_is_esem018(tmp_path, capsys):
    exit_code, codes = _diagnostics(tmp_path, capsys, ZERO_BUDGET)
    assert exit_code == 1
    assert "ESEM018" in codes


def test_unproven_error_identity_is_esem019(tmp_path, capsys):
    exit_code, codes = _diagnostics(tmp_path, capsys, UNKNOWN_IDENTITY)
    assert exit_code == 1
    assert "ESEM019" in codes


def test_effectful_retry_without_key_is_esem020(tmp_path, capsys):
    exit_code, codes = _diagnostics(tmp_path, capsys, NO_KEY)
    assert exit_code == 1
    assert "ESEM020" in codes


def test_key_that_is_not_a_parameter_is_esem020(tmp_path, capsys):
    exit_code, codes = _diagnostics(tmp_path, capsys, KEY_NOT_PARAM)
    assert exit_code == 1
    assert "ESEM020" in codes


def test_timeout_without_outcome_is_esem021(tmp_path, capsys):
    exit_code, codes = _diagnostics(tmp_path, capsys, NO_TIMEOUT_OUTCOME)
    assert exit_code == 1
    assert "ESEM021" in codes


def test_files_without_policies_are_unaffected(tmp_path, capsys):
    exit_code, codes = _diagnostics(tmp_path, capsys, BASE)
    assert exit_code == 0
    assert codes == []


# --------------------------------------------------------------------------
# Emission refusal
# --------------------------------------------------------------------------


@pytest.mark.parametrize("target", ["python", "typescript"])
def test_both_targets_refuse_policies_explicitly(tmp_path, capsys, target):
    path = _write(tmp_path, RETRY_OK)
    exit_code = main(["compile", str(path), "-t", target])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "ETARGET002" in captured.err
    assert "RETRY/TIMEOUT control policies" in captured.err
    suffix = ".py" if target == "python" else ".ts"
    assert not path.with_suffix(suffix).exists()


# --------------------------------------------------------------------------
# Review follow-ups
# --------------------------------------------------------------------------

DEADLINE_ONLY = RETRY_OK.replace(
    "  - after 5000ms -> cancel-and-reconcile", "  - after 5000ms"
)


def test_deadline_without_outcome_is_esem021(tmp_path, capsys):
    exit_code, codes = _diagnostics(tmp_path, capsys, DEADLINE_ONLY)
    assert exit_code == 1
    assert "ESEM021" in codes


def test_bullet_style_variants_parse(tmp_path, capsys):
    source = RETRY_OK.replace("  - ", "  * ").replace(
        "  * idempotency key", "  • idempotency key"
    )
    exit_code, codes = _diagnostics(tmp_path, capsys, source)
    assert exit_code == 0
    assert codes == []


def test_duplicate_policy_section_is_a_parse_error(tmp_path, capsys):
    source = RETRY_OK.replace(
        "  - idempotency key: order_id",
        "  - idempotency key: order_id\nRETRY:\n  - up to 2 attempts",
    )
    path = _write(tmp_path, source)
    assert main(["verify", str(path)]) == 1
    assert "Duplicate RETRY section" in capsys.readouterr().err


def test_inline_policy_header_is_a_parse_error(tmp_path, capsys):
    source = RETRY_OK.replace(
        "RETRY:\n  - up to 3 attempts on NetworkError",
        "RETRY: up to 3 attempts on NetworkError",
    )
    path = _write(tmp_path, source)
    assert main(["verify", str(path)]) == 1
    assert "own lines" in capsys.readouterr().err


@pytest.mark.parametrize("command", ["run", "test"])
def test_run_and_test_refuse_policies_too(tmp_path, capsys, command):
    """The python-only run/test paths must not silently drop policies."""
    path = _write(tmp_path, RETRY_OK)
    exit_code = main([command, str(path)])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "ETARGET002" in captured.err


def test_hint_says_no_target_emits_the_feature_yet(tmp_path, capsys):
    path = _write(tmp_path, RETRY_OK)
    assert main(["compile", str(path)]) == 1
    err = capsys.readouterr().err
    assert "no target emits it yet" in err


def test_unknown_failure_sets_accept_the_authors_classification(tmp_path, capsys):
    """The valid fixture has unknown failures (a method call) and is accepted."""
    exit_code, codes = _diagnostics(tmp_path, capsys, RETRY_OK)
    assert exit_code == 0
    assert codes == []
