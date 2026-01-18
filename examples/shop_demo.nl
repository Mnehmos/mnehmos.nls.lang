@module shop_demo
@version 1.0.0
@target python

[divide]
PURPOSE: Divide two numbers safely.
INPUTS:
  - numerator: number
  - divisor: number
GUARDS:
  - divisor != 0 -> ValueError("Cannot divide by zero")
LOGIC:
  1. result = numerator / divisor
RETURNS: result

[calculate-discount]
PURPOSE: Calculate a discounted final price.
INPUTS:
  - price: number
  - discount_percent: number
GUARDS:
  - discount_percent >= 0 -> ValueError("discount_percent must be >= 0")
  - discount_percent <= 100 -> ValueError("discount_percent must be <= 100")
LOGIC:
  1. discount_amount = price * (discount_percent / 100)
  2. final_price = price - discount_amount
RETURNS: final_price

@test [divide] {
  divide(10, 2) == 5
}

@test [calculate-discount] {
  calculate_discount(100, 25) == 75
  calculate_discount(50, 0) == 50
  calculate_discount(80, 100) == 0
}
