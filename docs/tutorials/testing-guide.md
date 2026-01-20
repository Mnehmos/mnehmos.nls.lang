# Tutorial: Testing Your Code

Master NLS's three testing mechanisms: example tests, property tests, and invariants.

## What You'll Learn

- Writing `@test` blocks for example-based testing
- Property-based testing with `@property` and Hypothesis
- Type invariants with `@invariant`
- When to use each testing approach

## Prerequisites

- Completed [Working with Types](working-with-types.md)
- Understanding of types and ANLUs

---

## The Three Testing Mechanisms

| Mechanism | Purpose | When to Use |
|-----------|---------|-------------|
| `@test` | Example-based tests | Specific cases, edge cases, documentation |
| `@property` | Property-based tests | Mathematical properties, invariants over random data |
| `@invariant` | Type constraints | Data validity that must always hold |

---

## Part 1: Example Tests with @test

### Basic Syntax

```nl
@test [function-name] {
  function_name(input1, input2) == expected_output
}
```

### Complete Example

```nl
@module math
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

[abs]
PURPOSE: Return absolute value
INPUTS:
  - x: number
RETURNS: x if x >= 0 else -x

@test [add] {
  add(2, 3) == 5
  add(-1, 1) == 0
  add(0, 0) == 0
  add(1.5, 2.5) == 4.0
  add(-5, -3) == -8
}

@test [abs] {
  abs(5) == 5
  abs(-5) == 5
  abs(0) == 0
  abs(-0.5) == 0.5
}
```

### Testing for Exceptions

For guard failures, test that the function raises the expected error:

```nl
[divide]
PURPOSE: Divide two numbers safely
INPUTS:
  - a: number
  - b: number
GUARDS:
  - b must not be zero -> ValueError("Cannot divide by zero")
RETURNS: a / b

@test [divide] {
  divide(10, 2) == 5.0
  divide(9, 3) == 3.0
  divide(-6, 2) == -3.0
}
```

!!! note "Exception Testing"
    Currently, `@test` blocks only support equality assertions. For exception testing, use generated pytest files or write additional Python tests.

### Running Tests

```bash
nlsc test src/math.nl
```

Output:

```
Running 9 test cases from src/math.nl...
  • [add]: 5 cases
  • [abs]: 4 cases

✓ All 9 tests passed!
```

For verbose output:

```bash
nlsc test src/math.nl -v
```

---

## Part 2: Property Tests with @property

Property tests verify that properties hold for **all valid inputs**, not just specific examples. NLS generates [Hypothesis](https://hypothesis.readthedocs.io/) tests.

### Basic Syntax

```nl
@property [function-name] {
  property_expression
}
```

### Mathematical Properties

```nl
@module math
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

[multiply]
PURPOSE: Multiply two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a * b

@property [add] {
  add(a, b) == add(b, a)           # Commutativity
  add(a, 0) == a                    # Identity
  add(add(a, b), c) == add(a, add(b, c))  # Associativity
}

@property [multiply] {
  multiply(a, b) == multiply(b, a)  # Commutativity
  multiply(a, 1) == a               # Identity
  multiply(a, 0) == 0               # Zero property
}
```

### Forall Quantifier

Use `forall` to explicitly specify variable types:

```nl
[abs]
PURPOSE: Return absolute value
INPUTS:
  - x: number
RETURNS: x if x >= 0 else -x

@property [abs] {
  forall x: number -> abs(x) >= 0        # Non-negativity
  forall x: number -> abs(-x) == abs(x)  # Symmetry
  forall x: number -> abs(x * x) == x * x  # Squares are non-negative
}
```

### Properties for Custom Types

```nl
@type Account {
  balance: number
  owner: string
}

[deposit]
PURPOSE: Add money to account
INPUTS:
  - account: Account
  - amount: number
GUARDS:
  - amount > 0 -> ValueError("Amount must be positive")
RETURNS: Account(balance=account.balance + amount, owner=account.owner)

@property [deposit] {
  deposit(acc, amt).balance == acc.balance + amt  # Correct addition
  deposit(acc, amt).balance > acc.balance         # Always increases
  deposit(acc, amt).owner == acc.owner            # Owner unchanged
}
```

### Generated Code

NLS generates Hypothesis tests like:

```python
from hypothesis import given, strategies as st

@given(a=st.floats(allow_nan=False, allow_infinity=False),
       b=st.floats(allow_nan=False, allow_infinity=False))
def test_property_add_commutativity(a, b):
    assert add(a, b) == add(b, a)
```

---

## Part 3: Type Invariants with @invariant

Invariants are conditions that must **always** hold for instances of a type. They're enforced at construction time.

### Basic Syntax

```nl
@invariant TypeName {
  condition1
  condition2
}
```

### Examples

```nl
@type Account {
  id: string, required
  owner: string, required
  balance: number
}

@invariant Account {
  balance >= 0                  # No negative balances
  len(owner) > 0                # Owner name required
  len(id) >= 8                  # ID must be at least 8 chars
}
```

### Using `self` Prefix

For clarity, you can use `self.` prefix:

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

### Generated Validation

Invariants generate `__post_init__` validation:

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
        if not (len(self.id) >= 8):
            raise ValueError("Invariant violated: len(id) >= 8")
```

### Invariants + Properties Together

Invariants and properties work together:

```nl
@module banking
@target python

@type Account {
  balance: number
  owner: string
}

@invariant Account {
  balance >= 0
}

[deposit]
PURPOSE: Add money to account
INPUTS:
  - account: Account
  - amount: number
GUARDS:
  - amount > 0 -> ValueError("Amount must be positive")
RETURNS: Account(balance=account.balance + amount, owner=account.owner)

[withdraw]
PURPOSE: Remove money from account
INPUTS:
  - account: Account
  - amount: number
GUARDS:
  - amount > 0 -> ValueError("Amount must be positive")
  - amount <= account.balance -> ValueError("Insufficient funds")
RETURNS: Account(balance=account.balance - amount, owner=account.owner)

@property [deposit] {
  deposit(acc, amt).balance >= 0  # Invariant preserved
}

@property [withdraw] {
  withdraw(acc, amt).balance >= 0  # Invariant preserved
}
```

The properties prove that the invariant is maintained by operations.

---

## When to Use Each Mechanism

| Scenario | Use |
|----------|-----|
| Document expected behavior | `@test` |
| Test edge cases | `@test` |
| Verify mathematical properties | `@property` |
| Test with random inputs | `@property` |
| Ensure data validity | `@invariant` |
| Prevent invalid object creation | `@invariant` |
| Prove operations preserve validity | `@property` + `@invariant` |

### Decision Tree

```
Is it about a specific example?
  └── Yes → @test
  └── No → Is it about a type's validity?
            └── Yes → @invariant
            └── No → @property
```

---

## Complete Example: Validated Stack

```nl
@module stack
@version 1.0.0
@target python

@type Stack {
  items: list of any
  max_size: number
}

@invariant Stack {
  len(items) <= max_size
  max_size > 0
}

[create-stack]
PURPOSE: Create a new empty stack with max size
INPUTS:
  - max_size: number
GUARDS:
  - max_size must be positive -> ValueError("Max size must be positive")
RETURNS: Stack(items=[], max_size=max_size)

[push]
PURPOSE: Add item to top of stack
INPUTS:
  - stack: Stack
  - item: any
GUARDS:
  - stack must not be full -> ValueError("Stack overflow")
RETURNS: Stack(items=stack.items + [item], max_size=stack.max_size)

[pop]
PURPOSE: Remove and return top item from stack
INPUTS:
  - stack: Stack
GUARDS:
  - stack must not be empty -> ValueError("Stack underflow")
LOGIC:
  1. Get the last item -> top_item
  2. Remove last item from list -> remaining_items
RETURNS: (top_item, Stack(items=remaining_items, max_size=stack.max_size))

[peek]
PURPOSE: Return top item without removing
INPUTS:
  - stack: Stack
GUARDS:
  - stack must not be empty -> ValueError("Stack is empty")
RETURNS: stack.items[-1]

[is-empty]
PURPOSE: Check if stack is empty
INPUTS:
  - stack: Stack
RETURNS: len(stack.items) == 0

[is-full]
PURPOSE: Check if stack is full
INPUTS:
  - stack: Stack
RETURNS: len(stack.items) >= stack.max_size

# Example-based tests
@test [is-empty] {
  is_empty(Stack(items=[], max_size=10)) == True
  is_empty(Stack(items=[1], max_size=10)) == False
}

@test [is-full] {
  is_full(Stack(items=[1, 2, 3], max_size=3)) == True
  is_full(Stack(items=[1, 2], max_size=3)) == False
}

# Property-based tests
@property [push] {
  not is_empty(push(stack, item))  # Push makes non-empty
}

@property [pop] {
  # Pop then push restores (for non-empty stack)
  push(pop(stack)[1], pop(stack)[0]) == stack
}
```

---

## What You've Learned

- [x] Writing example tests with `@test`
- [x] Property-based testing with `@property`
- [x] Using `forall` quantifiers
- [x] Type invariants with `@invariant`
- [x] When to use each testing mechanism
- [x] Combining all three for comprehensive testing

---

## Exercises

1. **Add tests for a `min` function** that finds the minimum of a list
2. **Add a property** that `min(list)` is always in the list
3. **Create a `NonEmptyList` type** with an invariant that length > 0
4. **Write a `head` function** that returns the first element (no guards needed with invariant!)

??? example "Solution"
    ```nl
    @type NonEmptyList {
      items: list of any
    }

    @invariant NonEmptyList {
      len(items) > 0
    }

    [min-value]
    PURPOSE: Find minimum value in a list
    INPUTS:
      - numbers: list of number
    GUARDS:
      - numbers must not be empty -> ValueError("Cannot find min of empty list")
    RETURNS: min(numbers)

    [head]
    PURPOSE: Get first element of non-empty list
    INPUTS:
      - nel: NonEmptyList
    RETURNS: nel.items[0]

    @test [min-value] {
      min_value([3, 1, 4, 1, 5]) == 1
      min_value([42]) == 42
      min_value([-5, 0, 5]) == -5
    }

    @property [min-value] {
      forall nums: list of number -> min_value(nums) in nums
      forall nums: list of number -> all(x >= min_value(nums) for x in nums)
    }

    @test [head] {
      head(NonEmptyList(items=[1, 2, 3])) == 1
      head(NonEmptyList(items=["a"])) == "a"
    }
    ```

---

## Next Steps

- **[Patterns](patterns.md)** — Real-world patterns and idioms
- **[Core Semantics](../core-semantics.md)** — How tests map to Python
- **[CLI Reference](../cli-reference.md)** — Test runner options
