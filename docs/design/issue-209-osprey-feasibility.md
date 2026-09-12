# Issue #209 — Osprey as an optional checked-IR target: feasibility study

**Status:** research deliverable (docs-only). Priority-low; does not block
Python/TypeScript.
**Pinned Osprey revision:** `8792de9f6d159922141f9d191e4bc5d256fbb971`
(osprey-lang, Nimblesite). All source links below point at that revision.
**Decision (ADR):** provisional **NO-GO** for implementing an Osprey target
now; revisit under the conditions in §5.

---

## 1. What was evaluated

[Osprey](https://github.com/Nimblesite/osprey) is a language whose checker
enforces, at compile time, exactly the class of guarantees NLS's checked IR
pipeline is building: canonical frontend lowering, versioned pass evidence,
typed algebraic effects with multiplicity, and target-capability gating
before any executable output. The question in
[#209](https://github.com/Mnehmos/mnehmos.nls.lang/issues/209) is whether
Osprey is worth adding as an *optional emission target* for NLS checked IR.

The comparison already paid for itself once: the "Osprey-informed
implementation refinements" adopted through #147/#202 — the canonical
frontend boundary, `CheckedModule` pass evidence, the target-capability
contract (`nlsc/capabilities.py`, `ETARGET002`), and emitter semantics
markers in lock identity — are NLS-side designs *informed by* Osprey's
architecture, not features requiring an Osprey backend.

## 2. Compatibility matrix

Verdicts: **direct** (shared checked IR maps 1:1), **adapter** (an emitter
runtime layer must translate), **blocked** (Osprey's pinned checker rejects
it, or NLS semantics do not exist yet).

| NLS semantic item | Osprey pinned-source evidence | Verdict | Probe |
| --- | --- | --- | --- |
| Structural expressions (literals, refs, fields, calls, operators) | [LanguageFlavors — canonical frontend contract](https://github.com/Nimblesite/osprey/blob/8792de9f6d159922141f9d191e4bc5d256fbb971/docs/specs/0023-LanguageFlavors.md) | direct | not yet executed |
| Ordered control: total branches, guarded results | same, plus checker regions | direct | not yet executed |
| Typed guard failures with identity (type, code, message) | typed failures in checker | adapter — NLS failure summaries (`IRFailureSpec`) must lower to Osprey typed errors | not yet executed |
| Numeric semantics (NLS division raises `ZeroDivisionError`; TS runtime helpers) | Osprey numerics | adapter — same helper-layer problem #202 solved for TypeScript | not yet executed |
| Structural equality / truthiness | Osprey equality | adapter (`__nls_eq`/`__nls_truthy` equivalents) | not yet executed |
| Records with constraints/invariants | Osprey types | adapter | not yet executed |
| Conservative effect summaries (`unknown` markers) | [effect_rows.rs — required operations](https://github.com/Nimblesite/osprey/blob/8792de9f6d159922141f9d191e4bc5d256fbb971/crates/osprey-types/src/effect_rows.rs) | adapter — NLS `unknown` has no Osprey row equivalent; would need widening | not yet executed |
| Resource state protocols (#200, planned) | multiplicity/linear tokens | adapter | blocked until #200 lands |
| Handlers with affine resumption (#207/#208, planned) | [0017-AlgebraicEffects](https://github.com/Nimblesite/osprey/blob/8792de9f6d159922141f9d191e4bc5d256fbb971/docs/specs/0017-AlgebraicEffects.md); [multiplicity.rs](https://github.com/Nimblesite/osprey/blob/8792de9f6d159922141f9d191e4bc5d256fbb971/crates/osprey-types/src/multiplicity.rs) | blocked today: NLS has no handler IR; Osprey is the *reference*, not a target, until #207/#208 define ours | blocked |
| Unsupported-capability gating | [target_capabilities.rs](https://github.com/Nimblesite/osprey/blob/8792de9f6d159922141f9d191e4bc5d256fbb971/crates/osprey-cli/src/target_capabilities.rs) — the pinned checker **rejects unsupported `many` and declaration-level `abort`** | direct — NLS `ETARGET002` implements the same law | design-level ✓ (executed as #202/#238, not as an Osprey compile) |
| `@literal` foreign blocks | Osprey foreign FFI | blocked — foreign NLS code has no Osprey meaning | n/a |

Evidence basis: pinned-source inspection during #202's audit (recorded in
that issue's body) plus the #202/#238–#242 implementations listed above. No
probe has executed Osprey tooling yet; every "not yet executed" row carries
its falsifiable expectation and can be turned into a probe without design
work.

## 3. Toolchain capture (structured for reproducibility)

Deliverable 3 of the issue requires capturing real versions/commands. The
executable spike is gated (§5), so this section pins the *procedure*:

- Obtain `osprey-cli` built at `8792de9f6d159922141f9d191e4bc5d256fbb971`
  (commit-locked checkout; record `cargo` version and `osprey --version`).
- Probe harness: NLS's existing cross-target runners
  (`tests/semantic/runners.py`) gain a third runner implementing the same
  `compile/execute/strict_check` interface; probe fixtures are the existing
  divergence-table modules plus one handler fixture once #207 lands.
- Each probe records: input `.nl`, emitted Osprey source, `osprey check`
  output, and pass/fail vs the Python/TypeScript oracle results.

## 4. What the spike would still have to prove

1. A shared checked-IR subset that both NLS and Osprey accept without
   adapter divergence in values, failures, or effect traces.
2. That Osprey's checker adds guarantees NLS's own `assert_checked_module`
   plus `tests/semantic` oracle do not already provide (otherwise the target
   duplicates existing verification at higher toolchain cost).
3. A maintenance story for tracking an external language's revisions.

## 5. Decision

**Provisional NO-GO.** An Osprey target is not worth building now because:

- The precondition NLS-side semantics (#195–#198 checked passes, #200
  protocols, #207/#208 handlers) are the actual work; the target would sit
  on top of them and add a third backend to keep conformant.
- #202's conformance harness and capability law already deliver the
  guarantees the comparison was after, without an external toolchain
  dependency.
- Priority-low by the issue's own label; Python/TypeScript conformance was
  explicitly the milestone.

**Revisit when:** (a) #195–#198 + #200 + #207 have landed and the semantic
suite executes the probe fixtures; (b) a concrete consumer needs Osprey
emission (none is known today); and (c) §4.2 shows at least one guarantee
Osprey adds beyond NLS's own checked pipeline. At that point, reopen with
the §3 harness as slice 1.
