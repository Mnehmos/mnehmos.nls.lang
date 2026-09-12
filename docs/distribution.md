# Distribution and the Workspace Contract

`nlsc` ships on PyPI and is the canonical implementation; the dashboard
contract lives in [`.mnehmos/tool.json`](../.mnehmos/tool.json) so a
distribution dashboard can discover, install, exercise, and health-check
the toolchain entirely from machine-readable metadata.

## Manifest

`.mnehmos/tool.json` declares:

- **distribution** — PyPI package `nlsc`, entry point, version command,
  Python requirement, install commands (plain / treesitter / workspace
  with pytest), publishing provenance (PyPI Trusted Publishing via
  `.github/workflows/publish.yml`), and the npm policy (a thin bootstrap
  is possible in the future; the compiler is never forked to npm).
- **workspace** — the workspace script and its actions, with the layout
  (`.venv`, `sample/src`, `sample/build`).
- **commands** — build, test, lint, typecheck, watch, start, health.
- **capabilities** — targets (python, typescript), the language server
  command plus its features (diagnostics, lint, formatting, hover,
  completion, definition, references), quality gates, and the
  IR/provenance interchange commands.
- **paths** — where specs live and which artifacts are generated.

## Workspace workflow

`scripts/nls_workspace.py` implements the manifest contract with JSON
output for every action:

```bash
# Isolated workspace: venv + nlsc (from PyPI, or a built wheel) + sample spec
python scripts/nls_workspace.py bootstrap --root .nls-workspace     --install-from dist/nlsc-0.2.5-py3-none-any.whl

python scripts/nls_workspace.py health        --root .nls-workspace --json
python scripts/nls_workspace.py verify        --root .nls-workspace --json
python scripts/nls_workspace.py test          --root .nls-workspace --json
python scripts/nls_workspace.py compile-sample --root .nls-workspace --json
```

`bootstrap --no-venv` writes only the sample and uses the running
interpreter — for dashboards that manage environments themselves. The
sample specification exercises types with invariants, guards, a total
branch, and `@test` cases, so a green workflow means the installed
artifact verifiably compiles and runs.

## Release flow

1. **CI validates packaging on every PR** (`distribution` job):
   builds sdist+wheel, then bootstraps a workspace **from the wheel** and
   runs health → verify → test → compile-sample. A wheel that misses
   package data fails here, not after publishing.
2. **`publish.yml`** builds the distributions, runs the same
   artifact-install validation (`verify-install` job), attests build
   provenance for the artifacts, and publishes to PyPI with Trusted
   Publishing (OIDC — no long-lived tokens). Manual dispatches publish to
   TestPyPI first.

## Versioning

Version output is stable and parseable: `nlsc --version` prints the
toolchain version and the supported language-spec revision
(`nlsc 0.2.5 (language spec 0.1)`); the manifest's
`distribution.version_command` is the contract. Compatibility rules are
in [versioning.md](versioning.md).
