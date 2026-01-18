"""
Target-specific execution runners for semantic tests.

The PythonRunner compiles NLS to Python and executes it.
Future runners (TypeScriptRunner) will implement the same interface.
"""
from typing import Any

from nlsc.parser import parse_nl_file
from nlsc.emitter import emit_python

from .base import ExecutionResult


class PythonRunner:
    """Execute NLS by compiling to Python and running."""

    def compile(self, nl_source: str) -> str:
        """Compile NLS source to Python code."""
        nl_file = parse_nl_file(nl_source)
        return emit_python(nl_file)

    def execute(
        self,
        code: str,
        function: str,
        args: tuple = (),
    ) -> ExecutionResult:
        """Execute a function from compiled code.

        Args:
            code: Compiled Python code
            function: Function name to call
            args: Arguments to pass to the function

        Returns:
            ExecutionResult with success status and return value or exception
        """
        namespace: dict[str, Any] = {}
        exec(code, namespace)

        try:
            result = namespace[function](*args)
            return ExecutionResult.from_success(result)
        except Exception as e:
            return ExecutionResult.from_exception(e)

    def create_instance(
        self,
        code: str,
        class_name: str,
        kwargs: dict[str, Any],
    ) -> ExecutionResult:
        """Create an instance of a type from compiled code.

        Args:
            code: Compiled Python code
            class_name: Name of the class/type to instantiate
            kwargs: Keyword arguments for the constructor

        Returns:
            ExecutionResult with the created instance or exception
        """
        namespace: dict[str, Any] = {}
        exec(code, namespace)

        try:
            cls = namespace[class_name]
            instance = cls(**kwargs)
            return ExecutionResult.from_success(instance)
        except Exception as e:
            return ExecutionResult.from_exception(e)

    def compile_and_execute(
        self,
        nl_source: str,
        function: str,
        args: tuple = (),
    ) -> ExecutionResult:
        """Convenience method to compile and execute in one step."""
        code = self.compile(nl_source)
        return self.execute(code, function, args)

    def compile_and_create_instance(
        self,
        nl_source: str,
        class_name: str,
        kwargs: dict[str, Any],
    ) -> ExecutionResult:
        """Convenience method to compile and create instance in one step."""
        code = self.compile(nl_source)
        return self.create_instance(code, class_name, kwargs)
