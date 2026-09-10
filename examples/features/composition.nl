# Feature: composing operations
# Calls resolve through the semantic symbol table; DEPENDS is verified
# against the calls actually made, and failures propagate to callers.

@module ex_composition
@version 1.0.0
@target python

[net-price]
PURPOSE: Price after a percentage discount
INPUTS:
  - price: number
  - discount_percent: number
GUARDS:
  - discount_percent >= 0 -> ValueError("discount cannot be negative")
  - discount_percent <= 100 -> ValueError("discount cannot exceed 100")
RETURNS: price * (1 - discount_percent / 100)

[tax]
PURPOSE: Tax on an amount
INPUTS:
  - amount: number
  - rate_percent: number, min: 0
RETURNS: amount * rate_percent / 100

[invoice-total]
PURPOSE: Net price plus tax, composed from two operations
INPUTS:
  - price: number
  - discount_percent: number
  - tax_percent: number
LOGIC:
  1. net = [net-price](price, discount_percent)
  2. tax_amount = [tax](net, tax_percent)
  3. total = net + tax_amount
RETURNS: total
DEPENDS: [net-price], [tax]

@main {
  PRINT invoice-total(100, 10, 20)
}

@test [invoice-total] {
  invoice_total(100, 10, 20) == 108
}
