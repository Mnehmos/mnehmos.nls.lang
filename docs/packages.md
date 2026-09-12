# Packages

NLS projects can depend on other NLS projects through a manifest and a
content-hashed lockfile. This is the **local** package model (Issue #146);
a hosted registry is tracked separately in #27.

## Manifest: `nls.pkg.json`

```json
{
  "schema": "nls.pkg/1",
  "name": "acme.project",
  "version": "1.0.0",
  "dependencies": {
    "acme.payments": {"path": "vendor/payments", "version": "^1.0.0"}
  }
}
```

- `name` / `version` describe the project itself. `version` is
  `MAJOR`, `MAJOR.MINOR`, or `MAJOR.MINOR.PATCH`.
- `dependencies` maps a dotted package name to a **local path** (relative
  to the manifest) and an optional semver constraint: `*`, an exact
  version, `^1.2.0` (compatible with the leftmost non-zero component), or
  `~1.2.0` (same major and minor). Git and registry sources are not part
  of this slice.
- Each dependency may carry its own `nls.pkg.json`; its `version` is what
  the constraint is checked against. Without one, the version is recorded
  as `unknown` and the constraint is not enforced.

## Using a package from `.nl`

`@use <package>.<domain>` resolves inside the dependency root, using the
same `v{major}/<domain path>.nl` layout as the [standard library](language-spec.md#use-directives):

```nl
@module app
@use acme.payments.charge
```

The longest dependency name that prefixes the domain wins, so the
`acme.payments` dependency above serves `@use acme.payments.charge` by
looking up `vendor/payments/v1/charge.nl`. A matching package root
**shadows** the stdlib for that namespace — there is no fallback to the
stdlib roots once a package name matches — so a dependency named `math`
owns `@use math.*` for the project. Domains that match no package resolve
against the stdlib roots (project `.nls/stdlib`, `--stdlib-path`,
`NLS_STDLIB_PATH`, bundled). A package name used alone
(`@use acme.payments`) is rejected with `EUSE001` — the package is a
namespace, not a domain.

**Current limit:** like stdlib `@use`, this slice resolves and records
dependencies but does not merge imported ANLUs into the caller's symbol
table, so an ANLU in another package cannot yet be called by name. Symbol
linking is the next package-model slice.

## Lockfile: `nls.pkg.lock`

```bash
nlsc install           # resolve dependencies, write nls.pkg.lock
nlsc install --check   # CI gate: fail (EPKG004) when the lock is stale
```

The lock records each dependency's resolved version, path, and a content
hash over its `.nl` files. `--check` re-resolves and compares, so CI
catches a dependency whose files changed without a lock refresh.

## Diagnostics

| Code | Meaning |
| --- | --- |
| `EPKG001` | Manifest missing, malformed, or a dependency without a path |
| `EPKG002` | A dependency path does not exist |
| `EPKG003` | A dependency's version does not satisfy the constraint |
| `EPKG004` | `nlsc install --check` found the lock out of date (content, version, or path changed) |
| `EPKG005` | The package lockfile could not be written |
| `EUSE001` | `@use` domain (including a package domain) could not be resolved |
