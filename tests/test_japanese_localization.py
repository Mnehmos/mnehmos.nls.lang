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
