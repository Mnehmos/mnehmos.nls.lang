"""Central catalog of stable CLI error codes."""

from __future__ import annotations

from dataclasses import dataclass

ECLI001 = "ECLI001"
EEXPLAIN001 = "EEXPLAIN001"
EINIT001 = "EINIT001"
EINIT002 = "EINIT002"
EINIT003 = "EINIT003"
EATOM001 = "EATOM001"
EATOM002 = "EATOM002"
EFILE001 = "EFILE001"
EPARSE001 = "EPARSE001"
EPARSE002 = "EPARSE002"
EUSE001 = "EUSE001"
E_RESOLUTION = "E_RESOLUTION"
ETEST001 = "ETEST001"
ECONTRACT001 = "ECONTRACT001"
ETARGET001 = "ETARGET001"
EVALIDATE001 = "EVALIDATE001"
E_RUN = "E_RUN"
EEXEC001 = "EEXEC001"
EGRAPH001 = "EGRAPH001"
EGRAPH002 = "EGRAPH002"
ELOCK001 = "ELOCK001"
ELOCK002 = "ELOCK002"
ELSP001 = "ELSP001"
ELSP002 = "ELSP002"
EASSOC001 = "EASSOC001"
EASSOC002 = "EASSOC002"
EASSOC003 = "EASSOC003"
EASSOC004 = "EASSOC004"
EWATCH001 = "EWATCH001"
EWATCH002 = "EWATCH002"


@dataclass(frozen=True)
class ErrorDefinition:
    code: str
    title: str
    summary: str
    emitted_by: tuple[str, ...]
    common_causes: tuple[str, ...]
    next_steps: tuple[str, ...]


ERROR_CATALOG: dict[str, ErrorDefinition] = {
    ECLI001: ErrorDefinition(
        code=ECLI001,
        title="CLI usage error",
        summary="Argument parsing failed before command dispatch, and `--json` requested a structured diagnostic instead of raw argparse stderr output.",
        emitted_by=(
            "init",
            "compile",
            "verify",
            "run",
            "test",
            "graph",
            "atomize",
            "diff",
            "lsp",
            "assoc",
            "watch",
            "lock:check",
            "lock:update",
            "unknown-subcommand",
        ),
        common_causes=(
            "A required CLI argument such as `file` was omitted.",
            "An option received an invalid value or the subcommand name is not recognized.",
        ),
        next_steps=(
            "Rerun the command with `--help` to inspect the required arguments and valid options.",
            "If you are using JSON automation, keep `--json` on the command so parse failures continue to return structured diagnostics.",
        ),
    ),
    EEXPLAIN001: ErrorDefinition(
        code=EEXPLAIN001,
        title="Unknown explain error code",
        summary="`nlsc explain` was asked to document an error code that is not present in the stable CLI error catalog.",
        emitted_by=("explain",),
        common_causes=(
            "The requested code is misspelled or uses the wrong prefix/number.",
            "The code refers to a diagnostic path that has not been cataloged yet in the current release.",
        ),
        next_steps=(
            "Run `nlsc explain --json ECLI001` or inspect the reported known codes to choose a cataloged error code.",
            "If you expected the code to exist, update the error catalog and reference docs before relying on it in automation.",
        ),
    ),
    EINIT001: ErrorDefinition(
        code=EINIT001,
        title="Init target path is invalid",
        summary="`nlsc init` received a target path that is blank or resolves to a non-directory filesystem object.",
        emitted_by=("init",),
        common_causes=(
            "Automation passed an empty string or whitespace-only path instead of omitting the optional argument.",
            "The requested init path already exists as a file, so the project scaffold cannot be created there.",
        ),
        next_steps=(
            "Pass a directory path to `nlsc init`, or omit the argument to use the current directory.",
            "If the path already points to a file, remove or rename the conflicting file and rerun the command.",
        ),
    ),
    EINIT002: ErrorDefinition(
        code=EINIT002,
        title="Init directory creation failed",
        summary="`nlsc init` could not create the project directory or one of the scaffold directories it needs.",
        emitted_by=("init",),
        common_causes=(
            "The parent path does not exist or is not writable by the current user.",
            "A permission, path-length, or filesystem error blocked directory creation.",
        ),
        next_steps=(
            "Check that the parent path exists and that you can create directories there, then rerun `nlsc init`.",
            "Inspect the reported path to see which directory creation step failed.",
        ),
    ),
    EINIT003: ErrorDefinition(
        code=EINIT003,
        title="Init project file write failed",
        summary="`nlsc init` created or opened the target project directory but failed while writing a scaffolded project file.",
        emitted_by=("init",),
        common_causes=(
            "The filesystem ran out of space or rejected the write operation.",
            "A permission or locking issue blocked writing `nl.config.yaml` or the package marker files.",
        ),
        next_steps=(
            "Check the destination path and filesystem permissions, then rerun `nlsc init`.",
            "Inspect the reported file path to identify which scaffold file could not be written.",
        ),
    ),
    EFILE001: ErrorDefinition(
        code=EFILE001,
        title="File not found",
        summary="The requested input file does not exist at the provided path.",
        emitted_by=(
            "atomize",
            "compile",
            "verify",
            "run",
            "test",
            "graph",
            "diff",
            "lock:check",
            "lock:update",
            "watch",
        ),
        common_causes=(
            "The .nl path is misspelled or points to the wrong working directory.",
            "The file has not been created yet or was moved.",
        ),
        next_steps=(
            "Check the file path and rerun the command.",
            "Use an absolute path if the current working directory is ambiguous.",
        ),
    ),
    EATOM001: ErrorDefinition(
        code=EATOM001,
        title="Python syntax error",
        summary="`nlsc atomize` could not parse the input Python source into an AST.",
        emitted_by=("atomize",),
        common_causes=(
            "The Python source contains invalid syntax such as an incomplete function signature or statement.",
            "The file was saved with partially edited code that no longer parses.",
        ),
        next_steps=(
            "Fix the reported Python syntax error and rerun `nlsc atomize`.",
            "Run the file through Python tooling such as `python -m py_compile` if you need an independent syntax check.",
        ),
    ),
    EATOM002: ErrorDefinition(
        code=EATOM002,
        title="Atomize write failed",
        summary="`nlsc atomize` hit an unexpected extraction or filesystem error before the `.nl` output could be written successfully.",
        emitted_by=("atomize",),
        common_causes=(
            "The requested output path points to a missing directory or unwritable location.",
            "Atomization hit an unexpected internal failure while reading, extracting, or writing output.",
        ),
        next_steps=(
            "Check the output path and local filesystem permissions, then rerun `nlsc atomize`.",
            "If the failure persists with a valid path, inspect the reported message for the failing read/write step.",
        ),
    ),
    EPARSE001: ErrorDefinition(
        code=EPARSE001,
        title="Parse error",
        summary="The .nl source contains syntax the parser cannot accept.",
        emitted_by=(
            "compile",
            "verify",
            "run",
            "test",
            "graph",
            "diff",
            "watch",
            "lock:check",
            "lock:update",
        ),
        common_causes=(
            "A required directive or section is malformed or missing.",
            "A LOGIC, INPUTS, or GUARDS line does not follow the expected shape.",
        ),
        next_steps=(
            "Use the reported line number to fix the source syntax.",
            "Run `nlsc verify <file>` after editing to confirm the file parses cleanly.",
        ),
    ),
    EPARSE002: ErrorDefinition(
        code=EPARSE002,
        title="Parser backend unavailable",
        summary="The requested parser backend could not be initialized before the command started.",
        emitted_by=(
            "init",
            "compile",
            "verify",
            "run",
            "explain",
            "test",
            "graph",
            "diff",
            "lsp",
            "assoc",
            "watch",
            "lock:check",
            "lock:update",
        ),
        common_causes=(
            "`--parser treesitter` was requested, but the optional tree-sitter dependency is not installed.",
            "The selected parser backend is not available in the current environment.",
        ),
        next_steps=(
            "Install the optional backend with `pip install nlsc[treesitter]`.",
            "Rerun the command with `--parser auto` or `--parser regex` if tree-sitter is not required.",
        ),
    ),
    EUSE001: ErrorDefinition(
        code=EUSE001,
        title="Missing stdlib domain",
        summary="A referenced `@use` domain could not be resolved from the stdlib roots.",
        emitted_by=("compile", "verify", "run", "test", "watch"),
        common_causes=(
            "The domain name is misspelled.",
            "The expected stdlib root was not included via project, CLI, or environment config.",
        ),
        next_steps=(
            "Confirm the expected `v<major>/.../.nl` file exists.",
            "Add a root with `--stdlib-path` or `NLS_STDLIB_PATH` and rerun the command.",
        ),
    ),
    E_RESOLUTION: ErrorDefinition(
        code=E_RESOLUTION,
        title="Dependency resolution error",
        summary="An ANLU dependency graph is invalid or references an unresolved ANLU.",
        emitted_by=("compile", "verify", "run", "test", "watch"),
        common_causes=(
            "A `DEPENDS` entry points at an ANLU that does not exist.",
            "Two or more ANLUs form a dependency cycle.",
        ),
        next_steps=(
            "Define the missing ANLU or remove the dependency reference.",
            "Break cycles so dependency edges form an acyclic graph.",
        ),
    ),
    ETEST001: ErrorDefinition(
        code=ETEST001,
        title="Test execution failed",
        summary="`nlsc test` generated pytest cases, but the test run did not complete successfully.",
        emitted_by=("test",),
        common_causes=(
            "One or more generated assertions failed.",
            "Pytest hit an import, collection, or local environment error while running the generated tests.",
        ),
        next_steps=(
            "Inspect the pytest stdout/stderr captured in the JSON payload.",
            "Fix the generated behavior, source spec, or local test environment and rerun `nlsc test`.",
        ),
    ),
    ECONTRACT001: ErrorDefinition(
        code=ECONTRACT001,
        title="Contract validation error",
        summary="A verified ANLU is missing required contract fields.",
        emitted_by=("verify",),
        common_causes=(
            "An ANLU is missing `PURPOSE:`.",
            "An ANLU is missing `RETURNS:`.",
        ),
        next_steps=("Add the missing contract field to the ANLU and verify again.",),
    ),
    ETARGET001: ErrorDefinition(
        code=ETARGET001,
        title="Unsupported target",
        summary="The requested CLI target is not supported for the selected command.",
        emitted_by=("compile", "run", "watch", "lock:update"),
        common_causes=(
            "The command was given a target that the emitter does not implement.",
            "The source target and CLI override do not match a supported execution path.",
        ),
        next_steps=(
            "Choose a supported target for the command and rerun it.",
            "Use `python` for `nlsc run`.",
        ),
    ),
    EVALIDATE001: ErrorDefinition(
        code=EVALIDATE001,
        title="Generated output validation failed",
        summary="Compiled output was emitted, but the generated artifact failed validation.",
        emitted_by=("compile", "watch"),
        common_causes=(
            "Generated Python did not pass `py_compile`.",
            "Emitter output and the validator expectations are out of sync.",
        ),
        next_steps=(
            "Inspect the generated artifact and the reported validation error.",
            "Fix the emitter bug or the source pattern that triggered it, then recompile.",
        ),
    ),
    E_RUN: ErrorDefinition(
        code=E_RUN,
        title="Unexpected run error",
        summary="`nlsc run` hit an internal error before execution completed.",
        emitted_by=("run",),
        common_causes=(
            "An unexpected parser or command setup failure occurred.",
            "The runtime path hit an unhandled exception before execution started.",
        ),
        next_steps=(
            "Retry with `--verbose` to capture more context.",
            "Inspect the parser backend and command inputs for unexpected state.",
        ),
    ),
    EEXEC001: ErrorDefinition(
        code=EEXEC001,
        title="Execution failed",
        summary="`nlsc run` failed while launching the generated module or the generated program exited with a non-zero status.",
        emitted_by=("run",),
        common_causes=(
            "The temporary execution environment could not be created or used.",
            "Launching the generated module raised an unexpected host-side exception.",
            "The generated program raised a runtime error or called `sys.exit` with a non-zero status.",
        ),
        next_steps=(
            "Inspect the generated module path, stdout, stderr, and runtime environment.",
            "Retry after fixing the local execution issue.",
        ),
    ),
    EGRAPH001: ErrorDefinition(
        code=EGRAPH001,
        title="Graph ANLU not found",
        summary="`nlsc graph --anlu` was asked to render an ANLU identifier that does not exist in the source file.",
        emitted_by=("graph",),
        common_causes=(
            "The requested ANLU identifier is misspelled.",
            "The file was edited and the requested ANLU no longer exists.",
        ),
        next_steps=(
            "Choose one of the ANLU identifiers defined in the file and rerun the command.",
            "Run `nlsc graph <file>` without `--anlu` to inspect the full graph first.",
        ),
    ),
    EGRAPH002: ErrorDefinition(
        code=EGRAPH002,
        title="Unsupported graph output format",
        summary="`nlsc graph --anlu` only supports formats that can render ANLU-level dataflow or FSM output.",
        emitted_by=("graph",),
        common_causes=(
            "`--format dot` was used together with `--anlu`.",
            "A graph output mode was selected that is only implemented for whole-file dependency graphs.",
        ),
        next_steps=(
            "Use `--format mermaid` or `--format ascii` when rendering a specific ANLU.",
            "Drop `--anlu` if you need a whole-file DOT graph.",
        ),
    ),
    ELOCK001: ErrorDefinition(
        code=ELOCK001,
        title="Lockfile unavailable",
        summary="`nlsc lock:check` could not load the `.nl.lock` file because it is missing or malformed.",
        emitted_by=("lock:check",),
        common_causes=(
            "The lockfile has not been generated yet for the source file.",
            "The existing `.nl.lock` file was edited manually or became corrupted.",
        ),
        next_steps=(
            "Run `nlsc compile <file>` or `nlsc lock:update <file>` to regenerate the lockfile.",
            "If the lockfile should already exist, inspect it for truncation or invalid contents before regenerating.",
        ),
    ),
    ELOCK002: ErrorDefinition(
        code=ELOCK002,
        title="Lockfile out of date",
        summary="`nlsc lock:check` found one or more ANLUs that no longer match the current source file.",
        emitted_by=("lock:check",),
        common_causes=(
            "The `.nl` source changed after the last compile or lockfile update.",
            "A new ANLU was added or renamed without regenerating the lockfile.",
        ),
        next_steps=(
            "Run `nlsc compile <file>` or `nlsc lock:update <file>` to regenerate the lockfile.",
            "Review the reported ANLU diagnostics to confirm the source changes are expected.",
        ),
    ),
    ELSP001: ErrorDefinition(
        code=ELSP001,
        title="LSP optional dependencies unavailable",
        summary="`nlsc lsp` could not import the optional LSP server dependencies before startup.",
        emitted_by=("lsp",),
        common_causes=(
            "The optional `nlsc[lsp]` extras were not installed in the current Python environment.",
            "A transitive LSP dependency such as `pygls` or `lsprotocol` is missing or broken.",
        ),
        next_steps=(
            "Install the optional dependencies with `pip install nlsc[lsp]`.",
            "Retry `nlsc lsp` in the same environment after the install completes.",
        ),
    ),
    ELSP002: ErrorDefinition(
        code=ELSP002,
        title="LSP server startup failed",
        summary="`nlsc lsp` loaded successfully, but the server failed during startup or transport initialization.",
        emitted_by=("lsp",),
        common_causes=(
            "The requested TCP host or port could not be bound.",
            "The language server raised an unexpected runtime error while initializing the selected transport.",
        ),
        next_steps=(
            "Check the selected transport, host, and port, then rerun `nlsc lsp`.",
            "Inspect the reported startup message to identify the failing runtime dependency or bind step.",
        ),
    ),
    EASSOC001: ErrorDefinition(
        code=EASSOC001,
        title="Association unsupported on this platform",
        summary="`nlsc assoc` was invoked on a non-Windows platform where the Explorer registry integration is unavailable.",
        emitted_by=("assoc",),
        common_causes=(
            "The command was run on macOS, Linux, or another non-Windows environment.",
            "Automation invoked `nlsc assoc` without checking the host platform first.",
        ),
        next_steps=(
            "Run `nlsc assoc` on Windows if you need Explorer integration for `.nl` files.",
            "Use your operating system's default-app tooling on non-Windows platforms.",
        ),
    ),
    EASSOC002: ErrorDefinition(
        code=EASSOC002,
        title="Association icon missing",
        summary="`nlsc assoc` could not find the packaged `nls-file.ico` asset required for the Explorer file type icon.",
        emitted_by=("assoc",),
        common_causes=(
            "The installed package is missing `nlsc/resources/nls-file.ico`.",
            "The icon asset was not generated or bundled before packaging.",
        ),
        next_steps=(
            "Regenerate the icon asset with `python windows/generate_ico.py` from the project root.",
            "Reinstall or rebuild the package so `nlsc/resources/nls-file.ico` is present.",
        ),
    ),
    EASSOC003: ErrorDefinition(
        code=EASSOC003,
        title="Association permission denied",
        summary="`nlsc assoc` reached the Windows registry update step, but the process lacked permission to write the required keys.",
        emitted_by=("assoc",),
        common_causes=(
            "The command attempted a machine-wide install without administrator rights.",
            "A group policy or endpoint security rule blocked registry writes for the association keys.",
        ),
        next_steps=(
            "Rerun from an elevated shell for a machine-wide association.",
            "Use `nlsc assoc --user` if a per-user association is sufficient.",
        ),
    ),
    EASSOC004: ErrorDefinition(
        code=EASSOC004,
        title="Association update failed",
        summary="`nlsc assoc` hit an unexpected runtime failure while creating, deleting, or finalizing the Windows file association.",
        emitted_by=("assoc",),
        common_causes=(
            "A registry API call failed for a reason other than a basic permission error.",
            "The local shell notification or registry state is inconsistent or temporarily unavailable.",
        ),
        next_steps=(
            "Inspect the reported runtime error and local registry state, then rerun `nlsc assoc`.",
            "If the failure persists, retry after repairing the local install or cleaning up partial association keys.",
        ),
    ),
    EWATCH001: ErrorDefinition(
        code=EWATCH001,
        title="Watch path is not a directory",
        summary="`nlsc watch` requires an existing directory path before it can start the watcher.",
        emitted_by=("watch",),
        common_causes=(
            "The watch path points at a single `.nl` file instead of a directory.",
            "The path exists but resolves to another filesystem object such as a file or symlink target that is not a directory.",
        ),
        next_steps=(
            "Pass a directory path to `nlsc watch` and rerun the command.",
            "Use `nlsc compile <file>` or `nlsc test <file>` when working with a single source file.",
        ),
    ),
    EWATCH002: ErrorDefinition(
        code=EWATCH002,
        title="Watch runtime compile failed",
        summary="`nlsc watch --json` hit an unexpected runtime compile failure after startup that did not map to a shared parse, resolution, target, or validation diagnostic.",
        emitted_by=("watch",),
        common_causes=(
            "Writing the generated artifact failed due to a filesystem or permission problem.",
            "A watch-triggered compile path hit an unexpected internal runtime error.",
        ),
        next_steps=(
            "Inspect the reported runtime message and the watched source file path.",
            "Fix the underlying environment or source issue, then save the file again to retrigger compilation.",
        ),
    ),
}


def get_error_definition(code: str) -> ErrorDefinition | None:
    return ERROR_CATALOG.get(code.strip().upper())


def known_error_codes() -> tuple[str, ...]:
    return tuple(sorted(ERROR_CATALOG))


def format_error_explanation(definition: ErrorDefinition) -> str:
    lines = [
        f"{definition.code}: {definition.title}",
        "",
        definition.summary,
        "",
        f"Emitted by: {', '.join(definition.emitted_by)}",
        "",
        "Common causes:",
        *[f"- {cause}" for cause in definition.common_causes],
        "",
        "Next steps:",
        *[f"- {step}" for step in definition.next_steps],
    ]
    return "\n".join(lines)
