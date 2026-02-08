# CLI Reference

The `nlsc` command-line interface provides 8 commands for working with NLS files.

## Global Options

```bash
nlsc [--parser {regex,treesitter}] [--version] [--help] <command>
```

| Option      | Description                                       |
| ----------- | ------------------------------------------------- |
| `--parser`  | Parser backend: `regex` (default) or `treesitter` |
| `--version` | Show version number                               |
| `--help`    | Show help message                                 |

---

## Commands

### `nlsc init`

Initialize a new NLS project with standard folder structure.

```bash
nlsc init [path]
```

| Argument | Description                                    |
| -------- | ---------------------------------------------- |
| `path`   | Project directory (default: current directory) |

**Example:**

```bash
nlsc init my-project
```

Creates:

```
my-project/
├── nl.config.yaml    # Project configuration
├── src/              # Source .nl files
│   └── __init__.py
└── tests/            # Generated tests
    └── __init__.py
```

---

### `nlsc compile`

Compile a `.nl` file to the target language (currently Python).

```bash
nlsc compile <file> [-t TARGET] [-o OUTPUT]
```

| Option         | Description                         |
| -------------- | ----------------------------------- |
| `file`         | Path to `.nl` file                  |
| `-t, --target` | Target language (default: `python`) |
| `-o, --output` | Output file path                    |
| `--stdlib-path` | Additional stdlib root (repeatable; higher precedence than env + bundled) |

**Examples:**

```bash
# Basic compile
nlsc compile src/auth.nl

# Compile with tree-sitter parser
nlsc --parser treesitter compile src/auth.nl

# Specify output file
nlsc compile src/auth.nl -o lib/auth.py

# Provide an additional stdlib root (repeatable)
nlsc compile src/main.nl --stdlib-path ./vendor/stdlib
```

#### Stdlib overrides for `@use` (Issue #90)

If your `.nl` file contains `@use <domain>` directives, `nlsc compile` resolves domains by searching stdlib roots in this order:

1. Project-local override: `.nls/stdlib/`
2. CLI override roots: `--stdlib-path <dir>` (repeatable; earlier flags win)
3. Environment override roots: `NLS_STDLIB_PATH` (path list; left-to-right)
4. Bundled stdlib shipped with `nlsc`: `nlsc/stdlib/`

Domain-to-path mapping is deterministic:

* `@use math.core` → `v{major}/math/core.nl`
* `@use v1.math.core` pins `major=1`

**Generated files:**

- `<name>.py` — Python module
- `test_<name>.py` — Test file (if `@test` blocks present)
- `<name>.nl.lock` — Lockfile for reproducibility

---

### `nlsc verify`

Validate a `.nl` file without generating code. Checks syntax and dependencies.

```bash
nlsc verify <file>
```

**Example:**

```bash
nlsc verify src/order.nl
```

Output:

```
Verifying src/order.nl (parser: regex)...
  ✓ Syntax valid: 5 ANLUs
  ✓ Dependencies valid
  ✓ All ANLUs valid

Verification passed!
```

---

### `nlsc test`

Run `@test` specifications from a `.nl` file.

```bash
nlsc test <file> [-v]
```

| Option          | Description        |
| --------------- | ------------------ |
| `file`          | Path to `.nl` file |
| `-v, --verbose` | Verbose output     |

**Example:**

```bash
nlsc test src/math.nl -v
```

The command:

1. Compiles the `.nl` file to a temp directory
2. Generates test code from `@test` blocks
3. Runs pytest on the generated tests

---

### `nlsc graph`

Generate dependency and dataflow visualizations.

```bash
nlsc graph <file> [-f FORMAT] [-a ANLU] [--dataflow] [-o OUTPUT]
```

| Option         | Description                                        |
| -------------- | -------------------------------------------------- |
| `file`         | Path to `.nl` file                                 |
| `-f, --format` | Output format: `mermaid` (default), `dot`, `ascii` |
| `-a, --anlu`   | Specific ANLU for dataflow visualization           |
| `--dataflow`   | Show dataflow instead of FSM states                |
| `-o, --output` | Output file path (default: stdout)                 |

**Examples:**

```bash
# Module dependency graph
nlsc graph src/order.nl --format mermaid

# Dataflow for specific ANLU
nlsc graph src/order.nl --anlu process-order --dataflow

# Export as DOT for Graphviz
nlsc graph src/order.nl --format dot -o deps.dot
```

---

### `nlsc diff`

Show changes since last compile by comparing against the lockfile.

```bash
nlsc diff <file> [--stat] [--full]
```

| Option   | Description            |
| -------- | ---------------------- |
| `file`   | Path to `.nl` file     |
| `--stat` | Show summary only      |
| `--full` | Show full unified diff |

**Examples:**

```bash
# Show changed ANLUs
nlsc diff src/api.nl

# Summary statistics
nlsc diff src/api.nl --stat

# Full unified diff
nlsc diff src/api.nl --full
```

---

### `nlsc watch`

Watch a directory for `.nl` file changes and automatically recompile.

```bash
nlsc watch [dir] [-q] [-t] [-d DEBOUNCE]
```

| Option           | Description                            |
| ---------------- | -------------------------------------- |
| `dir`            | Directory to watch (default: current)  |
| `-q, --quiet`    | Suppress success messages              |
| `-t, --test`     | Run tests after successful compile     |
| `-d, --debounce` | Debounce interval in ms (default: 100) |

**Examples:**

```bash
# Watch current directory
nlsc watch

# Watch with tests
nlsc watch src/ --test

# Quiet mode with custom debounce
nlsc watch src/ -q -d 500
```

Press `Ctrl+C` to stop watching.

---

### `nlsc atomize`

Extract ANLUs from existing Python source code (reverse compilation).

```bash
nlsc atomize <file> [-o OUTPUT] [-m MODULE]
```

| Option         | Description                     |
| -------------- | ------------------------------- |
| `file`         | Path to Python file             |
| `-o, --output` | Output `.nl` file path          |
| `-m, --module` | Module name for generated `.nl` |

**Example:**

```bash
nlsc atomize legacy/utils.py -o src/utils.nl -m utils
```

This extracts functions from Python and generates corresponding ANLU blocks.

---

## Exit Codes

| Code | Meaning                                       |
| ---- | --------------------------------------------- |
| 0    | Success                                       |
| 1    | Error (parse error, validation failure, etc.) |

## Environment Variables

| Variable      | Description                                      |
| ------------- | ------------------------------------------------ |
| `NLSC_PARSER` | Default parser backend (`regex` or `treesitter`) |

## Configuration

Project settings are stored in `nl.config.yaml`:

```yaml
project:
  name: my-project
  version: 0.1.0

compiler:
  default_target: python
  llm_backend: mock
  cache_strategy: aggressive

targets:
  python:
    version: ">=3.11"
    style: black
    type_hints: strict

validation:
  require_purpose: true
  require_guards: false
  max_anlu_complexity: 10
```
