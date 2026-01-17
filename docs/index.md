# NLS Compiler

> **The source code is English. The compiled artifact is Python.**

NLS is a programming language where specifications are written in plain English that anyone can read—managers, auditors, domain experts—not just programmers. The `nlsc` compiler translates `.nl` files into executable Python with full type hints, validation, and documentation.

## Why NLS?

- **Readable by everyone** — Non-programmers can review business logic
- **Auditable** — Clear mapping from intent to implementation
- **Testable** — Specifications include test cases
- **Versionable** — Lock files ensure reproducibility
- **Toolable** — Tree-sitter grammar enables IDE support

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

```bash
pip install nlsc
```

## Project Status

| Component              | Status      |
| ---------------------- | ----------- |
| Parser (regex)         | ✅ Complete |
| Parser (tree-sitter)   | ✅ Complete |
| Python emitter         | ✅ Complete |
| Type generation        | ✅ Complete |
| Guard validation       | ✅ Complete |
| Dataflow analysis      | ✅ Complete |
| Test runner            | ✅ Complete |
| Property-based testing | ✅ Complete |
| Type invariants        | ✅ Complete |
| Watch mode             | ✅ Complete |
| GitHub Action          | ✅ Complete |
| PyPI distribution      | ✅ Complete |
| VS Code extension      | 🔜 Planned  |
| TypeScript target      | 🔜 Planned  |

**239 tests passing** — Production-ready for Python target.

## Get Started

<div class="grid cards" markdown>

- :material-download: **[Installation](getting-started.md#installation)**

  Install nlsc with pip

- :material-console: **[CLI Reference](cli-reference.md)**

  All 8 commands documented

- :material-book-open: **[Language Spec](language-spec.md)**

  Full syntax reference

- :material-cog: **[Architecture](architecture.md)**

  How the compiler works

</div>
