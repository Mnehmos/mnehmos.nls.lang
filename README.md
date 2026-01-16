# Natural Language Source (NLS)

> **The source code is English. The compiled artifact is Python.**

NLS is a programming language where source code is written in plain English that anyone can read—managers, auditors, new developers—not just programmers. The `nlsc` compiler translates `.nl` specification files into executable Python.

## Quick Start

```bash
# Install
pip install -e .

# Initialize a project
nlsc init my-project

# Compile .nl to Python
nlsc compile src/math.nl
```

## Example

**Input:** `math.nl`

```nl
@module math
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  • a: number
  • b: number
RETURNS: a + b
```

**Output:** `math.py`

```python
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b
```

## The Thesis

_"The conversation is the programming. The `.nl` file is the receipt. The code is the artifact."_

- `.nl` files are human-readable specifications anyone can understand
- `.py` files are compiled artifacts (like assembly from C)
- `.nl.lock` files ensure deterministic, reproducible builds

## CLI Commands

| Command                  | Description                 |
| ------------------------ | --------------------------- |
| `nlsc init <path>`       | Initialize NLS project      |
| `nlsc compile <file.nl>` | Compile to Python           |
| `nlsc verify <file.nl>`  | Validate without generating |

## Status

**Phase 1 MVP** — Schema + Compiler foundation complete.

- ✅ Parser (regex-based)
- ✅ Resolver (dependency graph)
- ✅ Emitter (mock mode for simple expressions)
- ✅ Lockfile generation
- ⏳ LLM emitter for complex logic (next)

## License

MIT
