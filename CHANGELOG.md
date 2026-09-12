# Changelog

Spec-level changes are tracked separately from toolchain changes so users can
see what affects their `.nl` files and what only affects tooling. See
[docs/versioning.md](docs/versioning.md) for the compatibility policy and
`@nls` revision rules.

## Unreleased

### Spec

- `IF ... THEN ... ELSE ...` is the total-branch form; a value bound on one
  path only is rejected (`ESEM010`) instead of failing at runtime. *(0.1)*
- Bindings are immutable in checked code; rebinding is strict-only
  `ESEM011`. *(0.1)*
- `RETURNS` distinguishes a value expression from a declared type; a
  type-only return is rejected in strict mode (`EIR004`). *(0.1)*
- The checked core is defined: structural expressions (literals, refs,
  fields, indexing, calls, operators) are supported; comprehensions,
  ternaries, f-strings, dicts/sets, slices, and prose-with-intent are
  explicit foreign content, rejected under `--strict` (`EIR002`). *(0.1)*
- `@nls MAJOR.MINOR` directive declares the spec revision; mismatches are
  `EVER001` (fatal) / `EVER002` (strict-only). *(0.1)*
- New diagnostics: `EIR001`–`EIR004`, `ESEM001`–`ESEM013`, `EVER001`–`EVER002`
  with a diagnostics index in the language spec.
- Guard error types must be builtins or declared `@type`s (`ESEM012`);
  non-builtin error classes are generated on both targets.

### Toolchain

- `nlsc assoc --desktop` generates Linux integration files (a desktop
  entry with Verify/Compile/Test actions and the `text/x-nls` MIME
  definition) from any platform; the OS integration guide now covers
  Windows context-menu snippets, macOS Quick Actions, and Linux
  file-manager integration (Issue #91).
- `nlsc init --template {basic,library,service,cli}` — working project
  scaffolds (Issue #92): example specs that pass strict verification,
  compile, and run their tests; `nls.toml`, a README, and a CI workflow
  per template; `--list-templates`; unknown names fail with cataloged
  `EINIT004`.
- `nlsc fmt <file|dir>` — canonical formatting (Issue #95): uppercase
  headers, normalized bullets/arrows, canonical section order, aligned
  INPUTS types, one blank line between blocks. `--check` for CI,
  `--diff` preview, JSON output; comments and their positions are
  preserved, `@literal`/`@main` bodies stay verbatim, and any reformat
  that would change module structure is refused (`EFMT001`). The LSP
  serves `textDocument/formatting` from the same formatter, and the
  GitHub Action gains a `format-check` input.
- `nlsc lint <file|dir>` — semantic intent-quality linter with twelve rules
  (`ELINT001`–`ELINT012`: guards for inputs, test coverage, invariants for
  types, unguarded division/indexing/optionals, implicit mutation, module
  version, long LOGIC, nested conditionals, input coverage, typed guard
  errors). Warnings by default, `--strict` for CI, `--list-rules`, JSON
  output, rules disabled via `.nlslintrc`/`nls.toml`, findings reported as
  LSP warnings, and a `lint` input on the GitHub Action.
- Performance: fixed quadratic dependency resolution (a 2000-ANLU compile
  went from 470 s to 4 s), bulk lockfile hashing lowers the module once
  per file instead of once per ANLU, and function extraction from emitted
  code is a single pass. Benchmark harness in `benchmarks/`, budgets in
  `tests/test_performance_budgets.py`, results documented in
  `docs/performance.md` and tracked as a CI artifact.
- `nlsc run --sandbox [--timeout N]` — isolated interpreter with an audit
  hook blocking process execution, networking, native interop, and
  filesystem writes outside the run directory (defense in depth, not a
  security boundary). Security model, trust levels, and disclosure policy
  documented in `docs/security.md`.
- `nlsc ci` — strict gate + frozen lockfile, with reproducible-compile
  verification and optional test execution (`--compile --test`).
- `nlsc compile --frozen-lockfile` — verifies a current lock and never
  rewrites it; output-hash mismatches fail as non-reproducible.
- `nlsc ir` — target-neutral IR (canonical text and `--json`), with source
  spans, inferred `effects`/`fails` contracts, and `--strict`.
- Semantic pipeline: symbol-table type checking, control-flow checks
  (branch totality, immutability), conservative effect and failure-set
  inference propagated to callers, and checked parallel eligibility for
  `nlsc graph`.
- Lockfile semantic hashes (`sem2`) cover LOGIC, guards, constraints, edge
  cases, results, literals, dependency signatures, effects, and failures;
  legacy locks invalidate conservatively (see versioning doc).
- TypeScript backend: NLS runtime (structural equality, truthiness,
  Python-compatible division/modulo), validating `make_<Type>` factories
  with constraints and invariants, portable error classes, and IR-based
  expression rendering. A `TypeScriptRunner` and cross-target conformance
  suite run in CI (`tsc --strict` + Node).
- Python backend renders structural expressions from the same IR (nested
  call arguments no longer truncate; comparisons in assignments no longer
  vanish).
- `@literal`-defined functions are declared escapes callable from NLS
  logic; module/file names shadowing stdlib modules warn (`ESEM013`).
- Target capability matrix: compiling `@literal` blocks or `@main` to a
  target that cannot represent them fails explicitly (`ETARGET002`)
  instead of silently dropping content; dropped `@property` coverage is
  strict-only. `@nls` spec revisions with `EVER001`/`EVER002` checks.
- Return-type inference no longer scans text inside string literals as
  code (a `RETURNS: x` bound to `"True and False"` was typed `bool`).
- The TypeScript conformance runner falls back to `tsc`-emitted
  JavaScript on Node versions without native type stripping.
- `examples/features/` — 14 strictly-verified feature examples, each with a
  committed lockfile, run as a regression suite in CI.
- Docs: 15-minute quickstart (verified by tests), refreshed language spec
  with an unsupported/out-of-scope list, IR specification, examples
  gallery, CI gate guide, and the versioning policy.

## 0.2.5

### Toolchain

- Parser bootstrap and structured CLI JSON coverage for `init`, `atomize`,
  `assoc`, graph/diff success payloads, watch runtime, and `nlsc test`.

## 0.2.0

### Toolchain

- `@use` stdlib domain resolution, `nlsc lsp`, cross-platform CLI fixes,
  Windows file association, GitHub Action, and TypeScript initial compile
  support.
