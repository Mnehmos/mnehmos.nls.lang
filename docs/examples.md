# Examples Gallery

Complete, working NLS examples demonstrating various features and patterns.

## Basic Examples

### Calculator

A simple arithmetic calculator demonstrating basic ANLUs, guards, and tests.

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

[power]
PURPOSE: Raise base to exponent power
INPUTS:
  - base: number
  - exponent: number
RETURNS: base ** exponent

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

---

### String Utilities

String manipulation functions with literal blocks for regex.

```nl
@module strings
@version 1.0.0
@target python
@imports re

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

[truncate]
PURPOSE: Truncate string to maximum length with ellipsis
INPUTS:
  - text: string
  - max_length: number
  - suffix: string, optional, "Suffix to append (default: ...)"
GUARDS:
  - max_length must be at least 1 -> ValueError("Max length must be positive")
LOGIC:
  1. Use suffix or default to "..." -> actual_suffix
  2. IF text length <= max_length THEN return text unchanged
  3. Calculate truncation point -> cut_point
  4. Slice text and append suffix -> result
RETURNS: result

[capitalize-words]
PURPOSE: Capitalize the first letter of each word
INPUTS:
  - text: string
RETURNS: text.title()

[reverse]
PURPOSE: Reverse a string
INPUTS:
  - text: string
RETURNS: text[::-1]

@test [slugify] {
  slugify("Hello World") == "hello-world"
  slugify("  Multiple   Spaces  ") == "multiple-spaces"
  slugify("Special!@#Characters") == "specialcharacters"
}

@test [truncate] {
  truncate("Hello World", 5) == "He..."
  truncate("Hi", 10) == "Hi"
}

@test [reverse] {
  reverse("hello") == "olleh"
  reverse("") == ""
}
```

---

## Domain Models

### E-Commerce Shop

Complete shop module with products, orders, and inventory.

```nl
@module shop
@version 1.0.0
@target python

# Type Definitions
@type Product {
  id: string, required
  name: string, required
  price: number, min: 0
  stock: number, min: 0
  category: string
}

@type OrderItem {
  product_id: string, required
  quantity: number, min: 1
  unit_price: number
}

@type Order {
  id: string, required
  customer_id: string, required
  items: list of OrderItem
  subtotal: number
  tax: number
  total: number
  status: string
}

@invariant Order {
  len(items) > 0
  total >= 0
  status in ["pending", "confirmed", "shipped", "delivered", "cancelled"]
}

# Product Operations
[create-product]
PURPOSE: Create a new product in the catalog
INPUTS:
  - id: string, required
  - name: string, required
  - price: number
  - initial_stock: number, optional
  - category: string, optional
GUARDS:
  - price must be non-negative -> ValueError("Price cannot be negative")
RETURNS: Product(id=id, name=name, price=price, stock=initial_stock or 0, category=category or "uncategorized")

[update-stock]
PURPOSE: Update product stock level
INPUTS:
  - product: Product
  - quantity_change: number, "Positive to add, negative to remove"
GUARDS:
  - product.stock + quantity_change must be non-negative -> ValueError("Insufficient stock")
RETURNS: Product(id=product.id, name=product.name, price=product.price, stock=product.stock + quantity_change, category=product.category)

# Order Operations
[calculate-item-total]
PURPOSE: Calculate total price for an order item
INPUTS:
  - item: OrderItem
RETURNS: item.unit_price * item.quantity

[calculate-order-subtotal]
PURPOSE: Calculate subtotal for all items in order
INPUTS:
  - items: list of OrderItem
LOGIC:
  1. Sum total of each item -> subtotal
RETURNS: subtotal
DEPENDS: [calculate-item-total]

[calculate-order-tax]
PURPOSE: Calculate tax for order subtotal
INPUTS:
  - subtotal: number
  - tax_rate: number, "Tax rate as decimal (e.g., 0.08 for 8%)"
GUARDS:
  - tax_rate must be between 0 and 1 -> ValueError("Tax rate must be 0-1")
RETURNS: subtotal * tax_rate

[create-order]
PURPOSE: Create a new order from items
INPUTS:
  - order_id: string, required
  - customer_id: string, required
  - items: list of OrderItem
  - tax_rate: number
GUARDS:
  - items must not be empty -> ValueError("Order must have items")
LOGIC:
  1. Calculate subtotal -> subtotal
  2. Calculate tax -> tax
  3. Calculate total -> total
RETURNS: Order(id=order_id, customer_id=customer_id, items=items, subtotal=subtotal, tax=tax, total=subtotal + tax, status="pending")
DEPENDS: [calculate-order-subtotal], [calculate-order-tax]

# Tests
@test [calculate-item-total] {
  calculate_item_total(OrderItem(product_id="p1", quantity=2, unit_price=10.0)) == 20.0
  calculate_item_total(OrderItem(product_id="p2", quantity=1, unit_price=5.0)) == 5.0
}

@test [calculate-order-tax] {
  calculate_order_tax(100, 0.08) == 8.0
  calculate_order_tax(50, 0.10) == 5.0
}

@property [calculate-order-tax] {
  calculate_order_tax(subtotal, 0) == 0
  calculate_order_tax(0, rate) == 0
}
```

---

### Banking System

Account management with invariants and property tests.

```nl
@module banking
@version 1.0.0
@target python

@type Account {
  id: string, required
  owner: string, required
  balance: number
  account_type: string
}

@type Transaction {
  id: string, required
  from_account: string
  to_account: string
  amount: number
  timestamp: string
  status: string
}

@invariant Account {
  balance >= 0
  len(owner) > 0
  account_type in ["checking", "savings", "investment"]
}

[create-account]
PURPOSE: Create a new bank account
INPUTS:
  - account_id: string, required
  - owner_name: string, required
  - account_type: string, optional
  - initial_deposit: number, optional
GUARDS:
  - owner_name must not be empty -> ValueError("Owner name required")
  - initial_deposit must be non-negative if provided -> ValueError("Initial deposit cannot be negative")
RETURNS: Account(id=account_id, owner=owner_name, balance=initial_deposit or 0, account_type=account_type or "checking")

[deposit]
PURPOSE: Add money to an account
INPUTS:
  - account: Account
  - amount: number
GUARDS:
  - amount must be positive -> ValueError("Deposit amount must be positive")
RETURNS: Account(id=account.id, owner=account.owner, balance=account.balance + amount, account_type=account.account_type)

[withdraw]
PURPOSE: Remove money from an account
INPUTS:
  - account: Account
  - amount: number
GUARDS:
  - amount must be positive -> ValueError("Withdrawal amount must be positive")
  - amount must not exceed balance -> ValueError("Insufficient funds")
RETURNS: Account(id=account.id, owner=account.owner, balance=account.balance - amount, account_type=account.account_type)

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
  1. Withdraw from source account -> updated_from
  2. Deposit to destination account -> updated_to
RETURNS: (updated_from, updated_to)
DEPENDS: [withdraw], [deposit]

[get-balance]
PURPOSE: Get current account balance
INPUTS:
  - account: Account
RETURNS: account.balance

[calculate-interest]
PURPOSE: Calculate interest for savings account
INPUTS:
  - account: Account
  - annual_rate: number, "Annual interest rate as decimal"
  - days: number, "Number of days"
GUARDS:
  - account.account_type must be "savings" -> ValueError("Interest only for savings accounts")
  - annual_rate must be non-negative -> ValueError("Rate cannot be negative")
  - days must be positive -> ValueError("Days must be positive")
LOGIC:
  1. Calculate daily rate -> daily_rate
  2. Calculate interest -> interest
RETURNS: account.balance * (annual_rate / 365) * days

@test [deposit] {
  deposit(Account(id="1", owner="Alice", balance=100, account_type="checking"), 50).balance == 150
  deposit(Account(id="2", owner="Bob", balance=0, account_type="savings"), 100).balance == 100
}

@test [withdraw] {
  withdraw(Account(id="1", owner="Alice", balance=100, account_type="checking"), 30).balance == 70
}

@property [deposit] {
  deposit(account, amount).balance == account.balance + amount
  deposit(account, amount).balance > account.balance
}

@property [withdraw] {
  withdraw(account, amount).balance == account.balance - amount
  withdraw(account, amount).balance >= 0
}
```

---

## Workflow Examples

### Task Management

Task workflow with state machine pattern.

```nl
@module workflow
@version 1.0.0
@target python

@type Task {
  id: string, required
  title: string, required
  description: string
  status: string
  assignee: string?
  priority: number
  due_date: string?
}

@type TimeEstimate {
  optimistic: number
  realistic: number
  pessimistic: number
}

@invariant Task {
  status in ["pending", "in_progress", "review", "completed", "cancelled"]
  priority >= 1
  priority <= 5
}

[create-task]
PURPOSE: Create a new task with default values
INPUTS:
  - task_id: string, required
  - title: string, required
  - description: string, optional
  - priority: number, optional
GUARDS:
  - title must not be empty -> ValueError("Task title required")
RETURNS: Task(id=task_id, title=title, description=description or "", status="pending", assignee=None, priority=priority or 3, due_date=None)

[assign-task]
PURPOSE: Assign a task to a team member
INPUTS:
  - task: Task
  - assignee: string
GUARDS:
  - task.status must be "pending" or "in_progress" -> ValueError("Cannot assign completed task")
  - assignee must not be empty -> ValueError("Assignee required")
RETURNS: Task(id=task.id, title=task.title, description=task.description, status=task.status, assignee=assignee, priority=task.priority, due_date=task.due_date)

[start-task]
PURPOSE: Move task to in-progress status
INPUTS:
  - task: Task
GUARDS:
  - task.status must be "pending" -> ValueError("Task must be pending to start")
  - task.assignee must not be None -> ValueError("Task must be assigned before starting")
RETURNS: Task(id=task.id, title=task.title, description=task.description, status="in_progress", assignee=task.assignee, priority=task.priority, due_date=task.due_date)

[complete-task]
PURPOSE: Mark task as completed
INPUTS:
  - task: Task
GUARDS:
  - task.status must be "in_progress" or "review" -> ValueError("Task must be in progress or review")
RETURNS: Task(id=task.id, title=task.title, description=task.description, status="completed", assignee=task.assignee, priority=task.priority, due_date=task.due_date)

[estimate-task-time]
PURPOSE: Calculate expected time using PERT formula
INPUTS:
  - estimate: TimeEstimate
GUARDS:
  - estimate.optimistic must be positive -> ValueError("Optimistic must be positive")
  - estimate.realistic must be >= optimistic -> ValueError("Realistic must be >= optimistic")
  - estimate.pessimistic must be >= realistic -> ValueError("Pessimistic must be >= realistic")
RETURNS: (estimate.optimistic + 4 * estimate.realistic + estimate.pessimistic) / 6

[prioritize-tasks]
PURPOSE: Sort tasks by priority (highest first)
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Sort tasks by priority descending -> sorted_tasks
RETURNS: sorted_tasks

@test [estimate-task-time] {
  estimate_task_time(TimeEstimate(optimistic=1, realistic=2, pessimistic=3)) == 2.0
  estimate_task_time(TimeEstimate(optimistic=2, realistic=4, pessimistic=6)) == 4.0
}
```

---

## Authentication Example

JWT-based authentication flow.

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
  is_active: boolean
}

@type AuthToken {
  token: string, required
  user_id: string, required
  expires_at: string
  scopes: list of string
}

@type AuthResult {
  success: boolean
  user: User?
  token: AuthToken?
  error: string?
}

[validate-credentials]
PURPOSE: Validate username and password format
INPUTS:
  - email: string
  - password: string
GUARDS:
  - email must not be empty -> ValueError("Email required")
  - email must contain @ symbol -> ValueError("Invalid email format")
  - password must not be empty -> ValueError("Password required")
  - password must be at least 8 characters -> ValueError("Password too short")
RETURNS: True

[generate-token]
PURPOSE: Generate JWT token for authenticated user
INPUTS:
  - user: User
  - secret: string
  - expiry_hours: number, optional
GUARDS:
  - user.is_active must be True -> AuthError("User account is inactive")
LOGIC:
  1. Set expiry to expiry_hours or default 24 -> hours
  2. Calculate expiration timestamp -> expires_at
  3. Create JWT payload -> payload
  4. Sign token with secret -> signed_token
RETURNS: AuthToken(token=signed_token, user_id=user.id, expires_at=expires_at, scopes=[user.role])

[verify-token]
PURPOSE: Verify and decode a JWT token
INPUTS:
  - token: string
  - secret: string
GUARDS:
  - token must not be empty -> AuthError(MISSING_TOKEN, "Token required")
LOGIC:
  1. Decode token with secret -> payload
  2. Check if token has expired -> is_expired
  3. IF is_expired THEN raise AuthError
  4. Extract user_id and scopes -> user_id, scopes
RETURNS: AuthToken(token=token, user_id=user_id, expires_at=payload.exp, scopes=scopes)

[require-role]
PURPOSE: Check if user has required role
INPUTS:
  - user: User
  - required_role: string
GUARDS:
  - user must not be None -> AuthError("Authentication required")
  - user.role must equal required_role -> AuthError(FORBIDDEN, "Insufficient permissions")
RETURNS: True

[authenticate]
PURPOSE: Full authentication flow
INPUTS:
  - email: string
  - password: string
  - secret: string
LOGIC:
  1. Validate credentials format -> valid
  2. Look up user by email -> user
  3. IF user not found THEN return failure result
  4. Verify password hash -> password_match
  5. IF not password_match THEN return failure result
  6. Generate auth token -> token
RETURNS: AuthResult(success=True, user=user, token=token, error=None)
DEPENDS: [validate-credentials], [generate-token]

@test [validate-credentials] {
  validate_credentials("user@example.com", "password123") == True
}

@test [require-role] {
  require_role(User(id="1", email="a@b.c", name="Admin", role="admin", is_active=True), "admin") == True
}
```

---

## Download Examples

All examples are available in the `examples/` directory of the repository:

- [math.nl](https://github.com/Mnehmos/mnehmos.nls.lang/blob/master/examples/math.nl)
- [strings.nl](https://github.com/Mnehmos/mnehmos.nls.lang/blob/master/examples/strings.nl)
- [billing.nl](https://github.com/Mnehmos/mnehmos.nls.lang/blob/master/examples/billing.nl)
- [workflow_engine.nl](https://github.com/Mnehmos/mnehmos.nls.lang/blob/master/examples/workflow_engine.nl)
- [shop_demo.nl](https://github.com/Mnehmos/mnehmos.nls.lang/blob/master/examples/shop_demo.nl)

## Next Steps

- **[Tutorials](tutorials/index.md)** — Step-by-step learning
- **[Language Specification](language-spec.md)** — Complete syntax reference
- **[LLM Reference](llm-reference.md)** — AI-optimized documentation
