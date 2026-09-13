"""Tests for Japanese-localized NLS syntax."""

from pathlib import Path

from nlsc.emitter import emit_python
from nlsc.parser import parse_nl_file
from nlsc.pipeline import parse_nl_path_auto


JAPANESE_QUICKSORT = """\
@モジュール sorting-ja
@ターゲット python

[クイックソート]
目的: 数値のリストをクイックソートで並べ替える
入力:
  - 項目: list of number
エッジケース:
  - len(項目) < 2 -> return 項目
ロジック:
  1. 項目[0] -> ピボット
  2. [要素 for 要素 in 項目 if 要素 < ピボット] -> 小さい項目
  3. [要素 for 要素 in 項目 if 要素 == ピボット] -> 等しい項目
  4. [要素 for 要素 in 項目 if 要素 > ピボット] -> 大きい項目
  5. [クイックソート](小さい項目) -> 整列済みの小さい項目
  6. [クイックソート](大きい項目) -> 整列済みの大きい項目
返り値: 整列済みの小さい項目 + 等しい項目 + 整列済みの大きい項目

@テスト [クイックソート] {
  クイックソート([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]
}
"""


JAPANESE_QUICKSORT_NATURAL = """\
@モジュール sorting-ja
@ターゲット パイソン

[クイックソート]
目的: 数値のリストをクイックソートで並べ替える
入力:
  - 項目: 数値のリスト
エッジケース:
  - len(項目) < 2 -> 返す 項目
ロジック:
  1. 項目[0] -> ピボット
  2. [要素 for 要素 in 項目 if 要素 < ピボット] -> 小さい項目
  3. [要素 for 要素 in 項目 if 要素 == ピボット] -> 等しい項目
  4. [要素 for 要素 in 項目 if 要素 > ピボット] -> 大きい項目
  5. [クイックソート](小さい項目) -> 整列済みの小さい項目
  6. [クイックソート](大きい項目) -> 整列済みの大きい項目
返り値: 整列済みの小さい項目 + 等しい項目 + 整列済みの大きい項目
"""


JAPANESE_QUICKSORT_FULLY_LOCALIZED = """\
@モジュール sorting-ja
@ターゲット パイソン

[クイックソート]
目的: 数値のリストをクイックソートで並べ替える
入力:
  - 項目: 数値のリスト
エッジケース:
  - 長さ(項目) < 2 -> 返す 項目
ロジック:
  1. 項目[0] -> ピボット
  2. [要素 を 項目 から もし 要素 < ピボット] -> 小さい項目
  3. [要素 を 項目 から もし 要素 == ピボット] -> 等しい項目
  4. [要素 を 項目 から もし 要素 > ピボット] -> 大きい項目
  5. [クイックソート](小さい項目) -> 整列済みの小さい項目
  6. [クイックソート](大きい項目) -> 整列済みの大きい項目
返り値: 整列済みの小さい項目 + 等しい項目 + 整列済みの大きい項目
"""


def test_parse_japanese_keywords_and_identifiers():
    result = parse_nl_file(JAPANESE_QUICKSORT)

    assert result.module.name == "sorting-ja"
    assert result.module.target == "python"
    assert len(result.anlus) == 1
    assert result.anlus[0].identifier == "クイックソート"
    assert result.anlus[0].inputs[0].name == "項目"
    assert result.tests[0].anlu_id == "クイックソート"


def test_emit_japanese_quicksort_python_executes():
    nl_file = parse_nl_file(JAPANESE_QUICKSORT, source_path="sorting_ja.nl")

    code = emit_python(nl_file)

    assert "def クイックソート(項目: list[float]) -> list[float]:" in code

    namespace = {}
    exec(code, namespace)

    assert namespace["クイックソート"]([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]
    assert namespace["クイックソート"]([]) == []


def test_parse_nl_path_auto_supports_japanese_source(tmp_path: Path):
    source_path = tmp_path / "sorting_ja.nl"
    source_path.write_text(JAPANESE_QUICKSORT, encoding="utf-8")

    result = parse_nl_path_auto(source_path)

    assert result.anlus[0].identifier == "クイックソート"


def test_emit_japanese_quicksort_supports_more_natural_type_and_return_phrases():
    nl_file = parse_nl_file(JAPANESE_QUICKSORT_NATURAL, source_path="sorting_ja.nl")

    code = emit_python(nl_file)

    assert "def クイックソート(項目: list[float]) -> list[float]:" in code

    namespace = {}
    exec(code, namespace)

    assert namespace["クイックソート"]([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]


def test_emit_localized_return_type_defaults():
    source = """\
@モジュール test-ja
@ターゲット パイソン

[空の一覧]
目的: 空の数値リストを返す
返り値: 数値のリスト
"""

    nl_file = parse_nl_file(source)
    code = emit_python(nl_file)

    assert "def 空の一覧() -> list[float]:" in code
    assert "return []" in code


def test_emit_japanese_quicksort_supports_fully_localized_expressions():
    nl_file = parse_nl_file(
        JAPANESE_QUICKSORT_FULLY_LOCALIZED,
        source_path="sorting_ja.nl",
    )

    code = emit_python(nl_file)

    assert "if len(項目) < 2:" in code
    assert "小さい項目 = [要素 for 要素 in 項目 if 要素 < ピボット]" in code

    namespace = {}
    exec(code, namespace)

    assert namespace["クイックソート"]([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]


# --------------------------------------------------------------------------
# String literals and verbatim blocks (issues #251 / #252)
# --------------------------------------------------------------------------

LITERAL_STRING_RETURN = '''@モジュール t
@ターゲット パイソン

[結果]
目的: 文字列リテラルの保持を確認
返り値: "結果: なし"
'''

LITERAL_STRING_LOGIC = '''@モジュール t
@ターゲット パイソン

[組み立て]
目的: 文字列を組み立てる
返り値: なし
ロジック:
  1. ラベル = "長さ(項目) を返す"
  2. 表示 ラベル
'''


def test_alias_tokens_inside_string_literals_are_preserved():
    from nlsc.emitter import emit_python

    return_code = emit_python(parse_nl_file(LITERAL_STRING_RETURN, source_path="t.nl"))
    assert 'return "結果: なし"' in return_code
    assert '"結果: None"' not in return_code

    logic_code = emit_python(parse_nl_file(LITERAL_STRING_LOGIC, source_path="t.nl"))
    assert '"長さ(項目) を返す"' in logic_code
    assert '"len(項目) を返す"' not in logic_code


def test_alias_substitution_still_applies_outside_literals():
    from nlsc.localization import normalize_expression_text

    assert normalize_expression_text("x かつ y") == "x and y"
    assert normalize_expression_text("長さ(項目)") == "len(項目)"
    assert normalize_expression_text("なし または 真") == "None or True"
    assert normalize_expression_text('"A または B"') == '"A または B"'
    assert normalize_expression_text("'なし'") == "'なし'"
    assert normalize_expression_text('"""真"""') == '"""真"""'


def test_typescript_emitter_preserves_alias_tokens_in_literals():
    from nlsc.emitter_typescript import emit_typescript

    code = emit_typescript(parse_nl_file(LITERAL_STRING_RETURN, source_path="t.nl"))
    assert '"結果: なし"' in code
    assert '"結果: None"' not in code


LITERAL_BLOCK = '''@モジュール t
@ターゲット パイソン

[計算]
目的: literal テスト
@リテラル {
def helper():
    表示 = 1
    return 表示
}
返り値: なし
'''


def test_literal_block_body_is_copied_verbatim():
    from nlsc.emitter import emit_python

    code = emit_python(parse_nl_file(LITERAL_BLOCK, source_path="t.nl"))
    assert "def helper():\n    表示 = 1\n    return 表示" in code
    assert "PRINT = 1" not in code
    assert "len(" not in code


def test_literal_block_line_count_is_preserved():
    from nlsc.localization import normalize_localized_source

    source = LITERAL_BLOCK
    normalized = normalize_localized_source(source)
    assert normalized.count("\n") == source.count("\n")
    # Headers around the block are still normalized.
    assert "@module t" in normalized
    assert "PURPOSE: literal テスト" in normalized
    assert "RETURNS: なし" in normalized


def test_english_literal_block_is_unaffected():
    from nlsc.emitter import emit_python

    source = LITERAL_BLOCK.replace("@モジュール t", "@module t").replace(
        "@ターゲット パイソン", "@target python"
    ).replace("目的:", "PURPOSE:").replace("返り値:", "RETURNS:").replace(
        "@リテラル", "@literal"
    )
    code = emit_python(parse_nl_file(source, source_path="t.nl"))
    assert "def helper():\n    表示 = 1\n    return 表示" in code


# --------------------------------------------------------------------------
# Assertion localization (#253) and reserved aliases (#256)
# --------------------------------------------------------------------------

ASSERTIONS = '''@モジュール t
@ターゲット パイソン

[常に真]
目的: 真を返す
返り値: 真

@テスト [常に真] {
  常に真() == 真
}

@性質 [常に真] {
  forall x: 数値 -> 常に真() == 真 かつ x >= 0 または 偽
}
'''


def test_test_assertions_are_localized():
    from nlsc.emitter import emit_tests

    code = emit_tests(parse_nl_file(ASSERTIONS, source_path="t.nl"))
    assert "assert 常に真() == True" in code
    assert "== 真" not in code


def test_property_assertions_and_types_are_localized():
    from nlsc.emitter import emit_property_tests

    code = emit_property_tests(parse_nl_file(ASSERTIONS, source_path="t.nl"))
    assert "常に真() == True" in code
    assert " or False" in code
    assert " and " in code
    # The alias words themselves are gone from the assertion.
    assert "かつ" not in code and "または" not in code
    # The forall variable type is normalized for the hypothesis strategy.
    assert "st.floats" in code


def test_english_assertions_are_unchanged():
    from nlsc.emitter import emit_tests

    source = """@module t
@target python

[pair]
PURPOSE: two
RETURNS: 2

@test [pair] {
  pair() == 2
}
"""
    code = emit_tests(parse_nl_file(source, source_path="t.nl"))
    assert "assert pair() == 2" in code


COLLIDING_ANLU = """@モジュール t
@ターゲット パイソン

[長さ]
目的: 要素数を返す
入力:
  - 項目: 数値のリスト
返り値: 長さ(項目)
"""

COLLIDING_INPUT = """@モジュール t
@ターゲット パイソン

[件数]
目的: 数える
入力:
  - 真: 数値
返り値: 真
"""

LEN_STILL_BUILTIN = """@モジュール t
@ターゲット パイソン

[件数]
目的: 数える
入力:
  - 項目: 数値のリスト
返り値: 長さ(項目)
"""


def test_reserved_alias_anlu_is_rejected(tmp_path, capsys):
    from nlsc.cli import main

    path = tmp_path / "probe.nl"
    path.write_text(COLLIDING_ANLU, encoding="utf-8")
    assert main(["verify", str(path)]) == 1
    assert "ESEM022" in capsys.readouterr().err


def test_reserved_alias_input_is_rejected(tmp_path, capsys):
    from nlsc.cli import main

    path = tmp_path / "probe.nl"
    path.write_text(COLLIDING_INPUT, encoding="utf-8")
    assert main(["verify", str(path)]) == 1
    assert "ESEM022" in capsys.readouterr().err


def test_alias_builtin_still_works_without_a_definition(tmp_path, capsys):
    from nlsc.cli import main
    from nlsc.emitter import emit_python

    path = tmp_path / "probe.nl"
    path.write_text(LEN_STILL_BUILTIN, encoding="utf-8")
    assert main(["verify", str(path)]) == 0
    code = emit_python(parse_nl_file(LEN_STILL_BUILTIN, source_path="t.nl"))
    assert "return len(項目)" in code


# --------------------------------------------------------------------------
# Japanese conditionals in numbered steps (#254) and new section aliases (#255)
# --------------------------------------------------------------------------

CONDITIONAL_JA = '''@モジュール t
@ターゲット パイソン

[判定]
目的: 判定する
入力:
  - 値: number
返り値: 結果
ロジック:
  1. もし 値 > 0 なら "正" -> 結果 そうでなければ "負" -> 結果
'''

CONDITIONAL_EN = '''@module t
@target python

[判定]
PURPOSE: 判定する
INPUTS:
  - 値: number
RETURNS: 結果
LOGIC:
  1. IF 値 > 0 THEN "正" -> 結果 ELSE "負" -> 結果
'''


def test_numbered_japanese_conditional_emits_real_control_flow():
    from nlsc.emitter import emit_python

    code = emit_python(parse_nl_file(CONDITIONAL_JA, source_path="t.nl"))
    assert "if 値 > 0:" in code
    assert '結果 = "正"' in code
    assert "else:" in code
    assert '結果 = "負"' in code
    # No TODO scaffold leaked into the conditional.
    assert "TODO" not in code


def test_naraba_spelling_is_accepted():
    from nlsc.emitter import emit_python

    source = CONDITIONAL_JA.replace("なら", "ならば")
    code = emit_python(parse_nl_file(source, source_path="t.nl"))
    assert "if 値 > 0:" in code
    assert "TODO" not in code


def test_japanese_and_english_conditionals_are_equivalent():
    from nlsc.emitter import emit_python

    ja = emit_python(parse_nl_file(CONDITIONAL_JA, source_path="ja.nl"))
    en = emit_python(parse_nl_file(CONDITIONAL_EN, source_path="en.nl"))
    # The generated-from path differs; compare the code itself.
    ja_body = [
        line.strip()
        for line in ja.splitlines()
        if line.strip() and "Generated by nlsc from" not in line
    ]
    en_body = [
        line.strip()
        for line in en.splitlines()
        if line.strip() and "Generated by nlsc from" not in line
    ]
    assert ja_body == en_body


def test_nested_aliases_in_arms_are_normalized():
    from nlsc.emitter import emit_python

    source = CONDITIONAL_JA.replace(
        '1. もし 値 > 0 なら "正" -> 結果 そうでなければ "負" -> 結果',
        "1. もし 長さ(項目) > 0 なら 真を数える -> 結果 それ以外 なし -> 結果",
    ).replace("  - 値: number", "  - 項目: list of number")
    assert source != CONDITIONAL_JA  # the replace must have matched
    code = emit_python(parse_nl_file(source, source_path="t.nl"))
    assert "if len(項目) > 0:" in code
    assert "結果 = None" in code


def test_unknown_section_header_is_reported(tmp_path, capsys):
    from nlsc.cli import main

    source = CONDITIONAL_JA.replace("返り値: 結果", "返り値: 結果\n監査: すべて記録")
    path = tmp_path / "probe.nl"
    path.write_text(source, encoding="utf-8")
    assert main(["verify", str(path)]) == 1
    assert "Unknown section header '監査'" in capsys.readouterr().err


STATE_ALIASES = '''@モジュール t
@状態 Order: Pending, Validated

[validate-order]
目的: 検証する
入力:
  - order: Order<Pending>
影響: なし
返り値: Order<Validated>
'''


def test_states_effects_retry_timeout_aliases(tmp_path, capsys):
    from nlsc.cli import main
    from nlsc.parser import parse_nl_file

    parsed = parse_nl_file(STATE_ALIASES, source_path="t.nl")
    assert parsed.module.states == {"Order": ("Pending", "Validated")}
    assert parsed.anlus[0].declared_effects == "none"

    # RETRY/TIMEOUT parse identically to the English forms. The policy must
    # be shape-valid (#201): the retried identity comes from a guard, and
    # the idempotency key is a parameter.
    retry_source = STATE_ALIASES.replace(
        "影響: なし",
        "ガード:\n  - order == なし -> NetworkError(\"注文がありません\")\n"
        "再試行:\n  - up to 3 attempts on NetworkError\n  - idempotency key: order\n"
        "タイムアウト:\n  - after 5000ms -> cancel-and-reconcile",
    )
    parsed = parse_nl_file(retry_source, source_path="t.nl")
    assert parsed.anlus[0].retry is not None
    assert parsed.anlus[0].retry.attempts == 3
    assert parsed.anlus[0].retry.idempotency_key == "order"
    assert parsed.anlus[0].timeout is not None
    assert parsed.anlus[0].timeout.outcome == "cancel-and-reconcile"

    # Emission refusal matches the English behavior (no target emits policies).
    path = tmp_path / "probe.nl"
    path.write_text(retry_source, encoding="utf-8")
    assert main(["compile", str(path)]) == 1
    assert "ETARGET002" in capsys.readouterr().err


def test_effects_aliases_work_before_and_after_returns():
    from nlsc.parser import parse_nl_file

    before = STATE_ALIASES  # 影響 before 返り値
    after = STATE_ALIASES.replace(
        "影響: なし\n返り値: Order<Validated>", "返り値: Order<Validated>\n影響: なし"
    )
    for source in (before, after):
        parsed = parse_nl_file(source, source_path="t.nl")
        assert parsed.anlus[0].declared_effects == "none"


# --------------------------------------------------------------------------
# Normative alias tables in the spec stay in sync (#257)
# --------------------------------------------------------------------------


def _parse_spec_alias_table() -> set[tuple[str, str, str]]:
    import re
    from pathlib import Path

    spec = (
        Path(__file__).resolve().parents[1] / "docs" / "language-spec.md"
    ).read_text(encoding="utf-8")
    match = re.search(
        r"<!-- localization-aliases:begin -->\n(.*?)<!-- localization-aliases:end -->",
        spec,
        re.DOTALL,
    )
    assert match is not None, "the alias table markers are missing from the spec"
    rows: set[tuple[str, str, str]] = set()
    for line in match.group(1).splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3 or cells[0] in ("Category", "---", ""):
            continue
        category, canonical, spellings = cells
        for spelling in [s.strip().strip("`") for s in spellings.split(",")]:
            rows.add((category, canonical, spelling))
    return rows


def test_spec_alias_table_matches_the_module():
    import nlsc.localization as L

    documented = _parse_spec_alias_table()
    expected: set[tuple[str, str, str]] = set()

    def add(category, mapping):
        for surface, canonical in mapping.items():
            if surface == canonical:
                continue  # identity rows carry no localized spelling
            expected.add((category, canonical, surface))

    add("Directive", L._DIRECTIVE_ALIASES)
    for canonical, aliases in L._SECTION_ALIASES.items():
        add("Section", {alias: canonical for alias in aliases})
    add("Value", L._NONE_ALIASES)
    add("Type", L._TYPE_ALIASES)
    for surface, replacement in L._EXPRESSION_ALIASES.items():
        expected.add(("Expression alias (rewrites to)", surface, replacement))
    add("Target", L._TARGET_ALIASES)

    assert documented == expected, (
        "docs/language-spec.md's alias table is out of sync with "
        "nlsc/localization.py; update the marked table when aliases change."
    )
