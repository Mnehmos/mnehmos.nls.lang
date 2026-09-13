"""Issue #267: bounded iteration in the checked core.

Without iteration, every aggregation in the corpus is a hand-rolled recursive
walker threading an optional cursor — the least reviewable construct available,
handed to the non-expert reader NLS exists to serve.

The checked form is a bounded fold over a finite collection with an explicit
accumulating verb:

    FOR EACH <var> IN <iterable> [WHERE <cond>]: ADD <expr>     -> <binding>
    FOR EACH <var> IN <iterable> [WHERE <cond>]: COLLECT <expr> -> <binding>

`ADD` starts from 0 and sums; `COLLECT` starts from [] and appends. Both are
total and bounded, both lower to a checked IR region, and both emit on Python
and TypeScript. Unbounded `WHILE` is deliberately excluded from the core.
"""

from __future__ import annotations

from nlsc.cli import main
from nlsc.emitter import emit_python
from nlsc.emitter_typescript import emit_typescript
from nlsc.ir import IRForEach, iter_stmt_nodes
from nlsc.lowering import lower_module
from nlsc.parser import parse_nl_file

SUM_MODULE = """@module fold_sum
@target python

[total-of]
PURPOSE: Total every number in a list
INPUTS:
  - values: list of number
LOGIC:
  1. FOR EACH value IN values: ADD value -> total
RETURNS: total

@test [total-of] {
  total_of([]) == 0
  total_of([1, 2, 3]) == 6
}
"""

FILTERED_MODULE = """@module fold_filter
@target python

[total-of-large]
PURPOSE: Total only the numbers above a threshold
INPUTS:
  - values:    list of number
  - threshold: number
LOGIC:
  1. FOR EACH value IN values WHERE value > threshold: ADD value -> total
RETURNS: total

@test [total-of-large] {
  total_of_large([1, 5, 10], 4) == 15
  total_of_large([1, 2], 10) == 0
}
"""

COLLECT_MODULE = """@module fold_collect
@target python

[below]
PURPOSE: Keep the items under a pivot
INPUTS:
  - items: list of number
  - pivot: number
LOGIC:
  1. FOR EACH item IN items WHERE item < pivot: COLLECT item -> lesser
RETURNS: lesser

@test [below] {
  below([3, 1, 4], 3) == [1]
  below([], 3) == []
}
"""


def _write(tmp_path, source: str, name: str):
    path = tmp_path / name
    path.write_text(source, encoding="utf-8")
    return path


def _folds(module):
    found = []
    for operation in module.operations:
        for stmt in iter_stmt_nodes(operation.body):
            if isinstance(stmt, IRForEach):
                found.append(stmt)
    return found


# --------------------------------------------------------------------------
# Lowering: the construct is checked, not foreign
# --------------------------------------------------------------------------


def test_sum_fold_lowers_to_a_checked_region():
    module = lower_module(parse_nl_file(SUM_MODULE), strict=True)
    folds = _folds(module)
    assert len(folds) == 1
    fold = folds[0]
    assert fold.var == "value"
    assert fold.op == "add"
    assert fold.target == "total"
    assert fold.where is None


def test_filtered_fold_carries_its_condition():
    module = lower_module(parse_nl_file(FILTERED_MODULE), strict=True)
    fold = _folds(module)[0]
    assert fold.where is not None
    assert "threshold" in fold.where.render()


def test_collect_fold_lowers_with_its_verb():
    module = lower_module(parse_nl_file(COLLECT_MODULE), strict=True)
    fold = _folds(module)[0]
    assert fold.op == "collect"
    assert fold.target == "lesser"


def test_fold_renders_and_serialises():
    module = lower_module(parse_nl_file(FILTERED_MODULE), strict=True)
    fold = _folds(module)[0]
    text = fold.render()
    assert "for-each" in text
    payload = fold.to_json()
    assert payload["kind"] == "for-each"
    assert payload["op"] == "add"
    assert payload["var"] == "value"
    assert payload["target"] == "total"
    assert payload["where"] is not None


# --------------------------------------------------------------------------
# Strict compilation and execution
# --------------------------------------------------------------------------


def test_strict_compile_accepts_the_fold(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path, SUM_MODULE, "fold_sum.nl")
    code = main(["compile", "--strict", str(path)])
    captured = capsys.readouterr()
    assert code == 0, captured.err
    assert (tmp_path / "fold_sum.py").exists()
    assert not (tmp_path / "fold_sum.draft.py").exists()


def test_python_emission_executes(tmp_path):
    namespace: dict = {}
    exec(emit_python(parse_nl_file(SUM_MODULE)), namespace)
    assert namespace["total_of"]([]) == 0
    assert namespace["total_of"]([1, 2, 3]) == 6


def test_filtered_python_emission_executes():
    namespace: dict = {}
    exec(emit_python(parse_nl_file(FILTERED_MODULE)), namespace)
    assert namespace["total_of_large"]([1, 5, 10], 4) == 15
    assert namespace["total_of_large"]([1, 2], 10) == 0


def test_collect_python_emission_executes():
    namespace: dict = {}
    exec(emit_python(parse_nl_file(COLLECT_MODULE)), namespace)
    assert namespace["below"]([3, 1, 4], 3) == [1]
    assert namespace["below"]([], 3) == []


def test_embedded_tests_pass_through_the_cli(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for source, name in (
        (SUM_MODULE, "fold_sum.nl"),
        (FILTERED_MODULE, "fold_filter.nl"),
        (COLLECT_MODULE, "fold_collect.nl"),
    ):
        path = _write(tmp_path, source, name)
        assert main(["test", str(path)]) == 0, capsys.readouterr().out


# --------------------------------------------------------------------------
# The fold is not Python-only
# --------------------------------------------------------------------------


def test_typescript_emission_contains_a_real_loop():
    source = SUM_MODULE.replace("@target python", "@target typescript")
    code = emit_typescript(parse_nl_file(source))
    assert "for (const value of" in code
    assert "total" in code


def test_typescript_fold_executes():
    """Cross-target: the fold produces the same values on the TypeScript backend."""
    from tests.semantic.runners import require_typescript_runner

    runner = require_typescript_runner()

    summed = runner.compile_and_execute(SUM_MODULE, "total_of", ([1, 2, 3],))
    assert summed.success, summed.exception_message
    assert summed.return_value == 6

    collected = runner.compile_and_execute(COLLECT_MODULE, "below", ([3, 1, 4], 3))
    assert collected.success, collected.exception_message
    assert list(collected.return_value) == [1]

    filtered = runner.compile_and_execute(
        FILTERED_MODULE, "total_of_large", ([1, 5, 10], 4)
    )
    assert filtered.success, filtered.exception_message
    assert filtered.return_value == 15


def test_typescript_target_is_no_longer_refused(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = SUM_MODULE.replace("@target python", "@target typescript")
    path = _write(tmp_path, source, "fold_sum.nl")
    code = main(["compile", "--strict", str(path)])
    captured = capsys.readouterr()
    assert code == 0, captured.err
    assert (tmp_path / "fold_sum.ts").exists()


# --------------------------------------------------------------------------
# Scoping and error contracts
# --------------------------------------------------------------------------


def test_loop_variable_is_not_visible_after_the_step(tmp_path, capsys):
    source = SUM_MODULE.replace("RETURNS: total", "RETURNS: value")
    path = _write(tmp_path, source, "leak.nl")
    assert main(["verify", "--strict", str(path)]) == 1
    assert "value" in capsys.readouterr().err


def test_target_binding_is_visible_after_the_step():
    """RETURNS reads the fold's target, so lowering must leave no foreign node."""
    from nlsc.ir import operation_unchecked_nodes

    module = lower_module(parse_nl_file(SUM_MODULE), strict=True)
    for operation in module.operations:
        assert operation_unchecked_nodes(operation) == []


def test_fold_without_a_binding_is_rejected(tmp_path, capsys):
    source = SUM_MODULE.replace(
        "  1. FOR EACH value IN values: ADD value -> total",
        "  1. FOR EACH value IN values: ADD value",
    )
    path = _write(tmp_path, source, "nobind.nl")
    assert main(["verify", "--strict", str(path)]) == 1
    # The unbound accumulator surfaces as a fatal undefined value; the
    # lowering diagnostic below states the specific cause.
    assert "total" in capsys.readouterr().err


def test_fold_without_a_binding_reports_its_own_diagnostic():
    source = SUM_MODULE.replace(
        "  1. FOR EACH value IN values: ADD value -> total",
        "  1. FOR EACH value IN values: ADD value",
    )
    diagnostics: list = []
    lower_module(parse_nl_file(source), strict=False)
    from nlsc.pipeline import executable_contract_diagnostics

    diagnostics = executable_contract_diagnostics(parse_nl_file(source))
    assert any(
        d.code == "EIR002" and "must bind its result" in d.message
        for d in diagnostics
    ), [d.message for d in diagnostics]


def test_unknown_name_in_the_fold_body_is_fatal(tmp_path, capsys):
    source = SUM_MODULE.replace("ADD value", "ADD missing_name")
    path = _write(tmp_path, source, "unknown.nl")
    assert main(["verify", str(path)]) == 1
    assert "missing_name" in capsys.readouterr().err


def test_unbounded_while_is_still_not_in_the_core(tmp_path, capsys):
    source = SUM_MODULE.replace(
        "  1. FOR EACH value IN values: ADD value -> total",
        "  1. WHILE total < 10: ADD 1 -> total",
    )
    path = _write(tmp_path, source, "unbounded.nl")
    assert main(["verify", "--strict", str(path)]) == 1


QUICKSORT = """@module fold_sort
@target python

[quick-sort]
PURPOSE: Sort a list of numbers using the quicksort algorithm
INPUTS:
  - items: list of number
EDGE CASES:
  - len(items) < 2 -> return items
LOGIC:
  1. items[0] -> pivot
  2. FOR EACH x IN items WHERE x < pivot: COLLECT x -> lesser
  3. FOR EACH x IN items WHERE x == pivot: COLLECT x -> equal
  4. FOR EACH x IN items WHERE x > pivot: COLLECT x -> greater
  5. [quick-sort](lesser) -> sorted_lesser
  6. [quick-sort](greater) -> sorted_greater
RETURNS: sorted_lesser + equal + sorted_greater
"""


def test_collect_fold_keeps_a_list_return_type():
    """A COLLECT binding must not be mistaken for a numeric accumulator."""
    code = emit_python(parse_nl_file(QUICKSORT))
    assert "def quick_sort(items: list[float]) -> list[float]:" in code


def test_typescript_list_concatenation_uses_spread():
    """JS `+` stringifies arrays, so a list result must spread, not add."""
    source = QUICKSORT.replace("@target python", "@target typescript")
    code = emit_typescript(parse_nl_file(source))
    assert "return [...sorted_lesser, ...equal, ...sorted_greater];" in code
    assert "return sorted_lesser + equal" not in code


def test_quicksort_sorts_on_both_targets():
    from tests.semantic.runners import require_typescript_runner

    namespace: dict = {}
    exec(emit_python(parse_nl_file(QUICKSORT)), namespace)
    assert namespace["quick_sort"]([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]

    runner = require_typescript_runner()
    result = runner.compile_and_execute(
        QUICKSORT.replace("@target python", "@target typescript"),
        "quick_sort",
        ([3, 1, 4, 1, 5],),
    )
    assert result.success, result.exception_message
    assert list(result.return_value) == [1, 1, 3, 4, 5]
