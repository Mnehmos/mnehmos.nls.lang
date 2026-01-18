"""
Base classes and data structures for semantic tests.

These provide a target-agnostic foundation for testing NLS semantics.
When a TypeScript emitter is added, we can create a TypeScriptRunner
that implements the same interface.
"""
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class ExecutionResult:
    """Result of executing compiled NLS code."""

    success: bool
    return_value: Any = None
    exception: Exception | None = None
    exception_type: str | None = None
    exception_message: str | None = None
    side_effects: list[str] = field(default_factory=list)

    @classmethod
    def from_success(cls, value: Any) -> "ExecutionResult":
        """Create a successful execution result."""
        return cls(success=True, return_value=value)

    @classmethod
    def from_exception(cls, exc: Exception) -> "ExecutionResult":
        """Create a failed execution result from an exception."""
        return cls(
            success=False,
            exception=exc,
            exception_type=type(exc).__name__,
            exception_message=str(exc),
        )


class TargetRunner(Protocol):
    """Protocol for target-specific code runners.

    Implementations must be able to:
    1. Compile NLS source to target language
    2. Execute compiled code and capture results
    3. Optionally support observation of side effects
    """

    def compile(self, nl_source: str) -> str:
        """Compile NLS source to target language code."""
        ...

    def execute(
        self,
        code: str,
        function: str,
        args: tuple = ()
    ) -> ExecutionResult:
        """Execute a function from compiled code with given arguments."""
        ...

    def create_instance(
        self,
        code: str,
        class_name: str,
        kwargs: dict[str, Any],
    ) -> ExecutionResult:
        """Create an instance of a type from compiled code."""
        ...
