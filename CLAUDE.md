# CLAUDE.md - Agent Instructions for NLS

## Project Overview

NLS (Natural Language Source) is a compiler that translates `.nl` specification files written in plain English into executable Python code.

## Commands

```bash
# Install in development mode
pip install -e .[dev]

# Run tests
pytest tests/ -v

# Compile .nl file
nlsc compile examples/math.nl

# Verify syntax
nlsc verify examples/math.nl

# Initialize new project
nlsc init <path>
```

## Architecture

- `nlsc/parser.py` — Parses .nl files into AST
- `nlsc/resolver.py` — Validates dependencies
- `nlsc/emitter.py` — Generates Python (mock mode)
- `nlsc/lockfile.py` — Determinism via hashing

## Current Limitations

The mock emitter only handles simple expression returns (`a + b`). Complex LOGIC steps generate TODO stubs. LLM integration planned.

## Key Principle

_"The .nl file is the source. The .py file is the artifact."_
