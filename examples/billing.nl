@module billing
@version 1.0.0
@target python

# === Type Definitions ===

@type LineItem {
  description: string, required
  quantity: number, min: 1
  unit_price: number, min: 0
}

@type Invoice {
  id: string, required
  customer_name: string, required
  items: list of LineItem
  tax_rate: number
  discount_percent: number
}

@invariant Invoice {
  tax_rate >= 0
  tax_rate <= 100
  discount_percent >= 0
  discount_percent <= 100
}

# === Core Functions ===

[calculate-line-total]
PURPOSE: Calculate the total for a single line item.
INPUTS:
  - item: LineItem
RETURNS: item.quantity * item.unit_price

[calculate-subtotal]
PURPOSE: Sum all line item totals for an invoice.
INPUTS:
  - invoice: Invoice
LOGIC:
  1. Sum each item's total -> subtotal
RETURNS: sum(item.quantity * item.unit_price for item in invoice.items)

[apply-discount]
PURPOSE: Apply a percentage discount to an amount.
INPUTS:
  - amount: number
  - discount_percent: number
GUARDS:
  - discount_percent >= 0 -> ValueError("Discount cannot be negative")
  - discount_percent <= 100 -> ValueError("Discount cannot exceed 100%")
LOGIC:
  1. Calculate discount amount -> discount
  2. Subtract from original -> final
RETURNS: amount * (1 - discount_percent / 100)

[calculate-tax]
PURPOSE: Calculate tax on a given amount.
INPUTS:
  - amount: number
  - tax_rate: number
GUARDS:
  - tax_rate >= 0 -> ValueError("Tax rate cannot be negative")
RETURNS: amount * (tax_rate / 100)

[calculate-invoice-total]
PURPOSE: Calculate the final total for an invoice including tax and discount.
INPUTS:
  - invoice: Invoice
LOGIC:
  1. Calculate subtotal from all items -> subtotal
  2. Apply discount to subtotal -> discounted
  3. Calculate tax on discounted amount -> tax
  4. Add tax to discounted amount -> total
RETURNS: calculate_subtotal(invoice) * (1 - invoice.discount_percent / 100) * (1 + invoice.tax_rate / 100)
DEPENDS: [calculate-subtotal], [apply-discount], [calculate-tax]

# === Test Specifications ===

@test [calculate-line-total] {
  calculate_line_total(LineItem(description="Widget", quantity=5, unit_price=10)) == 50
  calculate_line_total(LineItem(description="Gadget", quantity=1, unit_price=99.99)) == 99.99
}

@test [apply-discount] {
  apply_discount(100, 10) == 90
  apply_discount(100, 0) == 100
  apply_discount(100, 100) == 0
  apply_discount(50, 25) == 37.5
}

@test [calculate-tax] {
  calculate_tax(100, 10) == 10
  calculate_tax(100, 0) == 0
  calculate_tax(200, 7.5) == 15
}

# === Property-Based Tests ===

@property [apply-discount] {
  apply_discount(x, 0) == x  # Zero discount returns original
  apply_discount(x, 100) == 0  # 100% discount returns zero
  apply_discount(x, d) <= x  # Discount never increases amount
}

@property [calculate-tax] {
  calculate_tax(x, 0) == 0  # Zero tax rate means no tax
  forall x: number -> calculate_tax(x, r) >= 0  # Tax is never negative
}
