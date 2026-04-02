# NLS Compiler

> **The source is natural language. The compiled artifact can be Python or TypeScript.**

NLS is a programming language where specifications are written in natural language that anyone can read—managers, auditors, domain experts—not just programmers. The `nlsc` compiler translates `.nl` files into executable Python or TypeScript with type hints, validation, and documentation.

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
| VS Code extension      | ✅ Complete |
| LSP server             | ✅ Complete |
| Windows installer      | ✅ Complete |
| TypeScript target      | ✅ Initial compile support |

**239 tests passing** — Production-ready for Python target.

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

    All 11 commands documented

- :material-cube-outline: **[Type System](type-system.md)**

    Primitives, composites, and custom types

- :material-alert-circle: **[Error Reference](error-reference.md)**

    Troubleshooting guide for all error types

</div>
