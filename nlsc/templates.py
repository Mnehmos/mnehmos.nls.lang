"""Project templates for ``nlsc init`` (Issue #92).

Each template produces a working project: the generated ``.nl`` files
pass strict verification, compile, and run their tests (enforced by
``tests/test_issue_92_templates.py``).  ``basic`` preserves the original
scaffold exactly; the others add example specs, ``nls.toml``, a README,
and a CI workflow.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProjectTemplate:
    name: str
    description: str
    files: dict[str, str] = field(default_factory=dict)

    @property
    def is_default_scaffold(self) -> bool:
        return not self.files


_CI_WORKFLOW = """name: NLS CI
on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install nlsc
      - run: |
          for f in $(find src -name '*.nl'); do
            nlsc verify "$f" --strict
            nlsc compile "$f"
            nlsc ci "$f" --test
          done
"""

_NLS_TOML = """# NLS project configuration.
# CLI settings live under [lint]; everything else is project metadata.

[project]
name = "{name}"
version = "0.1.0"
target = "python"

[lint]
# Rules to disable, e.g. disable = ["ELINT003"]
disable = []
"""

_LIBRARY_CORE = '''@module core
@version 0.1.0
@target python

@type Range {
  low: number
  high: number
}

@invariant Range {
  low <= high
}

[clamp]
PURPOSE: Clamp a value into a closed range
INPUTS:
  - value: number
  - bounds: Range
GUARDS:
  - bounds.low <= bounds.high -> ValueError("range bounds are inverted")
LOGIC:
  1. floored = max(value, bounds.low)
  2. IF floored > bounds.high THEN bounds.high -> result ELSE floored -> result
RETURNS: result

@test [clamp] {
  clamp(5, Range(low = 0, high = 10)) == 5
  clamp(-3, Range(low = 0, high = 10)) == 0
  clamp(99, Range(low = 0, high = 10)) == 10
}
'''

_LIBRARY_README = """# {name}

A reusable NLS specification library.

```bash
nlsc verify src/core.nl --strict
nlsc test src/core.nl
nlsc compile src/core.nl            # -> src/core.py
nlsc compile src/core.nl -t typescript
```

Edit `src/core.nl` — the spec is the source of truth; compiled artifacts
(`core.py`, `core.ts`) are generated, never hand-edited.
"""

_SERVICE_MODELS = '''@module models
@version 0.1.0
@target python

@type PaymentRequest {
  account_id: string, required
  amount_cents: integer, min: 1
  currency: string, required
}

@type PaymentResult {
  account_id: string
  amount_cents: integer
  status: string
}

[validate-request]
PURPOSE: Reject malformed payment requests before any processing
INPUTS:
  - request: PaymentRequest
GUARDS:
  - len(request.account_id) > 0 -> ValueError("account_id is required")
  - request.amount_cents > 0 -> ValueError("amount must be positive")
  - len(request.currency) == 3 -> ValueError("currency must be a 3-letter code")
RETURNS: request

@test [validate-request] {
  validate_request(PaymentRequest(account_id = "acct_1", amount_cents = 500, currency = "USD")).amount_cents == 500
}
'''

_SERVICE_HANDLERS = '''@module handlers
@version 0.1.0
@target python

@type Outcome {
  ok: boolean
  detail: string
}

[classify]
PURPOSE: Map an HTTP-style status code to an outcome
INPUTS:
  - status: integer
GUARDS:
  - status >= 100 -> ValueError("status codes are at least 100")
LOGIC:
  1. IF status >= 400 THEN False -> ok ELSE True -> ok
RETURNS: Outcome(ok = ok, detail = "classified")

@test [classify] {
  classify(200).ok == True
  classify(503).ok == False
}
'''

_SERVICE_README = """# {name}

An NLS service module: validated request shapes plus handler logic.

```bash
nlsc verify src/models.nl --strict
nlsc test src/models.nl
nlsc verify src/handlers.nl --strict
nlsc ci src/handlers.nl --compile --test
```

Patterns shown:

- `@type` records with `required`/`min` constraints enforced at construction.
- Guards that reject malformed input with typed errors.
- Total `IF/THEN/ELSE` branches so every path defines its result.
"""

_CLI_MAIN = '''@module main
@version 0.1.0
@target python

[format-price]
PURPOSE: Render a price in cents as a display string
INPUTS:
  - cents: integer
  - currency: string
GUARDS:
  - cents >= 0 -> ValueError("prices cannot be negative")
LOGIC:
  1. whole = cents / 100
  2. IF len(currency) == 3 THEN currency -> code ELSE "USD" -> code
RETURNS: code + " " + str(whole)

@main {
  PRINT format-price(1999, "USD")
}
'''

_CLI_COMMANDS = '''@module commands
@version 0.1.0
@target python

[add-tax]
PURPOSE: Add a percentage tax to an amount in cents
INPUTS:
  - cents: integer
  - rate_percent: number
GUARDS:
  - cents >= 0 -> ValueError("amount cannot be negative")
  - rate_percent >= 0 -> ValueError("rate cannot be negative")
RETURNS: cents * (1 + rate_percent / 100)

@test [add-tax] {
  add_tax(1000, 10) == 1100
}
'''

_CLI_README = """# {name}

An NLS command-line tool.

```bash
nlsc run src/main.nl            # executes the @main block
nlsc test src/commands.nl
nlsc fmt src/ --check
```

`src/main.nl` holds the entry point and presentation logic;
`src/commands.nl` holds reusable operations with their tests.
"""

TEMPLATES: dict[str, ProjectTemplate] = {
    "basic": ProjectTemplate(
        name="basic",
        description="Minimal scaffold (config, src/, tests/)",
    ),
    "library": ProjectTemplate(
        name="library",
        description="Reusable specifications with invariants and tests",
        files={
            "nls.toml": _NLS_TOML,
            "README.md": _LIBRARY_README,
            ".github/workflows/nls.yml": _CI_WORKFLOW,
            "src/core.nl": _LIBRARY_CORE,
        },
    ),
    "service": ProjectTemplate(
        name="service",
        description="Validated request models and handler logic",
        files={
            "nls.toml": _NLS_TOML,
            "README.md": _SERVICE_README,
            ".github/workflows/nls.yml": _CI_WORKFLOW,
            "src/models.nl": _SERVICE_MODELS,
            "src/handlers.nl": _SERVICE_HANDLERS,
        },
    ),
    "cli": ProjectTemplate(
        name="cli",
        description="Command-line tool with a @main entry point",
        files={
            "nls.toml": _NLS_TOML,
            "README.md": _CLI_README,
            ".github/workflows/nls.yml": _CI_WORKFLOW,
            "src/main.nl": _CLI_MAIN,
            "src/commands.nl": _CLI_COMMANDS,
        },
    ),
}


def render_template(template: ProjectTemplate, project_name: str) -> dict[str, str]:
    """Template files with the project name substituted."""
    return {
        path: content.replace("{name}", project_name)
        for path, content in template.files.items()
    }
