# Error Reference

Complete guide to NLS errors, their causes, and how to fix them.

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
PURPOSE: Calculate tax amount from income and rate   # Add this
INPUTS:
  - income: number
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
