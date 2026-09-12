"""Target emitter registry (Issue #147).

Emitter plugins register a :class:`TargetEmitter` here instead of editing
the CLI, the capability matrix, or the parser/resolver. The bundled
Python and TypeScript backends are registered through the same public
``register_target`` API a third-party plugin uses.

Third-party packages contribute targets through the ``nlsc.targets``
entry-point group: each entry point must load to a **zero-argument
factory returning a :class:`TargetEmitter`** (e.g.
``my_pkg.plugin:make_target``). Plugin loading happens lazily on first
lookup; a plugin that raises, returns a non-``TargetEmitter``, or
collides with an already-registered name is skipped so a broken plugin
can never break the CLI. Call :func:`ensure_plugins_loaded` to force
discovery (the capability views in ``nlsc.capabilities`` do this at
import so their snapshots include installed plugins).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping, Optional

from .schema import NLFile

ENTRY_POINTS_GROUP = "nlsc.targets"


@dataclass(frozen=True)
class TargetEmitter:
    """One emission target: how to emit, validate, and what it supports.

    ``capabilities`` maps feature names (``literal_blocks``, ``main_block``,
    ``property_tests``, ``loop_steps``) to support booleans;
    ``fatal_capabilities`` names the unsupported features whose loss would
    break the program (as opposed to losing test coverage, which is a
    warning). ``validate_output`` optionally post-checks an emitted
    artifact and returns an error string or None.
    """

    name: str
    module_suffix: str
    test_suffix: str
    emit_module: Callable[..., str]
    emit_tests: Optional[Callable[[NLFile], Optional[str]]]
    capabilities: Mapping[str, bool]
    fatal_capabilities: frozenset[str]
    semantics_version: str
    validate_output: Optional[Callable[[str], Optional[str]]] = None
    # Optional per-function extractor for lockfile generated-code slots:
    # (module_code, function_name) -> body or "". None means the target's
    # functions cannot be described individually; lock entries then record
    # the function-name hash instead.
    extract_function_code: Optional[Callable[[str, str], str]] = None


TARGET_REGISTRY: dict[str, TargetEmitter] = {}

_plugins_loaded = False


def register_target(entry: TargetEmitter, *, replace: bool = False) -> None:
    """Register an emission target (the plugin extension point)."""
    if entry.name in TARGET_REGISTRY and not replace:
        raise ValueError(f"target '{entry.name}' is already registered")
    TARGET_REGISTRY[entry.name] = entry


def _load_plugin_targets() -> None:
    global _plugins_loaded
    if _plugins_loaded:
        return
    _plugins_loaded = True
    try:
        from importlib.metadata import entry_points

        discovered = entry_points(group=ENTRY_POINTS_GROUP)
    except Exception:
        return
    for entry_point in discovered:
        try:
            factory = entry_point.load()
            entry = factory()
            if isinstance(entry, TargetEmitter):
                register_target(entry)
        except Exception:
            # A broken third-party plugin must never break the CLI.
            continue


def ensure_plugins_loaded() -> None:
    """Discover entry-point plugins now (idempotent)."""
    _load_plugin_targets()


def get_target(name: str) -> Optional[TargetEmitter]:
    """Look up a registered target by name (plugins load lazily)."""
    _load_plugin_targets()
    return TARGET_REGISTRY.get(name)


def registered_target_names() -> list[str]:
    _load_plugin_targets()
    return sorted(TARGET_REGISTRY)


def _register_builtin_targets() -> None:
    def emit_python_module(
        nl_file: NLFile, *, scaffold_anlus: Optional[set[str]] = None
    ) -> str:
        # Resolve through the module so the emitter stays patchable at its
        # source of truth (tests monkeypatch nlsc.emitter.emit_python).
        from . import emitter

        return emitter.emit_python(nl_file, mode="mock", scaffold_anlus=scaffold_anlus)

    def emit_typescript_module(
        nl_file: NLFile, *, scaffold_anlus: Optional[set[str]] = None
    ) -> str:
        from . import emitter_typescript

        return emitter_typescript.emit_typescript(
            nl_file, scaffold_anlus=scaffold_anlus
        )

    def emit_python_tests(nl_file: NLFile) -> Optional[str]:
        from . import emitter

        return emitter.emit_tests(nl_file)

    def emit_typescript_tests(nl_file: NLFile) -> Optional[str]:
        from . import emitter_typescript

        return emitter_typescript.emit_tests_typescript(nl_file)

    def validate_python_output(output_path: str) -> Optional[str]:
        import py_compile

        try:
            py_compile.compile(output_path, doraise=True)
        except py_compile.PyCompileError as exc:
            return str(exc)
        return None

    def extract_python_function(module_code: str, func_name: str) -> str:
        from .lockfile import extract_function_code

        return extract_function_code(module_code, func_name, target="python")

    def extract_typescript_function(module_code: str, func_name: str) -> str:
        from .lockfile import extract_function_code

        return extract_function_code(module_code, func_name, target="typescript")

    # py-3: IR-rendered checked bodies (canonical record kwargs); coded
    # guards raise with `.code` attached (#202).
    register_target(
        TargetEmitter(
            name="python",
            module_suffix=".py",
            test_suffix=".py",
            emit_module=emit_python_module,
            emit_tests=emit_python_tests,
            capabilities={
                "literal_blocks": True,
                "main_block": True,
                "property_tests": True,
                "loop_steps": True,
            },
            fatal_capabilities=frozenset(
                {"literal_blocks", "main_block", "loop_steps"}
            ),
            semantics_version="py-3",
            validate_output=validate_python_output,
            extract_function_code=extract_python_function,
        )
    )

    # ts-2: FOR-each loop steps are an explicit capability gap, and
    # branch-joined values hoist as `let` (#202).
    register_target(
        TargetEmitter(
            name="typescript",
            module_suffix=".ts",
            test_suffix=".ts",
            emit_module=emit_typescript_module,
            emit_tests=emit_typescript_tests,
            capabilities={
                "literal_blocks": False,
                "main_block": False,
                "property_tests": False,
                "loop_steps": False,
            },
            fatal_capabilities=frozenset(
                {"literal_blocks", "main_block", "loop_steps"}
            ),
            semantics_version="ts-2",
            extract_function_code=extract_typescript_function,
        )
    )


_register_builtin_targets()
