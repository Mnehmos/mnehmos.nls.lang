"""Structured JSON error output for CLI commands."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

from nlsc.cli import main


REPO_ROOT = Path(__file__).resolve().parents[1]


class _FakeRegistryKey:
    def __enter__(self) -> object:
        return object()

    def __exit__(self, exc_type: object, exc: object, tb: object) -> bool:
        return False


class _FakeWinreg(ModuleType):
    HKEY_CURRENT_USER = object()
    HKEY_CLASSES_ROOT = object()
    REG_SZ = 1

    def __init__(self, *, create_key_error: Exception | None = None) -> None:
        super().__init__("winreg")
        self._create_key_error = create_key_error

    def CreateKey(self, root_key: object, sub_key: str) -> _FakeRegistryKey:
        del root_key, sub_key
        if self._create_key_error is not None:
            raise self._create_key_error
        return _FakeRegistryKey()

    def SetValueEx(
        self,
        key: object,
        name: str,
        reserved: int,
        reg_type: int,
        value: str,
    ) -> None:
        del key, name, reserved, reg_type, value

    def DeleteKey(self, root_key: object, sub_key: str) -> None:
        del root_key, sub_key


def _run_nlsc(
    argv: list[str], *, cwd: Path, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "nlsc", *argv],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env=env,
    )


def _load_json_output(result: subprocess.CompletedProcess[str]) -> dict:
    assert result.stdout.strip(), f"expected JSON stdout, got stderr={result.stderr!r}"
    return json.loads(result.stdout)


def _treesitter_unavailable_env(tmp_path: Path) -> dict[str, str]:
    hook_dir = tmp_path / "sitecustomize"
    hook_dir.mkdir()
    (hook_dir / "sitecustomize.py").write_text(
        "import nlsc.parser_treesitter as parser_treesitter\n"
        "parser_treesitter.is_available = lambda: False\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    pythonpath_parts = [str(hook_dir), str(REPO_ROOT)]
    existing_pythonpath = env.get("PYTHONPATH")
    if existing_pythonpath:
        pythonpath_parts.append(existing_pythonpath)
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)
    return env


def test_verify_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.nl"

    result = _run_nlsc(["verify", str(missing_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["ok"] is False
    assert payload["command"] == "verify"
    assert payload["diagnostics"] == [
        {
            "code": "EFILE001",
            "file": str(missing_path),
            "line": None,
            "col": None,
            "message": f"File not found: {missing_path}",
            "hint": "Check that the path exists and try again.",
        }
    ]


def test_init_json_reports_blank_target_path(capsys: Any) -> None:
    exit_code = main(["init", "", "--json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["command"] == "init"
    assert payload["path"] == ""
    assert payload["diagnostics"] == [
        {
            "code": "EINIT001",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "Init target path is missing or blank.",
            "hint": "Pass a directory path to `nlsc init`, or omit the argument to use the current directory.",
        }
    ]
    assert captured.err == ""


def test_init_json_reports_target_path_that_is_a_file(
    capsys: Any, tmp_path: Path
) -> None:
    file_path = tmp_path / "not_a_directory.txt"
    file_path.write_text("occupied", encoding="utf-8")

    exit_code = main(["init", str(file_path), "--json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["command"] == "init"
    assert payload["path"] == str(file_path)
    assert payload["diagnostics"] == [
        {
            "code": "EINIT001",
            "file": str(file_path),
            "line": None,
            "col": None,
            "message": f"Init target path is not a directory: {file_path}",
            "hint": "Choose a directory path for `nlsc init`, or remove the conflicting file and rerun.",
        }
    ]
    assert captured.err == ""


def test_init_json_reports_directory_creation_failure(
    capsys: Any, monkeypatch: Any, tmp_path: Path
) -> None:
    project_dir = tmp_path / "init-fails"
    real_mkdir = Path.mkdir

    def fake_mkdir(self: Path, *args: Any, **kwargs: Any) -> None:
        if self == project_dir:
            raise PermissionError("permission denied")
        real_mkdir(self, *args, **kwargs)

    monkeypatch.setattr(Path, "mkdir", fake_mkdir)

    exit_code = main(["init", str(project_dir), "--json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["command"] == "init"
    assert payload["path"] == str(project_dir)
    assert payload["diagnostics"] == [
        {
            "code": "EINIT002",
            "file": str(project_dir),
            "line": None,
            "col": None,
            "message": f"Failed to create project directory: {project_dir} (permission denied)",
            "hint": "Check that the parent path exists and that you can create directories there, then rerun `nlsc init`.",
        }
    ]
    assert captured.err == ""


def test_init_json_reports_project_file_write_failure(
    capsys: Any, monkeypatch: Any, tmp_path: Path
) -> None:
    project_dir = tmp_path / "init-write-fails"
    config_path = project_dir / "nl.config.yaml"
    real_write_text = Path.write_text

    def fake_write_text(self: Path, data: str, *args: Any, **kwargs: Any) -> int:
        if self == config_path:
            raise OSError("disk full")
        return real_write_text(self, data, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", fake_write_text)

    exit_code = main(["init", str(project_dir), "--json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["command"] == "init"
    assert payload["path"] == str(project_dir)
    assert payload["diagnostics"] == [
        {
            "code": "EINIT003",
            "file": str(config_path),
            "line": None,
            "col": None,
            "message": f"Failed to write project file: {config_path} (disk full)",
            "hint": "Check the destination path and filesystem permissions, then rerun `nlsc init`.",
        }
    ]
    assert captured.err == ""


def test_verify_json_reports_missing_required_file_argument() -> None:
    result = _run_nlsc(["verify", "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["ok"] is False
    assert payload["command"] == "verify"
    assert payload["diagnostics"] == [
        {
            "code": "ECLI001",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "the following arguments are required: file",
            "hint": "Rerun the command with --help to inspect the required arguments and valid options.",
        }
    ]
    assert payload["usage"].startswith("usage: nlsc verify")


def test_explain_json_reports_known_error_definition() -> None:
    result = _run_nlsc(["explain", "EPARSE001", "--json"], cwd=REPO_ROOT)

    assert result.returncode == 0
    payload = _load_json_output(result)
    assert payload == {
        "ok": True,
        "command": "explain",
        "code": "EPARSE001",
        "title": "Parse error",
        "summary": "The .nl source contains syntax the parser cannot accept.",
        "emitted_by": [
            "compile",
            "verify",
            "run",
            "test",
            "graph",
            "diff",
            "watch",
            "lock:check",
            "lock:update",
        ],
        "common_causes": [
            "A required directive or section is malformed or missing.",
            "A LOGIC, INPUTS, or GUARDS line does not follow the expected shape.",
        ],
        "next_steps": [
            "Use the reported line number to fix the source syntax.",
            "Run `nlsc verify <file>` after editing to confirm the file parses cleanly.",
        ],
        "diagnostics": [],
    }


def test_explain_json_reports_unknown_error_code() -> None:
    result = _run_nlsc(["explain", "ENOPE999", "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["ok"] is False
    assert payload["command"] == "explain"
    assert payload["requested_code"] == "ENOPE999"
    assert payload["diagnostics"] == [
        {
            "code": "EEXPLAIN001",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "Unknown error code: ENOPE999",
            "hint": "Run `nlsc explain --json ECLI001` or inspect `known_codes` to choose a cataloged error code.",
        }
    ]
    assert "ECLI001" in payload["known_codes"]
    assert "EWATCH002" in payload["known_codes"]


def test_explain_json_reports_parser_backend_unavailable(tmp_path: Path) -> None:
    result = _run_nlsc(
        ["--parser", "treesitter", "explain", "EPARSE001", "--json"],
        cwd=REPO_ROOT,
        env=_treesitter_unavailable_env(tmp_path),
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "explain"
    assert payload["parser"] == "treesitter"
    assert payload["diagnostics"] == [
        {
            "code": "EPARSE002",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "Parser backend 'treesitter' is unavailable: tree-sitter is not installed",
            "hint": "Install with: pip install nlsc[treesitter], or rerun with --parser auto or --parser regex.",
        }
    ]


def test_explain_json_reports_parser_backend_unavailable_definition() -> None:
    result = _run_nlsc(["explain", "EPARSE002", "--json"], cwd=REPO_ROOT)

    assert result.returncode == 0
    payload = _load_json_output(result)
    assert payload["code"] == "EPARSE002"
    assert "atomize" in payload["emitted_by"]


def test_init_json_reports_parser_backend_unavailable(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"

    result = _run_nlsc(
        ["--parser", "treesitter", "init", str(project_dir), "--json"],
        cwd=REPO_ROOT,
        env=_treesitter_unavailable_env(tmp_path),
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "init"
    assert payload["parser"] == "treesitter"
    assert payload["diagnostics"] == [
        {
            "code": "EPARSE002",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "Parser backend 'treesitter' is unavailable: tree-sitter is not installed",
            "hint": "Install with: pip install nlsc[treesitter], or rerun with --parser auto or --parser regex.",
        }
    ]


def test_verify_json_reports_parse_error_location(tmp_path: Path) -> None:
    source_path = tmp_path / "broken.nl"
    source_path.write_text(
        """\
@module broken
@target python

[main]
PURPOSE: Broken
LOGIC:
  first step is not numbered
RETURNS: void
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "verify", str(source_path), "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["diagnostics"] == [
        {
            "code": "EPARSE001",
            "file": str(source_path),
            "line": 7,
            "col": None,
            "message": "Invalid LOGIC step format; expected numbered step like '1. ...'",
            "hint": "Rewrite the line as a numbered LOGIC step like '1. ...'.",
        }
    ]


def test_verify_json_reports_parser_backend_unavailable(tmp_path: Path) -> None:
    source_path = tmp_path / "verify_source.nl"
    source_path.write_text(
        "@module verify-source\n@target python\n\n[main]\nPURPOSE: Ok\nRETURNS: 1\n",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "treesitter", "verify", str(source_path), "--json"],
        cwd=REPO_ROOT,
        env=_treesitter_unavailable_env(tmp_path),
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "verify"
    assert payload["parser"] == "treesitter"
    assert payload["diagnostics"] == [
        {
            "code": "EPARSE002",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "Parser backend 'treesitter' is unavailable: tree-sitter is not installed",
            "hint": "Install with: pip install nlsc[treesitter], or rerun with --parser auto or --parser regex.",
        }
    ]


def test_verify_json_reports_stdlib_use_error(tmp_path: Path) -> None:
    source_path = tmp_path / "use_missing.nl"
    source_path.write_text(
        """\
@module use-missing
@target python
@use math.missing

[main]
PURPOSE: No-op
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "verify", str(source_path), "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["diagnostics"] == [
        {
            "code": "EUSE001",
            "file": str(source_path),
            "line": 3,
            "col": 1,
            "message": "Missing stdlib domain: math.missing",
            "hint": "Add the module under an stdlib root or pass --stdlib-path.",
        }
    ]


def test_verify_json_reports_dependency_resolution_error(tmp_path: Path) -> None:
    source_path = tmp_path / "missing_dep.nl"
    source_path.write_text(
        """\
@module missing-dep
@target python

[main]
PURPOSE: Needs helper
DEPENDS: [helper]
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "verify", str(source_path), "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["diagnostics"] == [
        {
            "code": "E_RESOLUTION",
            "file": str(source_path),
            "line": 4,
            "col": 1,
            "message": "main: Missing dependency: helper",
            "hint": "Define [helper] or remove it from DEPENDS.",
        }
    ]


def test_compile_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_compile.nl"

    result = _run_nlsc(["compile", str(missing_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "compile"
    assert payload["diagnostics"][0]["code"] == "EFILE001"


def test_compile_json_reports_invalid_target_choice(tmp_path: Path) -> None:
    source_path = tmp_path / "compile_source.nl"
    source_path.write_text(
        "@module compile-source\n@target python\n\n[main]\nPURPOSE: Ok\nRETURNS: 1\n",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["compile", str(source_path), "--target", "ruby", "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "compile"
    assert payload["diagnostics"] == [
        {
            "code": "ECLI001",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "argument -t/--target: invalid choice: 'ruby' (choose from python, typescript)",
            "hint": "Rerun the command with --help to inspect the required arguments and valid options.",
        }
    ]
    assert payload["usage"].startswith("usage: nlsc compile")


def test_compile_json_success_returns_structured_payload(tmp_path: Path) -> None:
    source_path = tmp_path / "compile_ok.nl"
    output_path = tmp_path / "compile_ok.py"
    lock_path = tmp_path / "compile_ok.nl.lock"
    source_path.write_text(
        """\
@module compile-ok
@target python

[main]
PURPOSE: Compile ok
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(["compile", str(source_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 0
    payload = _load_json_output(result)
    assert payload == {
        "ok": True,
        "command": "compile",
        "diagnostics": [],
        "file": str(source_path),
        "output": str(output_path),
        "lockfile": str(lock_path),
        "target": "python",
        "line_count": output_path.read_text(encoding="utf-8").count("\n") + 1,
    }


def test_compile_json_reports_artifact_write_failure(
    capsys: Any, monkeypatch: Any, tmp_path: Path
) -> None:
    source_path = tmp_path / "compile_write_fail.nl"
    output_path = tmp_path / "compile_write_fail.py"
    source_path.write_text(
        "@module compile-write-fail\n@target python\n\n[main]\nPURPOSE: Ok\nRETURNS: 1\n",
        encoding="utf-8",
    )
    real_write_text = Path.write_text

    def fake_write_text(self: Path, data: str, *args: Any, **kwargs: Any) -> int:
        if self == output_path:
            raise OSError("disk full")
        return real_write_text(self, data, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", fake_write_text)

    exit_code = main(["compile", str(source_path), "--json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload == {
        "ok": False,
        "command": "compile",
        "diagnostics": [
            {
                "code": "EARTIFACT001",
                "file": str(output_path),
                "line": None,
                "col": None,
                "message": f"Failed to write artifact: {output_path} (disk full)",
                "hint": "Check the output path and filesystem permissions, then rerun `nlsc compile`.",
            }
        ],
        "file": str(source_path),
    }
    assert captured.err == ""


def test_compile_json_reports_lockfile_write_failure(
    capsys: Any, monkeypatch: Any, tmp_path: Path
) -> None:
    source_path = tmp_path / "compile_lock_write_fail.nl"
    lock_path = tmp_path / "compile_lock_write_fail.nl.lock"
    source_path.write_text(
        "@module compile-lock-write-fail\n@target python\n\n[main]\nPURPOSE: Ok\nRETURNS: 1\n",
        encoding="utf-8",
    )
    real_write_text = Path.write_text

    def fake_write_text(self: Path, data: str, *args: Any, **kwargs: Any) -> int:
        if self == lock_path:
            raise OSError("permission denied")
        return real_write_text(self, data, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", fake_write_text)

    exit_code = main(["compile", str(source_path), "--json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload == {
        "ok": False,
        "command": "compile",
        "diagnostics": [
            {
                "code": "ELOCK003",
                "file": str(lock_path),
                "line": None,
                "col": None,
                "message": f"Failed to write lockfile: {lock_path} (permission denied)",
                "hint": "Check the destination path and filesystem permissions, then rerun `nlsc compile`.",
            }
        ],
        "file": str(source_path),
    }
    assert captured.err == ""


def test_unknown_subcommand_with_json_reports_structured_diagnostic() -> None:
    result = _run_nlsc(["frobnicate", "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "frobnicate"
    assert payload["diagnostics"] == [
        {
            "code": "ECLI001",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "argument command: invalid choice: 'frobnicate' (choose from init, compile, run, verify, explain, graph, test, atomize, diff, dif, watch, lock:check, lock:update, lsp, assoc)",
            "hint": "Rerun the command with --help to inspect the required arguments and valid options.",
        }
    ]
    assert payload["usage"].startswith("usage: nlsc")


def test_main_argv_json_parse_errors_use_supplied_argv(capsys: Any) -> None:
    exit_code = main(["verify", "--json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["command"] == "verify"
    assert payload["diagnostics"] == [
        {
            "code": "ECLI001",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "the following arguments are required: file",
            "hint": "Rerun the command with --help to inspect the required arguments and valid options.",
        }
    ]
    assert payload["usage"].startswith("usage: nlsc verify")
    assert captured.err == ""


def test_assoc_json_reports_non_windows_platform(capsys: Any, monkeypatch: Any) -> None:
    import nlsc.cli as cli_module

    monkeypatch.setattr(cli_module.platform, "system", lambda: "Linux")
    exit_code = main(["assoc", "--json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["command"] == "assoc"
    assert payload["diagnostics"] == [
        {
            "code": "EASSOC001",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "File association command is only available on Windows.",
            "hint": "Run `nlsc assoc` on Windows, or manage `.nl` file associations with your OS tooling.",
        }
    ]
    assert captured.err == ""


def test_assoc_json_reports_parser_backend_unavailable(tmp_path: Path) -> None:
    result = _run_nlsc(
        ["--parser", "treesitter", "assoc", "--json"],
        cwd=REPO_ROOT,
        env=_treesitter_unavailable_env(tmp_path),
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "assoc"
    assert payload["parser"] == "treesitter"
    assert payload["diagnostics"] == [
        {
            "code": "EPARSE002",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "Parser backend 'treesitter' is unavailable: tree-sitter is not installed",
            "hint": "Install with: pip install nlsc[treesitter], or rerun with --parser auto or --parser regex.",
        }
    ]


def test_assoc_json_reports_missing_icon_path(capsys: Any, monkeypatch: Any) -> None:
    import nlsc.cli as cli_module

    monkeypatch.setattr(cli_module.platform, "system", lambda: "Windows")
    monkeypatch.setitem(sys.modules, "winreg", _FakeWinreg())
    real_exists = cli_module.Path.exists
    monkeypatch.setattr(
        cli_module.Path,
        "exists",
        lambda self: False if self.name == "nls-file.ico" else real_exists(self),
    )

    exit_code = main(["assoc", "--json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["command"] == "assoc"
    assert payload["diagnostics"] == [
        {
            "code": "EASSOC002",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "Could not find `nls-file.ico` in package resources.",
            "hint": "Run `python windows/generate_ico.py` from the project root to regenerate the icon asset.",
        }
    ]
    assert captured.err == ""


def test_assoc_json_reports_permission_failure(
    capsys: Any, monkeypatch: Any, tmp_path: Path
) -> None:
    import nlsc.cli as cli_module

    monkeypatch.setattr(cli_module.platform, "system", lambda: "Windows")
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(cli_module, "_check", lambda: "[OK]")
    monkeypatch.setitem(
        sys.modules,
        "winreg",
        _FakeWinreg(create_key_error=PermissionError("Access is denied")),
    )

    exit_code = main(["assoc", "--json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["command"] == "assoc"
    assert payload["diagnostics"] == [
        {
            "code": "EASSOC003",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "Permission denied while updating file associations.",
            "hint": "Rerun with elevated permissions or use `nlsc assoc --user` for a per-user association.",
        }
    ]
    assert captured.err == ""


def test_assoc_json_reports_runtime_failure(
    capsys: Any, monkeypatch: Any, tmp_path: Path
) -> None:
    import nlsc.cli as cli_module

    monkeypatch.setattr(cli_module.platform, "system", lambda: "Windows")
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(cli_module, "_check", lambda: "[OK]")
    monkeypatch.setitem(
        sys.modules,
        "winreg",
        _FakeWinreg(create_key_error=RuntimeError("registry transaction aborted")),
    )

    exit_code = main(["assoc", "--json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["command"] == "assoc"
    assert payload["diagnostics"] == [
        {
            "code": "EASSOC004",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "File association update failed: registry transaction aborted",
            "hint": "Inspect the Windows registry state and the reported runtime failure, then rerun `nlsc assoc`.",
        }
    ]
    assert captured.err == ""


def test_lsp_json_reports_missing_optional_dependencies(
    capsys: Any, monkeypatch: Any
) -> None:
    import builtins

    real_import = builtins.__import__

    def fake_import(
        name: str,
        globals: dict[str, object] | None = None,
        locals: dict[str, object] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> Any:
        if name == "nlsc.lsp":
            raise ImportError("No module named 'pygls'")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.delitem(sys.modules, "nlsc.lsp", raising=False)
    monkeypatch.delitem(sys.modules, "nlsc.lsp.server", raising=False)
    monkeypatch.setattr(builtins, "__import__", fake_import)

    exit_code = main(["lsp", "--json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["command"] == "lsp"
    assert payload["diagnostics"] == [
        {
            "code": "ELSP001",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "LSP optional dependencies are unavailable: No module named 'pygls'",
            "hint": "Install with: pip install nlsc[lsp] and rerun `nlsc lsp`.",
        }
    ]
    assert captured.err == ""


def test_lsp_json_reports_import_time_failure(capsys: Any, monkeypatch: Any) -> None:
    import builtins

    real_import = builtins.__import__

    def fake_import(
        name: str,
        globals: dict[str, object] | None = None,
        locals: dict[str, object] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> Any:
        if name == "nlsc.lsp":
            raise RuntimeError("broken import-time startup")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.delitem(sys.modules, "nlsc.lsp", raising=False)
    monkeypatch.delitem(sys.modules, "nlsc.lsp.server", raising=False)
    monkeypatch.setattr(builtins, "__import__", fake_import)

    exit_code = main(["lsp", "--json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["command"] == "lsp"
    assert payload["diagnostics"] == [
        {
            "code": "ELSP002",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "LSP server failed to start: broken import-time startup",
            "hint": "Check the selected transport, host, and port, then rerun `nlsc lsp`.",
        }
    ]
    assert captured.err == ""


def test_lsp_json_reports_startup_failure(capsys: Any, monkeypatch: Any) -> None:
    fake_module = ModuleType("nlsc.lsp")

    def fake_start_server(*, transport: str, host: str, port: int) -> None:
        raise RuntimeError(f"failed to bind {transport} server on {host}:{port}")

    setattr(fake_module, "start_server", fake_start_server)
    monkeypatch.setitem(sys.modules, "nlsc.lsp", fake_module)

    exit_code = main(["lsp", "--json", "--transport", "tcp", "--port", "2088"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["command"] == "lsp"
    assert payload["transport"] == "tcp"
    assert payload["host"] == "127.0.0.1"
    assert payload["port"] == 2088
    assert payload["diagnostics"] == [
        {
            "code": "ELSP002",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "LSP server failed to start: failed to bind tcp server on 127.0.0.1:2088",
            "hint": "Check the selected transport, host, and port, then rerun `nlsc lsp`.",
        }
    ]
    assert captured.err == ""


def test_lsp_json_reports_parser_backend_unavailable(tmp_path: Path) -> None:
    result = _run_nlsc(
        ["--parser", "treesitter", "lsp", "--json"],
        cwd=REPO_ROOT,
        env=_treesitter_unavailable_env(tmp_path),
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "lsp"
    assert payload["parser"] == "treesitter"
    assert payload["diagnostics"] == [
        {
            "code": "EPARSE002",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "Parser backend 'treesitter' is unavailable: tree-sitter is not installed",
            "hint": "Install with: pip install nlsc[treesitter], or rerun with --parser auto or --parser regex.",
        }
    ]


def test_compile_json_reports_parser_backend_unavailable(tmp_path: Path) -> None:
    source_path = tmp_path / "compile_source.nl"
    source_path.write_text(
        "@module compile-source\n@target python\n\n[main]\nPURPOSE: Ok\nRETURNS: 1\n",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "treesitter", "compile", str(source_path), "--json"],
        cwd=REPO_ROOT,
        env=_treesitter_unavailable_env(tmp_path),
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "compile"
    assert payload["parser"] == "treesitter"
    assert payload["diagnostics"] == [
        {
            "code": "EPARSE002",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "Parser backend 'treesitter' is unavailable: tree-sitter is not installed",
            "hint": "Install with: pip install nlsc[treesitter], or rerun with --parser auto or --parser regex.",
        }
    ]


def test_run_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_run.nl"

    result = _run_nlsc(["run", str(missing_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "run"
    assert payload["diagnostics"][0]["code"] == "EFILE001"


def test_run_json_reports_runtime_exit_failures(tmp_path: Path) -> None:
    source_path = tmp_path / "runtime_failure.nl"
    source_path.write_text(
        """\
@module runtime-failure
@target python

[main]
PURPOSE: Trigger a runtime error
RETURNS: 1 / 0
""",
        encoding="utf-8",
    )

    result = _run_nlsc(["run", str(source_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "run"
    assert payload["ok"] is False
    assert payload["exit_code"] == 1
    assert payload["diagnostics"] == [
        {
            "code": "EEXEC001",
            "file": str(source_path),
            "line": None,
            "col": None,
            "message": "Generated program exited with code 1.",
            "hint": "Inspect stdout/stderr for the runtime failure and rerun `nlsc run` after fixing the generated behavior or inputs.",
        }
    ]
    assert "ZeroDivisionError" in payload["stderr"]


def test_graph_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_graph.nl"

    result = _run_nlsc(["graph", str(missing_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "graph"
    assert payload["diagnostics"][0]["code"] == "EFILE001"


def test_graph_json_reports_missing_anlu(tmp_path: Path) -> None:
    source_path = tmp_path / "graph_source.nl"
    source_path.write_text(
        """\
@module graph-source
@target python

[main]
PURPOSE: Show graph
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["graph", str(source_path), "--json", "--anlu", "helper"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "graph"
    assert payload["diagnostics"] == [
        {
            "code": "EGRAPH001",
            "file": str(source_path),
            "line": None,
            "col": None,
            "message": "ANLU 'helper' not found",
            "hint": "Choose one of the defined ANLUs: main.",
        }
    ]


def test_graph_json_reports_unsupported_dataflow_format(tmp_path: Path) -> None:
    source_path = tmp_path / "graph_dataflow.nl"
    source_path.write_text(
        """\
@module graph-dataflow
@target python

[main]
PURPOSE: Show graph
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["graph", str(source_path), "--json", "--anlu", "main", "--format", "dot"],
        cwd=REPO_ROOT,
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "graph"
    assert payload["diagnostics"] == [
        {
            "code": "EGRAPH002",
            "file": str(source_path),
            "line": 4,
            "col": 1,
            "message": "Format 'dot' is not supported for ANLU dataflow graphs",
            "hint": "Use --format mermaid or --format ascii when selecting --anlu.",
        }
    ]


def test_graph_json_success_returns_structured_payload(tmp_path: Path) -> None:
    source_path = tmp_path / "graph_ok.nl"
    source_path.write_text(
        """\
@module graph-ok
@target python

[main]
PURPOSE: Show graph
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(["graph", str(source_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 0
    payload = _load_json_output(result)
    assert payload == {
        "ok": True,
        "command": "graph",
        "diagnostics": [],
        "file": str(source_path),
        "format": "mermaid",
        "anlu": None,
        "dataflow": False,
        "graph_kind": "dependency",
        "output_file": None,
        "graph": "graph LR\n    main[main]",
    }


def test_graph_json_success_writes_output_file(tmp_path: Path) -> None:
    source_path = tmp_path / "graph_out.nl"
    output_path = tmp_path / "graph.mmd"
    source_path.write_text(
        """\
@module graph-out
@target python

[main]
PURPOSE: Show graph output
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["graph", str(source_path), "--json", "--output", str(output_path)],
        cwd=REPO_ROOT,
    )

    assert result.returncode == 0
    payload = _load_json_output(result)
    assert payload == {
        "ok": True,
        "command": "graph",
        "diagnostics": [],
        "file": str(source_path),
        "format": "mermaid",
        "anlu": None,
        "dataflow": False,
        "graph_kind": "dependency",
        "output_file": str(output_path),
        "graph": "graph LR\n    main[main]",
    }
    assert output_path.read_text(encoding="utf-8") == payload["graph"]


def test_graph_json_reports_rendered_dataflow_kind_for_anlu_ascii(
    tmp_path: Path,
) -> None:
    source_path = tmp_path / "graph_anlu_ascii.nl"
    source_path.write_text(
        """\
@module graph-anlu-ascii
@target python

[main]
PURPOSE: Show graph output
LOGIC:
  1. Set total = 1
  2. RETURN total
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["graph", str(source_path), "--json", "--anlu", "main", "--format", "ascii"],
        cwd=REPO_ROOT,
    )

    assert result.returncode == 0
    payload = _load_json_output(result)
    assert payload["ok"] is True
    assert payload["command"] == "graph"
    assert payload["diagnostics"] == []
    assert payload["file"] == str(source_path)
    assert payload["format"] == "ascii"
    assert payload["anlu"] == "main"
    assert payload["dataflow"] is True
    assert payload["graph_kind"] == "dataflow"
    assert payload["output_file"] is None
    assert "Step 1" in payload["graph"]


def test_atomize_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_atomize.py"

    result = _run_nlsc(["atomize", str(missing_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "atomize"
    assert payload["diagnostics"] == [
        {
            "code": "EFILE001",
            "file": str(missing_path),
            "line": None,
            "col": None,
            "message": f"File not found: {missing_path}",
            "hint": "Check that the path exists and try again.",
        }
    ]


def test_atomize_json_reports_parser_backend_unavailable(tmp_path: Path) -> None:
    source_path = tmp_path / "atomize_source.py"
    source_path.write_text("def main() -> int:\n    return 1\n", encoding="utf-8")

    result = _run_nlsc(
        ["--parser", "treesitter", "atomize", str(source_path), "--json"],
        cwd=REPO_ROOT,
        env=_treesitter_unavailable_env(tmp_path),
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "atomize"
    assert payload["parser"] == "treesitter"
    assert payload["diagnostics"] == [
        {
            "code": "EPARSE002",
            "file": "<cli>",
            "line": None,
            "col": None,
            "message": "Parser backend 'treesitter' is unavailable: tree-sitter is not installed",
            "hint": "Install with: pip install nlsc[treesitter], or rerun with --parser auto or --parser regex.",
        }
    ]


def test_atomize_json_reports_python_syntax_error(tmp_path: Path) -> None:
    source_path = tmp_path / "broken.py"
    source_path.write_text(
        "def broken(:\n    return 1\n",
        encoding="utf-8",
    )

    result = _run_nlsc(["atomize", str(source_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "atomize"
    assert payload["diagnostics"] == [
        {
            "code": "EATOM001",
            "file": str(source_path),
            "line": 1,
            "col": 12,
            "message": "Python syntax error: invalid syntax",
            "hint": "Fix the Python syntax and rerun `nlsc atomize`.",
        }
    ]


def test_atomize_json_reports_write_failure(tmp_path: Path) -> None:
    source_path = tmp_path / "ok.py"
    source_path.write_text(
        "def add(a: int, b: int) -> int:\n    return a + b\n",
        encoding="utf-8",
    )
    output_path = tmp_path / "missing" / "out.nl"

    result = _run_nlsc(
        ["atomize", str(source_path), "--output", str(output_path), "--json"],
        cwd=REPO_ROOT,
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "atomize"
    assert payload["diagnostics"] == [
        {
            "code": "EATOM002",
            "file": str(source_path),
            "line": None,
            "col": None,
            "message": payload["diagnostics"][0]["message"],
            "hint": "Check the output path and local filesystem permissions, then rerun `nlsc atomize`.",
        }
    ]
    assert str(output_path) in payload["diagnostics"][0]["message"]
    assert "No such file or directory" in payload["diagnostics"][0]["message"]


def test_atomize_json_reports_default_output_derivation_failure(tmp_path: Path) -> None:
    result = _run_nlsc(["atomize", ".", "--json"], cwd=tmp_path)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "atomize"
    assert payload["file"] == "."
    assert payload["diagnostics"] == [
        {
            "code": "EATOM002",
            "file": ".",
            "line": None,
            "col": None,
            "message": payload["diagnostics"][0]["message"],
            "hint": "Check the output path and local filesystem permissions, then rerun `nlsc atomize`.",
        }
    ]
    assert "Atomize failed" in payload["diagnostics"][0]["message"]
    assert result.stderr == ""


def test_diff_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_diff.nl"

    result = _run_nlsc(["diff", str(missing_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "diff"
    assert payload["diagnostics"][0]["code"] == "EFILE001"


def test_diff_json_reports_parse_error(tmp_path: Path) -> None:
    source_path = tmp_path / "diff_broken.nl"
    source_path.write_text(
        """\
@module diff-broken
@target python

[main]
PURPOSE: Broken diff
LOGIC:
  bad step
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "diff", str(source_path), "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "diff"
    assert payload["diagnostics"] == [
        {
            "code": "EPARSE001",
            "file": str(source_path),
            "line": 7,
            "col": None,
            "message": "Invalid LOGIC step format; expected numbered step like '1. ...'",
            "hint": "Rewrite the line as a numbered LOGIC step like '1. ...'.",
        }
    ]


def test_diff_json_success_returns_structured_payload_without_lockfile(
    tmp_path: Path,
) -> None:
    source_path = tmp_path / "diff_ok.nl"
    source_path.write_text(
        """\
@module diff-ok
@target python

[main]
PURPOSE: Compare source
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(["diff", str(source_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 0
    payload = _load_json_output(result)
    assert payload == {
        "ok": True,
        "command": "diff",
        "diagnostics": [],
        "file": str(source_path),
        "lockfile": str(source_path.with_suffix(".nl.lock")),
        "lockfile_present": False,
        "lockfile_loaded": False,
        "lockfile_error": None,
        "mode": "changes",
        "summary": {
            "unchanged": 0,
            "modified": 0,
            "new": 1,
            "removed": 0,
        },
        "changes": [
            {
                "identifier": "main",
                "status": "new",
                "details": "New ANLU added",
            }
        ],
        "text": "[main] - new",
    }


def test_diff_json_success_returns_stat_payload(tmp_path: Path) -> None:
    source_path = tmp_path / "diff_stat.nl"
    source_path.write_text(
        """\
@module diff-stat
@target python

[main]
PURPOSE: Compare source
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(["diff", str(source_path), "--json", "--stat"], cwd=REPO_ROOT)

    assert result.returncode == 0
    payload = _load_json_output(result)
    assert payload["ok"] is True
    assert payload["command"] == "diff"
    assert payload["diagnostics"] == []
    assert payload["mode"] == "stat"
    assert payload["lockfile_present"] is False
    assert payload["lockfile_loaded"] is False
    assert payload["lockfile_error"] is None
    assert payload["summary"] == {
        "unchanged": 0,
        "modified": 0,
        "new": 1,
        "removed": 0,
    }
    assert payload["changes"] == [
        {
            "identifier": "main",
            "status": "new",
            "details": "New ANLU added",
        }
    ]
    assert payload["text"] == "1 new"


def test_diff_json_success_returns_full_payload(tmp_path: Path) -> None:
    source_path = tmp_path / "diff_full.nl"
    source_path.write_text(
        """\
@module diff-full
@target python

[main]
PURPOSE: Compare source
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(["diff", str(source_path), "--json", "--full"], cwd=REPO_ROOT)

    assert result.returncode == 0
    payload = _load_json_output(result)
    assert payload["ok"] is True
    assert payload["command"] == "diff"
    assert payload["diagnostics"] == []
    assert payload["mode"] == "full"
    assert payload["lockfile_present"] is False
    assert payload["lockfile_loaded"] is False
    assert payload["lockfile_error"] is None
    assert payload["summary"] == {
        "unchanged": 0,
        "modified": 0,
        "new": 1,
        "removed": 0,
    }
    assert payload["changes"] == [
        {
            "identifier": "main",
            "status": "new",
            "details": "New ANLU added",
        }
    ]
    assert (
        payload["text"]
        == "No existing compiled output to diff against: diff_full.py.\n[main] - new"
    )


def test_diff_json_success_returns_full_payload_for_typescript_target(
    tmp_path: Path,
) -> None:
    source_path = tmp_path / "diff_full_typescript.nl"
    output_path = source_path.with_suffix(".ts")
    source_path.write_text(
        """\
@module diff-full-typescript
@target typescript

[main]
PURPOSE: Compare source
RETURNS: 1
""",
        encoding="utf-8",
    )
    output_path.write_text(
        "export function main(): number {\n  return 0;\n}\n", encoding="utf-8"
    )

    result = _run_nlsc(["diff", str(source_path), "--json", "--full"], cwd=REPO_ROOT)

    assert result.returncode == 0
    payload = _load_json_output(result)
    assert payload["ok"] is True
    assert payload["command"] == "diff"
    assert payload["diagnostics"] == []
    assert payload["mode"] == "full"
    assert payload["text"].startswith(
        "--- a/diff_full_typescript.ts\n+++ b/diff_full_typescript.ts\n"
    )


def test_diff_json_reports_unreadable_lockfile_in_payload(tmp_path: Path) -> None:
    source_path = tmp_path / "diff_bad_lock.nl"
    lock_path = source_path.with_suffix(".nl.lock")
    source_path.write_text(
        """\
@module diff-bad-lock
@target python

[main]
PURPOSE: Compare source
RETURNS: 1
""",
        encoding="utf-8",
    )
    lock_path.mkdir()

    result = _run_nlsc(["diff", str(source_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 0
    payload = _load_json_output(result)
    assert payload["ok"] is True
    assert payload["command"] == "diff"
    assert payload["diagnostics"] == []
    assert payload["lockfile"] == str(lock_path)
    assert payload["lockfile_present"] is True
    assert payload["lockfile_loaded"] is False
    assert payload["lockfile_error"]
    assert "regular file" in payload["lockfile_error"].lower()
    assert payload["summary"] == {
        "unchanged": 0,
        "modified": 0,
        "new": 1,
        "removed": 0,
    }
    assert payload["changes"] == [
        {
            "identifier": "main",
            "status": "new",
            "details": "New ANLU added",
        }
    ]
    assert payload["text"] == "[main] - new"
    assert result.stderr == ""


def test_test_json_reports_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_test.nl"

    result = _run_nlsc(["test", str(missing_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "test"
    assert payload["diagnostics"] == [
        {
            "code": "EFILE001",
            "file": str(missing_path),
            "line": None,
            "col": None,
            "message": f"File not found: {missing_path}",
            "hint": "Check that the path exists and try again.",
        }
    ]


def test_test_json_reports_parse_error(tmp_path: Path) -> None:
    source_path = tmp_path / "broken_test.nl"
    source_path.write_text(
        """\
@module broken-test
@target python

[main]
PURPOSE: Broken test file
LOGIC:
  bad step
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "test", str(source_path), "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "test"
    assert payload["diagnostics"] == [
        {
            "code": "EPARSE001",
            "file": str(source_path),
            "line": 7,
            "col": None,
            "message": "Invalid LOGIC step format; expected numbered step like '1. ...'",
            "hint": "Rewrite the line as a numbered LOGIC step like '1. ...'.",
        }
    ]


def test_lock_check_json_reports_missing_lockfile(tmp_path: Path) -> None:
    source_path = tmp_path / "lock_missing.nl"
    source_path.write_text(
        """\
@module lock-missing
@target python

[main]
PURPOSE: Missing lock
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(["lock:check", str(source_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "lock:check"
    assert payload["diagnostics"] == [
        {
            "code": "ELOCK001",
            "file": str(source_path.with_suffix(".nl.lock")),
            "line": None,
            "col": None,
            "message": f"Lockfile not found: {source_path.with_suffix('.nl.lock')}",
            "hint": "Run `nlsc compile <file>` or `nlsc lock:update <file>` to generate a lockfile.",
        }
    ]


def test_lock_check_json_reports_outdated_lockfile(tmp_path: Path) -> None:
    source_path = tmp_path / "lock_outdated.nl"
    source_path.write_text(
        """\
@module lock-outdated
@target python

[main]
PURPOSE: Updated lock
RETURNS: 2
""",
        encoding="utf-8",
    )
    lock_path = source_path.with_suffix(".nl.lock")
    lock_path.write_text(
        """\
# DO NOT EDIT - Generated by nlsc
schema_version: 1
generated_at: 2026-04-02T00:00:00+00:00
compiler_version: 0.0.0
llm_backend: mock

modules:
  lock-outdated:
    source_hash: sha256:deadbeefcafe
    anlus:
      main:
        source_hash: sha256:oldoldoldold
        output_hash: sha256:outdatedcode
        output_lines: 1

targets:
  python:
    file: lock_outdated.py
    hash: sha256:outdatedcode
    lines: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "lock:check", str(source_path), "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "lock:check"
    assert payload["diagnostics"] == [
        {
            "code": "ELOCK002",
            "file": str(source_path),
            "line": 4,
            "col": 1,
            "message": "ANLU main has changed since lock",
            "hint": "Run `nlsc compile <file>` or `nlsc lock:update <file>` to regenerate the lockfile.",
        }
    ]


def test_lock_update_json_reports_parse_error(tmp_path: Path) -> None:
    source_path = tmp_path / "lock_update_broken.nl"
    source_path.write_text(
        """\
@module lock-update-broken
@target python

[main]
PURPOSE: Broken lock update
LOGIC:
  bad step
RETURNS: 1
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "lock:update", str(source_path), "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "lock:update"
    assert payload["diagnostics"] == [
        {
            "code": "EPARSE001",
            "file": str(source_path),
            "line": 7,
            "col": None,
            "message": "Invalid LOGIC step format; expected numbered step like '1. ...'",
            "hint": "Rewrite the line as a numbered LOGIC step like '1. ...'.",
        }
    ]


def test_lock_update_json_success_returns_structured_payload(tmp_path: Path) -> None:
    source_path = tmp_path / "lock_update_ok.nl"
    output_path = tmp_path / "lock_update_ok.py"
    lock_path = tmp_path / "lock_update_ok.nl.lock"
    source_path.write_text(
        """\
@module lock-update-ok
@target python

[main]
PURPOSE: Refresh lock
RETURNS: 1
""",
        encoding="utf-8",
    )
    output_path.write_text("def main() -> int:\n    return 1\n", encoding="utf-8")

    result = _run_nlsc(
        ["--parser", "regex", "lock:update", str(source_path), "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 0
    payload = _load_json_output(result)
    assert payload == {
        "ok": True,
        "command": "lock:update",
        "diagnostics": [],
        "file": str(source_path),
        "lockfile": str(lock_path),
        "output": str(output_path),
        "target": "python",
        "anlu_count": 1,
    }


def test_lock_update_json_reports_compiled_artifact_read_failure(
    capsys: Any, monkeypatch: Any, tmp_path: Path
) -> None:
    source_path = tmp_path / "lock_update_read_fail.nl"
    output_path = tmp_path / "lock_update_read_fail.py"
    source_path.write_text(
        "@module lock-update-read-fail\n@target python\n\n[main]\nPURPOSE: Ok\nRETURNS: 1\n",
        encoding="utf-8",
    )
    output_path.write_text("def main() -> int:\n    return 1\n", encoding="utf-8")
    real_read_text = Path.read_text

    def fake_read_text(self: Path, *args: Any, **kwargs: Any) -> str:
        if self == output_path:
            raise OSError("access denied")
        return real_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", fake_read_text)

    exit_code = main(["lock:update", str(source_path), "--json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload == {
        "ok": False,
        "command": "lock:update",
        "diagnostics": [
            {
                "code": "EARTIFACT001",
                "file": str(output_path),
                "line": None,
                "col": None,
                "message": f"Failed to read artifact: {output_path} (access denied)",
                "hint": "Check that the compiled artifact exists and is readable, or remove it so `nlsc lock:update` can regenerate it.",
            }
        ],
        "file": str(source_path),
    }
    assert captured.err == ""


def test_lock_update_json_reports_lockfile_write_failure(
    capsys: Any, monkeypatch: Any, tmp_path: Path
) -> None:
    source_path = tmp_path / "lock_update_lock_write_fail.nl"
    output_path = tmp_path / "lock_update_lock_write_fail.py"
    lock_path = tmp_path / "lock_update_lock_write_fail.nl.lock"
    source_path.write_text(
        "@module lock-update-lock-write-fail\n@target python\n\n[main]\nPURPOSE: Ok\nRETURNS: 1\n",
        encoding="utf-8",
    )
    output_path.write_text("def main() -> int:\n    return 1\n", encoding="utf-8")
    real_write_text = Path.write_text

    def fake_write_text(self: Path, data: str, *args: Any, **kwargs: Any) -> int:
        if self == lock_path:
            raise OSError("disk full")
        return real_write_text(self, data, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", fake_write_text)

    exit_code = main(["lock:update", str(source_path), "--json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload == {
        "ok": False,
        "command": "lock:update",
        "diagnostics": [
            {
                "code": "ELOCK003",
                "file": str(lock_path),
                "line": None,
                "col": None,
                "message": f"Failed to write lockfile: {lock_path} (disk full)",
                "hint": "Check the destination path and filesystem permissions, then rerun `nlsc lock:update`.",
            }
        ],
        "file": str(source_path),
    }
    assert captured.err == ""


def test_test_json_reports_resolution_error(tmp_path: Path) -> None:
    source_path = tmp_path / "missing_dep_test.nl"
    source_path.write_text(
        """\
@module missing-dep-test
@target python

[main]
PURPOSE: Needs helper
DEPENDS: [helper]
RETURNS: 1

@test [main] {
  main() == 1
}
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "test", str(source_path), "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "test"
    assert payload["diagnostics"] == [
        {
            "code": "E_RESOLUTION",
            "file": str(source_path),
            "line": 4,
            "col": 1,
            "message": "main: Missing dependency: helper",
            "hint": "Define [helper] or remove it from DEPENDS.",
        }
    ]


def test_test_json_reports_stdlib_use_error(tmp_path: Path) -> None:
    source_path = tmp_path / "use_missing_test.nl"
    source_path.write_text(
        """\
@module use-missing-test
@target python
@use math.missing

[main]
PURPOSE: No-op
RETURNS: 1

@test [main] {
  main() == 1
}
""",
        encoding="utf-8",
    )

    result = _run_nlsc(
        ["--parser", "regex", "test", str(source_path), "--json"], cwd=REPO_ROOT
    )

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "test"
    assert payload["diagnostics"] == [
        {
            "code": "EUSE001",
            "file": str(source_path),
            "line": 3,
            "col": 1,
            "message": "Missing stdlib domain: math.missing",
            "hint": "Add the module under an stdlib root or pass --stdlib-path.",
        }
    ]


def test_test_json_reports_pytest_failures(tmp_path: Path) -> None:
    source_path = tmp_path / "failing_test.nl"
    source_path.write_text(
        """\
@module failing-test
@target python

[always-one]
PURPOSE: Always returns one
INPUTS:
  - value: number
RETURNS: 1

@test [always-one] {
  always_one(5) == 5
}
""",
        encoding="utf-8",
    )

    result = _run_nlsc(["test", str(source_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "test"
    assert payload["ok"] is False
    assert payload["diagnostics"] == [
        {
            "code": "ETEST001",
            "file": str(source_path),
            "line": None,
            "col": None,
            "message": "Generated tests failed with pytest exit code 1.",
            "hint": "Inspect pytest_stdout and pytest_stderr for failing assertions or setup errors.",
        }
    ]
    assert payload["total_cases"] == 1
    assert payload["pytest_exit_code"] == 1
    assert "assert 1 == 5" in payload["pytest_stdout"]


def test_test_json_reports_success_metadata(tmp_path: Path) -> None:
    source_path = tmp_path / "passing_test.nl"
    source_path.write_text(
        """\
@module passing-test
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

@test [add] {
  add(2, 3) == 5
  add(4, 1) == 5
}
""",
        encoding="utf-8",
    )

    result = _run_nlsc(["test", str(source_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 0
    payload = _load_json_output(result)
    assert payload["ok"] is True
    assert payload["command"] == "test"
    assert payload["diagnostics"] == []
    assert payload["file"] == str(source_path)
    assert payload["total_cases"] == 2
    assert payload["pytest_exit_code"] == 0
    assert payload["pytest_stdout"]


def test_test_json_verbose_preserves_clean_stdout_on_failure(tmp_path: Path) -> None:
    source_path = tmp_path / "verbose_failing_test.nl"
    source_path.write_text(
        """\
@module verbose-failing-test
@target python

[always-one]
PURPOSE: Always returns one
INPUTS:
  - value: number
RETURNS: 1

@test [always-one] {
  always_one(5) == 5
}
""",
        encoding="utf-8",
    )

    result = _run_nlsc(["test", str(source_path), "--json", "-v"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "test"
    assert payload["ok"] is False
    assert payload["pytest_exit_code"] == 1
    assert result.stderr == ""
    assert result.stdout.lstrip().startswith("{")
    assert (
        "============================= test session starts ============================="
        in payload["pytest_stdout"]
    )


def test_test_json_verbose_preserves_clean_stdout_on_success(tmp_path: Path) -> None:
    source_path = tmp_path / "verbose_passing_test.nl"
    source_path.write_text(
        """\
@module verbose-passing-test
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

@test [add] {
  add(2, 3) == 5
}
""",
        encoding="utf-8",
    )

    result = _run_nlsc(["test", str(source_path), "--json", "-v"], cwd=REPO_ROOT)

    assert result.returncode == 0
    payload = _load_json_output(result)
    assert payload["command"] == "test"
    assert payload["ok"] is True
    assert payload["pytest_exit_code"] == 0
    assert result.stderr == ""
    assert result.stdout.lstrip().startswith("{")
    assert "test session starts" in payload["pytest_stdout"]


def test_watch_json_reports_missing_directory(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_watch_dir"

    result = _run_nlsc(["watch", str(missing_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "watch"
    assert payload["diagnostics"] == [
        {
            "code": "EFILE001",
            "file": str(missing_path),
            "line": None,
            "col": None,
            "message": f"Directory not found: {missing_path}",
            "hint": "Check that the path exists and try again.",
        }
    ]


def test_watch_json_reports_not_a_directory(tmp_path: Path) -> None:
    source_path = tmp_path / "not_a_dir.nl"
    source_path.write_text("@module watch\n@target python\n", encoding="utf-8")

    result = _run_nlsc(["watch", str(source_path), "--json"], cwd=REPO_ROOT)

    assert result.returncode == 1
    payload = _load_json_output(result)
    assert payload["command"] == "watch"
    assert payload["diagnostics"] == [
        {
            "code": "EWATCH001",
            "file": str(source_path),
            "line": None,
            "col": None,
            "message": f"Watch path is not a directory: {source_path}",
            "hint": "Pass a directory path to `nlsc watch` and try again.",
        }
    ]
