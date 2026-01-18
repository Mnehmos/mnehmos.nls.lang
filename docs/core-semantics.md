# Core NLS Semantics

This document defines the target-neutral semantic core of NLS. All target emitters (Python, TypeScript, etc.) must preserve these semantics while adapting to target-specific idioms.

## Overview

NLS semantics are divided into:

1. **Core Semantics** — Must behave identically across all targets
2. **Target Semantics** — May differ in representation but must preserve behavior
3. **Implementation Details** — Left to target discretion

## Expressions

### Literals

| Literal Type | NLS Syntax | Semantics |
|--------------|------------|-----------|
| Number | `42`, `3.14`, `-1` | IEEE 754 double precision floating point |
| String | `"hello"`, `'world'` | UTF-8 encoded text |
| Boolean | `true`, `false` | Two-valued logic |
| None | `none`, `null` | Absence of value |
| List | `[1, 2, 3]` | Ordered, mutable sequence |
| Dict | `{key: value}` | String-keyed associative map |

**Invariants:**
- Numbers: All targets use IEEE 754 doubles (precision may vary for integers)
- Strings: UTF-8 encoding; immutable in semantics
- Lists: 0-indexed; mutable; may be heterogeneous if element type is `any`

### Operators

#### Arithmetic

| Operator | Meaning | Operand Types | Result Type |
|----------|---------|---------------|-------------|
| `+` | Addition | number, number | number |
| `-` | Subtraction | number, number | number |
| `*`, `×` | Multiplication | number, number | number |
| `/`, `÷` | Division | number, number | number |
| `%` | Modulo | number, number | number |

**Invariants:**
- Division by zero raises `DivisionError`
- Integer division uses `//` or explicit `floor(a / b)`

#### Comparison

| Operator | Meaning |
|----------|---------|
| `==` | Structural equality |
| `!=`, `≠` | Structural inequality |
| `<`, `>` | Ordering |
| `<=`, `>=`, `≤`, `≥` | Inclusive ordering |

**Invariants:**
- Equality is structural, not reference-based
- Ordering is defined for numbers and strings; undefined for other types

#### Logical

| Operator | Meaning |
|----------|---------|
| `and`, `&&` | Logical AND (short-circuit) |
| `or`, `\|\|` | Logical OR (short-circuit) |
| `not`, `!` | Logical NOT |

**Invariants:**
- Short-circuit evaluation is required
- Truthiness: `false`, `none`, `0`, `""`, `[]` are falsy; all else truthy

### Function Calls

```
function_name(arg1, arg2, ...)
```

**Semantics:**
- Arguments evaluated left-to-right
- Passed by value (for primitives) or by reference (for objects)
- Return value is the expression result of the function body

### Field Access

```
object.field
```

**Semantics:**
- Accesses named field on object
- Raises `AttributeError` if field doesn't exist
- For types with `@invariant`, field access on valid objects always succeeds

---

## Statements

### Let-Bindings

```nl
1. Calculate result -> result
```

**Semantics:**
- Binds a value to a name
- Bindings are **immutable by default** in NLS semantics
- Scope is local to the containing function

**Target Mapping:**
- Python: `result = <expression>` (relies on convention, not enforcement)
- TypeScript: `const result = <expression>` (enforced)

### Conditionals

NLS uses guard conditions for early exit:

```nl
GUARDS:
  - amount > 0 -> ValueError("Amount must be positive")
```

For inline conditionals in LOGIC:

```nl
3. IF discount_rate > 0 THEN apply discount -> final
```

**Semantics:**
- Guards are evaluated top-to-bottom
- First failing guard raises its error
- IF/THEN/ELSE is an expression, not statement (always has a value)

### Early Return

```nl
EDGE CASES:
  - Empty list -> return none
```

**Semantics:**
- Immediately exits function with given value
- Guards that fail cause early exit with error

---

## Type System

### Primitives

| NLS Type | Semantic Meaning | Python | TypeScript |
|----------|------------------|--------|------------|
| `number` | IEEE 754 double | `float` | `number` |
| `string` | UTF-8 text | `str` | `string` |
| `boolean` | true/false | `bool` | `boolean` |
| `none` | Null value | `None` | `null` |
| `void` | No return | `None` | `void` |
| `any` | Dynamic typing | `Any` | `any` |

### Compound Types

| NLS Type | Meaning | Python | TypeScript |
|----------|---------|--------|------------|
| `list of T` | Ordered sequence | `list[T]` | `T[]` |
| `dict of K to V` | Key-value map | `dict[K, V]` | `Record<K, V>` |
| `T?`, `optional T` | Nullable | `Optional[T]` | `T \| null` |
| `T \| U` | Union | `T \| U` | `T \| U` |

### User-Defined Types

```nl
@type Order {
  id: string, required
  items: list of OrderItem
  total: number
}
```

**Semantics:**
- Creates a record type with named fields
- Fields have types and optional constraints
- `required` fields must be provided at construction
- Omitting `required` allows field to be optional

**Invariants:**
- Type fields are accessed by name
- Field order is preserved (important for some serialization)
- Types are structural, not nominal (duck typing)

### Type Aliases

```nl
@type UserId = string
@type OrderList = list of Order
```

**Semantics:**
- Creates an alias; semantically equivalent to underlying type
- May be treated as distinct by some targets (for documentation)

---

## Error Model

NLS uses typed errors raised through guards.

### Guard Errors

```nl
GUARDS:
  - token must not be empty -> AuthError(MISSING, "Token required")
```

**Components:**
1. **Error Type**: `AuthError`, `ValueError`, `ValidationError`
2. **Error Code** (optional): `MISSING`, `INVALID_FORMAT`
3. **Message**: Human-readable description

**Semantics:**
- Guards fail fast (first violation wins)
- Error types map to target exception/error classes
- Standard errors: `ValueError`, `TypeError`, `RuntimeError`

### Error Propagation

**Design Decision:** NLS uses exceptions, not Result types.

**Rationale:**
- Matches Python's natural error model
- Keeps ANLU specifications focused on happy path
- Guards explicitly document expected failures

**Invariants:**
- Errors propagate up call stack until caught
- Uncaught errors terminate execution
- All guard errors are documented in specification

---

## Semantic Invariants

These MUST be preserved by all target emitters:

### 1. Guard Ordering

Guards are evaluated in specification order. This is observable when guards have side effects (e.g., logging).

### 2. Logic Step Dataflow

Variables assigned in earlier LOGIC steps are available in later steps. Emitters must preserve this dependency order.

### 3. Type Constraints

Field constraints (`required`, `min:`, `max:`) are enforced at construction time. Objects with invariants are always valid after construction.

### 4. Test Semantics

`@test` blocks execute in isolation. Each test case is independent—no shared state.

### 5. Property Semantics

`@property` assertions hold for all valid inputs. Emitters should generate property-based tests (using Hypothesis, fast-check, etc.).

---

## Target-Specific Allowances

These MAY differ between targets:

### Performance Characteristics

- List indexing complexity (O(1) vs O(n))
- String concatenation strategy
- Memory layout of types

### Runtime Representation

- How types are encoded at runtime
- Debug string formats
- Stack trace formatting

### Idioms

- Naming conventions in generated code (snake_case vs camelCase)
- Import style (relative vs absolute)
- Documentation format (docstrings vs JSDoc)

---

## Python Target Mapping

This section documents the **Core NLS → Python** mapping.

### Types

| NLS | Python |
|-----|--------|
| `number` | `float` (or `int` for known integers) |
| `string` | `str` |
| `boolean` | `bool` |
| `none` | `None` |
| `list of T` | `list[T]` |
| `dict of K to V` | `dict[K, V]` |
| `T?` | `Optional[T]` |
| `@type X` | `@dataclass class X` |

### Errors

| NLS Error | Python Exception |
|-----------|------------------|
| `ValueError` | `ValueError` |
| `TypeError` | `TypeError` |
| `RuntimeError` | `RuntimeError` |
| Custom `XError` | `class XError(Exception)` |

### Guards

```nl
GUARDS:
  - amount > 0 -> ValueError("Message")
```

Becomes:

```python
if not (amount > 0):
    raise ValueError("Message")
```

### Logic Steps

```nl
LOGIC:
  1. Calculate tax -> tax
  2. Add fee -> total
```

Becomes:

```python
tax = calculate_tax(...)  # Step 1
total = tax + fee         # Step 2
```

---

## Future Considerations

### TypeScript Target (Planned)

Will require:
- `number` → `number` (same IEEE 754)
- `@type` → `interface` or `type`
- Guards → thrown `Error` objects
- Properties → `fast-check` tests

### Result Type Option

Future version may support:

```nl
@config error_model = "result"

[divide]
RETURNS: Result<number, DivisionError>
```

This would generate `Either`/`Result` types instead of exceptions.

---

## References

- [Language Specification](language-spec.md) — Surface syntax
- [nl-grammar.ebnf](nl-grammar.ebnf) — Formal grammar
- Issue #88 — Core NLS Semantics tracking issue
