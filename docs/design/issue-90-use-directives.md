# Issue #90 — `@use` Directives (Slice C) — Contract / Design

Run: phase2-milestones-2026-02-08  
Task: issue-90-arch

This document defines the *end-to-end* contract for resolving `@use` directives against a bundled stdlib plus user overrides.

---

## 0) Goals / non-goals

### Goals

1. Deterministic mapping from `@use <domain>` → a single `.nl` source file.
2. Explicit, testable override precedence (project-local first, then user/CLI, then bundled).
3. Versionable stdlib domains without breaking existing projects.
4. Errors are structured enough to be asserted in tests (code + message + attempted search roots).

### Non-goals

* Defining new language semantics of imported symbols (type checking / export syntax is out of Slice C).
* Network resolution or package registry.

---

## 1) Stdlib layout proposal (bundled `.nl` files)

### 1.1 Bundled stdlib root

Bundled stdlib ships *inside the `nlsc` distribution* as plain `.nl` sources (not generated artifacts):

* Root directory: [`nlsc/stdlib/`](nlsc/stdlib/)

### 1.2 Versioned layout (major-version directories)

Stdlib modules are organized by **major version** at the top level, then by **domain path**:

```
nlsc/
  stdlib/
    MANIFEST.json
    v1/
      math/
        core.nl
        stats.nl
      text/
        core.nl
    v2/
      ...
```

**Rules**

* A **domain** is the dotted path in `@use`, e.g. `math.core`.
* Domain maps to a relative path under a version root by replacing `.` with `/` and appending `.nl`.
  * Example: `math.core` → `math/core.nl`
* Version roots are named `v{MAJOR}` (e.g. `v1`, `v2`).
* [`nlsc/stdlib/MANIFEST.json`](nlsc/stdlib/MANIFEST.json) declares the *default major* used when a directive does not specify a major.

### 1.3 Recommended project-local override layout

Project-local overrides are **in-repo** sources under a hidden config directory:

* Root directory: [`.nls/stdlib/`](.nls/stdlib/)
* Same layout as bundled stdlib, including major version roots.

Example:

```
.nls/
  stdlib/
    v1/
      math/
        core.nl   # project override
```

Rationale:

* Keeps overrides out of the normal source tree.
* Allows pinning/parallel majors the same way as bundled stdlib.

---

## 2) Domain resolution algorithm

### 2.1 Directive syntax (Slice C scope)

This contract assumes the parser produces a normalized directive object:

* `raw`: original text
* `domain`: dotted identifier, e.g. `math.core`
* optional `major`: integer major version (see §2.3)

Concrete surface forms are intentionally limited for Slice C:

* `@use math.core`
* Optional version prefix: `@use v1.math.core`

### 2.2 Resolution roots (search order)

Resolution searches a list of **roots**, in priority order (first match wins):

1. **Project-local override root**: [`.nls/stdlib/`](.nls/stdlib/)
2. **User-provided roots** (highest to lowest):
   * CLI: `--stdlib-path <dir>` (repeatable; earlier flags have higher precedence)
   * Env: `NLS_STDLIB_PATH` (path-list; left-to-right precedence)
3. **Bundled root**: [`nlsc/stdlib/`](nlsc/stdlib/)

Notes:

* Each root is treated as a *filesystem sandbox*. Resolution MUST NOT traverse outside roots.
* Roots that do not exist are ignored **except**: if provided explicitly via CLI, non-existent paths SHOULD fail fast with a CLI error (outside `@use` resolution).

### 2.3 Major-version selection

Given `@use <spec>`:

* If `<spec>` begins with `v{N}.` (e.g. `v1.math.core`), then `major=N` and the domain is the remainder (`math.core`).
* Otherwise `major` is taken from the bundled manifest default (and may be overridden by a future CLI option such as `--stdlib-major`, not required for Slice C).

Bundled manifest minimum fields:

```json
{
  "schema": 1,
  "default_major": 1,
  "versions": {
    "v1": { "semver": "1.2.0" },
    "v2": { "semver": "2.0.0" }
  }
}
```

### 2.4 Candidate path generation

For a resolved `(major, domain)` pair, generate candidates **in this exact order**:

1. `v{major}/{domain_as_path}.nl`

Where:

* `domain_as_path = domain.replace('.', '/')`

Example:

* `@use math.core` with default major 1 → candidate: `v1/math/core.nl`

Future-compatible extension (explicitly **out-of-scope** for Slice C but reserved):

* secondary candidate: `v{major}/{domain_as_path}/index.nl`

### 2.5 Conflict & error behavior (testable contract)

Resolution outcome is exactly one of:

* **Resolved**: a single filesystem path.
* **Missing domain**: no root contained the candidate module.
* **Ambiguous**: multiple roots at the *same precedence tier* contain the candidate.

Define precedence tiers:

* Tier 0: project-local override root
* Tier 1: CLI `--stdlib-path` roots (each flag is its own tier level; earlier flags higher)
* Tier 2: env roots (each entry is its own tier level; earlier entries higher)
* Tier 3: bundled root

**Ambiguity rule**

* If *two different roots* at the same tier level both contain the candidate path, raise an **Ambiguous** error.
  * Example: two `--stdlib-path` flags with the same precedence level is impossible if each flag is a level; ambiguity can still occur within env roots if you treat the entire env list as one level—this spec avoids that by defining each entry as a level.
  * Therefore, ambiguity most commonly occurs when the implementation allows multiple values within one “level” (e.g., a single CLI flag that accepts a list). If the implementation chooses list semantics, it MUST then implement ambiguity detection within that level.

**Error codes** (required for tests)

* `EUSE001` Missing domain
  * Include: `domain`, `major`, `attempted_roots[]`, `candidate_relpath`
* `EUSE002` Ambiguous domain
  * Include: `domain`, `major`, `candidate_relpath`, `matches[]` (absolute or normalized paths)

### 2.6 Deterministic resolution flow (reference pseudocode)

```python
def resolve_use(domain_spec: str, roots: list[Root], default_major: int) -> ResolvedUse:
    major, domain = parse_major_prefix(domain_spec, default_major)
    rel = f"v{major}/" + domain.replace(".", "/") + ".nl"

    tried: list[str] = []
    matches: list[str] = []

    for root in roots:  # already expanded into strict precedence order
        tried.append(root.path)
        candidate = join(root.path, rel)
        if exists(candidate):
            matches.append(candidate)
            return ResolvedUse(domain=domain, major=major, path=candidate)

    raise MissingDomain(code="EUSE001", domain=domain, major=major, rel=rel, tried=tried)
```

Implementation note: if an implementation permits multiple candidates per precedence step, replace the “return first match” with “collect matches within a step and error if >1”.

---

## 3) User override precedence (CLI/env/project-local)

### 3.1 Precedence summary

Highest to lowest:

1. [`.nls/stdlib/`](.nls/stdlib/) (project-local override)
2. CLI `--stdlib-path` (repeatable; left-to-right)
3. Env `NLS_STDLIB_PATH` (left-to-right)
4. Bundled [`nlsc/stdlib/`](nlsc/stdlib/)

### 3.2 Contract for “override” vs “conflict”

* If a higher-precedence root contains the module, it **overrides** all lower-precedence matches (no warning required for Slice C).
* If two matches are present at the *same* precedence step (implementation-defined; see §2.5), it is a hard error `EUSE002`.

---

## 4) Versioning strategy notes (stdlib domains)

### 4.1 Why version at the domain root

Stdlib changes will happen; without versioning, `@use math.core` is inherently unstable across compiler releases.

### 4.2 Proposed invariants

* Stdlib is semver-versioned **per major root**: `v1`, `v2`, …
* Within the same major root:
  * backward-compatible additions are allowed (new helpers, new domains)
  * breaking changes are not allowed
* Breaking changes require a new `v{major+1}` root.

### 4.3 Pinning & reproducibility (lockfile-facing, Slice C notes)

To support reproducible builds:

* The lockfile SHOULD record:
  * which stdlib major is in use when `@use` omits explicit major
  * the bundled stdlib semver for that major (from `MANIFEST.json`)
  * hashes for each resolved stdlib module file (content hash)

This allows:

* Detecting “stdlib drift” when upgrading `nlsc`.
* Keeping projects stable even as bundled stdlib evolves.

---

## 5) Test plan (Red-phase cases)

All tests below are stated as *black-box* scenarios that can be implemented against the resolver + CLI, without requiring semantic analysis.

### 5.1 Happy path — bundled stdlib

Given:

* Bundled root contains `v1/math/core.nl`.
* Program contains `@use math.core`.

Expect:

* Resolution selects bundled `.../nlsc/stdlib/v1/math/core.nl`.
* Dependency graph includes that file as an input (or equivalent representation).

### 5.2 Missing domain

Given:

* No roots contain `v1/math/missing.nl`.
* Program contains `@use math.missing`.

Expect:

* Compile fails with `EUSE001`.
* Error includes `domain=math.missing`, `major=1`, `candidate_relpath=v1/math/missing.nl`.
* Error includes `attempted_roots` in the exact precedence order used.

### 5.3 Project-local override wins

Given:

* Bundled root contains `v1/math/core.nl`.
* Project-local override root contains `.nls/stdlib/v1/math/core.nl`.
* Program contains `@use math.core`.

Expect:

* Resolution selects project-local `.nls/stdlib/v1/math/core.nl`.
* No error.

### 5.4 CLI override wins over env and bundled

Given:

* CLI provides `--stdlib-path <X>`.
* `<X>/v1/math/core.nl` exists.
* Env root also has a different copy.
* Bundled exists.

Expect:

* Resolution selects `<X>/v1/math/core.nl`.

### 5.5 Conflict / ambiguity at same precedence step

This is an *implementation choice test*: it becomes relevant if `--stdlib-path` accepts a list in one flag or if env list entries are treated as a single precedence step.

Given:

* Two stdlib roots considered the same precedence step both contain `v1/math/core.nl`.

Expect:

* Compile fails with `EUSE002`.
* Error includes `matches[]` listing both candidates.

---

## 6) Acceptance criteria (exact, testable)

### 6.1 Resolution correctness

1. `@use math.core` resolves to **exactly one** file path or fails with a structured error.
2. Domain-to-path mapping is deterministic: `math.core` → `math/core.nl` (with `.nl` suffix and version prefix).
3. If project-local override exists at [`.nls/stdlib/`](.nls/stdlib/), it is selected over any CLI/env/bundled match.
4. If CLI `--stdlib-path` is provided, it is selected over env and bundled.
5. If no roots contain the candidate file, compilation fails with error code `EUSE001` and includes the `candidate_relpath` and `attempted_roots`.

### 6.2 Version behavior

6. If `@use v1.math.core` is used, resolution MUST use major=1 regardless of bundled default.
7. If `@use math.core` omits explicit major, resolution MUST use bundled manifest `default_major` (until an explicit `--stdlib-major` is introduced).

### 6.3 Security / sandboxing

8. Resolver MUST NOT allow `@use` to escape roots (no `..`, no absolute paths, no path separators in domain segments).
9. When resolution fails, error output MUST NOT reveal unrelated filesystem paths beyond the declared roots.

### 6.4 Determinism & diagnostics

10. For a fixed set of roots and filesystem contents, resolution results are deterministic across runs.
11. Errors include a stable code (`EUSE001`/`EUSE002`) suitable for assertions.

---

## Appendix A — Mermaid overview

```mermaid
flowchart TD
  A[@use domain] --> B[Parse optional vN. prefix]
  B --> C[major + domain]
  C --> D[relpath = v{major}/domain_as_path.nl]
  D --> E{Search roots in order}
  E -->|found| F[Resolved path]
  E -->|not found| G[EUSE001 MissingDomain]
```

