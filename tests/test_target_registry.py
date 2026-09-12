"""Issue #147: the target emitter registry.

A target is a `TargetEmitter` registration; the CLI, capability matrix,
and lockfile identity all read the registry, so a plugin can add a target
without editing core parser/resolver/CLI code.
"""

from __future__ import annotations

import json

from nlsc.capabilities import (
    EMITTER_SEMANTICS_VERSION,
    TARGET_CAPABILITIES,
    capability_gaps,
    emitter_semantics_version,
)
from nlsc.cli import main
from nlsc.parser import parse_nl_file
from nlsc.targets import (
    TARGET_REGISTRY,
    TargetEmitter,
    get_target,
    register_target,
    registered_target_names,
)

SIMPLE = """@module registry_probe
[add]
PURPOSE: add
INPUTS:
  - a: number
  - b: number
LOGIC:
  1. total = a + b
RETURNS: total
"""


def _write(tmp_path, source: str = SIMPLE):
    path = tmp_path / "probe.nl"
    path.write_text(source, encoding="utf-8")
    return path


# --------------------------------------------------------------------------
# Built-in registrations
# --------------------------------------------------------------------------


def test_builtin_targets_are_registered():
    names = registered_target_names()
    assert {"python", "typescript"} <= set(names)
    assert get_target("python").module_suffix == ".py"
    assert get_target("typescript").module_suffix == ".ts"


def test_capability_views_match_the_registry():
    # The views snapshot load-time registrations; installed third-party
    # plugins legitimately add entries, so check the built-ins only.
    for name in ("python", "typescript"):
        entry = TARGET_REGISTRY[name]
        assert TARGET_CAPABILITIES[name] == dict(entry.capabilities)
        assert EMITTER_SEMANTICS_VERSION[name] == entry.semantics_version


def test_semantics_markers_are_preserved():
    # Lock identity embeds these values; a plugin refactor must not change
    # them (bump deliberately, per the marker policy).
    assert emitter_semantics_version("python") == "py-3"
    assert emitter_semantics_version("typescript") == "ts-2"
    assert emitter_semantics_version("nope") == "unknown"


def test_registry_drives_compile_output_suffix(tmp_path, capsys):
    path = _write(tmp_path)
    assert main(["compile", str(path), "-t", "typescript"]) == 0
    assert (tmp_path / "probe.ts").exists()


def test_unknown_target_is_rejected_with_registered_list(tmp_path, capsys):
    import pytest

    path = _write(tmp_path)
    with pytest.raises(SystemExit) as excinfo:
        main(["compile", str(path), "-t", "rust"])
    assert excinfo.value.code == 2
    # argparse choices come from the registry; unregistered targets are
    # rejected before any parsing or emission work.
    assert "invalid choice: 'rust'" in capsys.readouterr().err


# --------------------------------------------------------------------------
# Plugin registration
# --------------------------------------------------------------------------


def _stub_emitter(name: str = "stub") -> TargetEmitter:
    def emit_stub(nl_file, *, scaffold_anlus=None) -> str:
        names = ", ".join(f"# {a.identifier}" for a in nl_file.anlus)
        return f"// stub target\n{names}\n"

    def validate_stub(output_path: str) -> str | None:
        text = open(output_path, encoding="utf-8").read()
        return None if text.startswith("// stub") else "missing stub header"

    return TargetEmitter(
        name=name,
        module_suffix=".stub",
        test_suffix=".stub",
        emit_module=emit_stub,
        emit_tests=None,
        capabilities={"loop_steps": False},
        fatal_capabilities=frozenset({"loop_steps"}),
        semantics_version="stub-1",
        validate_output=validate_stub,
    )


def test_plugin_target_drives_compile_end_to_end(tmp_path, capsys, monkeypatch):
    """A plugin target works through compile with no core-file edits."""
    monkeypatch.setitem(TARGET_REGISTRY, "stub", _stub_emitter())
    path = _write(tmp_path)
    assert main(["compile", str(path), "-t", "stub"]) == 0
    artifact = (tmp_path / "probe.stub").read_text(encoding="utf-8")
    assert artifact.startswith("// stub target")
    assert "# add" in artifact
    # Lock identity records the plugin's own semantics marker.
    lock = (tmp_path / "probe.nl.lock").read_text(encoding="utf-8")
    assert "semantics_version: stub-1" in lock


def test_plugin_target_reaches_the_capability_gate(tmp_path, capsys, monkeypatch):
    monkeypatch.setitem(TARGET_REGISTRY, "stub", _stub_emitter())
    loop = SIMPLE.replace(
        "LOGIC:\n  1. total = a + b",
        "LOGIC:\n  1. total = 0\n  2. FOR each item IN items: total = total + item",
    ).replace("RETURNS: total\n", "RETURNS: total\n")
    loop = loop.replace("  - b: number", "  - b: number\n  - items: list of number")
    path = _write(tmp_path, loop)
    assert main(["compile", str(path), "-t", "stub"]) == 1
    captured = capsys.readouterr()
    assert "ETARGET002" in captured.err
    assert "does not support FOR each LOGIC loop steps" in captured.err


def test_plugin_registration_rejects_duplicates():
    import pytest

    existing = get_target("python")
    assert existing is not None
    with pytest.raises(ValueError):
        register_target(existing)
    register_target(existing, replace=True)  # explicit replace is allowed


def test_plugin_target_json_payload(tmp_path, capsys, monkeypatch):
    monkeypatch.setitem(TARGET_REGISTRY, "stub", _stub_emitter())
    path = _write(tmp_path)
    assert main(["compile", "--json", str(path), "-t", "stub"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["target"] == "stub"


LOOP_SOURCE = """@module registry_loop
[total-all]
PURPOSE: sum every value
INPUTS:
  - items: list of number
LOGIC:
  1. total = 0
  2. FOR each item IN items: total = total + item
RETURNS: total
"""


def test_registry_capability_gap_uses_plugin_fatal_set(monkeypatch):
    monkeypatch.setitem(TARGET_REGISTRY, "stub", _stub_emitter())
    assert capability_gaps(parse_nl_file(SIMPLE, source_path="x.nl"), "stub") == []
    gaps = capability_gaps(
        parse_nl_file(LOOP_SOURCE, source_path="loop.nl"), "stub"
    )
    assert [gap.feature for gap in gaps] == ["loop_steps"]
    assert gaps[0].fatal is True


# --------------------------------------------------------------------------
# Public registration API and entry-point discovery
# --------------------------------------------------------------------------


def test_register_target_happy_path(tmp_path, capsys, monkeypatch):
    registered = _stub_emitter("registered-stub")
    register_target(registered)
    try:
        assert get_target("registered-stub") is registered
        path = _write(tmp_path)
        assert main(["compile", str(path), "-t", "registered-stub"]) == 0
        assert (tmp_path / "probe.stub").exists()
    finally:
        TARGET_REGISTRY.pop("registered-stub", None)


def test_plugin_validator_failure_fails_compile(tmp_path, capsys, monkeypatch):
    def validate_always_fails(output_path: str) -> str | None:
        return "stub artifact rejected by plugin validator"

    entry = _stub_emitter("validated-stub")
    import dataclasses

    monkeypatch.setitem(
        TARGET_REGISTRY,
        "validated-stub",
        dataclasses.replace(entry, validate_output=validate_always_fails),
    )
    path = _write(tmp_path)
    exit_code = main(["compile", str(path), "-t", "validated-stub"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "output validation failed" in captured.err
    assert "plugin validator" in captured.err


def test_entry_point_plugins_load_once_and_isolate_failures(monkeypatch):
    import nlsc.targets as targets_module

    calls: list[str] = []

    class _FakeEntryPoint:
        def __init__(self, name: str, factory):
            self.name = name
            self._factory = factory

        def load(self):
            return self._factory

    def _make_plugin() -> TargetEmitter:
        calls.append("loaded")
        return _stub_emitter("entry-point-stub")

    def _broken_factory():
        raise RuntimeError("plugin is broken")

    def _fake_entry_points(*, group: str):
        assert group == "nlsc.targets"
        return [
            _FakeEntryPoint("ok", _make_plugin),
            _FakeEntryPoint("broken", _broken_factory),
            _FakeEntryPoint("not-an-emitter", lambda: "nope"),
        ]

    import importlib.metadata as metadata

    monkeypatch.setattr(targets_module, "_plugins_loaded", False)
    monkeypatch.setattr(metadata, "entry_points", _fake_entry_points)
    try:
        targets_module.ensure_plugins_loaded()
        assert calls == ["loaded"]
        assert get_target("entry-point-stub") is not None
        # Idempotent: a second call must not reload.
        targets_module.ensure_plugins_loaded()
        assert calls == ["loaded"]
    finally:
        TARGET_REGISTRY.pop("entry-point-stub", None)


def test_plugin_target_without_extractor_skips_generated_code(tmp_path, capsys, monkeypatch):
    """A target with no extractor records name hashes, not foreign guesses."""
    monkeypatch.setitem(TARGET_REGISTRY, "stub", _stub_emitter())
    path = _write(tmp_path)
    assert main(["compile", str(path), "-t", "stub"]) == 0
    lock = (tmp_path / "probe.nl.lock").read_text(encoding="utf-8")
    assert "generated_code" not in lock
