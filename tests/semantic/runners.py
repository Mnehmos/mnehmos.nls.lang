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

        try:
            exec(code, namespace)
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

        try:
            exec(code, namespace)
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


def node_available() -> bool:
    """True when a Node.js runtime can execute compiled TypeScript."""
    import shutil

    return shutil.which("node") is not None


class TypeScriptRunner:
    """Execute NLS by compiling to TypeScript and running under Node.

    The compiled module is type-checked with ``tsc --strict`` (see
    ``strict_check``) and executed with Node's type stripping.  Results
    cross the boundary as JSON so Python tests can compare values,
    normalized failures, and error identities directly against the
    Python target (#202).
    """

    name = "typescript"

    def compile(self, nl_source: str) -> str:
        """Compile NLS source to TypeScript code."""
        from nlsc.emitter_typescript import emit_typescript

        nl_file = parse_nl_file(nl_source)
        return emit_typescript(nl_file)

    def _run_node(self, code: str, driver: str) -> ExecutionResult:
        import json
        import subprocess
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory(prefix="nlsc_ts_") as tmp:
            module_path = Path(tmp) / "module.ts"
            module_path.write_text(code + "\n" + driver, encoding="utf-8")
            try:
                completed = subprocess.run(
                    ["node", "--experimental-strip-types", str(module_path)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                return ExecutionResult.from_exception(RuntimeError(f"node failed: {exc}"))

        marker = "__NLS_RESULT__"
        for line in completed.stdout.splitlines():
            if line.startswith(marker):
                payload = json.loads(line[len(marker):])
                if payload.get("ok"):
                    return ExecutionResult.from_success(payload.get("value"))
                return ExecutionResult(
                    success=False,
                    exception=None,
                    exception_type=payload.get("name", "Error"),
                    exception_message=payload.get("message", ""),
                )
        stderr = completed.stderr.strip() or completed.stdout.strip()
        return ExecutionResult.from_exception(
            RuntimeError(f"typescript execution produced no result: {stderr[:500]}")
        )

    def execute(
        self,
        code: str,
        function: str,
        args: tuple = (),
    ) -> ExecutionResult:
        """Execute a function from compiled TypeScript code."""
        import json

        args_literal = json.dumps(list(args))
        driver = (
            "const __nls_args = "
            + args_literal
            + " as any[];\n"
            + "try {\n"
            + f"  const __nls_value = {function}(...__nls_args);\n"
            + "  const __nls_out = __nls_value === undefined ? null : __nls_value;\n"
            + '  console.log("__NLS_RESULT__" + JSON.stringify({ ok: true, value: __nls_out }));\n'
            + "} catch (e) {\n"
            + '  console.log("__NLS_RESULT__" + JSON.stringify({ ok: false, name: (e as Error).name ?? "Error", message: (e as Error).message ?? String(e) }));\n'
            + "}\n"
        )
        return self._run_node(code, driver)

    def create_instance(
        self,
        code: str,
        class_name: str,
        kwargs: dict[str, Any],
    ) -> ExecutionResult:
        """Create an instance of a generated interface/type.

        TypeScript records are structural: construction returns the
        plain object.  Constraint/invariant enforcement at construction
        is Python-only until the TS backend emits executable checks
        (tracked in #202).
        """
        import json

        kwargs_literal = json.dumps(kwargs)
        driver = (
            "try {\n"
            + f"  const __nls_value = {kwargs_literal};\n"
            + '  console.log("__NLS_RESULT__" + JSON.stringify({ ok: true, value: __nls_value }));\n'
            + "} catch (e) {\n"
            + '  console.log("__NLS_RESULT__" + JSON.stringify({ ok: false, name: (e as Error).name ?? "Error", message: (e as Error).message ?? String(e) }));\n'
            + "}\n"
        )
        return self._run_node(code, driver)

    def strict_check(self, code: str) -> tuple[bool, str]:
        """Type-check compiled code with tsc --strict (best effort)."""
        import shutil
        import subprocess
        import tempfile
        from pathlib import Path

        npx = shutil.which("npx")
        if npx is None:
            return False, "npx not found on PATH"

        with tempfile.TemporaryDirectory(prefix="nlsc_tsc_") as tmp:
            module_path = Path(tmp) / "module.ts"
            module_path.write_text(code, encoding="utf-8")
            try:
                completed = subprocess.run(
                    [npx, "-y", "-p", "typescript", "tsc", "--strict", "--noEmit",
                     "--skipLibCheck", str(module_path)],
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                return False, f"tsc failed to run: {exc}"
        if completed.returncode == 0:
            return True, ""
        return False, (completed.stdout + completed.stderr).strip()

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
