# tree-sitter-nl

Tree-sitter grammar for NL (Natural Language Source) files.

NL is a specification language that compiles to executable code. This grammar enables IDE support, syntax highlighting, code folding, and error recovery.

## Features

- **Syntax Highlighting**: Full semantic highlighting for all NL constructs
- **Code Folding**: Fold ANLU blocks, type definitions, test blocks, and sections
- **Language Injection**: Syntax highlighting within `@literal` blocks (Python, TypeScript, Rust, etc.)
- **Text Objects**: Structural selection and navigation for editors like Neovim
- **Error Recovery**: Parse partial files and continue on errors

## Installation

### From npm

```bash
npm install tree-sitter-nl
```

### From source

```bash
cd tree-sitter-nl
npm install
npm run build
```

## Usage

### Node.js

```javascript
const Parser = require("tree-sitter");
const NL = require("tree-sitter-nl");

const parser = new Parser();
parser.setLanguage(NL);

const sourceCode = `
@module math
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b
`;

const tree = parser.parse(sourceCode);
console.log(tree.rootNode.toString());
```

### Neovim

Add to your nvim-treesitter configuration:

```lua
require("nvim-treesitter.parsers").get_parser_configs().nl = {
  install_info = {
    url = "https://github.com/Mnehmos/mnehmos.nls.lang",
    files = { "tree-sitter-nl/src/parser.c" },
    branch = "main",
  },
  filetype = "nl",
}
```

### VS Code

The tree-sitter grammar is used by the NL VS Code extension for syntax highlighting and language features.

## Grammar Overview

### Directives

```nl
@module myapp          # Module name
@version 1.0.0         # Semantic version
@target python         # Compilation target
@imports utils, core   # Dependencies
```

### ANLU Blocks

```nl
[function-name]
PURPOSE: Describe what this does
INPUTS:
  - param: type
GUARDS:
  - condition -> Error(message)
LOGIC:
  1. First step
  2. Second step -> result
RETURNS: result
DEPENDS: [other-function]
EDGE CASES:
  - edge condition -> behavior
```

### Type Definitions

```nl
@type Person {
  name: string
  age: number
  friends: list of Person
}

@type Employee extends Person {
  salary: number
}
```

### Test Blocks

```nl
@test [add] {
  add(1, 2) == 3
  add(-1, 1) == 0
}
```

### Literal Blocks

```nl
@literal python {
def complex_function():
    # Exact code that bypasses the compiler
    return result
}
```

## Queries

### Highlighting (`queries/highlights.scm`)

Semantic highlighting for all NL constructs:
- Directives as `@keyword.directive`
- ANLU names as `@function.definition`
- Section headers as `@keyword`
- Types as `@type`
- And more...

### Folding (`queries/folds.scm`)

Foldable regions:
- ANLU blocks
- Type definitions
- Test blocks
- Literal blocks
- Individual sections (INPUTS, LOGIC, etc.)

### Injections (`queries/injections.scm`)

Language injection for `@literal` blocks based on the language tag.

### Text Objects (`queries/textobjects.scm`)

For structural navigation in editors like Neovim:
- `@function.outer/inner` - ANLU blocks
- `@class.outer/inner` - Type blocks
- `@parameter.outer/inner` - Input definitions
- And more...

## Development

### Generate parser

```bash
npm run generate
```

### Run tests

```bash
npm run test
```

### Parse a file

```bash
npm run parse -- examples/math.nl
```

## License

MIT
