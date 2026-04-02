"""Central catalog of stable CLI error codes."""

from __future__ import annotations

from dataclasses import dataclass

EFILE001 = "EFILE001"
EPARSE001 = "EPARSE001"
EUSE001 = "EUSE001"
E_RESOLUTION = "E_RESOLUTION"
ECONTRACT001 = "ECONTRACT001"
ETARGET001 = "ETARGET001"
EVALIDATE001 = "EVALIDATE001"
E_RUN = "E_RUN"
EEXEC001 = "EEXEC001"
EGRAPH001 = "EGRAPH001"
EGRAPH002 = "EGRAPH002"


@dataclass(frozen=True)
class ErrorDefinition:
    code: str
    title: str
    summary: str
    emitted_by: tuple[str, ...]
    common_causes: tuple[str, ...]
    next_steps: tuple[str, ...]


ERROR_CATALOG: dict[str, ErrorDefinition] = {
    EFILE001: ErrorDefinition(
        code=EFILE001,
        title="File not found",
        summary="The requested source file does not exist at the provided path.",
        emitted_by=("compile", "verify", "run"),
        common_causes=(
            "The .nl path is misspelled or points to the wrong working directory.",
            "The file has not been created yet or was moved.",
        ),
        next_steps=(
            "Check the file path and rerun the command.",
            "Use an absolute path if the current working directory is ambiguous.",
        ),
    ),
    EPARSE001: ErrorDefinition(
        code=EPARSE001,
        title="Parse error",
        summary="The .nl source contains syntax the parser cannot accept.",
        emitted_by=("compile", "verify", "run"),
        common_causes=(
            "A required directive or section is malformed or missing.",
            "A LOGIC, INPUTS, or GUARDS line does not follow the expected shape.",
        ),
        next_steps=(
            "Use the reported line number to fix the source syntax.",
            "Run `nlsc verify <file>` after editing to confirm the file parses cleanly.",
        ),
    ),
    EUSE001: ErrorDefinition(
        code=EUSE001,
        title="Missing stdlib domain",
        summary="A referenced `@use` domain could not be resolved from the stdlib roots.",
        emitted_by=("compile", "verify", "run"),
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
        emitted_by=("compile", "verify", "run"),
        common_causes=(
            "A `DEPENDS` entry points at an ANLU that does not exist.",
            "Two or more ANLUs form a dependency cycle.",
        ),
        next_steps=(
            "Define the missing ANLU or remove the dependency reference.",
            "Break cycles so dependency edges form an acyclic graph.",
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
        emitted_by=("compile", "run"),
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
        emitted_by=("compile",),
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
        title="Execution setup error",
        summary="`nlsc run` failed while preparing or launching the generated module.",
        emitted_by=("run",),
        common_causes=(
            "The temporary execution environment could not be created or used.",
            "Launching the generated module raised an unexpected host-side exception.",
        ),
        next_steps=(
            "Inspect the generated module path and runtime environment.",
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
