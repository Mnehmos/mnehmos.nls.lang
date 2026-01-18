# NLS - Natural Language Source

![NLS Logo](images/icon.png)

> **The source code is English. The compiled artifact is Python.**

Language support for [NLS](https://github.com/Mnehmos/mnehmos.nls.lang) (Natural Language Source) specification files in Visual Studio Code.

## Features

### Syntax Highlighting

Full syntax highlighting for `.nl` files including:

- **Directives** - `@module`, `@version`, `@target`, `@imports`
- **ANLU blocks** - `[function-name]` with PURPOSE, INPUTS, GUARDS, LOGIC, RETURNS
- **Type definitions** - `@type`, `@invariant`
- **Test blocks** - `@test`, `@property`
- **Comments** - Line comments with `#`


### Code Snippets

Quickly scaffold NLS constructs:

| Prefix | Description |
|--------|-------------|
| `anlu` | Full ANLU function block |
| `type` | Type definition |
| `test` | Test block |
| `prop` | Property-based test |
| `inv` | Type invariant |
| `module` | Module header |
| `guard` | Guard clause |

### Diagnostics

Real-time validation powered by the `nlsc` compiler:

- Syntax errors
- Undefined dependencies
- Type mismatches
- Invalid guards

### Commands

- **NLS: Compile File** - Compile the current `.nl` file to Python
- **NLS: Verify File** - Validate syntax without compiling
- **NLS: Run Tests** - Execute `@test` blocks

## Requirements

Install the NLS compiler:

```bash
pip install nlsc
```

## Quick Start

1. Create a new file with `.nl` extension
2. Start with a module directive:

```nl
@module calculator
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
```

3. Run **NLS: Compile File** to generate Python code

## Links

- [Documentation](https://mnehmos.github.io/mnehmos.nls.lang/)
- [GitHub Repository](https://github.com/Mnehmos/mnehmos.nls.lang)
- [PyPI Package](https://pypi.org/project/nlsc/)
- [Report Issues](https://github.com/Mnehmos/mnehmos.nls.lang/issues)

## License

MIT
