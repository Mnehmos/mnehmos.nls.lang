# Contributing to NLS

Thank you for your interest in contributing to the Natural Language Source compiler!

## Quick Links

- **Repository:** https://github.com/Mnehmos/mnehmos.nls.lang
- **PyPI:** https://pypi.org/project/nlsc/
- **Documentation:** https://mnehmos.github.io/mnehmos.nls.lang/
- **Issues:** https://github.com/Mnehmos/mnehmos.nls.lang/issues

## Development Setup

```bash
# Clone the repository
git clone https://github.com/Mnehmos/mnehmos.nls.lang.git
cd mnehmos.nls.lang

# Install in development mode with all extras
pip install -e ".[dev,treesitter]"

# Verify installation
nlsc --version
pytest tests/ -v
```

### Requirements

- Python 3.11+
- Node.js 18+ (for tree-sitter grammar development)

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test module
pytest tests/test_parser.py -v

# Run with coverage
pytest tests/ --cov=nlsc --cov-report=html

# Run tree-sitter grammar tests
cd tree-sitter-nl
npx tree-sitter test
```

## Code Style

- **Python 3.11+** required
- **Type hints** on all public functions
- **Docstrings** for public modules, classes, and functions
- **Ruff** for linting: `ruff check nlsc/ --select=E,F,W --ignore=E501`

## Project Structure

```
nlsc/                    # Compiler package
├── cli.py              # Command-line interface
├── parser.py           # Regex-based parser
├── parser_treesitter.py # Tree-sitter parser
├── schema.py           # AST data structures
├── emitter.py          # Python code generation
├── resolver.py         # Dependency validation
├── lockfile.py         # Deterministic hashing
├── atomize.py          # Reverse compilation
├── diff.py             # Change detection
├── watch.py            # File watching
├── roundtrip.py        # Round-trip testing
└── graph.py            # Dependency visualization

tests/                   # Test modules (239 tests)
tree-sitter-nl/          # Tree-sitter grammar
docs/                    # MkDocs documentation
examples/                # Working examples
```

## Contribution Workflow

1. **Check existing issues** for what needs work
2. **Create an issue** if none exists for your change
3. **Fork and clone** the repository
4. **Create a feature branch** from `master`
5. **Write tests first** (TDD is strongly encouraged)
6. **Implement your changes**
7. **Run the full test suite**
8. **Submit a pull request**

### Commit Convention

```
feat(component): add new feature
fix(component): fix bug description
test(component): add tests for X
refactor(component): refactor without behavior change
docs(component): update documentation
```

## Areas for Contribution

### Good First Issues

- Documentation improvements
- Additional test cases
- Error message improvements

### Intermediate

- New CLI commands
- Parser edge case handling
- Emitter enhancements

### Advanced

- TypeScript target (#20)
- Rust target (#24)
- LSP server (#25)
- VS Code extension

## Tree-Sitter Grammar

The `tree-sitter-nl/` directory contains the official grammar:

```bash
cd tree-sitter-nl
npm install
npx tree-sitter generate
npx tree-sitter test
```

Files:
- `grammar.js` — Grammar definition
- `src/scanner.c` — Custom lexer for @literal blocks
- `queries/*.scm` — Syntax highlighting, folding, text objects
- `test/corpus/` — Parser test cases

## Questions?

Open an issue or check the [documentation](https://mnehmos.github.io/mnehmos.nls.lang/).

## License

MIT — See [LICENSE](LICENSE)
