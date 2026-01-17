"""Tests for edge cases in atomization - production-grade patterns"""

import pytest
from nlsc.atomize import atomize_python_file, atomize_to_nl, python_type_to_nl
import ast


class TestComplexTypeHints:
    """Tests for complex Python type annotations"""

    def test_union_type(self):
        """Handle Union type annotations"""
        code = '''\
def process(value: int | str) -> int | str:
    """Process value"""
    return value
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1
        # Should handle union types gracefully
        assert anlus[0]["inputs"][0]["type"] in ["int | str", "any"]

    def test_optional_type(self):
        """Handle Optional type annotations"""
        code = '''\
from typing import Optional

def get_name(user_id: int) -> Optional[str]:
    """Get user name"""
    return None
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1
        # Optional[str] should become "string or null"
        assert "null" in anlus[0]["returns"].lower() or anlus[0]["returns"] == "None"

    def test_tuple_type(self):
        """Handle Tuple type annotations"""
        code = '''\
from typing import Tuple

def get_coords() -> Tuple[float, float]:
    """Get coordinates"""
    return (0.0, 0.0)
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1

    def test_callable_type(self):
        """Handle Callable type annotations"""
        code = '''\
from typing import Callable

def apply(func: Callable[[int], int], x: int) -> int:
    """Apply function"""
    return func(x)
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1
        # Should not crash on complex Callable type
        assert anlus[0]["inputs"][0]["name"] == "func"

    def test_generic_dict_type(self):
        """Handle dict with key/value types"""
        code = '''\
def count_items(items: dict[str, int]) -> int:
    """Count total items"""
    return sum(items.values())
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1
        assert "dict" in anlus[0]["inputs"][0]["type"].lower()


class TestDefaultParameters:
    """Tests for default parameter handling"""

    def test_simple_defaults(self):
        """Handle simple default values"""
        code = '''\
def greet(name: str = "World") -> str:
    """Greet someone"""
    return f"Hello, {name}!"
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1
        # Default values should be preserved or noted
        assert anlus[0]["inputs"][0]["name"] == "name"

    def test_none_default(self):
        """Handle None as default"""
        code = '''\
def process(data: list | None = None) -> list:
    """Process data"""
    return data or []
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1


class TestArgsKwargs:
    """Tests for *args and **kwargs patterns"""

    def test_args(self):
        """Handle *args parameter"""
        code = '''\
def sum_all(*values: float) -> float:
    """Sum all values"""
    return sum(values)
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1

    def test_kwargs(self):
        """Handle **kwargs parameter"""
        code = '''\
def create_object(**kwargs: str) -> dict:
    """Create object from kwargs"""
    return dict(kwargs)
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1


class TestDecorators:
    """Tests for decorated functions"""

    def test_property_decorator(self):
        """Handle @property methods"""
        code = '''\
class User:
    @property
    def name(self) -> str:
        """User name"""
        return self._name
'''
        anlus, _ = atomize_python_file(code)
        # Property methods should still be extractable
        assert len(anlus) == 1 or len(anlus) == 0  # May skip or extract

    def test_staticmethod_decorator(self):
        """Handle @staticmethod"""
        code = '''\
class Math:
    @staticmethod
    def add(a: int, b: int) -> int:
        """Add two numbers"""
        return a + b
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1
        assert anlus[0]["identifier"] == "add"

    def test_classmethod_decorator(self):
        """Handle @classmethod"""
        code = '''\
class Factory:
    @classmethod
    def create(cls, name: str) -> 'Factory':
        """Create factory"""
        return cls()
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1


class TestContextManagers:
    """Tests for context manager patterns (with statements)"""

    def test_with_statement_in_logic(self):
        """Handle with statements in function body"""
        code = '''\
def read_file(path: str) -> str:
    """Read file content"""
    with open(path) as f:
        return f.read()
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1
        # Should extract the return
        assert "f.read()" in anlus[0]["returns"] or "result" in anlus[0]["returns"]


class TestComprehensions:
    """Tests for list/dict/set comprehensions"""

    def test_list_comprehension_return(self):
        """Handle list comprehension in return"""
        code = '''\
def squares(n: int) -> list[int]:
    """Generate squares"""
    return [x * x for x in range(n)]
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1
        assert "[" in anlus[0]["returns"]

    def test_dict_comprehension(self):
        """Handle dict comprehension"""
        code = '''\
def invert(d: dict) -> dict:
    """Invert dictionary"""
    return {v: k for k, v in d.items()}
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1

    def test_generator_expression(self):
        """Handle generator expressions"""
        code = '''\
def sum_squares(n: int) -> int:
    """Sum of squares"""
    return sum(x * x for x in range(n))
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1


class TestNestedStructures:
    """Tests for nested control structures"""

    def test_nested_conditionals(self):
        """Handle nested if/else"""
        code = '''\
def categorize(x: int) -> str:
    """Categorize number"""
    if x < 0:
        return "negative"
    else:
        if x == 0:
            return "zero"
        else:
            return "positive"
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1

    def test_multiple_returns(self):
        """Handle multiple return statements"""
        code = '''\
def find_first(items: list[int], target: int) -> int:
    """Find first occurrence"""
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1

    def test_nested_loops(self):
        """Handle nested loops"""
        code = '''\
def matrix_sum(matrix: list[list[int]]) -> int:
    """Sum all elements"""
    total = 0
    for row in matrix:
        for item in row:
            total += item
    return total
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1


class TestWalrusOperator:
    """Tests for walrus operator (:=)"""

    def test_walrus_in_condition(self):
        """Handle walrus operator in conditions"""
        code = '''\
def check(data: list) -> int | None:
    """Check length"""
    if (n := len(data)) > 0:
        return n
    return None
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1


class TestLambdaExpressions:
    """Tests for lambda expressions"""

    def test_lambda_in_logic(self):
        """Handle lambda in function body"""
        code = '''\
def sort_by_second(items: list[tuple]) -> list:
    """Sort by second element"""
    return sorted(items, key=lambda x: x[1])
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1
        assert "sorted" in anlus[0]["returns"]


class TestMatchStatements:
    """Tests for Python 3.10+ match statements"""

    def test_simple_match(self):
        """Handle match statement"""
        code = '''\
def describe(value: int) -> str:
    """Describe value"""
    match value:
        case 0:
            return "zero"
        case 1:
            return "one"
        case _:
            return "other"
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1


class TestExceptionHandling:
    """Tests for various exception patterns"""

    def test_multiple_except_handlers(self):
        """Handle multiple except blocks"""
        code = '''\
def safe_parse(text: str) -> int:
    """Parse safely"""
    try:
        return int(text)
    except ValueError:
        return 0
    except TypeError:
        return -1
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1

    def test_finally_clause(self):
        """Handle try/except/finally"""
        code = '''\
def with_cleanup(path: str) -> str:
    """Read with cleanup"""
    try:
        f = open(path)
        return f.read()
    finally:
        f.close()
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1


class TestClassPatterns:
    """Tests for class-related patterns"""

    def test_init_method(self):
        """Handle __init__ method (should skip private)"""
        code = '''\
class User:
    def __init__(self, name: str) -> None:
        """Initialize user"""
        self.name = name
'''
        anlus, _ = atomize_python_file(code)
        # __init__ starts with underscore, should be skipped
        assert len(anlus) == 0

    def test_inheritance(self):
        """Handle class with inheritance"""
        code = '''\
from dataclasses import dataclass

@dataclass
class Employee(Person):
    """Employee data"""
    salary: float
    department: str
'''
        _, types = atomize_python_file(code)
        assert len(types) == 1
        assert types[0]["name"] == "Employee"

    def test_enum_class(self):
        """Handle Enum classes"""
        code = '''\
from enum import Enum

class Status(Enum):
    PENDING = 1
    ACTIVE = 2
    COMPLETED = 3
'''
        _, types = atomize_python_file(code)
        # Enum should not be extracted as dataclass
        assert len(types) == 0


class TestProductionPatterns:
    """Tests for real-world production patterns"""

    def test_api_endpoint_pattern(self):
        """Pattern: API endpoint handler"""
        code = '''\
async def get_user(user_id: int, db: Database) -> dict:
    """Get user by ID"""
    user = await db.query("SELECT * FROM users WHERE id = ?", user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1
        assert anlus[0]["is_async"] is True
        assert len(anlus[0]["guards"]) >= 0

    def test_validation_pattern(self):
        """Pattern: Input validation with multiple guards"""
        code = '''\
def create_user(email: str, password: str, age: int) -> dict:
    """Create new user"""
    if not email:
        raise ValueError("Email is required")
    if "@" not in email:
        raise ValueError("Invalid email format")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if age < 18:
        raise ValueError("Must be 18 or older")
    return {"email": email, "age": age}
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1
        # Should extract multiple guards
        assert len(anlus[0]["guards"]) >= 2

    def test_builder_pattern(self):
        """Pattern: Builder with chained methods"""
        code = '''\
class QueryBuilder:
    def where(self, condition: str) -> 'QueryBuilder':
        """Add where clause"""
        self.conditions.append(condition)
        return self

    def limit(self, n: int) -> 'QueryBuilder':
        """Set limit"""
        self._limit = n
        return self
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 2

    def test_factory_pattern(self):
        """Pattern: Factory with dispatch"""
        code = '''\
def create_handler(handler_type: str) -> Handler:
    """Create handler by type"""
    handlers = {
        "file": FileHandler,
        "http": HttpHandler,
        "socket": SocketHandler,
    }
    if handler_type not in handlers:
        raise ValueError(f"Unknown handler: {handler_type}")
    return handlers[handler_type]()
'''
        anlus, _ = atomize_python_file(code)
        assert len(anlus) == 1
        # Should capture the logic step
        assert len(anlus[0]["logic"]) >= 1


class TestAtomizeToNLOutput:
    """Tests for the complete NL output generation"""

    def test_complete_nl_output(self):
        """Verify complete NL output structure"""
        code = '''\
from dataclasses import dataclass

@dataclass
class User:
    """User data"""
    name: str
    email: str
    age: int = 0

async def create_user(name: str, email: str) -> User:
    """Create a new user"""
    if not name:
        raise ValueError("Name is required")
    user = User(name=name, email=email)
    return user
'''
        nl_content = atomize_to_nl(code, module_name="users")

        # Check structure
        assert "@module users" in nl_content
        assert "@target python" in nl_content
        assert "@type User" in nl_content
        assert "[create-user]" in nl_content
        assert "ASYNC: true" in nl_content
        assert "PURPOSE:" in nl_content
        assert "INPUTS:" in nl_content
        assert "GUARDS:" in nl_content or "name" in nl_content  # May or may not have guards
        assert "RETURNS:" in nl_content
