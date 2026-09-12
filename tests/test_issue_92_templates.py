"""Issue #92: `nlsc init --template` produces working projects.

Every template's generated `.nl` files must pass strict verification,
compile, run their tests, and (where applicable) execute their `@main`
block through the real CLI, so templates cannot rot.
"""

from __future__ import annotations

import json

import pytest

from nlsc.cli import main
from nlsc.templates import TEMPLATES

TEMPLATE_NAMES = sorted(TEMPLATES)
NON_BASIC = [name for name in TEMPLATE_NAMES if not TEMPLATES[name].is_default_scaffold]


def _init(tmp_path, name: str, project: str = "demo"):
    project_dir = tmp_path / project
    assert main(["init", str(project_dir), "--template", name]) == 0
    return project_dir


def _nl_files(project_dir):
    return sorted((project_dir / "src").glob("*.nl"))


# --------------------------------------------------------------------------
# Registry and listing
# --------------------------------------------------------------------------


def test_expected_templates_registered():
    assert set(TEMPLATE_NAMES) >= {"basic", "library", "service", "cli"}


def test_list_templates_text(capsys):
    assert main(["init", "--list-templates"]) == 0
    out = capsys.readouterr().out
    for name in TEMPLATE_NAMES:
        assert name in out


def test_list_templates_json(capsys):
    assert main(["init", "--list-templates", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    names = [t["name"] for t in payload["templates"]]
    assert set(names) == set(TEMPLATE_NAMES)
    assert all(t["description"] for t in payload["templates"])


def test_unknown_template_reports_einit004(tmp_path, capsys):
    exit_code = main(["init", str(tmp_path / "x"), "--template", "nope"])
    assert exit_code == 1
    assert "EINIT004" in capsys.readouterr().err


# --------------------------------------------------------------------------
# basic preserves the original scaffold
# --------------------------------------------------------------------------


def test_basic_template_writes_no_extra_files(tmp_path):
    project_dir = _init(tmp_path, "basic")
    assert (project_dir / "nl.config.yaml").exists()
    assert not (project_dir / "nls.toml").exists()
    assert not list((project_dir / "src").glob("*.nl"))


# --------------------------------------------------------------------------
# Every template generates a working project
# --------------------------------------------------------------------------


@pytest.mark.parametrize("name", NON_BASIC)
def test_template_files_created(tmp_path, name):
    project_dir = _init(tmp_path, name)
    assert (project_dir / "nls.toml").exists()
    assert (project_dir / "README.md").exists()
    assert (project_dir / ".github" / "workflows" / "nls.yml").exists()
    assert _nl_files(project_dir), "template must ship example specs"


@pytest.mark.parametrize("name", NON_BASIC)
def test_template_specs_verify_compile_and_test(tmp_path, name):
    project_dir = _init(tmp_path, name)
    for nl_path in _nl_files(project_dir):
        assert main(["verify", str(nl_path), "--strict"]) == 0, nl_path
        assert main(["compile", str(nl_path)]) == 0, nl_path
        assert main(["ci", str(nl_path), "--test"]) == 0, nl_path


def test_cli_template_main_block_runs(tmp_path, capsys):
    project_dir = _init(tmp_path, "cli")
    assert main(["run", str(project_dir / "src" / "main.nl")]) == 0
    assert "USD 19.99" in capsys.readouterr().out


def test_nls_toml_uses_project_name(tmp_path):
    project_dir = _init(tmp_path, "library", project="pricing-lib")
    config = (project_dir / "nls.toml").read_text(encoding="utf-8")
    assert 'name = "pricing-lib"' in config


def test_reinit_reports_existing_files(tmp_path, capsys):
    project_dir = _init(tmp_path, "library")
    capsys.readouterr()
    assert main(["init", str(project_dir), "--template", "library"]) == 0
    out = capsys.readouterr().out
    assert "already exists" in out


def test_init_json_reports_template(tmp_path, capsys):
    project_dir = tmp_path / "demo"
    assert main(["init", str(project_dir), "--template", "service", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["template"] == "service"
    assert any(entry.endswith("models.nl") for entry in payload["created"])
