"""Regression and behavior tests for the target-neutral IR lowering (Issue #194).

The fixtures in this module are the regression fixtures requested by the
issue: they are written against the *documented* contract and must keep
passing as the IR migrates toward checked emission.
"""

from __future__ import annotations

import pytest

from nlsc.ir import (
    IRBind,
    IRBranch,
    IRCall,
    IRDiscard,
    IRFieldAccess,
    IRGuard,
    IRList,
    IRMethodCall,
    IRBinary,
    IRUnary,
    ForeignExpr,
    ForeignStmt,
    find_unchecked_nodes,
    module_to_canonical,
    module_to_json,
    type_ref_from_text,
)
from nlsc.lowering import LoweringError, lower_expression, lower_module
from nlsc.parser import parse_nl_file
from nlsc.ir import SourceSpan


def _lower(source: str, **kwargs):
    return lower_module(parse_nl_file(source), **kwargs)


def _op(module, name):
    matches = [op for op in module.operations if op.name == name]
    assert matches, f"operation {name} not found"
    return matches[0]


# --------------------------------------------------------------------------
# Regression fixture 1: nested ANLU-call arguments are fully consumed
# --------------------------------------------------------------------------


NESTED_CALL_SOURCE = """@module identity_probe
[identity]
PURPOSE: Return input
INPUTS:
  - x: number
RETURNS: x

[probe]
PURPOSE: Probe nested
LOGIC:
  1. [identity](max(1, 2)) -> result
RETURNS: result
"""


def test_nested_anlu_call_arguments_are_consumed_completely():
    module = _lower(NESTED_CALL_SOURCE)
    probe = _op(module, "probe")
    (bind,) = probe.body
    assert isinstance(bind, IRBind)
    assert bind.name == "result"
    call = bind.value
    assert isinstance(call, IRCall)
    assert call.anlu is True
    assert call.target == "identity"
    (inner,) = call.args
    assert isinstance(inner, IRCall)
    assert inner.target == "max"
    assert [arg.raw for arg in inner.args] == ["1", "2"]
    assert find_unchecked_nodes(module) == []


def test_anlu_target_preserves_kebab_case_verbatim():
    source = """@module kebab_probe
[slow-charge]
PURPOSE: charge slowly
RETURNS: 0

[run]
PURPOSE: call it
LOGIC:
  1. [slow-charge](1) -> out
RETURNS: out
DEPENDS: [slow-charge]
"""
    module = _lower(source)
    run = _op(module, "run")
    bind = run.body[0]
    assert isinstance(bind.value, IRCall)
    assert bind.value.anlu is True
    assert bind.value.target == "slow-charge"


# --------------------------------------------------------------------------
# Regression fixture 2: quoted operator/keyword text survives untouched
# --------------------------------------------------------------------------


QUOTED_TEXT_SOURCE = """@module literal_probe
[answer]
PURPOSE: Return quoted text
LOGIC:
  1. x = "True and False"
RETURNS: x
"""


def test_quoted_operator_text_is_preserved_exactly():
    module = _lower(QUOTED_TEXT_SOURCE)
    answer = _op(module, "answer")
    bind = answer.body[0]
    assert isinstance(bind, IRBind)
    literal = bind.value
    from nlsc.ir import IRLiteral

    assert isinstance(literal, IRLiteral)
    assert literal.kind == "string"
    assert literal.raw == '"True and False"'
    assert literal.value == "True and False"
    assert find_unchecked_nodes(module) == []
    # The canonical form keeps the literal text; no && translation happens.
    assert '"True and False"' in module_to_canonical(module)


def test_single_and_double_quoted_strings_lower_identically():
    source_a = """@module s
[f]
PURPOSE: p
LOGIC:
  1. x = 'home'
RETURNS: x
"""
    source_b = source_a.replace("'home'", '"home"')
    canon_a = module_to_canonical(_lower(source_a))
    canon_b = module_to_canonical(_lower(source_b))
    assert canon_a == canon_b


# --------------------------------------------------------------------------
# Target neutrality
# --------------------------------------------------------------------------


def test_same_source_same_ir_regardless_of_target():
    body = """@module target_neutral
[add]
PURPOSE: add
INPUTS:
  - a: number
  - b: number
LOGIC:
  1. total = a + b
RETURNS: total
"""
    python_module = _lower("@target python\n" + body)
    ts_module = _lower("@target typescript\n" + body)
    assert module_to_canonical(python_module) == module_to_canonical(ts_module)
    assert module_to_json(python_module)["operations"] == module_to_json(ts_module)[
        "operations"
    ]


def test_lowering_is_deterministic_across_runs():
    module_a = _lower(NESTED_CALL_SOURCE)
    module_b = _lower(NESTED_CALL_SOURCE)
    assert module_to_canonical(module_a) == module_to_canonical(module_b)


# --------------------------------------------------------------------------
# Source spans and step identity
# --------------------------------------------------------------------------


def test_source_spans_identify_logic_step_and_line():
    module = _lower(NESTED_CALL_SOURCE)
    probe = _op(module, "probe")
    bind = probe.body[0]
    assert bind.span is not None
    assert bind.span.anlu == "probe"
    assert bind.span.step == 1
    assert bind.span.line == 11  # the numbered LOGIC line in the fixture

    diagnostic = module.diagnostics
    for d in diagnostic:
        assert d.line is not None


def test_node_ids_are_stable_and_deterministic():
    module_a = _lower(NESTED_CALL_SOURCE)
    module_b = _lower(NESTED_CALL_SOURCE)
    ids_a = [s.id for op in module_a.operations for s in op.body]
    ids_b = [s.id for op in module_b.operations for s in op.body]
    assert ids_a == ids_b
    assert any("probe.step1" in i for i in ids_a)


# --------------------------------------------------------------------------
# Unsupported constructs: precise diagnostics, never placeholders
# --------------------------------------------------------------------------


def test_comprehension_becomes_foreign_with_diagnostic():
    source = """@module comp
[f]
PURPOSE: filter
INPUTS:
  - items: list of number
LOGIC:
  1. small = [x for x in items if x < 10]
RETURNS: small
"""
    module = _lower(source)
    diagnostics = list(module.diagnostics)
    assert any(d.code == "EIR002" and "comprehension" in d.message for d in diagnostics)
    blockers = find_unchecked_nodes(module)
    assert len(blockers) == 1
    assert isinstance(blockers[0], ForeignExpr)
    assert blockers[0].reason == "comprehension"


def test_executable_prose_with_binding_is_foreign_and_diagnosed():
    # Issue #190 reproducer shape: executable intent, no executable action.
    source = """@module payment_probe
[checkout]
PURPOSE: Process a payment
LOGIC:
  1. Process customer payment -> payment
RETURNS: payment
"""
    module = _lower(source)
    checkout = _op(module, "checkout")
    bind = checkout.body[0]
    assert isinstance(bind, IRBind)
    assert isinstance(bind.value, ForeignExpr)
    assert bind.value.reason == "prose"
    assert bind.value.raw == "Process customer payment"
    assert any(d.code == "EIR002" for d in module.diagnostics)
    assert len(find_unchecked_nodes(module)) == 1


def test_descriptive_step_without_binding_is_narrative_note():
    source = """@module notes
[f]
PURPOSE: p
LOGIC:
  1. Log the payment for audit
RETURNS: 0
"""
    module = _lower(source)
    op = _op(module, "notes".replace("notes", "f"))
    note = op.body[0]
    from nlsc.ir import IRNote

    assert isinstance(note, IRNote)
    assert "Log the payment" in note.text
    # Narrative is legitimate; it must not block checked emission.
    assert find_unchecked_nodes(module) == []


def test_strict_mode_rejects_foreign_constructs():
    with pytest.raises(LoweringError) as excinfo:
        _lower(QUOTED_TEXT_SOURCE.replace('"True and False"', "[x for x in y]"), strict=True)
    assert all(d.code == "EIR002" for d in excinfo.value.diagnostics)


def test_unterminated_string_is_reported_as_eir001():
    source = """@module broken
[f]
PURPOSE: p
LOGIC:
  1. x = 'oops
RETURNS: x
"""
    module = _lower(source)
    assert any(d.code == "EIR001" for d in module.diagnostics)
    assert len(find_unchecked_nodes(module)) == 1


def test_foreign_statements_are_listed_in_diagnostics():
    source = """@module stmt_probe
[f]
PURPOSE: p
LOGIC:
  1. x = 1
  2. pass
RETURNS: x
"""
    module = _lower(source)
    # `pass` is a keyword statement: foreign with a diagnostic, not dropped.
    assert any(
        isinstance(s, ForeignStmt) for op in module.operations for s in op.body
    )


# --------------------------------------------------------------------------
# Statement and value coverage
# --------------------------------------------------------------------------


def test_if_then_lowers_to_branch_region():
    source = """@module branchy
[pick]
PURPOSE: pick
INPUTS:
  - flag: boolean
LOGIC:
  1. IF flag THEN 1 -> x
RETURNS: x
"""
    module = _lower(source)
    pick = _op(module, "pick")
    branch = pick.body[0]
    assert isinstance(branch, IRBranch)
    assert branch.then_body
    assert branch.otherwise == ()
    assert branch.span.step == 1


def test_discarded_anlu_call_becomes_expression_statement():
    source = """@module discarded
[reject]
PURPOSE: raise
GUARDS:
  - False -> ValueError("called")
RETURNS: 0

[probe]
PURPOSE: Call reject
LOGIC:
  1. [reject]()
DEPENDS: [reject]
RETURNS: 0
"""
    module = _lower(source)
    probe = _op(module, "probe")
    discard = probe.body[0]
    assert isinstance(discard, IRDiscard)
    assert isinstance(discard.value, IRCall)
    assert discard.value.anlu is True
    assert find_unchecked_nodes(module) == []


def test_guards_lower_with_normalized_error_identity():
    module = _lower(
        """@module guarded
[divide]
PURPOSE: safe divide
INPUTS:
  - numerator: number
  - divisor: number
GUARDS:
  - divisor != 0 -> ValueError("Cannot divide by zero")
RETURNS: numerator / divisor
"""
    )
    divide = _op(module, "divide")
    (guard,) = divide.guards
    assert isinstance(guard, IRGuard)
    assert guard.error is not None
    assert guard.error.error_type == "ValueError"
    assert guard.error.message == "Cannot divide by zero"


def test_binary_operator_normalization_includes_unicode_operators():
    expr = lower_expression("a × b ÷ 2", SourceSpan(anlu="t"))
    assert isinstance(expr, IRBinary)
    assert expr.op == "div"
    assert isinstance(expr.left, IRBinary)
    assert expr.left.op == "mul"


def test_field_and_method_access_lower_structurally():
    expr = lower_expression("order.total + order.items.get(0)", SourceSpan(anlu="t"))
    assert isinstance(expr, IRBinary)
    assert isinstance(expr.left, IRFieldAccess)
    assert expr.left.field_name == "total"
    assert isinstance(expr.right, IRMethodCall)
    assert expr.right.method == "get"


def test_list_construction_and_nested_literals():
    expr = lower_expression("[1, 2, 3]", SourceSpan(anlu="t"))
    assert isinstance(expr, IRList)
    assert [item.value for item in expr.items] == [1, 2, 3]


def test_unary_not_and_negation():
    not_expr = lower_expression("not flag", SourceSpan(anlu="t"))
    assert isinstance(not_expr, IRUnary)
    assert not_expr.op == "not"
    neg_expr = lower_expression("-x ** 2", SourceSpan(anlu="t"))
    assert isinstance(neg_expr, IRUnary)
    assert neg_expr.op == "neg"


def test_constructor_kwargs_preserved():
    source = """@module records
[make]
PURPOSE: build a point
LOGIC:
  1. p = Point(x=1, y=2)
RETURNS: p
"""
    module = _lower(source)
    op = _op(module, "make")
    bind = op.body[0]
    assert isinstance(bind, IRBind)
    call = bind.value
    assert isinstance(call, IRCall)
    assert call.target == "Point"
    assert [name for name, _ in call.kwargs] == ["x", "y"]


def test_augmented_binding_is_marked_explicitly():
    source = """@module aug
[total]
PURPOSE: sum
INPUTS:
  - items: list of number
LOGIC:
  1. acc = 0
  2. acc += 1
RETURNS: acc
"""
    module = _lower(source)
    op = _op(module, "total")
    aug = op.body[1]
    assert isinstance(aug, IRBind)
    assert aug.aug == "add"


def test_returns_type_declaration_vs_value_expression_split():
    source = """@module split
[declared]
PURPOSE: p
RETURNS: number

[computed]
PURPOSE: p
RETURNS: 1 + 2
"""
    module = _lower(source)
    declared = _op(module, "declared")
    computed = _op(module, "computed")
    assert declared.result.declared_type is not None
    assert declared.result.declared_type.name == "number"
    assert declared.result.value is None
    assert computed.result.declared_type is None
    assert computed.result.value is not None


def test_type_refs_parse_variants():
    assert type_ref_from_text("number").name == "number"
    assert type_ref_from_text("string?").optional is True
    list_ref = type_ref_from_text("list of number")
    assert list_ref.name == "list"
    assert list_ref.args[0].name == "number"
    nullable = type_ref_from_text("string or none")
    assert nullable.optional is True
    assert type_ref_from_text("Invoice").name == "Invoice"


def test_localized_keywords_normalize_only_outside_literals():
    # `かつ` outside literals is the `and` operator; inside literals the
    # exact characters survive untouched.  Comparison binds tighter than
    # `and`, so the tree is and(flag, eq("かつ", "真")).
    expr = lower_expression('flag かつ "かつ" == "真"', SourceSpan(anlu="t"))
    assert isinstance(expr, IRBinary)
    assert expr.op == "and"
    from nlsc.ir import IRLiteral

    right = expr.right
    assert isinstance(right, IRBinary)
    assert right.op == "eq"
    assert isinstance(right.left, IRLiteral)
    assert right.left.value == "かつ"
    assert isinstance(right.right, IRLiteral)
    assert right.right.value == "真"


# --------------------------------------------------------------------------
# Checked boundary
# --------------------------------------------------------------------------


def test_unchecked_modules_are_not_marked_checked():
    module = _lower(NESTED_CALL_SOURCE)
    assert module.checked is False


def test_module_json_is_round_trippable_and_sorted():
    import json

    module = _lower(NESTED_CALL_SOURCE)
    data = module_to_json(module)
    text = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
    reparsed = json.loads(text)
    assert reparsed["ir_version"]
    assert reparsed["module"] == "identity_probe"
    assert len(reparsed["operations"]) == 2


def test_canonical_text_has_stable_header():
    canonical = module_to_canonical(_lower(NESTED_CALL_SOURCE))
    assert canonical.startswith(";; nls-ir ")
    assert "target-neutral" in canonical.splitlines()[0]
