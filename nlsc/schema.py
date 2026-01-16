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
    edge_cases: list[EdgeCase] = field(default_factory=list)
    depends: list[str] = field(default_factory=list)
    literal: Optional[str] = None
    
    # Metadata
    line_number: int = 0
    
    def to_python_return_type(self) -> str:
        """Convert RETURNS to Python type hint"""
        # Simple expressions like "a + b" -> infer from operation
        if "+" in self.returns or "-" in self.returns:
            return "float"
        if "×" in self.returns or "*" in self.returns:
            return "float"
        
        type_map = {
            "number": "float",
            "string": "str",
            "boolean": "bool",
            "void": "None",
        }
        return type_map.get(self.returns, self.returns)
    
    @property
    def python_name(self) -> str:
        """Convert kebab-case identifier to snake_case for Python"""
        return self.identifier.replace("-", "_")


@dataclass
class TypeDefinition:
    """A custom type definition from @types block"""
    name: str
    fields: dict[str, str] = field(default_factory=dict)
    base: Optional[str] = None


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
