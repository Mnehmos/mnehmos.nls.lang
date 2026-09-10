"""Issue #144: language-spec versioning and compatibility guarantees.

``@nls MAJOR.MINOR`` declares the spec revision a file targets. Same major
is compatible; a newer minor warns under strict; a different major or a
malformed revision fails in every mode.
"""

from __future__ import annotations

import json

from nlsc import SPEC_VERSION
from nlsc.cli import main
from nlsc.parser import parse_nl_file
from nlsc.typecheck import check_module

BASE = """@module versioned
@nls {revision}
[answer]
PURPOSE: the answer
RETURNS: 42
"""


def _write(tmp_path, revision: str):
    path = tmp_path / "versioned.nl"
    path.write_text(BASE.format(revision=revision), encoding="utf-8")
    return path


def _check(revision: str):
    source = BASE.format(revision=revision)
    return check_module(parse_nl_file(source, source_path="versioned.nl"))


def test_current_revision_is_compatible():
    result = _check(SPEC_VERSION)
    assert result.errors == []
    assert result.warnings == []


def test_missing_revision_is_treated_as_current():
    result = check_module(
        parse_nl_file(
            "@module plain\n[answer]\nPURPOSE: p\nRETURNS: 42\n",
            source_path="plain.nl",
        )
    )
    assert result.errors == []
    assert not any(d.code.startswith("EVER") for d in result.warnings)


def test_newer_minor_warns_strict_only():
    result = _check("0.2")
    assert result.errors == []
    assert [d.code for d in result.warnings] == ["EVER002"]


def test_different_major_is_always_fatal():
    result = _check("1.0")
    assert "EVER001" in [d.code for d in result.errors]


def test_malformed_revision_is_fatal():
    result = _check("latest")
    assert "EVER001" in [d.code for d in result.errors]


def test_directive_parses_on_both_backends(tmp_path):
    from nlsc.parser_treesitter import is_available, parse_nl_file_treesitter

    source = BASE.format(revision="0.1")
    assert parse_nl_file(source).module.spec_version == "0.1"
    if is_available():
        assert parse_nl_file_treesitter(source).module.spec_version == "0.1"


# --------------------------------------------------------------------------
# CLI behavior
# --------------------------------------------------------------------------


def test_incompatible_revision_fails_verify(tmp_path, capsys):
    path = _write(tmp_path, "1.0")
    assert main(["verify", str(path)]) == 1
    assert "EVER001" in capsys.readouterr().err


def test_newer_minor_fails_strict_but_warns_by_default(tmp_path, capsys):
    path = _write(tmp_path, "0.2")
    assert main(["verify", "--strict", str(path)]) == 1
    assert "EVER002" in capsys.readouterr().err

    assert main(["verify", str(path)]) == 0
    assert "EVER002" in capsys.readouterr().err


def test_version_output_names_both_versions(capsys):
    import pytest

    with pytest.raises(SystemExit) as excinfo:
        main(["--version"])
    assert excinfo.value.code == 0
    out = capsys.readouterr().out
    assert "nlsc" in out
    assert f"language spec {SPEC_VERSION}" in out


def test_json_reports_version_diagnostics(tmp_path, capsys):
    path = _write(tmp_path, "9.9")
    assert main(["verify", "--json", str(path)]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert "EVER001" in [d["code"] for d in payload["diagnostics"]]
