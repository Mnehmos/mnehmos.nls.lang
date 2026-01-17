# Language Specification

This document defines the complete syntax of `.nl` files.

## File Structure

An `.nl` file consists of:

1. **Directives** — Module metadata (`@module`, `@version`, `@target`, `@imports`)
2. **ANLU Blocks** — Function specifications (`[name]`)
3. **Type Definitions** — Custom types (`@type`)
4. **Test Blocks** — Test specifications (`@test`)
5. **Literal Blocks** — Code escape hatches (`@literal`)
6. **Comments** — Lines starting with `#`

## Directives

### `@module`

**Required.** Declares the module name.

```nl
@module calculator
```

Pattern: `^[a-z][a-z0-9_]*$` (lowercase snake_case)

### `@version`

Optional semantic version.

```nl
@version 1.0.0
```

### `@target`

**Required.** Specifies the compilation target.

```nl
@target python
```

Supported: `python` (more coming)

### `@imports`

Optional comma-separated import list.

```nl
@imports jwt, datetime, typing
```

---

## ANLU Blocks

ANLU (Atomic Natural Language Unit) blocks define functions.

```nl
[function-name]
PURPOSE: Single sentence describing what this does
INPUTS:
  - param1: type
  - param2: type, optional
GUARDS:
  - condition -> ErrorType("message")
LOGIC:
  1. Description of step -> variable
  2. Another step
EDGE CASES:
  - condition -> behavior
RETURNS: expression
DEPENDS: [other-function], [another]
```

### Identifier

ANLU names use **kebab-case**:

```nl
[calculate-tax]
[is-empty]
[validate-user-token]
```

Pattern: `^[a-z][a-z0-9-]*$`

For methods, use dot notation:

```nl
[User.validate]
[Order.calculate-total]
```

### PURPOSE

**Required.** Single sentence in imperative mood.

```nl
PURPOSE: Calculate the total price including tax
```

### INPUTS

Typed parameter list with optional constraints.

```nl
INPUTS:
  - amount: number
  - rate: number, "Tax rate as decimal"
  - currency: string, optional
```

Bullets can be `•`, `-`, or `*`.

### GUARDS

Preconditions with error mappings.

```nl
GUARDS:
  - amount must be non-negative -> ValueError("Amount cannot be negative")
  - rate must be between 0 and 1 -> ValidationError(INVALID_RATE, "Rate must be 0-1")
```

### LOGIC

Numbered steps describing the algorithm.

```nl
LOGIC:
  1. Calculate base tax -> tax
  2. Add service fee if applicable -> fee
  3. Combine tax and fee -> total
```

Steps can include:

- **Output binding**: `-> variable`
- **Conditionals**: `IF condition THEN action`
- **State markers**: `[state] action`

### EDGE CASES

Explicit boundary condition handling.

```nl
EDGE CASES:
  - Zero amount -> return 0
  - Empty list -> return None
```

### RETURNS

**Required.** Output expression or type.

```nl
RETURNS: base + tax
RETURNS: TaxResult with amount, effective_rate
RETURNS: list of Order
```

### DEPENDS

Dependencies on other ANLUs.

```nl
DEPENDS: [validate-input], [calculate-base]
```

---

## Type System

### Primitives

| Type      | Description                 |
| --------- | --------------------------- |
| `number`  | Integer or float            |
| `string`  | Text                        |
| `boolean` | `true` / `false`            |
| `void`    | No return value             |
| `any`     | Dynamic typing escape hatch |

### Composites

**List:**

```nl
list of number
list of User
```

**Optional:**

```nl
string?
User?
```

**Map:**

```nl
map of string to number
```

**Union:**

```nl
string | number
Success | Error
```

---

## Type Definitions

Define custom types with `@type`:

```nl
@type Point {
  x: number
  y: number
}

@type Order {
  id: string, required
  items: list of OrderItem
  total: number, "Order total in cents"
  status: string
}
```

### Inheritance

```nl
@type OrderItem extends BaseItem {
  quantity: number
  price: number
}
```

### Field Constraints

```nl
@type User {
  email: string, required
  age: number, optional
  role: string, "User role in system"
}
```

---

## Test Blocks

Define test cases with `@test`:

```nl
@test [add] {
  add(1, 2) == 3
  add(0, 0) == 0
  add(-5, 5) == 0
}

@test [divide] {
  divide(10, 2) == 5.0
  divide(9, 3) == 3.0
}
```

Test blocks generate executable pytest code.

---

## Literal Blocks

Escape hatch for exact code when needed:

```nl
[slugify]
PURPOSE: Convert text to URL-friendly slug format
INPUTS:
  - text: string

@literal python {
import re

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug format."""
    text = text.lower().strip()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^a-z0-9-]', '', text)
    return text.strip('-')
}
```

Literal blocks bypass the compiler and emit code exactly as written.

---

## Comments

Lines starting with `#` are comments:

```nl
# Math Module
# This provides basic arithmetic operations

@module math
@target python

# Addition function
[add]
PURPOSE: Add two numbers
...
```

---

## Formatting Notes

1. **Bullets** are flexible: `•`, `-`, or `*`
2. **Arrows** are flexible: `→` (Unicode) or `->` (ASCII)
3. **Section headers** are case-insensitive
4. **Indentation** uses spaces for visual structure
5. **Unicode** is supported in text content

## Grammar Reference

For the complete formal grammar, see [nl-grammar.ebnf](nl-grammar.ebnf).
