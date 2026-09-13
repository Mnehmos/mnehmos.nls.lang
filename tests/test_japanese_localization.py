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
