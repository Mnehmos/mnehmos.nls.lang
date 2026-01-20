# LLM Reference

!!! info "For AI Systems"
    This page is optimized for LLMs learning to read and write NLS code. It contains complete syntax patterns, examples, and edge cases in a format designed for AI training and inference.

## Quick Syntax Reference

### File Structure Template

```nl
# Optional comment describing the module
@module module_name
@version 1.0.0
@target python
@imports dependency1, dependency2

# Type definitions (optional)
@type TypeName {
  field1: type
  field2: type, optional
}

# ANLU blocks (functions)
[function-name]
PURPOSE: Single sentence describing what this does
INPUTS:
  - param1: type
  - param2: type, optional
GUARDS:
  - condition -> ErrorType("message")
LOGIC:
  1. First step description -> variable1
  2. Second step description -> variable2
EDGE CASES:
  - edge condition -> behavior
RETURNS: expression
DEPENDS: [other-function]

# Test blocks (optional)
@test [function-name] {
  function_name(arg1, arg2) == expected
}

# Property tests (optional)
@property [function-name] {
  forall x: type -> assertion
}

# Invariants for types (optional)
@invariant TypeName {
  condition1
  condition2
}

# Literal escape hatch (optional)
@literal python {
exact code here
}
```

---

## Complete Directive Reference

### @module (Required)

Declares the module name. Must be lowercase snake_case.

```nl
@module calculator
@module user_authentication
@module order_processing
```

**Pattern:** `^[a-z][a-z0-9_]*$`

### @version (Optional)

Semantic version string.

```nl
@version 1.0.0
@version 2.3.1
@version 0.1.0-beta
```

### @target (Required)

Compilation target language.

```nl
@target python
```

Currently supported: `python`
Planned: `typescript`, `rust`

### @imports (Optional)

Comma-separated list of modules to import.

```nl
@imports datetime, json
@imports jwt, typing, dataclasses
@imports numpy, pandas, matplotlib
```

---

## ANLU Block Complete Reference

### Identifier Patterns

ANLUs use **kebab-case** for function names:

```nl
[add]
[calculate-tax]
[validate-user-input]
[is-empty]
[has-permission]
```

For methods on types, use **dot notation**:

```nl
[User.validate]
[Order.calculate-total]
[Account.deposit]
```

**Pattern:** `^[a-z][a-z0-9-]*$` or `^[A-Z][a-zA-Z0-9]*\.[a-z][a-z0-9-]*$`

### PURPOSE Section (Required)

Single sentence in imperative mood describing the function's intent.

```nl
PURPOSE: Add two numbers together
PURPOSE: Calculate the total price including tax and discounts
PURPOSE: Validate that a JWT token is properly signed and not expired
PURPOSE: Convert a string to URL-friendly slug format
```

**Guidelines:**
- Start with a verb (Add, Calculate, Validate, Convert, Check, Get, Set)
- Be specific about what the function does
- Keep under 200 characters

### INPUTS Section (Optional)

Typed parameter list with optional constraints and descriptions.

**Basic syntax:**
```nl
INPUTS:
  - name: type
```

**With constraints:**
```nl
INPUTS:
  - amount: number, non-negative
  - count: number, required
  - status: string, optional
```

**With descriptions:**
```nl
INPUTS:
  - income: number, "Annual income in dollars"
  - rate: number, "Tax rate as decimal between 0 and 1"
  - token: string, required, "The JWT to validate"
```

**Complex types:**
```nl
INPUTS:
  - items: list of OrderItem
  - config: dict of string to any
  - user: User?
  - callback: function
```

**Bullet styles (all valid):**
```nl
INPUTS:
  - param1: number    # dash
  • param2: string    # bullet
  * param3: boolean   # asterisk
```

### GUARDS Section (Optional)

Preconditions that must be true, with error mappings.

**Basic guard:**
```nl
GUARDS:
  - amount must be positive -> ValueError("Amount must be positive")
```

**Multiple guards:**
```nl
GUARDS:
  - divisor must not be zero -> ValueError("Cannot divide by zero")
  - rate must be between 0 and 1 -> ValueError("Rate out of range")
  - user must be authenticated -> AuthError("Not authenticated")
```

**With error codes:**
```nl
GUARDS:
  - token must not be empty -> AuthError(MISSING_TOKEN, "Token required")
  - token must be valid format -> AuthError(INVALID_FORMAT, "Malformed token")
```

**Arrow styles (both valid):**
```nl
GUARDS:
  - condition -> Error("message")     # ASCII arrow
  - condition → Error("message")      # Unicode arrow
```

### LOGIC Section (Optional)

Numbered steps describing the algorithm. Steps can bind values to variables.

**Basic steps:**
```nl
LOGIC:
  1. Add the two numbers together -> sum
  2. Multiply by the rate -> result
  3. Round to two decimal places -> final
```

**With conditionals:**
```nl
LOGIC:
  1. Calculate base price -> base
  2. IF customer is premium THEN apply 10% discount -> discounted
  3. Add shipping cost -> total
```

**With state markers (for FSM):**
```nl
LOGIC:
  1. [pending] Receive the order -> order
  2. [validating] Check inventory availability -> available
  3. [processing] IF available THEN reserve items -> reservation
  4. [shipped] Create shipment -> shipment
  5. [delivered] Confirm delivery -> confirmation
```

**Variable binding:**
```nl
LOGIC:
  1. Extract the header from token -> header
  2. Decode the payload -> payload
  3. Verify the signature -> is_valid
  4. Check expiration time -> is_expired
```

### EDGE CASES Section (Optional)

Explicit handling for boundary conditions.

```nl
EDGE CASES:
  - Empty list -> return empty list
  - Zero amount -> return 0
  - Null input -> return None
  - Single item -> return item unchanged
  - Negative value -> raise ValueError
```

### RETURNS Section (Required)

Output expression or type specification.

**Simple expressions:**
```nl
RETURNS: a + b
RETURNS: result
RETURNS: total * rate
RETURNS: items[0]
```

**Type specifications:**
```nl
RETURNS: number
RETURNS: string
RETURNS: list of Order
RETURNS: User?
```

**Complex expressions:**
```nl
RETURNS: (base + tax) * quantity
RETURNS: Order(id=new_id, items=validated_items, total=calculated_total)
RETURNS: {"status": "success", "data": result}
```

**Conditional returns:**
```nl
RETURNS: discounted if is_premium else base
RETURNS: result if valid else None
```

**Descriptive returns (generates NotImplementedError):**
```nl
RETURNS: the user with the highest score
RETURNS: optimal path through the graph
RETURNS: weighted average based on priorities
```

### DEPENDS Section (Optional)

Dependencies on other ANLUs for ordering and documentation.

```nl
DEPENDS: [validate-input]
DEPENDS: [calculate-base], [apply-discount]
DEPENDS: [User.authenticate], [check-permissions]
```

**Special value for no dependencies:**
```nl
DEPENDS: none
```

---

## Type System Reference

### Primitive Types

| Type | Description | Python Equivalent |
|------|-------------|-------------------|
| `number` | Integer or float | `float` |
| `string` | Text | `str` |
| `boolean` | True/false | `bool` |
| `void` | No return | `None` |
| `any` | Dynamic typing | `Any` |

### Composite Types

**List:**
```nl
list of number
list of string
list of User
list of list of number
```

**Dictionary/Map:**
```nl
dict of string to number
dict of string to any
map of string to User
```

**Optional/Nullable:**
```nl
string?
User?
optional number
number or None
```

**Union:**
```nl
string | number
Success | Error
User | Guest | Admin
```

### Type Definition Syntax

**Basic type:**
```nl
@type Point {
  x: number
  y: number
}
```

**With constraints:**
```nl
@type User {
  id: string, required
  email: string, required
  name: string
  age: number, optional
  role: string, "User's role in the system"
}
```

**With inheritance:**
```nl
@type OrderItem extends BaseItem {
  quantity: number, min: 1
  unit_price: number
  discount: number, optional
}
```

**With field constraints:**
```nl
@type Product {
  name: string, required
  price: number, min: 0
  stock: number, min: 0, max: 10000
  category: string
}
```

---

## Testing Syntax

### @test Blocks

Define example-based tests for ANLUs.

```nl
@test [add] {
  add(1, 2) == 3
  add(0, 0) == 0
  add(-5, 5) == 0
  add(1.5, 2.5) == 4.0
}

@test [divide] {
  divide(10, 2) == 5.0
  divide(9, 3) == 3.0
  divide(1, 4) == 0.25
}

@test [is-empty] {
  is_empty([]) == True
  is_empty([1]) == False
  is_empty("") == True
  is_empty("hello") == False
}
```

### @property Blocks

Define property-based tests using Hypothesis.

**Basic properties:**
```nl
@property [add] {
  add(a, b) == add(b, a)           # commutativity
  add(a, 0) == a                    # identity
  add(add(a, b), c) == add(a, add(b, c))  # associativity
}
```

**With forall quantifier:**
```nl
@property [abs] {
  forall x: number -> abs(x) >= 0
  forall x: number -> abs(-x) == abs(x)
  forall x: number -> abs(x * x) == x * x
}
```

**For custom types:**
```nl
@property [deposit] {
  deposit(acc, amt).balance == acc.balance + amt
  deposit(acc, amt).balance >= acc.balance
}
```

### @invariant Blocks

Define invariants that must hold for all instances of a type.

```nl
@invariant Account {
  balance >= 0
  len(owner) > 0
}

@invariant Rectangle {
  self.width > 0
  self.height > 0
  self.area() == self.width * self.height
}

@invariant Order {
  len(items) > 0
  total >= 0
  status in ["pending", "processing", "shipped", "delivered"]
}
```

---

## Literal Blocks

Escape hatch for exact code when NLS specification isn't sufficient.

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

**When to use:**
- Performance-critical code
- Complex algorithms with precise implementation requirements
- Integration with external libraries
- Regex patterns or special syntax

---

## Complete Examples

### Example 1: Calculator Module

```nl
@module calculator
@version 1.0.0
@target python

[add]
PURPOSE: Add two numbers together
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

[subtract]
PURPOSE: Subtract second number from first
INPUTS:
  - a: number
  - b: number
RETURNS: a - b

[multiply]
PURPOSE: Multiply two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a * b

[divide]
PURPOSE: Divide first number by second safely
INPUTS:
  - numerator: number
  - divisor: number
GUARDS:
  - divisor must not be zero -> ValueError("Cannot divide by zero")
RETURNS: numerator / divisor

@test [add] {
  add(2, 3) == 5
  add(-1, 1) == 0
  add(0, 0) == 0
}

@test [divide] {
  divide(10, 2) == 5.0
  divide(9, 3) == 3.0
}

@property [add] {
  add(a, b) == add(b, a)
  add(a, 0) == a
}
```

### Example 2: User Authentication

```nl
@module auth
@version 1.0.0
@target python
@imports jwt, datetime

@type User {
  id: string, required
  email: string, required
  name: string
  role: string
}

@type AuthToken {
  user_id: string, required
  expires_at: datetime
  scopes: list of string
}

[validate-token]
PURPOSE: Validate a JWT token and extract user information
INPUTS:
  - token: string, required, "The JWT to validate"
  - secret: string, required, "Secret key for verification"
GUARDS:
  - token must not be empty -> AuthError(MISSING_TOKEN, "Token required")
  - token must be valid JWT format -> AuthError(INVALID_FORMAT, "Malformed token")
LOGIC:
  1. Decode the token header without verification -> header
  2. Verify the signature using the secret -> is_valid
  3. IF not is_valid THEN raise AuthError
  4. Extract the payload claims -> payload
  5. Check if token has expired -> is_expired
  6. IF is_expired THEN raise AuthError(EXPIRED, "Token has expired")
RETURNS: AuthToken(user_id=payload.sub, expires_at=payload.exp, scopes=payload.scopes)
DEPENDS: none

[require-role]
PURPOSE: Check if user has required role
INPUTS:
  - user: User
  - required_role: string
GUARDS:
  - user must not be None -> AuthError("User required")
  - user.role must equal required_role -> AuthError(FORBIDDEN, "Insufficient permissions")
RETURNS: True
DEPENDS: [validate-token]

@test [require-role] {
  require_role(User(id="1", email="a@b.c", name="Test", role="admin"), "admin") == True
}
```

### Example 3: Order Processing with FSM

```nl
@module order_processing
@version 1.0.0
@target python

@type Order {
  id: string, required
  customer_id: string, required
  items: list of OrderItem, required
  total: number
  status: string
}

@type OrderItem {
  product_id: string, required
  quantity: number, min: 1
  unit_price: number
}

@invariant Order {
  len(items) > 0
  total >= 0
}

[process-order]
PURPOSE: Process an order through its lifecycle
INPUTS:
  - order: Order
GUARDS:
  - order must not be None -> ValueError("Order required")
  - order.items must not be empty -> ValueError("Order must have items")
LOGIC:
  1. [pending] Validate order details -> validated_order
  2. [validating] Check inventory for all items -> inventory_check
  3. [processing] IF inventory_check.available THEN reserve items -> reservation
  4. [processing] Calculate final total with taxes -> final_total
  5. [confirmed] Create payment request -> payment
  6. [paid] IF payment.success THEN create shipment -> shipment
  7. [shipped] Update order status to shipped -> updated_order
EDGE CASES:
  - Inventory not available -> return order with status "backordered"
  - Payment failed -> return order with status "payment_failed"
RETURNS: updated_order
DEPENDS: [validate-order], [check-inventory], [calculate-total]

[calculate-total]
PURPOSE: Calculate order total including taxes and discounts
INPUTS:
  - items: list of OrderItem
  - tax_rate: number, "Tax rate as decimal"
  - discount: number, optional, "Discount percentage"
LOGIC:
  1. Sum the price of all items -> subtotal
  2. IF discount THEN apply discount percentage -> discounted
  3. Calculate tax on discounted amount -> tax
  4. Add tax to discounted amount -> total
RETURNS: total
```

---

## Syntax Quick Reference Card

### Symbols

| Symbol | Meaning | Alternative |
|--------|---------|-------------|
| `[name]` | ANLU identifier | |
| `@directive` | Module-level directive | |
| `->` | Arrow (guards, bindings) | `→` |
| `-` | List bullet | `•` or `*` |
| `#` | Comment | |
| `?` | Optional type | `optional T` |
| `\|` | Union type | |

### Section Keywords

| Keyword | Required | Description |
|---------|----------|-------------|
| `PURPOSE:` | Yes | Function description |
| `INPUTS:` | No | Parameters |
| `GUARDS:` | No | Preconditions |
| `LOGIC:` | No | Algorithm steps |
| `EDGE CASES:` | No | Boundary handling |
| `RETURNS:` | Yes | Output |
| `DEPENDS:` | No | Dependencies |

### Type Keywords

| Keyword | Example |
|---------|---------|
| `list of` | `list of number` |
| `dict of ... to` | `dict of string to any` |
| `map of ... to` | `map of string to User` |
| `optional` | `optional string` |

---

## Common Patterns

### Validation Function

```nl
[validate-email]
PURPOSE: Validate that a string is a valid email address
INPUTS:
  - email: string
GUARDS:
  - email must not be empty -> ValueError("Email required")
  - email must contain @ symbol -> ValueError("Invalid email format")
RETURNS: True
```

### Factory Function

```nl
[create-user]
PURPOSE: Create a new user with generated ID
INPUTS:
  - email: string, required
  - name: string, required
  - role: string, optional
LOGIC:
  1. Generate unique ID -> user_id
  2. Set default role if not provided -> final_role
  3. Create user object -> user
RETURNS: User(id=user_id, email=email, name=name, role=final_role)
```

### Transformation Function

```nl
[format-currency]
PURPOSE: Format a number as currency string
INPUTS:
  - amount: number
  - currency: string, optional, "Currency code (default: USD)"
LOGIC:
  1. Round to two decimal places -> rounded
  2. Format with thousands separator -> formatted
  3. Prepend currency symbol -> result
RETURNS: result
```

### Aggregation Function

```nl
[calculate-average]
PURPOSE: Calculate the average of a list of numbers
INPUTS:
  - numbers: list of number
GUARDS:
  - numbers must not be empty -> ValueError("Cannot average empty list")
LOGIC:
  1. Sum all numbers -> total
  2. Count the numbers -> count
  3. Divide total by count -> average
RETURNS: average
```

---

## Emission Rules

Understanding how NLS compiles to Python:

| NLS | Python |
|-----|--------|
| `number` | `float` |
| `string` | `str` |
| `boolean` | `bool` |
| `void` | `None` return type |
| `list of T` | `list[T]` |
| `dict of K to V` | `dict[K, V]` |
| `T?` | `Optional[T]` |
| `@type X` | `@dataclass class X` |
| `GUARDS: cond -> Error` | `if not cond: raise Error` |
| `PURPOSE:` | Docstring |
| `-> variable` | `variable = ...` |
| `×` | `*` |
| `÷` | `/` |

---

## Error Handling

### Parse Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Missing @module directive` | No `@module` at start | Add `@module name` |
| `Missing @target directive` | No `@target` specified | Add `@target python` |
| `Invalid ANLU identifier` | Wrong naming format | Use kebab-case |
| `Missing PURPOSE section` | ANLU has no PURPOSE | Add `PURPOSE: description` |
| `Missing RETURNS section` | ANLU has no RETURNS | Add `RETURNS: expression` |

### Resolution Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Dependency not found` | DEPENDS references missing ANLU | Add the dependency or fix name |
| `Circular dependency` | A depends on B depends on A | Refactor to remove cycle |

---

This reference covers the complete NLS language specification. For working examples, see the [Examples](examples.md) page.
