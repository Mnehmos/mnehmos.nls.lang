"""Issue #202 slice: the TypeScript emitter renders checked bodies from IR.

Mirror of the Python slice: an ANLU whose content lowered fully to the
structural IR is emitted from its IR statement and expression nodes; any
foreign node falls back to the legacy prose path byte-for-byte.
"""

from __future__ import annotations

from nlsc.emitter_typescript import emit_typescript
from nlsc.parser import parse_nl_file

CHECKED_BODY = """@module ts_ir_body
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
RETURNS: total
"""

JOINED_BINDING = """@module ts_join
[pick]
PURPOSE: pick a value
INPUTS:
  - flag: boolean
  - n: number
LOGIC:
  1. IF flag THEN n + 1 -> value ELSE n - 1 -> value
RETURNS: value
"""

FOREIGN_STEP = """@module ts_foreign
[price]
PURPOSE: price an order
INPUTS:
  - amount: number
LOGIC:
  1. total = amount
  2. total = apply the discount policy to total
RETURNS: total
"""

LIST_CONCAT = """@module ts_lists
[combine]
PURPOSE: combine two lists
INPUTS:
  - items: list of number
  - extra: list of number
RETURNS: items + extra
"""


def _emit(source: str) -> str:
    return emit_typescript(parse_nl_file(source, source_path="probe.nl"))


def test_checked_body_renders_guards_bindings_and_branches_from_ir():
    code = _emit(CHECKED_BODY)
    assert "  if (!__nls_truthy(score >= 0)) {" in code
    assert (
        '    throw new ValueError("score must not be negative", "NEGATIVE");'
        in code
    )
    assert "  const bonus = 10;" in code
    # A value assigned in both branch arms is hoisted so it survives the
    # block scope and can be read after the branch.
    assert "  let capped;" in code
    assert "    capped = 100;" in code
    assert "    capped = score;" in code
    assert "  const total = capped + bonus;" in code
    assert "  return total;" in code


def test_branch_joined_output_binding_hoists():
    code = _emit(JOINED_BINDING)
    assert "  let value;" in code
    assert "    value = n + 1;" in code
    assert "    value = n - 1;" in code
    assert "  return value;" in code


def test_foreign_step_falls_back_to_legacy_path():
    code = _emit(FOREIGN_STEP)
    # The prose re-binding is foreign (EIR002 scaffold) and the legacy
    # fallback renders it verbatim; the gate flags it, so it is never
    # silent — the IR path just refuses to participate.
    assert "  let total = amount;" in code
    assert "  total = apply the discount policy to total;" in code


def test_list_addition_matches_legacy_return_rendering():
    code = _emit(LIST_CONCAT)
    # Return-type inference reads `+` as numeric, so both the legacy and IR
    # paths render plain addition here; the IR path introduces no new
    # interpretation of its own.
    assert "  return items + extra;" in code


def test_ir_emitted_module_typechecks_strict():
    from tests.semantic.runners import require_typescript_runner

    runner = require_typescript_runner()
    code = runner.compile(CHECKED_BODY + "\n" + JOINED_BINDING.split("@module", 1)[1])
    ok, diagnostics = runner.strict_check(code)
    assert ok, diagnostics
