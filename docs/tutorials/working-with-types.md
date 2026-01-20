# Tutorial: Working with Types

Learn to define custom types, use constraints, and model real-world domain objects.

## What You'll Learn

- Defining types with `@type`
- Field constraints (required, optional, min, max)
- Type inheritance with `extends`
- Using types in ANLUs
- Type invariants with `@invariant`

## Prerequisites

- Completed [Your First Module](first-module.md)
- Understanding of basic NLS syntax

---

## Step 1: Define a Simple Type

Let's model a simple e-commerce system. Create `src/shop.nl`:

```nl
@module shop
@target python

@type Product {
  id: string
  name: string
  price: number
}
```

This generates a Python dataclass:

```python
from dataclasses import dataclass

@dataclass
class Product:
    """Product type."""
    id: str
    name: str
    price: float
```

---

## Step 2: Add Field Constraints

Make fields required or optional, and add descriptions:

```nl
@type Product {
  id: string, required
  name: string, required
  price: number, min: 0
  description: string, optional
  stock: number, optional, "Number of items in inventory"
}
```

**Constraint types:**

| Constraint | Meaning |
|------------|---------|
| `required` | Field must be provided |
| `optional` | Field can be omitted (default) |
| `min: N` | Numeric minimum value |
| `max: N` | Numeric maximum value |
| `"description"` | Human-readable description |

---

## Step 3: Use Composite Types

Create types that reference other types:

```nl
@module shop
@target python

@type Product {
  id: string, required
  name: string, required
  price: number, min: 0
}

@type OrderItem {
  product: Product, required
  quantity: number, min: 1
}

@type Order {
  id: string, required
  customer_id: string, required
  items: list of OrderItem, required
  total: number
  status: string
}
```

The `items: list of OrderItem` field shows how to compose types.

---

## Step 4: Type Inheritance

Use `extends` to create specialized types:

```nl
@type BaseItem {
  id: string, required
  created_at: string
}

@type Product extends BaseItem {
  name: string, required
  price: number, min: 0
  category: string
}

@type DigitalProduct extends Product {
  download_url: string, required
  file_size: number
}
```

The generated Python uses inheritance:

```python
@dataclass
class BaseItem:
    id: str
    created_at: str

@dataclass
class Product(BaseItem):
    name: str
    price: float
    category: str

@dataclass
class DigitalProduct(Product):
    download_url: str
    file_size: float
```

---

## Step 5: Use Types in ANLUs

Now use your types in function specifications:

```nl
@module shop
@target python

@type Product {
  id: string, required
  name: string, required
  price: number, min: 0
}

@type OrderItem {
  product: Product, required
  quantity: number, min: 1
}

@type Order {
  id: string, required
  items: list of OrderItem, required
  total: number
}

[calculate-item-total]
PURPOSE: Calculate the total price for an order item
INPUTS:
  - item: OrderItem
RETURNS: item.product.price * item.quantity

[calculate-order-total]
PURPOSE: Calculate the total for an entire order
INPUTS:
  - order: Order
LOGIC:
  1. Sum the total of each item -> total
RETURNS: total
DEPENDS: [calculate-item-total]

[create-order]
PURPOSE: Create a new order from a list of items
INPUTS:
  - order_id: string, required
  - items: list of OrderItem, required
GUARDS:
  - items must not be empty -> ValueError("Order must have at least one item")
LOGIC:
  1. Calculate total for all items -> total
RETURNS: Order(id=order_id, items=items, total=total)
DEPENDS: [calculate-order-total]
```

---

## Step 6: Type Invariants

Use `@invariant` to enforce rules that must always be true:

```nl
@type Account {
  id: string, required
  owner: string, required
  balance: number
}

@invariant Account {
  balance >= 0
  len(owner) > 0
}
```

This generates validation in `__post_init__`:

```python
@dataclass
class Account:
    id: str
    owner: str
    balance: float

    def __post_init__(self):
        if not (self.balance >= 0):
            raise ValueError("Invariant violated: balance >= 0")
        if not (len(self.owner) > 0):
            raise ValueError("Invariant violated: len(owner) > 0")
```

Now invalid accounts can never be created:

```python
# This works:
account = Account(id="1", owner="Alice", balance=100)

# This raises ValueError:
account = Account(id="2", owner="Bob", balance=-50)
# ValueError: Invariant violated: balance >= 0
```

---

## Step 7: Complete Banking Example

Here's a full example combining everything:

```nl
@module banking
@version 1.0.0
@target python

@type Account {
  id: string, required
  owner: string, required
  balance: number
}

@invariant Account {
  balance >= 0
  len(owner) > 0
}

[create-account]
PURPOSE: Create a new account with initial balance
INPUTS:
  - account_id: string, required
  - owner_name: string, required
  - initial_balance: number, optional
GUARDS:
  - owner_name must not be empty -> ValueError("Owner name required")
  - initial_balance must be non-negative if provided -> ValueError("Initial balance cannot be negative")
LOGIC:
  1. Set balance to initial_balance or 0 -> balance
RETURNS: Account(id=account_id, owner=owner_name, balance=balance)

[deposit]
PURPOSE: Add money to an account
INPUTS:
  - account: Account
  - amount: number
GUARDS:
  - amount must be positive -> ValueError("Deposit amount must be positive")
RETURNS: Account(id=account.id, owner=account.owner, balance=account.balance + amount)

[withdraw]
PURPOSE: Remove money from an account
INPUTS:
  - account: Account
  - amount: number
GUARDS:
  - amount must be positive -> ValueError("Withdrawal amount must be positive")
  - amount must not exceed balance -> ValueError("Insufficient funds")
RETURNS: Account(id=account.id, owner=account.owner, balance=account.balance - amount)

[transfer]
PURPOSE: Transfer money between accounts
INPUTS:
  - from_account: Account
  - to_account: Account
  - amount: number
GUARDS:
  - amount must be positive -> ValueError("Transfer amount must be positive")
  - amount must not exceed from_account balance -> ValueError("Insufficient funds")
LOGIC:
  1. Withdraw amount from source -> updated_from
  2. Deposit amount to destination -> updated_to
RETURNS: (updated_from, updated_to)
DEPENDS: [withdraw], [deposit]

@test [deposit] {
  deposit(Account(id="1", owner="Alice", balance=100), 50).balance == 150
}

@test [withdraw] {
  withdraw(Account(id="1", owner="Alice", balance=100), 30).balance == 70
}

@property [deposit] {
  deposit(acc, amt).balance == acc.balance + amt
  deposit(acc, amt).balance > acc.balance
}

@property [withdraw] {
  withdraw(acc, amt).balance == acc.balance - amt
  withdraw(acc, amt).balance < acc.balance
}
```

---

## Type System Reference

### Primitive Types

| NLS Type | Python Type | Description |
|----------|-------------|-------------|
| `number` | `float` | Any numeric value |
| `string` | `str` | Text |
| `boolean` | `bool` | True/false |
| `any` | `Any` | Dynamic typing |

### Composite Types

| NLS Syntax | Python Type | Example |
|------------|-------------|---------|
| `list of T` | `list[T]` | `list of Product` |
| `dict of K to V` | `dict[K, V]` | `dict of string to number` |
| `T?` | `Optional[T]` | `User?` |
| `T \| U` | `T \| U` | `Success \| Error` |

---

## What You've Learned

- [x] Defining types with `@type`
- [x] Using field constraints
- [x] Type inheritance with `extends`
- [x] Composite types (`list of`, `dict of`)
- [x] Type invariants with `@invariant`
- [x] Using types in ANLU inputs and returns

---

## Exercises

1. **Create a `Customer` type** with id, name, email, and VIP status
2. **Add an invariant** that email must contain "@"
3. **Create a `calculate-discount` ANLU** that returns 10% off for VIP customers
4. **Write tests** for the discount function

??? example "Solution"
    ```nl
    @type Customer {
      id: string, required
      name: string, required
      email: string, required
      is_vip: boolean
    }

    @invariant Customer {
      "@" in email
      len(name) > 0
    }

    [calculate-discount]
    PURPOSE: Calculate discount percentage for a customer
    INPUTS:
      - customer: Customer
      - base_price: number
    LOGIC:
      1. IF customer.is_vip THEN apply 10% discount -> discount_rate
      2. Calculate discounted price -> final_price
    RETURNS: base_price * (1 - discount_rate) if customer.is_vip else base_price

    @test [calculate-discount] {
      calculate_discount(Customer(id="1", name="Alice", email="a@b.c", is_vip=True), 100) == 90
      calculate_discount(Customer(id="2", name="Bob", email="b@c.d", is_vip=False), 100) == 100
    }
    ```

---

## Next Steps

- **[Testing Guide](testing-guide.md)** — Property-based testing and invariants
- **[Patterns](patterns.md)** — Common real-world patterns
- **[Language Specification](../language-spec.md)** — Complete type system reference
