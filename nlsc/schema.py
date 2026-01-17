"""
ANLU Schema - Data structures for Natural Language Units

These dataclasses represent the parsed structure of .nl files.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class InputType(Enum):
    """Primitive types supported in NLS"""
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    VOID = "void"
    ANY = "any"
    LIST = "list"
    CUSTOM = "custom"


@dataclass
class Input:
    """A single input parameter for an ANLU"""
    name: str
    type: str
    constraints: list[str] = field(default_factory=list)
    description: Optional[str] = None
    
    def to_python_type(self) -> str:
        """Convert NLS type to Python type hint"""
        type_map = {
            "number": "float",
            "string": "str",
            "boolean": "bool",
            "void": "None",
            "any": "Any",
        }
        
        # Handle "list of X"
        if self.type.startswith("list of "):
            inner = self.type[8:]  # Remove "list of "
            inner_py = type_map.get(inner, inner)
            return f"list[{inner_py}]"
        
        return type_map.get(self.type, self.type)


@dataclass
class Guard:
    """A precondition check for an ANLU"""
    condition: str
    error_type: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class EdgeCase:
    """An explicit edge case handling"""
    condition: str
    behavior: str


@dataclass
class LogicStep:
    """A parsed LOGIC step with dataflow and FSM information"""
    number: int
    description: str
    assigns: list[str] = field(default_factory=list)
    uses: list[str] = field(default_factory=list)
    depends_on: list[int] = field(default_factory=list)

    # FSM features (Issue #3)
    state_name: Optional[str] = None
    output_binding: Optional[str] = None
    condition: Optional[str] = None

    @property
    def is_independent(self) -> bool:
        """True if this step has no dependencies on other steps"""
        return len(self.depends_on) == 0

    @property
    def is_conditional(self) -> bool:
        """True if this step has an IF condition"""
        return self.condition is not None


@dataclass
class ANLU:
    """
    Atomic Natural Language Unit

    The fundamental building block of NLS - describes one logical operation
    in human-readable terms that can be compiled to executable code.
    """
    identifier: str
    purpose: str
    returns: str

    # Optional fields
    inputs: list[Input] = field(default_factory=list)
    guards: list[Guard] = field(default_factory=list)
    logic: list[str] = field(default_factory=list)
    logic_steps: list["LogicStep"] = field(default_factory=list)
    edge_cases: list[EdgeCase] = field(default_factory=list)
    depends: list[str] = field(default_factory=list)
    literal: Optional[str] = None

    # Metadata
    line_number: int = 0

    def parallel_groups(self) -> list[list[int]]:
        """
        Return groups of step numbers that can execute in parallel.
        Each group contains steps that have all their dependencies satisfied
        by previous groups.
        """
        if not self.logic_steps:
            return []

        groups = []
        completed = set()

        remaining = {step.number: step for step in self.logic_steps}

        while remaining:
            # Find all steps whose dependencies are satisfied
            ready = []
            for num, step in remaining.items():
                if all(dep in completed for dep in step.depends_on):
                    ready.append(num)

            if not ready:
                # Circular dependency or error - break to avoid infinite loop
                break

            groups.append(ready)
            for num in ready:
                completed.add(num)
                del remaining[num]

        return groups

    def fsm_states(self) -> list[str]:
        """Return list of state names from LOGIC steps (FSM nodes)"""
        return [
            step.state_name
            for step in self.logic_steps
            if step.state_name is not None
        ]

    def fsm_transitions(self) -> list[tuple[str, str]]:
        """
        Return list of (from_state, to_state) transitions based on dependencies.
        Only includes transitions between named states.
        """
        transitions = []

        # Build map of step number -> state name
        step_to_state = {
            step.number: step.state_name
            for step in self.logic_steps
            if step.state_name is not None
        }

        for step in self.logic_steps:
            if step.state_name is None:
                continue

            for dep_num in step.depends_on:
                if dep_num in step_to_state:
                    from_state = step_to_state[dep_num]
                    to_state = step.state_name
                    if (from_state, to_state) not in transitions:
                        transitions.append((from_state, to_state))

        return transitions

    @property
    def bound_type(self) -> Optional[str]:
        """If identifier is Type.method, returns 'Type', else None"""
        if "." in self.identifier:
            return self.identifier.split(".")[0]
        return None

    @property
    def method_name(self) -> Optional[str]:
        """If identifier is Type.method, returns 'method', else None"""
        if "." in self.identifier:
            return self.identifier.split(".", 1)[1]
        return None
    
    def to_python_return_type(self) -> str:
        """Convert RETURNS to Python type hint"""
        returns = self.returns.strip()

        # Handle boolean literals
        if returns == "True" or returns == "False":
            return "bool"

        # Handle f-strings (f'...' or f"...")
        if returns.startswith("f'") or returns.startswith('f"'):
            return "str"

        # Handle ternary expressions (x if condition else y)
        if " if " in returns and " else " in returns:
            return "Any"

        # Handle dictionary keyword
        if returns.lower() == "dictionary":
            return "dict"

        # Handle function calls with arguments (e.g., json.loads(text), max(a, b))
        # These are expressions, not types
        if "(" in returns and ")" in returns:
            # Method calls like "json.loads(text)" or "obj.method()"
            if "." in returns:
                return "Any"
            # Built-in function calls like "max(a, b)", "len(x)"
            # Check if it starts with lowercase (not a constructor)
            if returns and returns[0].islower():
                return "Any"

        # Simple expressions like "a + b" -> infer from operation
        if "+" in returns or "-" in returns:
            return "float"
        if "×" in returns or "*" in returns or "/" in returns or "÷" in returns:
            return "float"

        type_map = {
            "number": "float",
            "string": "str",
            "boolean": "bool",
            "void": "None",
        }

        # Check if it's a known type name
        if returns.lower() in type_map:
            return type_map[returns.lower()]

        # Check if it's a custom type name (capitalized)
        if returns and returns[0].isupper():
            # If it's a constructor call like "Point(1, 2)", extract "Point"
            if "(" in returns:
                return returns.split("(")[0]
            return returns

        # Check if RETURNS is a variable assigned in logic_steps
        if self.logic_steps:
            for step in self.logic_steps:
                if returns in step.assigns:
                    # Variable was assigned - infer from the assignment expression
                    desc = step.description.strip()
                    # Check if assignment is arithmetic
                    if "=" in desc:
                        expr = desc.split("=", 1)[1].strip()
                        if any(op in expr for op in ["+", "-", "*", "/", "×", "÷"]):
                            return "float"
                        # Check if it's a function call that might return a number
                        if "sum(" in expr or "len(" in expr or "max(" in expr or "min(" in expr:
                            return "float"
                        # Check if it looks like a boolean expression
                        if any(op in expr for op in [">", "<", "==", "!=", ">=", "<=", " and ", " or ", " not "]):
                            return "bool"
                        # Check if it's a constructor call (Type(...))
                        import re
                        ctor_match = re.match(r'([A-Z][a-zA-Z0-9_]*)\s*\(', expr)
                        if ctor_match:
                            return ctor_match.group(1)
                        # Check if it's an empty list []
                        if expr.strip() == "[]":
                            return "list"
                        # Check if it's an empty dict {}
                        if expr.strip() == "{}":
                            return "dict"
                    break

        # Check if RETURNS variable matches an input name - use input's type
        for inp in self.inputs:
            if returns == inp.name:
                return inp.to_python_type()

        # Default fallback for unknown identifiers
        if returns.isidentifier():
            # If it starts with uppercase, treat as custom type
            if returns[0].isupper():
                return returns
            # Otherwise it's probably a variable - use Any
            return "Any"

        return type_map.get(returns, returns)
    
    @property
    def python_name(self) -> str:
        """Convert kebab-case identifier to snake_case for Python"""
        return self.identifier.replace("-", "_")


@dataclass
class TypeField:
    """A single field in a type definition"""
    name: str
    type: str
    constraints: list[str] = field(default_factory=list)
    description: Optional[str] = None

    def to_python_type(self) -> str:
        """Convert NLS type to Python type hint"""
        type_map = {
            "number": "float",
            "string": "str",
            "boolean": "bool",
            "void": "None",
            "any": "Any",
        }

        # Handle "list of X"
        if self.type.startswith("list of "):
            inner = self.type[8:]  # Remove "list of "
            inner_py = type_map.get(inner, inner)
            return f"list[{inner_py}]"

        return type_map.get(self.type, self.type)


@dataclass
class TypeDefinition:
    """A custom type definition from @type block"""
    name: str
    fields: list[TypeField] = field(default_factory=list)
    base: Optional[str] = None
    line_number: int = 0


@dataclass 
class TestCase:
    """A test assertion for an ANLU"""
    expression: str
    expected: str


@dataclass
class TestSuite:
    """Test specifications from @test block"""
    anlu_id: str
    cases: list[TestCase] = field(default_factory=list)


@dataclass
class Module:
    """Module-level metadata from directives"""
    name: str
    version: str = "0.1.0"
    target: str = "python"
    imports: list[str] = field(default_factory=list)
    types: list[TypeDefinition] = field(default_factory=list)


@dataclass
class NLFile:
    """
    Complete parsed representation of a .nl file
    """
    module: Module
    anlus: list[ANLU] = field(default_factory=list)
    tests: list[TestSuite] = field(default_factory=list)
    literals: list[str] = field(default_factory=list)
    main_block: list[str] = field(default_factory=list)  # @main block content
    
    # Source info
    source_path: Optional[str] = None
    
    def get_anlu(self, identifier: str) -> Optional[ANLU]:
        """Find an ANLU by identifier"""
        for anlu in self.anlus:
            if anlu.identifier == identifier:
                return anlu
        return None
    
    def dependency_order(self) -> list[ANLU]:
        """Return ANLUs in topological order based on dependencies"""
        # Simple implementation - assumes no circular deps for V0
        ordered = []
        remaining = list(self.anlus)
        resolved = set()
        
        while remaining:
            for anlu in remaining[:]:
                deps_satisfied = all(
                    dep.strip("[]") in resolved 
                    for dep in anlu.depends
                )
                if deps_satisfied:
                    ordered.append(anlu)
                    resolved.add(anlu.identifier)
                    remaining.remove(anlu)
        
        return ordered
