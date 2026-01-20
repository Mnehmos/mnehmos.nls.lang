# Tutorial: Real-World Patterns

Common patterns and idioms for effective NLS development.

## What You'll Learn

- Validation patterns
- Factory patterns
- State machine patterns
- Error handling patterns
- Composition patterns

## Prerequisites

- Completed previous tutorials
- Familiarity with NLS syntax

---

## Pattern 1: Validation Functions

Validation functions check input and return boolean or raise errors.

### Boolean Validator

```nl
[is-valid-email]
PURPOSE: Check if a string is a valid email address
INPUTS:
  - email: string
LOGIC:
  1. Check if email contains @ symbol -> has_at
  2. Check if email has domain after @ -> has_domain
  3. Check if email has local part before @ -> has_local
RETURNS: has_at and has_domain and has_local
```

### Raising Validator

```nl
[validate-email]
PURPOSE: Validate email address or raise error
INPUTS:
  - email: string
GUARDS:
  - email must not be empty -> ValueError("Email required")
  - email must contain @ symbol -> ValueError("Invalid email: missing @")
  - email must have text before @ -> ValueError("Invalid email: missing local part")
  - email must have text after @ -> ValueError("Invalid email: missing domain")
RETURNS: True
```

### Validation with Multiple Fields

```nl
@type UserInput {
  email: string
  password: string
  age: number
}

[validate-user-input]
PURPOSE: Validate all fields of user registration input
INPUTS:
  - input: UserInput
GUARDS:
  - input.email must be valid email -> ValueError("Invalid email")
  - input.password must be at least 8 chars -> ValueError("Password too short")
  - input.age must be at least 13 -> ValueError("Must be at least 13 years old")
  - input.age must be at most 120 -> ValueError("Invalid age")
RETURNS: True
DEPENDS: [is-valid-email]
```

---

## Pattern 2: Factory Functions

Factory functions create and return new objects.

### Simple Factory

```nl
@type User {
  id: string, required
  email: string, required
  name: string
  created_at: string
}

[create-user]
PURPOSE: Create a new user with generated ID and timestamp
INPUTS:
  - email: string, required
  - name: string, required
GUARDS:
  - email must be valid -> ValueError("Invalid email")
  - name must not be empty -> ValueError("Name required")
LOGIC:
  1. Generate unique ID -> user_id
  2. Get current timestamp -> timestamp
RETURNS: User(id=user_id, email=email, name=name, created_at=timestamp)
```

### Factory with Defaults

```nl
@type Config {
  host: string
  port: number
  timeout: number
  retries: number
}

[create-config]
PURPOSE: Create configuration with sensible defaults
INPUTS:
  - host: string, optional
  - port: number, optional
  - timeout: number, optional
  - retries: number, optional
LOGIC:
  1. Use host or default to "localhost" -> final_host
  2. Use port or default to 8080 -> final_port
  3. Use timeout or default to 30 -> final_timeout
  4. Use retries or default to 3 -> final_retries
RETURNS: Config(host=final_host, port=final_port, timeout=final_timeout, retries=final_retries)
```

### Builder Pattern

```nl
@type QueryBuilder {
  table: string
  conditions: list of string
  order_by: string?
  limit: number?
}

[new-query]
PURPOSE: Create a new query builder for a table
INPUTS:
  - table: string
RETURNS: QueryBuilder(table=table, conditions=[], order_by=None, limit=None)

[query-where]
PURPOSE: Add a WHERE condition to the query
INPUTS:
  - builder: QueryBuilder
  - condition: string
RETURNS: QueryBuilder(table=builder.table, conditions=builder.conditions + [condition], order_by=builder.order_by, limit=builder.limit)

[query-order]
PURPOSE: Set ORDER BY clause
INPUTS:
  - builder: QueryBuilder
  - column: string
RETURNS: QueryBuilder(table=builder.table, conditions=builder.conditions, order_by=column, limit=builder.limit)

[query-limit]
PURPOSE: Set LIMIT clause
INPUTS:
  - builder: QueryBuilder
  - count: number
GUARDS:
  - count must be positive -> ValueError("Limit must be positive")
RETURNS: QueryBuilder(table=builder.table, conditions=builder.conditions, order_by=builder.order_by, limit=count)
```

---

## Pattern 3: State Machines

Use LOGIC state markers to model finite state machines.

### Order Processing FSM

```nl
@type Order {
  id: string
  status: string
  items: list of OrderItem
}

[process-order]
PURPOSE: Process an order through its lifecycle
INPUTS:
  - order: Order
GUARDS:
  - order.status must be "pending" -> ValueError("Order must be pending to process")
LOGIC:
  1. [pending] Validate order details -> validated
  2. [validating] Check inventory availability -> available
  3. [checking_inventory] IF not available THEN mark as backordered
  4. [reserving] Reserve inventory items -> reservation
  5. [processing_payment] Process payment -> payment_result
  6. [payment_complete] IF payment_result.success THEN create shipment
  7. [shipping] Generate shipping label -> shipment
  8. [complete] Mark order as fulfilled -> final_order
EDGE CASES:
  - Inventory not available -> return order with status "backordered"
  - Payment failed -> return order with status "payment_failed"
RETURNS: final_order
```

Visualize with:

```bash
nlsc graph src/orders.nl --anlu process-order
```

### Authentication Flow

```nl
[authenticate-user]
PURPOSE: Authenticate a user through multi-step flow
INPUTS:
  - credentials: Credentials
LOGIC:
  1. [init] Receive credentials -> creds
  2. [validating] Validate credential format -> valid_format
  3. [looking_up] Look up user by username -> user
  4. [verifying] IF user exists THEN verify password -> password_match
  5. [checking_2fa] IF 2FA enabled THEN verify 2FA code -> code_valid
  6. [generating_token] Generate session token -> token
  7. [complete] Create auth result -> result
EDGE CASES:
  - User not found -> return AuthResult(success=False, error="User not found")
  - Password mismatch -> return AuthResult(success=False, error="Invalid password")
  - 2FA failed -> return AuthResult(success=False, error="2FA verification failed")
RETURNS: result
```

---

## Pattern 4: Error Handling

### Structured Errors

Define error types for different failure modes:

```nl
@type ValidationError {
  field: string
  message: string
  code: string
}

@type Result {
  success: boolean
  data: any?
  error: ValidationError?
}

[validate-and-process]
PURPOSE: Validate input and process or return structured error
INPUTS:
  - input: UserInput
LOGIC:
  1. Validate email -> email_valid
  2. IF not email_valid THEN return error result
  3. Validate password -> password_valid
  4. IF not password_valid THEN return error result
  5. Process valid input -> processed_data
RETURNS: Result(success=True, data=processed_data, error=None)
```

### Error Aggregation

```nl
[validate-all-fields]
PURPOSE: Validate all fields and collect all errors
INPUTS:
  - input: FormInput
LOGIC:
  1. Initialize empty error list -> errors
  2. Validate each field, adding errors to list -> errors
  3. IF errors is empty THEN return success
RETURNS: ValidationResult(valid=len(errors) == 0, errors=errors)
```

---

## Pattern 5: Transformation Pipelines

### Map Pattern

```nl
[map-items]
PURPOSE: Apply transformation to each item in list
INPUTS:
  - items: list of any
  - transform: function
LOGIC:
  1. Apply transform to each item -> transformed
RETURNS: transformed
```

### Filter Pattern

```nl
[filter-items]
PURPOSE: Keep only items matching predicate
INPUTS:
  - items: list of any
  - predicate: function
LOGIC:
  1. Keep items where predicate returns true -> filtered
RETURNS: filtered
```

### Reduce Pattern

```nl
[reduce-items]
PURPOSE: Reduce list to single value
INPUTS:
  - items: list of any
  - reducer: function
  - initial: any
LOGIC:
  1. Start with initial value -> accumulator
  2. Apply reducer to each item with accumulator -> result
RETURNS: result
```

### Pipeline Composition

```nl
[process-orders-pipeline]
PURPOSE: Process orders through transformation pipeline
INPUTS:
  - orders: list of Order
LOGIC:
  1. Filter orders to only pending -> pending_orders
  2. Map orders to calculate totals -> orders_with_totals
  3. Filter orders above minimum -> valid_orders
  4. Sort by priority -> sorted_orders
RETURNS: sorted_orders
DEPENDS: [filter-items], [map-items]
```

---

## Pattern 6: Dependency Injection

### Configuration-Based Behavior

```nl
@type EmailConfig {
  provider: string
  api_key: string
  from_address: string
}

[send-email]
PURPOSE: Send email using configured provider
INPUTS:
  - config: EmailConfig
  - to: string
  - subject: string
  - body: string
LOGIC:
  1. Select provider based on config.provider -> provider
  2. Build email payload -> payload
  3. Send through provider -> result
RETURNS: result
```

### Strategy Pattern

```nl
@type PricingStrategy {
  type: string
  discount_rate: number?
  minimum_purchase: number?
}

[calculate-price]
PURPOSE: Calculate price using selected strategy
INPUTS:
  - base_price: number
  - strategy: PricingStrategy
LOGIC:
  1. IF strategy.type is "flat" THEN return base_price
  2. IF strategy.type is "percentage" THEN apply percentage discount
  3. IF strategy.type is "tiered" THEN apply tiered pricing
RETURNS: final_price
```

---

## Pattern 7: Batch Operations

### Batch Processing

```nl
[process-batch]
PURPOSE: Process multiple items in batch
INPUTS:
  - items: list of Item
  - batch_size: number
LOGIC:
  1. Split items into batches of batch_size -> batches
  2. Process each batch -> results
  3. Combine batch results -> combined
RETURNS: combined
```

### Batch with Error Collection

```nl
@type BatchResult {
  successful: list of Item
  failed: list of FailedItem
  total: number
  success_count: number
  failure_count: number
}

[process-batch-with-errors]
PURPOSE: Process batch and collect successes and failures separately
INPUTS:
  - items: list of Item
LOGIC:
  1. Initialize success and failure lists -> successes, failures
  2. For each item, try to process -> result
  3. IF result.success THEN add to successes ELSE add to failures
  4. Build batch result -> batch_result
RETURNS: batch_result
```

---

## Anti-Patterns to Avoid

### 1. Giant ANLUs

**Bad:**
```nl
[do-everything]
PURPOSE: Handle all user operations
LOGIC:
  1. Validate input
  2. Check permissions
  3. Process request
  4. Update database
  5. Send notifications
  6. Log activity
  7. Return result
RETURNS: result
```

**Good:** Split into focused ANLUs with DEPENDS.

### 2. Vague PURPOSE

**Bad:**
```nl
PURPOSE: Process the thing
```

**Good:**
```nl
PURPOSE: Calculate the total price including tax and shipping for an order
```

### 3. Missing GUARDS

**Bad:**
```nl
[divide]
INPUTS:
  - a: number
  - b: number
RETURNS: a / b
```

**Good:**
```nl
[divide]
GUARDS:
  - b must not be zero -> ValueError("Cannot divide by zero")
RETURNS: a / b
```

### 4. Unclear Variable Names

**Bad:**
```nl
LOGIC:
  1. Do calculation -> x
  2. More work -> y
  3. Final step -> z
```

**Good:**
```nl
LOGIC:
  1. Calculate subtotal -> subtotal
  2. Apply discount -> discounted_price
  3. Add tax -> final_price
```

---

## What You've Learned

- [x] Validation patterns (boolean, raising, multi-field)
- [x] Factory patterns (simple, defaults, builder)
- [x] State machine patterns with LOGIC markers
- [x] Error handling patterns
- [x] Transformation pipelines
- [x] Dependency injection and strategy patterns
- [x] Batch processing patterns
- [x] Anti-patterns to avoid

---

## Next Steps

- **[Examples Gallery](../examples.md)** — Complete working examples
- **[CLI Reference](../cli-reference.md)** — Visualization commands
- **[LLM Reference](../llm-reference.md)** — Complete syntax reference
