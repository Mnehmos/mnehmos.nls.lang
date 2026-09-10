# Language Specification

This document defines the complete syntax of `.nl` files, the semantic
guarantees the compiler checks, and — just as important — what is explicitly
**not** supported.

Revision: 2026-09, describing the language as implemented by `nlsc` 0.2.x.
The compiler validates this spec at two boundaries: the surface parser and
the target-neutral IR ([IR specification](ir-spec.md)). A construct is
*supported* when it lowers to structural IR; constructs outside that core are
either rejected with a diagnostic or carried as explicitly marked *foreign*
content (see [Unsupported and out of scope](#unsupported-and-out-of-scope)).

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

### `@use`

Declare a dependency on a **stdlib domain module**.

```nl
@use math.core
```

`@use` supports an optional major-version prefix:

```nl
@use v1.math.core
```

Resolution (Issue #90, Slice C):

1. Project-local override: `.nls/stdlib/`
2. CLI override roots: `nlsc compile ... --stdlib-path <dir>` (repeatable; earlier flags win)
3. Environment override roots: `NLS_STDLIB_PATH` (path-list; left-to-right)
4. Bundled stdlib: `nlsc/stdlib/`

Domain-to-path mapping is deterministic:

* `math.core` → `v{major}/math/core.nl`

If the domain cannot be resolved, compilation fails with a stable error code (see [`docs/error-reference.md`](docs/error-reference.md)).

### Edit Provenance (normative reference)

All systems that emit or persist `.nl` edit metadata SHOULD use the canonical Edit Provenance schema and validation contract defined in [`Issue #93 — Standardized Edit Provenance for .nl Changes`](design/issue-93-edit-provenance.md).

Normative requirements for provenance producers/consumers:

1. Records MUST include `schema_version`, `record_id`, `timestamp`, `target`, `edit`, and `source`.
2. `schema_version` MUST be semver and MUST use a supported major.
3. `source.kind` MUST be one of `human`, `llm`, or `tool`.
4. `edit.operation` MUST be one of `create`, `update`, `delete`, `rename`, or `move`.
5. Hash fields in `target` MUST follow the nullability and SHA-256 rules defined by Issue #93.

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
- **Conditionals**: `IF condition THEN action` and total branches
  `IF condition THEN action ELSE action`. A value bound in only one arm
  of a branch cannot be used afterwards (ESEM010) — make the branch
  total with `ELSE ... -> name` so every path defines it. Bindings are
  immutable in checked code; rebinding the same name is rejected under
  `--strict` (ESEM011).
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

## Semantics: what the compiler guarantees

Compilation runs one shared contract before any backend emits code. `verify`
and `compile` report the same diagnostics for every target.

### Two severity tiers

**Always fatal** (any mode, `verify`/`compile`/`run`/`test`/`watch`):

- unknown `[anlu]` calls (`ESEM001`);
- wrong argument counts (`ESEM002`);
- values used before they are defined (`ESEM004`);
- unknown fields, constructor fields, or field access on non-records (`ESEM005`);
- incompatible operands such as `"name" + 1` (`ESEM006`);
- duplicate identifiers and kebab/snake target-name collisions (`ESEM007`);
- a value defined on only one branch path and used afterwards (`ESEM010`);
- augmented assignment targeting an undefined value (reported as `ESEM004`).

**Strict-only** — warnings in default (scaffold) mode, failures under
`--strict` or `nlsc ci`:

- argument type mismatches (`ESEM003`);
- DEPENDS drift versus the calls actually made (`ESEM008`);
- undeclared foreign calls and unresolved bound methods (`ESEM009`);
- rebinding an already-defined name (`ESEM011`);
- guard error types that are neither builtins nor declared `@type`s (`ESEM012`).

### Type checking

Calls resolve through a semantic symbol table: module ANLUs (both `[kebab-case]`
and `snake_case` spellings), declared `@type` records, documented builtins
(`len`, `sum`, `max`, `min`, `abs`, `round`, `sqrt`, `str`, `int`, `float`,
`bool`), and `@imports` names (usable as explicit unknowns). Optional inputs
may be omitted at call sites. Self-recursion is supported and needs no
self-entry in `DEPENDS`.

Type compatibility is conservative: `any`/unknown values pass checks but are
never treated as proof of type safety. `integer` values are accepted where
`number` is expected.

### Bindings, branches, and guards

- LOGIC steps execute in source order; a binding is visible from its defining
  step onward, and in `RETURNS`.
- Bindings are **immutable** in checked code: rebinding is `ESEM011`.
- A branch is *total* only when every path binds the joined value:
  `IF c THEN a ELSE b` (both arms binding the same name, or both effect-only).
  A one-armed branch that binds a value makes that value partial —
  using it afterwards is `ESEM010`, not a runtime `UnboundLocalError`.
- Guards evaluate in declaration order and the first failing guard raises its
  typed error. No complementary conditions or exhaustiveness are inferred from
  prose: make branches explicit.
- `RETURNS` is either a value expression (`RETURNS: total`) or a declared
  result type (`RETURNS: number`). A declared type without an implementing
  expression is not a default value — strict mode rejects it (`EIR004`).
  `none`/`void` are valid explicit results.

### Effects and failure contracts

Every operation carries inferred contracts in the IR:

- **failures** (`fails`): typed guard failures, failures propagated
  transitively from called operations, and an `unknown` marker for foreign
  calls, method calls, division/modulo, indexing, and `@literal` bodies.
  Unknown external failures are never an empty set, and pure operations are
  analyzed-empty.
- **effects** (`effects`): analyzed-empty for purely structural code;
  `unknown` markers for anything that can touch the world.

These contracts participate in lockfile semantic hashes: changing a guard
message or adding a foreign call invalidates the affected entries and their
callers. Portability: guard failures raise the same `ValueError`-style
identity with the same message on Python and TypeScript; non-builtin error
types get generated classes on both targets.

### Execution and analysis are separate

The emitters execute LOGIC **sequentially**; `nlsc graph` displays
data-dependency layers, and a layer is labeled `parallel-eligible` only when
effect, alias, and failure constraints certify independence
(see [the parallel analysis](../nlsc/parallel.py)). No automatic concurrency
or reordering is claimed or performed.

### Literal blocks

`@literal python { ... }` is a sanctioned escape hatch: the body is carried
verbatim as a foreign implementation. It contributes an `unknown` effect and
failure marker, participates in the lockfile hash, and is emitted only for the
target it names.

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

## Unsupported and out of scope

This list is authoritative: if a construct is here, its absence is a design
decision, not a compiler bug. Anything not listed as supported should be
reported as an issue.

### Rejected executable content

The following are *not* part of the checked core. They lower to explicitly
marked foreign nodes: accepted (with an `EIR001`/`EIR002` diagnostic) in
default scaffold mode, **rejected under `--strict` and `nlsc ci`**, and they
block checked emission (`EIR003`):

| Construct | Example | Status |
| --- | --- | --- |
| List/dict/set comprehensions | `[x for x in items]` | Foreign; LLM/target-specific escape |
| Conditional expressions | `a if c else b` | Use `IF/THEN/ELSE` steps instead |
| f-strings, lambdas, slices, star-args | `f"{x}"`, `lambda t: t` | Foreign |
| Dict/set literals | `{"a": 1}` | Foreign |
| Prose with executable intent | `Process payment -> pay` | `EIR002`; rewrite as a call or `@literal` |
| Declared return type without a value | `RETURNS: number` alone | `EIR004`; return the value or `none` |

### Not yet implemented (tracked)

| Feature | Tracking |
| --- | --- |
| Loops in LOGIC (`WHILE`/`FOR` steps; the IR has a reserved loop region) | #196 follow-up |
| try/catch-style handlers, retry/timeout policies | #198, #201 |
| Typestate/resource state transitions | #200 |
| `FAILS`/`RAISES` declarations (failure sets are inferred) | #198 |
| Read/write resource identities in effect contracts | #197 |
| Rust target | #24 |
| Package registry / versioned dependency resolution | #27, #146 |

### Deliberately out of scope

- **Automatic concurrency**: scheduling claims are analysis-only; nothing is
  reordered or run in parallel by the toolchain.
- **Global commutativity proofs** for arbitrary operations.
- **Guessing intent**: prose is never inferred into executable code — the
  compiler reports what it cannot prove instead of inventing behavior.

---

## Diagnostics index

Error messages name their code; the table below points at the spec section
that defines the rule. `nlsc explain <CODE>` prints the full catalog entry
with causes and next steps.

| Code family | Rule | Section |
| --- | --- | --- |
| `EPARSE001` | Surface syntax, step numbering (duplicate step numbers name both lines) | [LOGIC](#logic), [ANLU Blocks](#anlu-blocks) |
| `EIR001`–`EIR004` | Structural lowering: tokenization, foreign constructs, declared-type returns | [Unsupported and out of scope](#unsupported-and-out-of-scope) |
| `ESEM001`, `ESEM002`, `ESEM009` | Call resolution and arity | [Type checking](#type-checking) |
| `ESEM003` | Argument types | [Type checking](#type-checking) |
| `ESEM004`, `ESEM011` | Binding definition and immutability | [Bindings, branches, and guards](#bindings-branches-and-guards) |
| `ESEM005`, `ESEM006` | Fields and operand types | [Type checking](#type-checking) |
| `ESEM007` | Identifier identity | [ANLU Blocks](#anlu-blocks) |
| `ESEM008` | DEPENDS contract | [ANLU Blocks](#anlu-blocks) |
| `ESEM010` | Branch totality | [Bindings, branches, and guards](#bindings-branches-and-guards) |
| `ESEM012` | Guard error identity | [Effects and failure contracts](#effects-and-failure-contracts) |
| `ESEM013` | Module/file name shadows a host stdlib module | [File Structure](#file-structure) |

---

## Grammar Reference

For the complete formal grammar, see [nl-grammar.ebnf](nl-grammar.ebnf).
