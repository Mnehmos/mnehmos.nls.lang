"""Issue #202 slice: the Python emitter renders checked bodies from IR.

An ANLU whose content lowered fully to the structural IR is emitted from
its IR statement and expression nodes — the same structure the checkers
validated — instead of being re-parsed from LOGIC prose.  Anything foreign
falls back to the legacy prose path, so scaffold output is unchanged.
"""

from __future__ import annotations

from nlsc.emitter import emit_python
from nlsc.parser import parse_nl_file

CHECKED_BODY = """@module ir_body
[adjust]
PURPOSE: adjust a score
INPUTS:
  - score: number
GUARDS:
  - score >= 0 -> ValueError(NEGATIVE, "score must not be negative")
LOGIC:
  1. bonus = 10
  2. IF score > 100 THEN capped = 100 ELSE capped = score
  3. total = capped + bonus
  4. total += 1
RETURNS: total
"""

FOREIGN_STEP = """@module foreign_step
[price]
PURPOSE: price an order
INPUTS:
  - amount: number
LOGIC:
  1. total = amount
  2. total = apply the discount policy to total
RETURNS: total
"""

LOOP_STEP = """@module loop_step
[total-all]
PURPOSE: sum every value
INPUTS:
  - items: list of number
LOGIC:
  1. total = 0
  2. FOR each item IN items: total = total + item
RETURNS: total
"""

TYPE_WORD_RETURN = """@module type_word
[empty-list]
PURPOSE: an empty list of numbers
RETURNS: 数値のリスト
"""

RECORD_RETURN = """@module record_return
@type Account
  - owner: string
  - balance: number

[rebuild]
PURPOSE: rebuild an account
INPUTS:
  - owner: string
  - balance: number
LOGIC:
  1. account = Account(owner=owner, balance=balance)
RETURNS: account
"""


def _emit(source: str) -> str:
    return emit_python(parse_nl_file(source, source_path="probe.nl"))


def test_checked_body_renders_guards_bindings_and_branches_from_ir():
    code = _emit(CHECKED_BODY)
    assert "    if not (score >= 0):" in code
    assert "        __nls_error.code = 'NEGATIVE'" in code
    assert "    bonus = 10" in code
    assert "    if score > 100:" in code
    assert "    else:" in code
    assert "        capped = score" in code
    assert "    total += 1" in code
    assert "    return total" in code
    # No legacy placeholder leaked into a checked body.
    assert "TODO" not in code


def test_foreign_step_falls_back_to_legacy_placeholder():
    code = _emit(FOREIGN_STEP)
    # The prose re-binding is foreign (EIR002 scaffold), so the legacy path
    # keeps it visible as a comment instead of reinterpreting it.
    assert "# total = apply the discount policy to total" in code
    assert "    total = amount" in code
    assert "    return total" in code


def test_loop_step_still_emits_a_real_python_loop():
    code = _emit(LOOP_STEP)
    assert "    for item in items:" in code
    assert "        total = total + item" in code
    assert "# FOR each" not in code


def test_type_word_return_keeps_legacy_default():
    code = _emit(TYPE_WORD_RETURN)
    assert "    return []" in code


def test_record_kwargs_render_canonically():
    code = _emit(RECORD_RETURN)
    assert "account = Account(owner=owner, balance=balance)" in code


def test_ir_emitted_output_is_valid_python():
    import ast

    for source in (CHECKED_BODY, FOREIGN_STEP, LOOP_STEP, RECORD_RETURN):
        ast.parse(_emit(source))
