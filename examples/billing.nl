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

[line-items-total]
PURPOSE: Recursively total the line items from a starting position.
INPUTS:
  - items:  list of LineItem
  - cursor: number, optional
LOGIC:
  1. IF cursor is not None THEN cursor -> index ELSE 0 -> index
  2. IF index >= len(items) THEN 0 -> total ELSE [calculate-line-total](items[(index)]) + [line-items-total](items, index + 1) -> total
RETURNS: total
DEPENDS: [calculate-line-total]

[calculate-subtotal]
PURPOSE: Sum all line item totals for an invoice.
INPUTS:
  - invoice: Invoice
LOGIC:
  1. [line-items-total](invoice.items) -> subtotal
RETURNS: subtotal
DEPENDS: [line-items-total]

[apply-discount]
PURPOSE: Apply a percentage discount to an amount.
INPUTS:
  - amount: number
  - discount_percent: number
GUARDS:
  - discount_percent >= 0 -> ValueError("Discount cannot be negative")
  - discount_percent <= 100 -> ValueError("Discount cannot exceed 100%")
LOGIC:
  1. amount * (discount_percent / 100) -> discount
  2. amount - discount -> final
RETURNS: final

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
  1. [calculate-subtotal](invoice) -> subtotal
  2. [apply-discount](subtotal, invoice.discount_percent) -> discounted
  3. [calculate-tax](discounted, invoice.tax_rate) -> tax
  4. discounted + tax -> total
RETURNS: total
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

@test [line-items-total] {
  line_items_total([]) == 0
  line_items_total([LineItem(description="Widget", quantity=5, unit_price=10)]) == 50
}

@test [calculate-subtotal] {
  calculate_subtotal(Invoice(id="INV-1", customer_name="Acme", items=[], tax_rate=0, discount_percent=0)) == 0
  calculate_subtotal(Invoice(id="INV-2", customer_name="Acme", items=[LineItem(description="Widget", quantity=2, unit_price=25), LineItem(description="Gadget", quantity=1, unit_price=50)], tax_rate=0, discount_percent=0)) == 100
}

@test [calculate-invoice-total] {
  calculate_invoice_total(Invoice(id="INV-3", customer_name="Acme", items=[LineItem(description="Widget", quantity=1, unit_price=100)], tax_rate=0, discount_percent=0)) == 100
  calculate_invoice_total(Invoice(id="INV-4", customer_name="Acme", items=[LineItem(description="Widget", quantity=1, unit_price=100)], tax_rate=10, discount_percent=0)) == 110
  calculate_invoice_total(Invoice(id="INV-5", customer_name="Acme", items=[LineItem(description="Widget", quantity=1, unit_price=100)], tax_rate=0, discount_percent=25)) == 75
  calculate_invoice_total(Invoice(id="INV-6", customer_name="Acme", items=[LineItem(description="Widget", quantity=1, unit_price=200)], tax_rate=10, discount_percent=50)) == 110
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
