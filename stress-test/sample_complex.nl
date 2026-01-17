@module sample-complex
@target python

[validate-email]
PURPOSE: Validate an email address format.
INPUTS:
  - email: string
RETURNS: True

[calculate-discount]
PURPOSE: Calculate the discounted price.
INPUTS:
  - price: number
  - discount_percent: number
LOGIC:
  1. discount_amount = price * (discount_percent / 100)
  2. final_price = price - discount_amount
RETURNS: final_price

[process-order]
PURPOSE: Process an order for a user.
INPUTS:
  - user: User
  - products: list of Product
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
