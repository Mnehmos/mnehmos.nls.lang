# Type System

NLS has a rich type system designed for clarity and safety. Types map directly to Python types with full type hints.

## Primitive Types

### number

Represents any numeric value (integers and floats).

```nl
INPUTS:
  - count: number
  - price: number
  - rate: number
```

**Python mapping:** `float`

!!! note "Integer Handling"
    All numbers are floats in NLS. For integer-specific operations, use Python's `int()` in literal blocks.

### string

Text values of any length.

```nl
INPUTS:
  - name: string
  - email: string
  - description: string
```

**Python mapping:** `str`

### boolean

True or false values.

```nl
INPUTS:
  - is_active: boolean
  - has_permission: boolean
```

**Python mapping:** `bool`

**Literals:** `true`, `false`, `True`, `False`

### void

Indicates a function returns nothing.

```nl
[log-message]
PURPOSE: Log a message to the console
INPUTS:
  - message: string
RETURNS: void
```

**Python mapping:** `None` return type

### any

Dynamic typing escape hatch. Use sparingly.

```nl
INPUTS:
  - data: any
  - callback: any
```

**Python mapping:** `Any` from `typing`

---

## Composite Types

### list of T

Ordered, mutable sequence of elements.

```nl
INPUTS:
  - numbers: list of number
  - users: list of User
  - items: list of OrderItem
  - matrix: list of list of number
```

**Python mapping:** `list[T]`

**Examples:**

| NLS | Python |
|-----|--------|
| `list of number` | `list[float]` |
| `list of string` | `list[str]` |
| `list of User` | `list[User]` |
| `list of list of number` | `list[list[float]]` |

### dict of K to V / map of K to V

Key-value mapping.

```nl
INPUTS:
  - config: dict of string to any
  - scores: dict of string to number
  - user_cache: map of string to User
```

**Python mapping:** `dict[K, V]`

**Examples:**

| NLS | Python |
|-----|--------|
| `dict of string to number` | `dict[str, float]` |
| `dict of string to any` | `dict[str, Any]` |
| `map of string to User` | `dict[str, User]` |

### Optional Types

Values that may be absent.

```nl
INPUTS:
  - middle_name: string?
  - config: Config?
  - deadline: string, optional
```

**Syntax variants:**

- `T?` — Shorthand optional
- `optional T` — Explicit optional
- Field with `optional` constraint

**Python mapping:** `Optional[T]` or `T | None`

### Union Types

Values that can be one of several types.

```nl
INPUTS:
  - id: string | number
  - result: Success | Error
  - value: string | number | boolean
```

**Python mapping:** `T | U` (Python 3.10+) or `Union[T, U]`

---

## Custom Type Definitions

### Basic @type

Define a new record type:

```nl
@type Point {
  x: number
  y: number
}

@type User {
  id: string
  email: string
  name: string
}
```

**Python output:**

```python
from dataclasses import dataclass

@dataclass
class Point:
    """Point type."""
    x: float
    y: float

@dataclass
class User:
    """User type."""
    id: str
    email: str
    name: str
```

### Field Constraints

Add constraints to fields:

```nl
@type Product {
  id: string, required
  name: string, required
  price: number, min: 0
  stock: number, min: 0, max: 10000
  description: string, optional
  category: string, "Product category for filtering"
}
```

**Constraint types:**

| Constraint | Meaning | Example |
|------------|---------|---------|
| `required` | Field must be provided | `id: string, required` |
| `optional` | Field can be omitted | `notes: string, optional` |
| `min: N` | Minimum numeric value | `price: number, min: 0` |
| `max: N` | Maximum numeric value | `count: number, max: 100` |
| `"description"` | Human-readable description | `email: string, "User's email"` |

### Type Inheritance

Use `extends` for inheritance:

```nl
@type BaseEntity {
  id: string, required
  created_at: string
  updated_at: string
}

@type User extends BaseEntity {
  email: string, required
  name: string
  role: string
}

@type Product extends BaseEntity {
  name: string, required
  price: number, min: 0
  category: string
}
```

**Python output:**

```python
@dataclass
class BaseEntity:
    id: str
    created_at: str
    updated_at: str

@dataclass
class User(BaseEntity):
    email: str
    name: str
    role: str

@dataclass
class Product(BaseEntity):
    name: str
    price: float
    category: str
```

### Nested Types

Types can reference other types:

```nl
@type Address {
  street: string
  city: string
  country: string
  postal_code: string
}

@type Customer {
  id: string, required
  name: string, required
  email: string
  billing_address: Address
  shipping_address: Address?
}

@type Order {
  id: string, required
  customer: Customer
  items: list of OrderItem
  total: number
}
```

---

## Type Invariants

Invariants are conditions that must always hold for a type.

### Basic @invariant

```nl
@type Account {
  balance: number
  owner: string
}

@invariant Account {
  balance >= 0
  len(owner) > 0
}
```

**Python output:**

```python
@dataclass
class Account:
    balance: float
    owner: str

    def __post_init__(self):
        if not (self.balance >= 0):
            raise ValueError("Invariant violated: balance >= 0")
        if not (len(self.owner) > 0):
            raise ValueError("Invariant violated: len(owner) > 0")
```

### Using self Prefix

For clarity, use `self.` to reference fields:

```nl
@type Rectangle {
  width: number
  height: number
}

@invariant Rectangle {
  self.width > 0
  self.height > 0
}
```

### Multiple Conditions

```nl
@type Order {
  items: list of OrderItem
  total: number
  status: string
}

@invariant Order {
  len(items) > 0
  total >= 0
  status in ["pending", "confirmed", "shipped", "delivered", "cancelled"]
}
```

### Invariants with Relationships

```nl
@type DateRange {
  start_date: string
  end_date: string
}

@invariant DateRange {
  start_date <= end_date
}

@type Discount {
  percentage: number
  min_purchase: number
}

@invariant Discount {
  percentage >= 0
  percentage <= 100
  min_purchase >= 0
}
```

---

## Type Conversion Reference

### NLS to Python Mapping

| NLS Type | Python Type | Import Required |
|----------|-------------|-----------------|
| `number` | `float` | No |
| `string` | `str` | No |
| `boolean` | `bool` | No |
| `void` | `None` | No |
| `any` | `Any` | `from typing import Any` |
| `list of T` | `list[T]` | No |
| `dict of K to V` | `dict[K, V]` | No |
| `T?` | `Optional[T]` | `from typing import Optional` |
| `T \| U` | `T \| U` | No (Python 3.10+) |
| `@type X` | `@dataclass class X` | `from dataclasses import dataclass` |

### Type Aliases (Future)

```nl
# Planned feature
@type UserId = string
@type Money = number
@type UserList = list of User
```

---

## Best Practices

### 1. Use Specific Types

```nl
# Good
INPUTS:
  - user_id: string
  - amount: number
  - items: list of OrderItem

# Avoid
INPUTS:
  - user_id: any
  - amount: any
  - items: any
```

### 2. Add Invariants for Business Rules

```nl
@type Account {
  balance: number
}

@invariant Account {
  balance >= 0  # Business rule: no overdrafts
}
```

### 3. Use Optional for Nullable Fields

```nl
@type User {
  id: string, required
  email: string, required
  phone: string?           # May not have phone
  middle_name: string?     # May not have middle name
}
```

### 4. Document with Field Descriptions

```nl
@type Config {
  host: string, "Server hostname or IP"
  port: number, min: 1, max: 65535, "Port number"
  timeout: number, "Connection timeout in seconds"
  retries: number, min: 0, "Number of retry attempts"
}
```

### 5. Use Inheritance for Shared Fields

```nl
@type Timestamped {
  created_at: string
  updated_at: string
}

@type User extends Timestamped {
  # Gets created_at and updated_at automatically
  email: string
}
```

---

## Related Documentation

- **[Language Specification](language-spec.md)** — Full syntax reference
- **[Core Semantics](core-semantics.md)** — Type system semantics
- **[Testing Guide](tutorials/testing-guide.md)** — Testing with invariants
- **[LLM Reference](llm-reference.md)** — Complete type examples
