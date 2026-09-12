# Emission targets

NLS compiles a checked module to a target language through a registered
emitter. This page records what exists, what is gated, and what a new
target requires.

## Registered targets

| Target | Status | Semantics marker | Notes |
| --- | --- | --- | --- |
| `python` | supported | `py-3` | Reference semantics; `nlsc run` executes Python only. |
| `typescript` | supported | `ts-2` | `tsc --strict` + Node conformance in CI; `@literal`, `@main`, `@property`, and `FOR each` LOGIC loops are capability gaps (see below). |
| `rust` | **not implemented** — design only | — | Tracked in [#24](https://github.com/Mnehmos/mnehmos.nls.lang/issues/24). `@target rust` parses (the directive is recognized), but compilation fails with `ETARGET001` before any emission. |

`nlsc compile --target` accepts exactly the registered targets, and
`nlsc explain ETARGET002` documents the capability-gap diagnostic.

## Capability gaps

A registered target declares which features it can represent
(`nlsc/targets.py`). Compiling a file that uses an unsupported feature
fails with `ETARGET002` **before** anything is written: dropped program
content is fatal in every mode, while dropped test coverage (`@property`)
is strict-only.

| Feature | Python | TypeScript |
| --- | --- | --- |
| `@literal` blocks | yes | no (fatal) |
| `@main` block | yes | no (fatal) |
| `FOR each` LOGIC loop steps | yes | no (fatal) |
| `@property` specifications | yes | no (strict-only) |

## Rust target — design intent (gated, no timeline)

#24 is not started. When it is picked up, the expected shape is:

| NLS construct | Rust mapping (design intent) |
| --- | --- |
| `number` / `integer` | `f64` / `i64` |
| `string` / `boolean` | `String` / `bool` |
| `list of T` | `Vec<T>` (borrowed `&[T]` for read-only parameters) |
| records (`@type`) | `struct` with a validating `new` constructor mirroring the Python/TypeScript factory behavior |
| `RETURNS: none` | `()` |
| Guards | `Result<T, E>` with generated error types, or `panic!` only where the spec declares an unrecoverable error |
| `@literal` / `@main` | Rust has no sanctioned escape hatch yet; both would be capability gaps until designed |
| Structural equality / truthiness | Rust has neither; a runtime helper layer (like TypeScript's `__nls_eq` / `__nls_truthy`) must exist before emission can claim conformance |

Two hard prerequisites before an implementation PR: the checked IR
pipeline's remaining semantics issues (#197, #200, #207) so the target
does not freeze unverified semantics, and the #202 conformance harness
(a `RustRunner` in `tests/semantic/runners.py`) so divergence is caught
the way it was for TypeScript.

## Adding a target

Third-party targets register a `TargetEmitter` (`nlsc/targets.py`) either
in-process or through the `nlsc.targets` entry-point group — no parser,
resolver, or CLI edits. See
[architecture.md](architecture.md#adding-a-new-target) for the checklist.
