@module sample-complex
@target python

[validate-email]
PURPOSE: Validate an email address format.
INPUTS:
  - email: string
GUARDS:
  - email | ValueError: "Email cannot be empty"
  - NOT ('@' not in email) | ValueError: "Email must contain @"
RETURNS: True

[calculate-discount]
PURPOSE: Calculate the discounted price.
INPUTS:
  - price: number
  - discount_percent: number
GUARDS:
  - NOT (price < 0) | ValueError: "Price cannot be negative"
  - NOT (discount_percent < 0 or discount_percent > 100) | ValueError: "Discount must be between 0 and 100"
LOGIC:
  1. discount_amount = price * (discount_percent / 100)
  2. final_price = price - discount_amount
RETURNS: final_price

[process-order]
PURPOSE: Process an order for a user.
INPUTS:
  - user: User
  - products: list of Product
GUARDS:
  - products | ValueError: "Order must contain at least one product"
LOGIC:
  1. total = sum((p.price for p in products))
  2. order_id = f'ORD-{user.email}-{len(products)}'
RETURNS: dictionary

[get-or-default]
PURPOSE: Return value if not None, otherwise default.
INPUTS:
  - value: string or null
  - default: string
RETURNS: value if value is not None else default

[format-price]
PURPOSE: Format a price with currency symbol.
INPUTS:
  - price: number
  - currency: string
LOGIC:
  1. symbols = {'USD': '$', 'EUR': '€', 'GBP': '£'}
  2. symbol = symbols.get(currency, currency)
RETURNS: f'{symbol}{price:.2f}'
