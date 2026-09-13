# NLS Target-Neutral IR Specification

Status: **experimental, version 0.1** — the IR boundary described in issue #194 under the emitter-abstraction plan (#147). It is the interchange format between the surface language and every backend, designed to be readable by LLMs and by people who do not read code for a living.

- Schema module: `nlsc/ir.py`
- Deterministic lowering: `nlsc/lowering.py` (shared by both parser backends)
- CLI: `nlsc ir <file.nl>` (canonical text), `nlsc ir <file.nl> --json` (JSON form), `nlsc ir <file.nl> --check` (backend-free validation: shared semantic gate plus checked-emission eligibility; exit 1 with `EIR003` blockers when the spec is not valid checked IR)

## Design rules

1. **Target-neutral.** The same `.nl` source lowers to byte-identical IR regardless of `@target`. Python-ness stops at the IR boundary.
2. **Deterministic.** Same source in, same canonical text out — stable node ids, stable ordering, no addresses or hashes that depend on run environment.
3. **Honest about gaps.** Anything outside the supported core becomes an explicit `foreign` node plus a diagnostic (`EIR001`/`EIR002`). Lowering never silently drops work, invents placeholder values, or guesses that the last binding is the return value.
4. **Unchecked ≠ checked.** Lowering produces an *unchecked* module (`checked: false`). A module containing foreign nodes is never eligible for checked emission (`EIR003`). Unfilled contract slots (`effects`, `failures`, `typestate`) mean *not analyzed* — they are never implicit proof of purity or safety.
5. **Narrative is preserved.** PURPOSE text, descriptive LOGIC notes, and EDGE CASES ride along as attached narrative (`purpose`, `note`, `edge-case`) and never become executable statements.

## Canonical text grammar

The canonical form is an S-expression dialect — minimal punctuation, one statement per line, trivially parseable and diffable.

```
;; nls-ir 0.1 target-neutral module=<name> [version=<version>]
(imports <name>...)
(uses <domain>...)
(type <Name> [extends <Base>]
  (field <name> <typeref> ["constraint"...] ["description"]))
(op <anlu-name> [(line <n>)]
  (purpose "...")
  (param <name> <typeref> [optional])
  (guard <expr> -> (error <Type> [code=<code>] ["message"]))
  (body
    (bind <name> <expr>)                          ;; step=<n> line=<n> comment
    (bind <name> <expr> aug=<op>)
    (expr <expr>)                                 ;; value discarded, effects kept
    (branch <expr>
      ( ...then stmts... )
      [else ( ...else stmts... )])
    (loop while <expr> ( ...body... ))
    (note "narrative text")
    (foreign-stmt reason=<why> "raw text"))
  (result [(type <typeref>)] [(value <expr>)])
  (depends <anlu-name>...)
  (literal "verbatim target implementation")
  (edge-case "condition" -> "behavior"))
```

### Values

```
(lit 42)                        number, raw token preserved
(lit "True and False")          string, exact decoded text; source token kept on the node
(lit True) (lit False) (lit None)
(ref <name>)                    local binding / parameter reference
(get <expr> <field>)            field access
(at <expr> <expr>)              index access
(list <expr>...)                list construction
(binary <op> <l> <r>)           op: add sub mul div floor_div mod pow
                                eq ne lt le gt ge and or is is_not in not_in
(unary neg|not <expr>)
(call <name> [<args>] [(kw <expr>)...])            builtin/foreign/constructor call
(anlu <kebab-name> [<args>])                       ANLU call, kebab name verbatim
(method <base> .<name> [<args>])                   method call, structural
(foreign reason=<why> "raw text")                  outside the supported core
```

### Type references

```
number integer string boolean void any     primitives
(list <typeref>)                           list of X
(<Name>)                                   declared record type
(<typeref> optional)                       nullable / optional
```

### Effect sets (Issue #197)

Operations carry an analyzed ``effects`` set with read/write resource
identities where the analysis can attribute one:

- purely structural code yields ``(effects)`` — an analyzed **empty** set;
- a method call on a parameter or binding yields a **named write**
  (``items.append(x)`` -> ``write(items)``);
- anything unattributable — foreign calls, ``@literal`` bodies, method
  calls on unnamed bases — stays an ``unknown`` marker;
- callee effects propagate to callers with **call-site substitution**:
  the caller sees its own argument name (``[mutate](rows)`` ->
  ``write(rows) origin=callee``), and a callee-internal resource that
  cannot be attributed to a caller name propagates as ``unknown``.

```
(effects (effect write items origin=call) (effect unknown origin=callee))
```

An optional ``EFFECTS:`` contract line declares an upper bound —
``pure``, ``unknown``, ``read``, ``write``, ``read(name)``,
``write(name)`` — checked as ``EFX001`` (exceeded) / ``EFX002``
(malformed, fatal in every mode). ``None`` still means *not analyzed* and
is never an implicit proof of purity.  Effects participate in lockfile
semantic hashes (scheme ``sem3``).

### Control policies (Issue #201)

``RETRY:`` / ``TIMEOUT:`` sections lower onto ``IROperation.retry`` and
``.timeout`` and render canonically (``(retry attempts=3 on=NetworkError
key=order_id)``, ``(timeout after=5000ms outcome=...)``).  They are part
of the checked contract and the semantic hash; no emitter produces them
yet, so both targets refuse policy files with ``ETARGET002``.

### State tokens (Issue #200)

Protocol parameters and results carry state tokens on their type
references (``Order<Pending>``), lowered as ``TypeRef`` arguments.  The
typestate checker consumes them; emitted annotations use the base type.
See [language-spec.md](language-spec.md#resource-state-protocols-opt-in).

### Failure sets (Issue #198)

Every operation carries an analyzed ``fails`` set after lowering:

```
(fails (fail ValueError code=MISSING "Token required" origin=guard)
       (fail ValueError "called" origin=callee)
       (fail unknown))
```

- ``origin=guard`` — raised by one of the operation's guards (typed
  error, optional code, message preserved).
- ``origin=callee`` — propagated from a called operation, transitively
  and deterministically.
- ``(fail unknown)`` — a conservative marker for foreign calls, method
  calls, division/modulo, index access, and literal implementations. An
  unknown external failure is never treated as an empty set, and pure
  operations carry an analyzed-empty ``(fails)`` (``None`` still means
  *not analyzed*).

Failure sets participate in lockfile semantic identity: changing a
callee's guard payload invalidates its callers.

### Foreign reasons (stable vocabulary)

`comprehension`, `generator-expression`, `ternary`, `fstring`, `raw-string`,
`dict-literal`, `slice`, `star-args`, `lambda`, `tuple`, `walrus-or-slice`,
`multiple-statements`, `augmented-binding`, `call-on-non-name`,
`positional-after-keyword`, `prose`, `tokenize-error`, `unexpected-token`,
`trailing-tokens`, `unexpected-end`, `keyword-<word>`.

## Node identity and spans

Every value and statement node carries:

- a **stable id** — a structural path like `checkout.step1.value.left`, derived purely from the lowered shape, never from run state;
- a **source span** — `{anlu, line, step}` identifying the ANLU, the source line, and the originating LOGIC step (when applicable).

Diagnostics produced during lowering always carry the span's line, so a tool can point back at the exact numbered step.

## JSON form

`module_to_json()` (and `nlsc ir --json`) emits the same content as a
deterministic JSON document: every node is an object with a `kind`
discriminator, ids, and spans. Keys are sorted; the payload embeds the
canonical text for convenience (`canonical`) so LLM round-trips can pick
either representation.

## Extension and version policy

- `IR_SCHEMA_VERSION` is `"0.1"` and appears in every serialized form (`;; nls-ir 0.1`, `"ir_version": "0.1"`).
- **Additive changes** (new optional node fields, new foreign reasons, new normalized operators) bump the minor version; consumers must ignore unknown fields and unknown reasons.
- **Breaking changes** (removing/renaming node kinds, changing canonical text of existing nodes) bump the major version and require a migration note here.
- Later passes (type checking #195, control checks #196, effects #197, failure sets #198) fill the reserved contract slots and may *add* node kinds; they must not reinterpret existing ones.
- The checked-emission gate (`EIR003`) is the enforcement point: backends that consume IR (see #202) must refuse unchecked modules.

## What lowers today

| Surface | IR |
| --- | --- |
| `LOGIC` step `x = expr` | `bind` |
| Step `action -> binding` | `bind` |
| Step `name += expr` | `bind` with `aug` |
| Step `[anlu](args)` (value unused) | `expr` statement (effects preserved) |
| Step `IF c THEN action` | `branch` with `then` region |
| GUARDS bullet | `guard` with normalized error identity |
| RETURNS expression / type | `result` with `value` and/or `type` slots |
| Descriptive step (no binding) | `note` |
| `FOR EACH ... : ADD\|COLLECT ... -> name` | `for-each` node (bounded fold, #267) |
| Anything else executable | `foreign` node + `EIR001`/`EIR002` diagnostic |

Not yet lowered (tracked in follow-up issues): loops (`loop` region is
reserved), EDGE CASES as executable regions (#190/#196), `@test`/`@property`
bodies, `@main` blocks.
