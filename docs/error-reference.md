# Error Reference

Complete guide to NLS errors, their causes, and how to fix them.

## Active CLI Error Codes

These are the stable error codes currently emitted by `nlsc atomize`, `nlsc compile`, `nlsc verify`, `nlsc run`, `nlsc graph`, `nlsc diff`, `nlsc test`, `nlsc watch`, `nlsc lock:check`, and `nlsc lock:update`.

Use the CLI to get the extended explanation for any code:

```bash
nlsc explain EPARSE001
```

| Code | Commands | Meaning |
| --- | --- | --- |
| `EFILE001` | `atomize`, `compile`, `verify`, `run`, `test`, `graph`, `diff`, `watch`, `lock:check`, `lock:update` | The requested input path does not exist. |
| `EATOM001` | `atomize` | The input Python file failed syntax parsing during atomization. |
| `EATOM002` | `atomize` | `nlsc atomize` hit an unexpected extraction or write failure. |
| `EPARSE001` | `compile`, `verify`, `run`, `test`, `graph`, `diff`, `lock:check`, `lock:update` | The source file failed syntax parsing. |
| `EPARSE002` | `compile`, `verify`, `run`, `test`, `graph`, `diff`, `watch`, `lock:check`, `lock:update` | The requested parser backend could not be initialized before command execution. |
| `EUSE001` | `compile`, `verify`, `run`, `test` | A referenced `@use` stdlib domain could not be resolved. |
| `E_RESOLUTION` | `compile`, `verify`, `run`, `test` | The ANLU dependency graph contains a missing or circular dependency. |
| `ETEST001` | `test` | `nlsc test` generated pytest cases, but the run failed or could not be executed successfully. |
| `ECONTRACT001` | `verify` | An ANLU is missing a required contract field such as `PURPOSE` or `RETURNS`. |
| `ETARGET001` | `compile`, `run`, `lock:update` | The requested target is not supported by the command. |
| `EVALIDATE001` | `compile` | Generated output failed post-emit validation. |
| `E_RUN` | `run` | `nlsc run` hit an unexpected internal error before execution completed. |
| `EEXEC001` | `run` | `nlsc run` failed while setting up or launching the generated module. |
| `EGRAPH001` | `graph` | `nlsc graph --anlu` requested an ANLU that is not defined in the source file. |
| `EGRAPH002` | `graph` | `nlsc graph --anlu` was asked for an output format that is not supported for ANLU-level graphs. |
| `ELOCK001` | `lock:check` | `nlsc lock:check` could not load the `.nl.lock` file because it is missing or malformed. |
| `ELOCK002` | `lock:check` | `nlsc lock:check` found source content that no longer matches the lockfile. |
| `EWATCH001` | `watch` | `nlsc watch` was given a path that exists but is not a directory. |

### `EFILE001` - File not found

Raised when the input path passed to `atomize`, `compile`, `verify`, `run`, or `watch` does not exist.

**Fix:** Check the path, ensure the file exists, and rerun the command.

### `EATOM001` - Python syntax error

Raised when `nlsc atomize --json` cannot parse the input `.py` file into a Python AST.

**Fix:** Correct the reported Python syntax error and rerun `nlsc atomize <file>`.

### `EATOM002` - Atomize write failed

Raised when `nlsc atomize --json` hits an unexpected read/extract/write failure, such as an invalid output path.

**Fix:** Check the output path and filesystem permissions, then rerun `nlsc atomize <file>`.

### `EPARSE001` - Parse error

Raised when the parser rejects the `.nl` source.

**Fix:** Use the reported line number, correct the syntax, then rerun `nlsc verify <file>`.

### `EPARSE002` - Parser backend unavailable

Raised when a parser bootstrap step fails before the command can parse the source, starting with `--parser treesitter` when tree-sitter support is unavailable.

**Fix:** Install the optional backend with `pip install nlsc[treesitter]`, or rerun with `--parser auto` or `--parser regex`.

### `EUSE001` - Missing stdlib domain

Raised when a referenced `@use` module cannot be found in the stdlib search roots.

**Fix:** Verify the domain name and add the correct stdlib root with `--stdlib-path` or `NLS_STDLIB_PATH`.

### `E_RESOLUTION` - Dependency resolution error

Raised when an ANLU depends on a missing ANLU or participates in a dependency cycle.

**Fix:** Define the missing dependency, rename the dependency reference, or break the cycle.

### `ETEST001` - Test execution failed

Raised when `nlsc test --json` successfully generates tests but pytest exits non-zero or cannot be launched.

**Fix:** Inspect `pytest_stdout` and `pytest_stderr` in the JSON payload, then fix the failing assertion, import/setup error, or local pytest environment issue.

### `ECONTRACT001` - Contract validation error

Raised by `nlsc verify` when an ANLU is missing a required contract field.

**Fix:** Add the missing `PURPOSE:` or `RETURNS:` field and verify again.

### `ETARGET001` - Unsupported target

Raised when the requested target is not implemented for the current command.

**Fix:** Use a supported target. For `nlsc run`, use `python`.

### `EVALIDATE001` - Generated output validation failed

Raised when emitted output is written successfully but fails validation, such as `py_compile`.

**Fix:** Inspect the generated artifact and the validator error, then recompile after fixing the source or emitter issue.

### `E_RUN` - Unexpected run error

Raised when `nlsc run` encounters an internal setup or parser-path failure before execution completes.

**Fix:** Retry with `--verbose` and inspect the parser/backend state.

### `EEXEC001` - Execution setup error

Raised when `nlsc run` fails while preparing or launching the generated Python module.

**Fix:** Inspect the generated module path and local runtime environment, then rerun.

### `EGRAPH001` - Graph ANLU not found

Raised when `nlsc graph --anlu <id>` names an ANLU that does not exist in the `.nl` file.

**Fix:** Use one of the ANLU identifiers defined in the file, or omit `--anlu` to render the full dependency graph.

### `EGRAPH002` - Unsupported graph output format

Raised when `nlsc graph --anlu` is combined with an output format that only supports whole-file graphs, such as `--format dot`.

**Fix:** Use `--format mermaid` or `--format ascii` for ANLU-level graphs, or remove `--anlu` when generating a DOT graph.

### `ELOCK001` - Lockfile unavailable

Raised when `nlsc lock:check --json` cannot load the `.nl.lock` file because it is missing or malformed.

**Fix:** Run `nlsc compile <file>` or `nlsc lock:update <file>` to generate a fresh lockfile.

### `ELOCK002` - Lockfile out of date

Raised when `nlsc lock:check --json` finds ANLUs that no longer match the current `.nl` source.

**Fix:** Regenerate the lockfile with `nlsc compile <file>` or `nlsc lock:update <file>` after reviewing the reported ANLU mismatches.

### `EWATCH001` - Watch path is not a directory

Raised when `nlsc watch --json` is given a path that exists but is not a directory.

**Fix:** Pass a directory path to `nlsc watch`, or use a file-oriented command such as `nlsc compile <file>` for a single source file.

## Parse Errors

Parse errors occur when the `.nl` file has invalid syntax.

### Missing Module Directive

```
ParseError: Missing @module directive
```

**Cause:** Every `.nl` file must start with `@module`.

**Fix:**
```nl
@module my_module    # Add this at the top
@target python
```

### Missing Target Directive

```
ParseError: Missing @target directive
```

**Cause:** No compilation target specified.

**Fix:**
```nl
@module my_module
@target python       # Add this after @module
```

### Invalid Module Name

```
ParseError: Invalid module name: 'My-Module'
```

**Cause:** Module names must be lowercase snake_case.

**Valid names:**
```nl
@module calculator
@module user_auth
@module order_processing
```

**Invalid names:**
```nl
@module My-Module     # No hyphens or capitals
@module 123module     # Cannot start with number
@module module name   # No spaces
```

### Invalid ANLU Identifier

```
ParseError: Invalid ANLU identifier: 'CalculateTax'
```

**Cause:** ANLU names must be kebab-case (lowercase with hyphens).

**Valid identifiers:**
```nl
[calculate-tax]
[is-valid]
[get-user-by-id]
```

**Invalid identifiers:**
```nl
[CalculateTax]        # No PascalCase
[calculate_tax]       # No underscores
[123-function]        # Cannot start with number
```

### Missing PURPOSE

```
ParseError: ANLU 'calculate-tax' missing required PURPOSE section
```

**Cause:** Every ANLU must have a PURPOSE.

**Fix:**
```nl
[calculate-tax]
PURPOSE: Calculate tax amount from income and rate
INPUTS:
  - income: number
  - rate: number
RETURNS: income * rate
```

### Missing RETURNS

```
ParseError: ANLU 'validate-user' missing required RETURNS section
```

**Cause:** Every ANLU must have a RETURNS section.

**Fix:**
```nl
[validate-user]
PURPOSE: Validate user credentials
INPUTS:
  - user: User
RETURNS: True         # Add this
```

### Invalid Section Name

```
ParseError: Unknown section 'OUTPUT:' in ANLU 'process-order'
```

**Cause:** Using an invalid section keyword.

**Valid sections:**
- `PURPOSE:`
- `INPUTS:`
- `GUARDS:`
- `LOGIC:`
- `EDGE CASES:`
- `RETURNS:`
- `DEPENDS:`

**Fix:** Check spelling and use exact keywords.

### Unclosed Type Definition

```
ParseError: Unclosed @type block starting at line 15
```

**Cause:** Missing closing brace for `@type`.

**Fix:**
```nl
@type User {
  id: string
  email: string
}                     # Don't forget the closing brace
```

### Unclosed Test Block

```
ParseError: Unclosed @test block starting at line 30
```

**Cause:** Missing closing brace for `@test`.

**Fix:**
```nl
@test [add] {
  add(1, 2) == 3
  add(0, 0) == 0
}                     # Don't forget the closing brace
```

### Invalid Input Syntax

```
ParseError: Invalid input definition: 'amount number'
```

**Cause:** Missing colon between name and type.

**Fix:**
```nl
INPUTS:
  - amount: number    # Include the colon
```

### Invalid Guard Syntax

```
ParseError: Invalid guard: 'amount positive'
```

**Cause:** Guards must follow the pattern: `condition -> Error("message")`

**Fix:**
```nl
GUARDS:
  - amount must be positive -> ValueError("Amount must be positive")
```

---

## Resolution Errors

Resolution errors occur during dependency validation.

### Dependency Not Found

```
ResolutionError: ANLU 'process-order' depends on unknown ANLU 'validate-order'
```

**Cause:** The `DEPENDS` section references an ANLU that doesn't exist.

**Fix options:**

1. Create the missing ANLU:
```nl
[validate-order]
PURPOSE: Validate order data
INPUTS:
  - order: Order
RETURNS: True
```

2. Fix the dependency name:
```nl
DEPENDS: [validate-input]    # Use correct name
```

3. Remove the dependency:
```nl
DEPENDS: none
```

### Circular Dependency

```
ResolutionError: Circular dependency detected:
  process-order -> validate-items -> check-inventory -> process-order
```

**Cause:** ANLUs depend on each other in a cycle.

**Fix:** Refactor to break the cycle:

```nl
# Before (circular):
[a]
DEPENDS: [b]

[b]
DEPENDS: [a]

# After (no cycle):
[common]
DEPENDS: none

[a]
DEPENDS: [common]

[b]
DEPENDS: [common]
```

---

## Stdlib `@use` Errors (Issue #90)

Errors in this section are raised when resolving `@use <domain>` directives against stdlib roots.

### `EUSE001` — Missing stdlib domain

Compilation failed because a referenced stdlib **domain** could not be resolved.

Typical output includes stable fields suitable for assertions:

* `code=EUSE001`
* `domain=<domain>`
* `major=<major>`
* `candidate_relpath=v{major}/.../.nl`
* `attempted_roots=[...]`

**Example** (`@use math.missing`):

```text
Error: EUSE001 domain=math.missing major=1 candidate_relpath=v1/math/missing.nl attempted_roots=[...]
```

**Common causes**

1. The domain is misspelled.
2. The stdlib root you expected is not in the search path.
3. You forgot to include a project-local override in `.nls/stdlib/`.

**Fix**

* Ensure the module exists at the expected path (example for default major 1):
  * `v1/math/core.nl` for `@use math.core`
* Provide an override root:
  * CLI: `nlsc compile src/main.nl --stdlib-path ./vendor/stdlib`
  * Env: set `NLS_STDLIB_PATH` to a path-list of stdlib roots
  * Project: create `.nls/stdlib/v1/...`

### Self Dependency

```
ResolutionError: ANLU 'recursive-func' cannot depend on itself
```

**Cause:** An ANLU lists itself in DEPENDS.

**Fix:** Remove self-reference from DEPENDS. For recursive functions, implement in a `@literal` block.

---

## Emission Errors

Emission errors occur during code generation.

### Invalid Return Expression

```
EmissionWarning: Return expression 'the calculated total' is descriptive,
generating NotImplementedError stub
```

**Cause:** RETURNS contains natural language instead of code.

**Valid returns:**
```nl
RETURNS: a + b
RETURNS: result
RETURNS: Order(id=new_id, items=items)
```

**Invalid returns (generate stubs):**
```nl
RETURNS: the calculated total
RETURNS: user with highest score
RETURNS: filtered list of items
```

**Fix:** Use concrete expressions or implement in `@literal` block.

### Unknown Type

```
EmissionWarning: Unknown type 'UserData', using 'Any'
```

**Cause:** Using a type that isn't defined.

**Fix:** Define the type:
```nl
@type UserData {
  id: string
  name: string
}
```

### Invalid Constraint Value

```
EmissionWarning: Invalid constraint 'min: abc', ignoring
```

**Cause:** Non-numeric value for numeric constraint.

**Fix:**
```nl
@type Product {
  price: number, min: 0        # Use number, not string
  stock: number, max: 10000    # Use number, not string
}
```

---

## Runtime Errors

These errors occur when running generated code.

### Guard Violation

```python
ValueError: Amount must be positive
```

**Cause:** Guard condition failed.

**Example ANLU:**
```nl
[deposit]
GUARDS:
  - amount must be positive -> ValueError("Amount must be positive")
```

**Fix in calling code:**
```python
# Wrong
deposit(account, -50)

# Right
if amount > 0:
    deposit(account, amount)
else:
    handle_invalid_amount()
```

### Invariant Violation

```python
ValueError: Invariant violated: balance >= 0
```

**Cause:** Tried to create object that violates invariant.

**Example:**
```nl
@invariant Account {
  balance >= 0
}
```

```python
# This raises ValueError
account = Account(id="1", owner="Alice", balance=-100)
```

**Fix:** Validate data before creating objects.

### NotImplementedError

```python
NotImplementedError: TODO: Implement 'the optimal result based on criteria'
```

**Cause:** RETURNS contained descriptive text that couldn't be compiled.

**Fix options:**

1. Replace with concrete expression:
```nl
RETURNS: max(scores)
```

2. Implement in literal block:
```nl
@literal python {
def find_optimal(items, criteria):
    # Your implementation here
    return best_item
}
```

---

## Lockfile Errors

### Lockfile Out of Date

```
LockfileError: ANLU 'calculate-tax' has changed since lock
```

**Cause:** Source file changed without recompiling.

**Fix:**
```bash
nlsc compile src/module.nl
# or
nlsc lock:update src/module.nl
```

### Missing Lockfile

```
LockfileWarning: No lockfile found for src/module.nl
```

**Cause:** First compilation, or lockfile was deleted.

**Fix:** Compile to generate lockfile:
```bash
nlsc compile src/module.nl
```

---

## CLI Errors

### File Not Found

```
Error: File not found: src/missing.nl
```

**Cause:** Specified file doesn't exist.

**Fix:** Check the path and filename.

### Invalid Parser

```
Error: Tree-sitter parser not available
Install with: pip install nlsc[treesitter]
```

**Cause:** Requested tree-sitter parser without installing it.

**Fix:**
```bash
pip install "nlsc[treesitter]"
```

### Watch Directory Error

```
Error: Not a directory: src/file.nl
```

**Cause:** `nlsc watch` requires a directory, not a file.

**Fix:**
```bash
nlsc watch src/        # Directory, not file
```

---

## Error Recovery Tips

### 1. Check Line Numbers

Error messages include line numbers:
```
ParseError at line 25: Invalid input definition
```

Go to that line to find the issue.

### 2. Use Verify First

```bash
nlsc verify src/module.nl
```

This checks syntax without generating code, making it faster to iterate.

### 3. Use Verbose Mode

```bash
nlsc test src/module.nl -v
```

Verbose mode shows more details about failures.

### 4. Check Generated Code

If runtime errors occur, examine the generated `.py` file:
```bash
cat src/module.py
```

### 5. Compare with Examples

Check the [Examples](examples.md) for correct syntax.

---

## Getting Help

If you encounter an error not listed here:

1. Check [GitHub Issues](https://github.com/Mnehmos/mnehmos.nls.lang/issues)
2. Search for similar errors
3. Open a new issue with:
   - The full error message
   - The `.nl` file content (or minimal reproduction)
   - NLS version (`nlsc --version`)
   - Python version

---

## Related Documentation

- **[Language Specification](language-spec.md)** — Correct syntax
- **[CLI Reference](cli-reference.md)** — Command options
- **[LLM Reference](llm-reference.md)** — Complete syntax patterns
