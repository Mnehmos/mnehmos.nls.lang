# Versioning and Compatibility Guarantees

NLS versions two things independently:

| Version | Where it lives | What it means |
| --- | --- | --- |
| **Toolchain version** | `nlsc --version`, PyPI | The compiler's own release (currently 0.2.x). |
| **Language-spec revision** | `nlsc --version`, declared per file with `@nls` | The surface language + semantics contract (currently **0.1**). |

## Declaring a revision

```nl
@module billing
@nls 0.1
@version 1.0.0        # your module's own version, unrelated
```

`@nls` is optional; a file without it is treated as targeting the current
revision. `@version` remains your module's semantic version.

## Compatibility rules

Given a toolchain supporting spec revision `MAJOR.MINOR`:

| Declared `@nls` | Result |
| --- | --- |
| same `MAJOR.MINOR` | Compatible — no diagnostic. |
| same major, newer minor (e.g. `0.2` on a `0.1` toolchain) | `EVER002` — **strict-only warning**; the file may use features this compiler does not implement. `nlsc ci` fails. |
| different major (e.g. `1.0`) | `EVER001` — **always fatal**; semantics cannot be guaranteed. |
| malformed (e.g. `@nls latest`) | `EVER001` — always fatal. |

Older minor revisions within the same major are compatible: the spec is
additive within a major line.

## What counts as a breaking change

**Spec revision bump — MAJOR** (files may stop compiling):

- removing or renaming syntax, sections, directives, or operators;
- changing the meaning of an existing construct;
- turning previously accepted input into a fatal error (e.g. a construct
  moving from "foreign pass-through" to "rejected");
- changing the semantics of emitted code for existing programs.

**Spec revision bump — MINOR** (existing files keep working):

- new syntax, directives, or section keywords;
- new diagnostics for cases that previously produced broken output — when
  the old behavior was never a valid program;
- new constraint names, builtins, or type forms;
- widening what strict mode accepts.

**Toolchain-only release** (no spec bump):

- emitter output changes that preserve behavior (formatting, helper names);
- new commands, flags, JSON fields, or error catalog entries that do not
  change meaning of existing programs;
- performance, packaging, and documentation changes.

Two deliberate nuances beyond plain semver:

1. **Checker tightening is major.** Promoting a warning to a fatal error
   breaks files that previously verified; that is a spec-level change.
2. **Lockfile hash-scheme changes are toolchain releases with a documented
   migration.** Semantic-hash revisions (like the `sem2` scheme) invalidate
   old lock entries conservatively; the next `nlsc compile` or
   `nlsc lock:update` regenerates them. No spec bump is implied, because
   program meaning is unchanged.

## Upgrade guidance

1. `nlsc --version` prints both the toolchain and the supported spec revision.
2. Files declaring a newer spec revision warn under `--strict`; run
   `nlsc ci` after upgrading to catch anything the new toolchain tightened.
3. `nlsc diff <file>` compares against the committed lockfile, so semantic
   changes caused by an upgrade surface exactly where they happened.

## Where changes are recorded

- **Language-spec changes** (surface syntax, semantics, diagnostics
  severity): the `Spec` section of the [CHANGELOG](https://github.com/Mnehmos/mnehmos.nls.lang/blob/master/CHANGELOG.md).
- **Toolchain changes** (commands, flags, emitters, tooling): the
  `Toolchain` section of the same changelog.
- The spec itself is revised in [language-spec.md](language-spec.md), which
  carries its revision header and the diagnostics index.
