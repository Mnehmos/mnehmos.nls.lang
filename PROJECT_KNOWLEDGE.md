# NLS Project Knowledge

## Quick Reference

| Property | Value |
|----------|-------|
| **Repository** | https://github.com/Mnehmos/mnehmos.nls.lang |
| **Package** | [nlsc on PyPI](https://pypi.org/project/nlsc/) |
| **Docs** | https://mnehmos.github.io/mnehmos.nls.lang/ |
| **Language** | Python 3.11+ |
| **Status** | Alpha (239 tests passing) |
| **License** | MIT |

---

## Overview

**Natural Language Source (NLS)** is a programming language where specifications are written in plain English. The `nlsc` compiler translates `.nl` files into executable Python with full type hints, validation, and documentation.

> _"The source code is English. The compiled artifact is Python."_

---

## Architecture

### Compilation Pipeline

```
.nl file
    ↓
┌─────────────────┐
│     Parser      │  ← Regex (fallback) or Tree-sitter (production)
└────────┬────────┘
         ↓
┌─────────────────┐
│    Resolver     │  ← Validates dependencies, detects cycles
└────────┬────────┘
         ↓
┌─────────────────┐
│     Emitter     │  ← Generates Python code
└────────┬────────┘
         ↓
    .py file + .nl.lock
```

### Core Components

| Component | File | Purpose |
|-----------|------|---------|
| **Parser** | `parser.py` | Regex-based .nl parser (607 lines) |
| **Parser (TS)** | `parser_treesitter.py` | Tree-sitter parser (636 lines) |
| **Schema** | `schema.py` | AST data structures (451 lines) |
| **Emitter** | `emitter.py` | Python code generation (692 lines) |
| **Resolver** | `resolver.py` | Dependency validation (122 lines) |
| **Lockfile** | `lockfile.py` | Deterministic hashing (428 lines) |
| **CLI** | `cli.py` | Command-line interface (840 lines) |
| **Atomize** | `atomize.py` | Extract ANLUs from Python (616 lines) |
| **Diff** | `diff.py` | Change detection (191 lines) |
| **Watch** | `watch.py` | File watching (212 lines) |
| **Roundtrip** | `roundtrip.py` | Round-trip testing (124 lines) |
| **Graph** | `graph.py` | Dependency visualization (270 lines) |

**Total:** ~5,200 lines of compiler code

---

## Key Concepts

### ANLU (Atomic Natural Language Unit)

The fundamental building block - a single function specification:

```nl
[function-name]
PURPOSE: What this function does
INPUTS:
  - param1: type
  - param2: type, optional
GUARDS:
  - validation condition -> ErrorType("message")
LOGIC:
  1. step description -> variable
  2. another step
EDGE CASES:
  - condition -> behavior
RETURNS: expression
DEPENDS: [other-function]
```

### Type Definitions

```nl
@type Order {
  id: string, required
  items: list of OrderItem
  total: number
}

@invariant Order {
  total >= 0
}
```

### Property-Based Testing

```nl
@property [add] {
  add(a, b) == add(b, a)              # commutativity
  forall x: number -> add(x, 0) == x  # identity
}
```

---

## CLI Commands

```bash
nlsc init <path>              # Initialize new project
nlsc compile <file>           # Compile .nl → .py
nlsc verify <file>            # Parse validation only
nlsc test <file>              # Run @test blocks
nlsc graph <file>             # Dependency visualization
nlsc diff <file>              # Show changes vs compiled
nlsc watch <dir>              # Continuous compilation
nlsc atomize <file.py>        # Extract ANLUs from Python
```

**Global Options:**
- `--parser {regex,treesitter}` - Select parser backend
- `--version` - Show version
- `--help` - Show help

---

## Data Structures (schema.py)

### Core AST Types

| Class | Purpose |
|-------|---------|
| `Input` | Parameter with type, constraints, description |
| `Guard` | Precondition with error type and message |
| `EdgeCase` | Condition-behavior pair |
| `LogicStep` | Numbered step with dataflow (assigns, uses, depends_on) |
| `ANLU` | Complete function spec |
| `TypeField` | Field in a type definition |
| `TypeDefinition` | Dataclass spec with fields and constraints |
| `Module` | Metadata (name, version, target, imports) |
| `NLFile` | Complete parsed .nl file |
| `TestSuite` / `TestCase` | Executable assertions |
| `PropertyTest` / `PropertyAssertion` | Property-based testing |
| `Invariant` | Type invariants |

---

## File Structure

```
mnehmos.nls.lang/
├── nlsc/                     # Compiler package
│   ├── __init__.py
│   ├── cli.py               # Command-line interface
│   ├── schema.py            # Data structures
│   ├── parser.py            # Regex parser
│   ├── parser_treesitter.py # Tree-sitter parser
│   ├── emitter.py           # Python code generation
│   ├── resolver.py          # Dependency validation
│   ├── lockfile.py          # Determinism
│   ├── atomize.py           # Reverse compilation
│   ├── diff.py              # Change detection
│   ├── watch.py             # File watching
│   ├── roundtrip.py         # Round-trip testing
│   └── graph.py             # Visualization
│
├── tests/                    # 19 test modules (239 tests)
├── docs/                     # MkDocs documentation
├── examples/                 # Working examples
├── tree-sitter-nl/           # Grammar & parser
├── action/                   # GitHub Action
├── stress-test/              # Performance tests
│
├── pyproject.toml           # Package config
├── mkdocs.yml               # Docs config
├── nl-schema.yaml           # Formal grammar
└── README.md
```

---

## Tree-Sitter Grammar

The `tree-sitter-nl/` directory contains:

- `grammar.js` - Official grammar definition (680+ lines)
- `src/parser.c` - Generated C parser
- `src/scanner.c` - Lexical scanner for @literal blocks
- `queries/*.scm` - Syntax highlighting, folding, text objects
- `test/corpus/` - Parser test cases

**Building:**
```bash
cd tree-sitter-nl
npm install
npx tree-sitter generate
npx tree-sitter test
```

---

## Development

### Setup

```bash
git clone https://github.com/Mnehmos/mnehmos.nls.lang.git
cd mnehmos.nls.lang
pip install -e ".[dev,treesitter]"
```

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test module
pytest tests/test_parser.py -v

# Run with coverage
pytest tests/ --cov=nlsc --cov-report=html
```

### Linting

```bash
ruff check nlsc/ --select=E,F,W --ignore=E501
```

---

## Reproducibility

**.nl.lock** files ensure deterministic builds:

```yaml
version: "0.1.0"
source_hash: "sha256:abc123..."
generated_hash: "sha256:def456..."
timestamp: "2025-01-17T14:00:00Z"
```

---

## GitHub Action

```yaml
- uses: Mnehmos/mnehmos.nls.lang/action@master
  with:
    verify: 'true'
    compile: 'false'
    test: 'false'
    lock-check: 'false'
```

---

## Status

| Component | Status |
|-----------|--------|
| Parser (regex) | ✅ Complete |
| Parser (tree-sitter) | ✅ Complete |
| Python emitter | ✅ Complete |
| Type generation | ✅ Complete |
| Guard validation | ✅ Complete |
| Dataflow analysis | ✅ Complete |
| Test runner | ✅ Complete |
| Property-based testing | ✅ Complete |
| Type invariants | ✅ Complete |
| Watch mode | ✅ Complete |
| GitHub Action | ✅ Complete |
| PyPI distribution | ✅ Complete |
| VS Code extension | 🔜 Planned |
| TypeScript target | 🔜 Planned |
| LSP server | 🔜 Planned |

---

## Next Steps

1. **VS Code Extension** - Syntax highlighting, snippets, diagnostics
2. **LSP Server** - Go-to-definition, hover, completions
3. **TypeScript Target** - Multi-language code generation
4. **LLM Emitter** - Complex logic generation with caching

---

## Links

- **PyPI:** https://pypi.org/project/nlsc/
- **Docs:** https://mnehmos.github.io/mnehmos.nls.lang/
- **Issues:** https://github.com/Mnehmos/mnehmos.nls.lang/issues
