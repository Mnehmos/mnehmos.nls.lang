# NLS Compiler

> **The source is natural language. The compiled artifact can be Python or TypeScript.**

NLS is a programming language where specifications are written in natural language that anyone can read—managers, auditors, domain experts—not just programmers. The `nlsc` compiler translates `.nl` files into executable Python or TypeScript with type hints, validation, and documentation.

## Why NLS?

- **Readable by everyone** — Non-programmers can review business logic
- **Auditable** — Clear mapping from intent to implementation
- **Testable** — Specifications include test cases
- **Versionable** — Lock files ensure reproducibility
- **Toolable** — Tree-sitter grammar enables IDE support
- **Checked, not guessed** — types, control flow, effects, resource states, and retry policies are verified against the IR before any code is emitted
- **Reproducible** — lockfiles pin semantic hashes of the checked IR; `nlsc ci` re-derives and compares them

## Quick Example

```nl
@module calculator
@target python

[divide]
PURPOSE: Divide two numbers safely
INPUTS:
  - numerator: number
  - divisor: number
GUARDS:
  - divisor must not be zero -> ValueError("Cannot divide by zero")
RETURNS: numerator / divisor
```

Compiles to:

```python
def divide(numerator: float, divisor: float) -> float:
    """Divide two numbers safely."""
    if divisor == 0:
        raise ValueError("Cannot divide by zero")
    return numerator / divisor
```

## Installation

=== "pip"

    ```bash
    pip install nlsc
    ```

=== "pip (with tree-sitter)"

    ```bash
    pip install "nlsc[treesitter]"
    ```

=== "VS Code"

    Search "NLS" in Extensions, or:
    ```
    ext install mnehmos.nls-language
    ```

## What the compiler checks

Everything below is enforced on every `nlsc compile` / `nlsc ci`, before any
code is written:

| Check | Diagnostics |
| ----- | ----------- |
| Types, call resolution, arity, fields, operand types | `ESEM001`–`ESEM009` |
| Branch totality, binding immutability, definite assignment | `ESEM010`, `ESEM011` |
| Guard error identities (builtins or declared `@type`s) | `ESEM012` |
| Effects: named resource writes, `unknown` for foreign content, and declared `EFFECTS:` upper bounds | `EFX001`, `EFX002` |
| Resource state protocols: wrong state, consumed-token reuse, fabrication, ambiguous joins | `ESEM014`–`ESEM017` |
| Retry/timeout policy shape: bounded budget, retryable identities, idempotency key, explicit timeout outcome | `ESEM018`–`ESEM021` |
| Target capability gate: a feature the target cannot emit is refused, never dropped | `ETARGET002` |
| Executable contract: prose instead of code, invented defaults, missing results | `EIR002`, `EIR004`, `EIR005` |
| Scaffold containment: an unresolved module is never executed and never claims its importable filename | `ESCAF001` |

## Project Status

| Component | Status |
| --------- | ------ |
| Both parsers (regex + tree-sitter), canonical lowering | ✅ Complete |
| Target-neutral IR with canonical text/JSON (`nlsc ir`) | ✅ Complete |
| Checked pipeline: types, control, failures, effects, typestate, retry policies | ✅ Complete |
| Python emitter (IR-driven) | ✅ Complete |
| TypeScript emitter (IR-driven, `tsc --strict` conformance in CI) | ✅ Complete |
| Cross-target semantic conformance suite (Python + Node) | ✅ Complete |
| Guard validation, edge cases, type invariants, property tests | ✅ Complete |
| Semantic lock identity + `--frozen-lockfile` reproducibility | ✅ Complete |
| Capability matrix + emitter semantics markers | ✅ Complete |
| Quality gates: `ci`, `lint`, `fmt`, `provenance` | ✅ Complete |
| Local package model (`nls.pkg.json`, `nlsc install`) | ✅ Complete |
| Watch mode, LSP server, GitHub Action, PyPI distribution, VS Code extension | ✅ Complete |
| Emitter plugin registry (`nlsc.targets` entry points) | ✅ Complete |
| Retry/timeout **runtime** emission | ◐ Checked, not yet emitted (both targets refuse explicitly) |
| Typed effect handlers (#207/#208) | ◐ Planned — design staged in the issues |
| Rust target (#24) | ◐ Design intent documented; not implemented |

**1,229 tests passing** across three operating systems and two Python
versions, including a cross-target conformance suite that executes
compiled modules on both backends.


## Get Started

<div class="grid cards" markdown>

- :material-rocket-launch: **[Tutorials](tutorials/index.md)**

    Step-by-step learning path from first module to advanced patterns

- :material-book-open: **[Language Spec](language-spec.md)**

    Complete syntax reference for all NLS constructs

- :material-code-braces: **[Examples](examples.md)**

    Real-world examples: calculators, e-commerce, banking, auth

- :material-robot: **[LLM Reference](llm-reference.md)**

    AI-optimized documentation for training and inference

</div>

## Quick Links

<div class="grid cards" markdown>

- :material-download: **[Installation](getting-started.md#installation)**

    Install nlsc with pip or VS Code

- :material-console: **[CLI Reference](cli-reference.md)**

    All 20 commands, every flag, and the exit codes

- :material-cube-outline: **[Type System](type-system.md)**

    Primitives, composites, and custom types

- :material-alert-circle: **[Error Reference](error-reference.md)**

    Troubleshooting guide for all error types

</div>
