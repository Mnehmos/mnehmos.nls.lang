# Getting Started

This guide will walk you through installing NLS and creating your first compiled specification.

## Installation

=== "From PyPI"

    ```bash
    pip install nlsc
    ```

=== "With Tree-sitter Parser"

    ```bash
    pip install "nlsc[treesitter]"
    ```

    The tree-sitter parser provides faster parsing and better error recovery.

=== "Development Setup"

    ```bash
    git clone https://github.com/Mnehmos/mnehmos.nls.lang.git
    cd mnehmos.nls.lang
    pip install -e ".[dev,treesitter]"
    ```

## Initialize a Project

Create a new NLS project with the proper folder structure:

```bash
nlsc init my-project
cd my-project
```

This creates:

```
my-project/
├── nl.config.yaml    # Project configuration
├── src/              # Source .nl files
│   └── __init__.py
└── tests/            # Generated tests
    └── __init__.py
```

## Your First .nl File

Create `src/calculator.nl`:

```nl
@module calculator
@target python

[add]
PURPOSE: Add two numbers together
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

[divide]
PURPOSE: Divide two numbers safely
INPUTS:
  - numerator: number
  - divisor: number
GUARDS:
  - divisor must not be zero -> ValueError("Cannot divide by zero")
RETURNS: numerator / divisor

@test [add] {
  add(2, 3) == 5
  add(-1, 1) == 0
}
```

## Compile to Python

```bash
nlsc compile src/calculator.nl
```

Output:

```
Compiling src/calculator.nl (parser: regex)...
  ✓ Parsed 2 ANLUs
  ✓ Resolved dependencies
  ✓ Generated calculator.py (25 lines)
  ✓ Generated test_calculator.py
  ✓ Updated calculator.nl.lock

Compilation complete!
```

## Run the Tests

```bash
nlsc test src/calculator.nl
```

Output:

```
Running 2 test cases from src/calculator.nl...
  • [add]: 2 cases

✓ All 2 tests passed!
```

## Use the Generated Code

```python
from src.calculator import add, divide

result = add(2, 3)  # 5
ratio = divide(10, 2)  # 5.0

try:
    divide(1, 0)
except ValueError as e:
    print(e)  # "Cannot divide by zero"
```

## Next Steps

- **[CLI Reference](cli-reference.md)** — Learn all 8 nlsc commands
- **[Language Specification](language-spec.md)** — Full syntax reference
- **[Architecture](architecture.md)** — How the compiler works

## Workflow Tips

### Watch Mode

Automatically recompile on file changes:

```bash
nlsc watch src/ --test
```

### Visualize Dependencies

Generate Mermaid diagrams:

```bash
nlsc graph src/calculator.nl --format mermaid
```

### See What Changed

View differences since last compile:

```bash
nlsc diff src/calculator.nl
```
