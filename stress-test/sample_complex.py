"""Sample Python module with complex patterns for atomize testing."""
from dataclasses import dataclass
from typing import Optional, Union

@dataclass
class User:
    """A user in the system."""
    name: str
    email: str
    age: Optional[int] = None

@dataclass
class Product:
    """A product for sale."""
    id: str
    name: str
    price: float
    in_stock: bool = True

def validate_email(email: str) -> bool:
    """Validate an email address format."""
    if not email:
        raise ValueError("Email cannot be empty")
    if "@" not in email:
        raise ValueError("Email must contain @")
    return True

def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate the discounted price."""
    if price < 0:
        raise ValueError("Price cannot be negative")
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    discount_amount = price * (discount_percent / 100)
    final_price = price - discount_amount
    return final_price

def process_order(user: User, products: list[Product]) -> dict:
    """Process an order for a user."""
    if not products:
        raise ValueError("Order must contain at least one product")

    total = sum(p.price for p in products)
    order_id = f"ORD-{user.email}-{len(products)}"

    return {
        "order_id": order_id,
        "user": user.name,
        "total": total,
        "item_count": len(products)
    }

async def fetch_user(user_id: str) -> Optional[User]:
    """Fetch a user by ID asynchronously."""
    # Simulate async operation
    await some_async_call()
    return User(name="Test", email="test@example.com")

def get_or_default(value: Optional[str], default: str = "") -> str:
    """Return value if not None, otherwise default."""
    return value if value is not None else default

def format_price(price: float, currency: str = "USD") -> str:
    """Format a price with currency symbol."""
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{price:.2f}"
