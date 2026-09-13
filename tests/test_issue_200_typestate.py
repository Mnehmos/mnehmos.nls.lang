"""Issue #200: resource state protocols (`@states` + `<State>` tokens).

Tokens are unforgeable in checked code: the checker tracks each token's
state across transitions, aliases, and branch joins.  Files without
`@states` are unaffected (opt-in).
"""

from __future__ import annotations

import json

from nlsc.cli import main
from nlsc.ir import type_ref_from_text
from nlsc.parser import parse_nl_file

PROTOCOL_HEADER = """@module order_flow
@states Order: Pending, Validated, Charged

[validate-order]
PURPOSE: validate a pending order
INPUTS:
  - order: Order<Pending>
EFFECTS: unknown
RETURNS: Order<Validated>

[charge-order]
PURPOSE: charge a validated order
INPUTS:
  - order: Order<Validated>
EFFECTS: unknown
RETURNS: Order<Charged>
"""

GOOD_FLOW = PROTOCOL_HEADER + """
[good-flow]
PURPOSE: validates then charges
INPUTS:
  - order: Order<Pending>
EFFECTS: unknown
LOGIC:
  1. validated = [validate-order](order)
  2. charged = [charge-order](validated)
RETURNS: Order<Charged>
DEPENDS: [validate-order], [charge-order]
"""

BAD_STATE = PROTOCOL_HEADER + """
[bad-flow]
PURPOSE: charges without validating
INPUTS:
  - order: Order<Pending>
EFFECTS: unknown
LOGIC:
  1. charged = [charge-order](order)
RETURNS: Order<Charged>
DEPENDS: [charge-order]
"""

CONSUMED_REUSE = PROTOCOL_HEADER + """
[reuse]
PURPOSE: reuses a consumed token
INPUTS:
  - order: Order<Pending>
EFFECTS: unknown
LOGIC:
  1. validated = [validate-order](order)
  2. again = [validate-order](order)
RETURNS: Order<Validated>
DEPENDS: [validate-order]
"""

ALIASED_REUSE = PROTOCOL_HEADER + """
[aliased]
PURPOSE: consumes through an alias
INPUTS:
  - order: Order<Pending>
EFFECTS: unknown
LOGIC:
  1. copy = order
  2. validated = [validate-order](order)
  3. again = [validate-order](copy)
RETURNS: Order<Validated>
DEPENDS: [validate-order]
"""

UNDECLARED_STATE = PROTOCOL_HEADER + """
[bad-state]
PURPOSE: undeclared state
INPUTS:
  - order: Order<Refunded>
EFFECTS: unknown
RETURNS: Order<Validated>
"""

UNLABELED_PARAM = PROTOCOL_HEADER + """
[no-token]
PURPOSE: unlabeled protocol parameter
INPUTS:
  - order: Order
EFFECTS: unknown
RETURNS: Order<Validated>
"""

UNLABELED_RESULT = PROTOCOL_HEADER + """
[no-result-state]
PURPOSE: transition without a result state
INPUTS:
  - order: Order<Pending>
EFFECTS: unknown
RETURNS: Order
"""

AMBIGUOUS_JOIN = PROTOCOL_HEADER + """
[hold-order]
PURPOSE: keep pending
INPUTS:
  - order: Order<Pending>
EFFECTS: unknown
RETURNS: Order<Pending>

[ambiguous]
PURPOSE: one arm transitions, one does not
INPUTS:
  - order: Order<Pending>
  - flag: boolean
EFFECTS: unknown
LOGIC:
  1. IF flag THEN [validate-order](order) -> current ELSE [hold-order](order) -> current
  2. charged = [charge-order](current)
RETURNS: Order<Charged>
DEPENDS: [validate-order], [hold-order], [charge-order]
"""

SAME_STATE_JOIN = PROTOCOL_HEADER + """
[both-transition]
PURPOSE: both arms validate
INPUTS:
  - order: Order<Pending>
  - flag: boolean
EFFECTS: unknown
LOGIC:
  1. IF flag THEN [validate-order](order) -> current ELSE [validate-order](order) -> current
  2. charged = [charge-order](current)
RETURNS: Order<Charged>
DEPENDS: [validate-order], [charge-order]
"""

NO_PROTOCOL = """@module plain
[add]
PURPOSE: add
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
"""


def _write(tmp_path, source: str):
    path = tmp_path / "probe.nl"
    path.write_text(source, encoding="utf-8")
    return path


def _codes(tmp_path, source: str, command=("verify",)) -> list[str]:
    import io
    from contextlib import redirect_stderr

    path = _write(tmp_path, source)
    buffer = io.StringIO()
    with redirect_stderr(buffer):
        main([*command, str(path), "--json"])
    return [line for line in buffer.getvalue().splitlines()]


def _json_diagnostics(tmp_path, capsys, source: str, command: str = "verify"):
    path = _write(tmp_path, source)
    exit_code = main([command, "--json", str(path)])
    payload = json.loads(capsys.readouterr().out)
    return exit_code, [d["code"] for d in payload["diagnostics"]]


# --------------------------------------------------------------------------
# Surface
# --------------------------------------------------------------------------


def test_states_directive_parses():
    nl_file = parse_nl_file(PROTOCOL_HEADER, source_path="p.nl")
    assert nl_file.module.states == {
        "Order": ("Pending", "Validated", "Charged"),
    }


def test_protocol_type_refs_split_base_and_state():
    type_ref = type_ref_from_text("Order<Pending>")
    assert type_ref.name == "Order"
    assert type_ref.args[0].name == "Pending"


def test_duplicate_state_is_a_parse_error(tmp_path, capsys):
    source = "@module dup\n@states Order: Pending, Pending\n[op]\nPURPOSE: p\nRETURNS: 1\n"
    path = _write(tmp_path, source)
    assert main(["verify", str(path)]) == 1
    assert "Duplicate state" in capsys.readouterr().err


# --------------------------------------------------------------------------
# Transitions
# --------------------------------------------------------------------------


def test_legal_transition_chain_passes(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, GOOD_FLOW)
    assert exit_code == 0
    assert codes == []


def test_wrong_state_is_esem014(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, BAD_STATE)
    assert exit_code == 1
    assert codes == ["ESEM014"]


def test_consumed_token_reuse_is_esem015(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, CONSUMED_REUSE)
    assert exit_code == 1
    assert codes == ["ESEM015"]


def test_aliased_consumption_is_esem015(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, ALIASED_REUSE)
    assert exit_code == 1
    assert codes == ["ESEM015"]


def test_undeclared_state_is_esem016(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, UNDECLARED_STATE)
    assert exit_code == 1
    assert codes == ["ESEM016"]


def test_unlabeled_parameter_is_esem016(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, UNLABELED_PARAM)
    assert exit_code == 1
    assert codes == ["ESEM016"]


def test_transition_without_result_state_is_esem016(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, UNLABELED_RESULT)
    assert exit_code == 1
    assert codes == ["ESEM016"]


def test_ambiguous_branch_join_is_esem017(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, AMBIGUOUS_JOIN)
    assert exit_code == 1
    assert codes == ["ESEM017"]


def test_agreeing_branch_join_passes(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, SAME_STATE_JOIN)
    assert exit_code == 0
    assert codes == []


def test_plain_modules_are_unaffected(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, NO_PROTOCOL)
    assert exit_code == 0
    assert codes == []


def test_compile_rejects_the_violation_in_every_mode(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, BAD_STATE, "compile")
    assert exit_code == 1
    assert codes == ["ESEM014"]


def test_ci_reports_the_violation_after_a_lock_exists(tmp_path, capsys):
    """CI must catch a protocol violation introduced after a clean compile."""
    implemented = PROTOCOL_HEADER + """
[good-flow]
PURPOSE: validates then charges
INPUTS:
  - order: Order<Pending>
EFFECTS: unknown
LOGIC:
  1. validated = [validate-order](order)
  2. charged = [charge-order](validated)
RETURNS: Order<Charged>
DEPENDS: [validate-order], [charge-order]

@literal python {
def validate_order(order):
    return {"state": "Validated"}


def charge_order(order):
    return {"state": "Charged"}
}
"""
    path = _write(tmp_path, implemented)
    assert main(["compile", str(path)]) == 0
    capsys.readouterr()

    path.write_text(BAD_STATE + """
@literal python {
def validate_order(order):
    return {"state": "Validated"}


def charge_order(order):
    return {"state": "Charged"}
}
""", encoding="utf-8")
    exit_code, codes = _json_diagnostics(tmp_path, capsys, BAD_STATE, "ci")
    assert exit_code == 1
    # ESEM014 leads; the fixture's unimplemented anlu adds EIR004 scaffold
    # diagnostics, which ci also rejects.
    assert codes[0] == "ESEM014"


def test_protocol_files_parse_through_the_auto_backend(tmp_path, capsys):
    from nlsc.pipeline import parse_nl_path_auto

    path = _write(tmp_path, GOOD_FLOW)
    parsed = parse_nl_path_auto(path)
    assert parsed.module.states["Order"] == ("Pending", "Validated", "Charged")
    assert parsed.anlus[0].inputs[0].type == "Order<Pending>"


# --------------------------------------------------------------------------
# Review follow-ups: soundness holes the first pass silently accepted
# --------------------------------------------------------------------------

VIOLATION_IN_ARM = PROTOCOL_HEADER + """
[arm-violation]
PURPOSE: violates inside a branch arm
INPUTS:
  - order: Order<Pending>
  - flag: boolean
EFFECTS: unknown
LOGIC:
  1. IF flag THEN [charge-order](order) -> result ELSE [validate-order](order) -> result
RETURNS: Order<Charged>
DEPENDS: [validate-order], [charge-order]
"""

CROSS_PROTOCOL = """@module cross_protocol
@states Order: Pending, Validated
@states Payment: Pending, Validated

[pay]
PURPOSE: pay a pending payment
INPUTS:
  - payment: Payment<Pending>
EFFECTS: unknown
RETURNS: Payment<Validated>

[wrong-resource]
PURPOSE: passes an order token where a payment is required
INPUTS:
  - order: Order<Pending>
EFFECTS: unknown
LOGIC:
  1. paid = [pay](order)
RETURNS: Payment<Validated>
DEPENDS: [pay]
"""

ALIAS_ACROSS_BRANCH = PROTOCOL_HEADER + """
[hold-order]
PURPOSE: keep pending
INPUTS:
  - order: Order<Pending>
EFFECTS: unknown
RETURNS: Order<Pending>

[alias-across-branch]
PURPOSE: consumes one alias in each arm, then reuses the other
INPUTS:
  - order: Order<Pending>
  - flag: boolean
EFFECTS: unknown
LOGIC:
  1. copy = order
  2. IF flag THEN [hold-order](copy) -> current ELSE [hold-order](copy) -> current
  3. again = [hold-order](order)
RETURNS: Order<Pending>
DEPENDS: [hold-order]
"""

NESTED_CALLS = PROTOCOL_HEADER + """
[nested]
PURPOSE: nested transition calls
INPUTS:
  - order: Order<Pending>
EFFECTS: unknown
LOGIC:
  1. charged = [charge-order]([validate-order](order))
  2. again = [charge-order](charged)
RETURNS: Order<Charged>
DEPENDS: [validate-order], [charge-order]
"""

LIST_OF_PROTOCOL = PROTOCOL_HEADER + """
[batch]
PURPOSE: list of protocol tokens
INPUTS:
  - orders: list of Order<Validated>
EFFECTS: unknown
RETURNS: Order<Validated>
"""

FACTORY_FABRICATION = """@module factory
@states Order: Pending, Validated

[make-order]
PURPOSE: fabricates a token out of nothing
INPUTS:
  - name: string
EFFECTS: unknown
RETURNS: Order<Refunded>
"""

MISSPELLED_RESULT_PROTOCOL = """@module misspelled
@states Order: Pending, Validated

[make]
PURPOSE: misspelled protocol on the result
INPUTS:
  - name: string
EFFECTS: unknown
RETURNS: Ordre<Validated>
"""

EMPTY_TOKEN = """@module empty_token
@states Order: Pending, Validated

[make]
PURPOSE: empty token
INPUTS:
  - name: string
EFFECTS: unknown
RETURNS: Order<>
"""

OPTIONAL_TOKEN = """@module optional_token
@states Order: Pending, Validated

[validate-order]
PURPOSE: validate
INPUTS:
  - order: Order<Pending>
EFFECTS: unknown
RETURNS: Order<Validated>

[maybe]
PURPOSE: optional protocol parameter
INPUTS:
  - order: Order<Pending>?
EFFECTS: unknown
LOGIC:
  1. validated = [validate-order](order)
RETURNS: Order<Validated>
DEPENDS: [validate-order]
"""


def test_violation_inside_a_branch_arm_is_reported(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, VIOLATION_IN_ARM)
    assert exit_code == 1
    assert "ESEM014" in codes


def test_cross_protocol_token_is_rejected(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, CROSS_PROTOCOL)
    assert exit_code == 1
    assert codes == ["ESEM014"]


def test_alias_consumption_survives_a_branch(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, ALIAS_ACROSS_BRANCH)
    assert exit_code == 1
    assert "ESEM015" in codes


def test_nested_call_binding_records_the_outer_result(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, NESTED_CALLS)
    assert exit_code == 1
    assert codes == ["ESEM014"]


def test_list_of_protocol_parameter_is_accepted(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, LIST_OF_PROTOCOL)
    assert exit_code == 0
    assert codes == []


def test_factory_fabrication_is_esem016(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, FACTORY_FABRICATION)
    assert exit_code == 1
    assert codes == ["ESEM016"]


def test_misspelled_result_protocol_is_esem016(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, MISSPELLED_RESULT_PROTOCOL)
    assert exit_code == 1
    assert codes == ["ESEM016"]


def test_empty_token_is_esem016(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, EMPTY_TOKEN)
    assert exit_code == 1
    assert codes == ["ESEM016"]


def test_optional_protocol_token_compiles(tmp_path, capsys):
    from nlsc.emitter import emit_python
    from nlsc.parser import parse_nl_file as _parse

    source = OPTIONAL_TOKEN
    code = emit_python(_parse(source, source_path="p.nl"))
    assert "Optional[Order]" in code


def test_duplicate_protocol_declaration_is_a_parse_error(tmp_path, capsys):
    source = (
        "@module dup_protocol\n@states Order: Pending\n@states Order: Other\n"
        "[op]\nPURPOSE: p\nRETURNS: 1\n"
    )
    path = _write(tmp_path, source)
    assert main(["verify", str(path)]) == 1
    assert "already declared" in capsys.readouterr().err


EMPTY_INPUT_TOKEN = """@module empty_input
@states Order: Pending, Validated, Charged

[charge-order]
PURPOSE: charge
INPUTS:
  - order: Order<Validated>
EFFECTS: unknown
RETURNS: Order<Charged>

[bad]
PURPOSE: empty input token bypasses the protocol
INPUTS:
  - order: Order<>
EFFECTS: unknown
LOGIC:
  1. charged = [charge-order](order)
RETURNS: Order<Charged>
DEPENDS: [charge-order]
"""

UNDECLARED_INPUT_PROTOCOL = """@module undeclared_input
@states Order: Pending, Validated

[bad]
PURPOSE: protocol that was never declared
INPUTS:
  - thing: Payment<Pending>
EFFECTS: unknown
RETURNS: Order<Validated>
"""


def test_empty_input_token_is_esem016(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(tmp_path, capsys, EMPTY_INPUT_TOKEN)
    assert exit_code == 1
    assert "ESEM016" in codes


def test_undeclared_input_protocol_is_esem016(tmp_path, capsys):
    exit_code, codes = _json_diagnostics(
        tmp_path, capsys, UNDECLARED_INPUT_PROTOCOL
    )
    assert exit_code == 1
    assert codes == ["ESEM016"]


def test_typescript_protocol_declaration_emits_a_typed_todo():
    from nlsc.emitter_typescript import emit_typescript
    from nlsc.parser import parse_nl_file as _parse

    code = emit_typescript(_parse(PROTOCOL_HEADER, source_path="p.nl"))
    assert "// TODO: implement the transition declared as Order<Validated>" in code
    assert "return undefined as any;" in code
