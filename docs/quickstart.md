# 15-Minute Quickstart

Build something real in NLS: a **shipping quote calculator** with typed records,
validation guards, total branches, cross-operation calls, and executable tests.
Every command and output below is exercised by the test suite
(`tests/test_issue_145_walkthrough.py`), so this guide cannot drift from the
toolchain.

You need: Python 3.11+ and a terminal. No compiler background required — the
`.nl` file *is* the program you review.

## 1. Install (1 min)

```bash
pip install nlsc
nlsc --version
```

## 2. Start a project (1 min)

```bash
nlsc init shop
cd shop
```

`nlsc init` creates `nl.config.yaml`, `src/`, and `tests/`.

## 3. Write the spec (5 min)

Create `src/shipping.nl`. Read it top to bottom — that is the whole program:

```nl
@module shipping
@version 1.0.0
@target python

@type Parcel {
  weight_kg: number, min: 0
  declared_value: number, min: 0
}

@type Quote {
  currency: string
  base_fee: number, min: 0
  insurance: number, min: 0
  total: number, min: 0
}

[base-rate]
PURPOSE: Tiered base rate for a parcel by weight
INPUTS:
  - weight_kg: number
GUARDS:
  - weight_kg >= 0 -> ValueError("weight cannot be negative")
LOGIC:
  1. IF weight_kg <= 1 THEN 5.0 -> rate ELSE 5.0 + (weight_kg - 1) * 2.0 -> rate
RETURNS: rate

[insurance-fee]
PURPOSE: Insurance proportional to declared value
INPUTS:
  - declared_value: number
GUARDS:
  - declared_value >= 0 -> ValueError("declared value cannot be negative")
RETURNS: declared_value * 0.02

[shipping-quote]
PURPOSE: Full quote for a parcel, with an express surcharge option
INPUTS:
  - parcel: Parcel
  - express: boolean
LOGIC:
  1. base = [base-rate](parcel.weight_kg)
  2. insurance = [insurance-fee](parcel.declared_value)
  3. IF express THEN base * 1.5 -> surcharge ELSE 0 -> surcharge
  4. total = base + insurance + surcharge
RETURNS: Quote(currency = "USD", base_fee = base, insurance = insurance, total = total)
DEPENDS: [base-rate], [insurance-fee]

@test [base-rate] {
  base_rate(1) == 5
  base_rate(2) == 7
  base_rate(0.5) == 5
}

@test [shipping-quote] {
  shipping_quote(Parcel(weight_kg = 2, declared_value = 100), False).total == 9
  shipping_quote(Parcel(weight_kg = 2, declared_value = 100), True).total == 19.5
}
```

Reading guide:

- **`@type`** blocks are the shapes of your data; `min: 0` constraints are
  enforced on every construction, on both targets.
- **`[name]` blocks** are operations. `PURPOSE` is for humans, `INPUTS` /
  `RETURNS` are the contract, `GUARDS` are the failure contract.
- **`IF ... THEN ... ELSE ... -> name`** is a *total* branch: both paths bind
  `rate`/`surcharge`, so no path can leave a value undefined.
- **`[base-rate](x)`** calls another operation; `DEPENDS` declares it as a
  contract, and the checker verifies your calls match.
- **`@test` blocks** are runnable specifications, not documentation.

## 4. Verify strictly (2 min)

```bash
nlsc verify src/shipping.nl --strict
```

```
Verifying src/shipping.nl (parser: tree-sitter)...
  ✓ Syntax valid: 3 ANLUs
  ✓ Dependencies valid
  ✓ All ANLUs valid

Verification passed!
```

Strict mode refuses anything the compiler cannot prove: unknown calls,
undefined values, prose pretending to be logic, type mismatches, broken
branches. If you get an error here, the message names the line, the ANLU, and
the fix — for example `ESEM010: value 'rate' is only defined under a branch
condition` tells you to make the branch total with `ELSE`.

## 5. Run the tests (1 min)

```bash
nlsc test src/shipping.nl
```

```
Running 5 test cases from src/shipping.nl...
  • [base-rate]: 3 cases
  • [shipping-quote]: 2 cases

✓ All 5 tests passed!
```

## 6. Compile (2 min)

```bash
nlsc compile src/shipping.nl            # -> shipping.py
nlsc compile src/shipping.nl -t typescript   # -> shipping.ts (+ vitest tests)
```

Both artifacts come from the same checked internal representation, so
behavior matches: guard errors raise `ValueError("weight cannot be negative")`
in Python *and* under Node, `[1] == [1]` is true in both, and empty lists are
falsy in both.

## 7. Look behind the curtain — the IR (2 min)

LLMs and tools consume the same target-neutral IR you can read:

```bash
nlsc ir src/shipping.nl
```

```
(op shipping-quote (line 35)
  (purpose "Full quote for a parcel, with an express surcharge option")
  (param parcel Parcel)
  (param express boolean)
  (body
    (bind base (anlu base-rate (get (ref parcel) weight_kg)))  ;; step=1 line=41
    ...
    (branch (ref express)
      ( (bind surcharge (binary mul (ref base) (lit 1.5))) )
      else ( (bind surcharge (lit 0)) )
    )  ;; step=3 line=43
    (bind total (binary add (binary add (ref base) (ref insurance)) (ref surcharge)))
  )
  (result (value (call Quote ...)))
  (depends [base-rate] [insurance-fee])
  (effects (effect unknown origin=call))
  (fails (fail unknown))
)
```

Every node has a source line; `effects`/`fails` are inferred contracts. Add
`--json` for the machine-readable form your tooling (or an LLM) can consume.

## 8. Make it CI-proof (1 min)

```bash
nlsc ci src/shipping.nl --compile --test
```

```
ci passed (parse: passed, gate: passed, lockfile: current, compile: reproducible, test: passed)
```

`nlsc ci` is strict by default and requires the committed `.nl.lock` file
(created by your first `nlsc compile`) — it never rewrites it, and it verifies
the recompiled output reproduces the locked hash. Exit code **0** means
everything passed; **1** means any diagnostic. Add it to CI exactly like this:

```yaml
- run: pip install nlsc
- run: nlsc ci src/shipping.nl --compile --test
```

## Where to go next

- **Change something and watch the tooling catch it**: delete the `ELSE 0 ->
  surcharge` arm and run `nlsc verify --strict` — the total-branch rule fires
  with a precise line. Change a guard message and run `nlsc diff
  src/shipping.nl` — the lockfile knows the semantics changed.
- **Let an LLM work on it**: hand it `nlsc ir --json` output instead of the
  source; the IR is the smallest complete description of what the program
  means, with every construct explicit.
- [Language specification](language-spec.md) — the full surface syntax
- [IR specification](ir-spec.md) — the interchange format
- [CLI reference](cli-reference.md) — every command and flag
- [Error reference](error-reference.md) — what each code means and how to fix it
