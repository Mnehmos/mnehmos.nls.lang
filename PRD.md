# Natural Language Source (NLS)

**Product Requirements Document — v2**

Author: Vario (Mnehmos)
Status: Alpha (0.1.0)

---

## 1. The Problem

Code is opaque to most stakeholders who need to understand it.

- Managers approve features they can't audit
- Compliance reviews code they can't read
- Vibe coders ship logic they can't explain
- Junior devs inherit systems they can't parse

Documentation drifts. Comments lie. The only truth is the code—and most people can't read it.

**NLS makes code logic readable by anyone who can read English.**

---

## 2. The Solution

NLS introduces a **specification layer** between intent and execution:

```
Human intent → .nl specification → Compiled code
                      ↑
               Auditable artifact
               Version controlled
               Machine-parseable
               Human-readable
```

The `.nl` file is structured English that compiles deterministically to code. It's not documentation—it's source.

**Bidirectional flow:**

```
.nl spec  ──compile──▶  Python/TypeScript/Rust
    ▲                           │
    └────────atomize────────────┘
```

Existing codebases can be atomized into `.nl` specs. New specs compile to code. The specification is the contract.

---

## 3. Core Invariant

> **No LLM participates in compilation.**

AI may help humans *write* specifications. AI never decides what *runs*.

This separation is non-negotiable:

| Layer | Role | Determinism |
|-------|------|-------------|
| Cognition | AI helps articulate intent, clean specs, extract from legacy | Probabilistic |
| Specification | `.nl` files—the auditable artifact | Frozen |
| Execution | Parser → Resolver → Emitter → Code | 100% deterministic |

The spec is the checkpoint. Everything before it is conversation. Everything after it is mechanical.

---

## 4. The ANLU (Atomic Natural Language Unit)

An ANLU is a single function described in structured English:

```
ANLU calculate-tax:
  PURPOSE: Compute tax owed based on income and filing status

  INPUTS:
    - income: number (gross annual income in USD)
    - filing_status: string (one of: single, married, head_of_household)

  GUARDS:
    - income >= 0 → "Income cannot be negative"
    - filing_status in [single, married, head_of_household] → "Invalid filing status"

  LOGIC:
    1. Look up tax brackets for filing_status
    2. Calculate marginal tax for each bracket
    3. Sum bracket amounts to get total_tax
    4. Compute effective_rate as total_tax / income

  RETURNS: TaxResult with total_tax, effective_rate

  EDGE CASES:
    - income = 0 → return TaxResult(0, 0)
```

**What this gives you:**

- A manager can read the guards and know what validation exists
- An auditor can trace the logic steps without reading Python
- A vibe coder can verify their intent was captured correctly
- The compiler guarantees this exact logic executes

---

## 5. Architecture

### Layer 1: Parser

Reads `.nl` files, extracts structure into an AST.

- Current: regex-based (sufficient for MVP)
- Future: formal grammar (tree-sitter or PEG)

The parser doesn't interpret meaning. It extracts structure.

### Layer 2: Resolver

Builds dependency graph between ANLUs. Detects:
- Missing references
- Circular dependencies
- Compilation order

Standard compiler infrastructure.

### Layer 3: Emitter

Translates AST → target language. Rule-based, deterministic.

For a given `.nl` + compiler version:
> Output is identical every time.

Current target: Python
Planned: TypeScript, Rust

### Layer 4: Lockfile

Every compilation produces a lockfile:

```yaml
module: billing
compiler: nlsc 0.1.0
timestamp: 2026-01-17T14:32:00Z
anlus:
  calculate-tax:
    source_hash: a7f3b2...
    output_hash: 9c2e1d...
targets:
  billing.py:
    hash: 4d8f2a...
    lines: 127
```

This proves: spec → code relationship is frozen and verifiable.

---

## 6. Use Cases

### Vibe Coder Audit

```
1. Developer builds feature with Claude
2. Run: nlsc atomize feature.py → feature.nl
3. Non-technical stakeholder reads feature.nl
4. Stakeholder approves or requests changes
5. Changes made to .nl, recompiled
```

### Legacy Code Onboarding

```
1. New dev joins team
2. Run: nlsc atomize billing.py → billing.nl
3. Dev reads English specs instead of deciphering Python
4. Specs become living documentation
```

### Compliance Review

```
1. Auditor requests logic for sensitive function
2. Provide .nl file + lockfile
3. Auditor verifies:
   - Guards exist for all edge cases
   - Logic matches stated requirements
   - Lockfile proves code matches spec
```

### AI-Assisted Spec Writing

```
1. Human describes intent in conversation
2. AI drafts .nl spec
3. Human reviews and edits spec
4. nlsc compile → deterministic code
5. AI never touched the compiler
```

---

## 7. What NLS Is Not

**Not AI code generation.** The AI helps write specs, not code. The compiler is deterministic.

**Not documentation.** Documentation describes code. NLS *is* code—in a human-readable form that compiles.

**Not a DSL.** Domain-specific languages have custom syntax. NLS uses structured English with a formal schema.

**Not literate programming.** Literate programming embeds docs in code. NLS inverts this: code is generated from specs.

---

## 8. Roadmap

### Phase 1: Foundation (Current)
- [x] ANLU schema definition
- [x] Regex parser
- [x] Dependency resolver
- [x] Python emitter
- [x] Lockfile generation
- [x] Atomizer (Python → .nl)
- [x] CLI: compile, verify, atomize, graph
- [x] Round-trip equivalence testing
- [ ] Formal grammar parser
- [ ] Complete lockfile verification

### Phase 2: Tooling
- [ ] VS Code extension (syntax highlighting, folding, error reporting)
- [ ] Graph visualization in editor
- [ ] Watch mode for incremental compilation

### Phase 3: Multi-Target
- [ ] TypeScript emitter
- [ ] Rust emitter
- [ ] Target-specific type mappings

### Phase 4: Ecosystem
- [ ] ANLU package registry
- [ ] Shared spec libraries
- [ ] Import resolution across packages

---

## 9. Success Criteria

NLS succeeds when:

1. **Readability**: A non-programmer can understand what a function does by reading its `.nl` spec
2. **Determinism**: Same `.nl` + same compiler version = identical output, always
3. **Round-trip fidelity**: `atomize(compile(spec)) ≈ spec` for well-formed inputs
4. **Adoption signal**: Developers choose to write `.nl` first, not atomize after

Quantitative targets:
- Parser handles 95%+ of well-formed specs without error
- Lockfile verification catches 100% of spec/code drift
- Atomizer extracts meaningful specs from 80%+ of simple functions

---

## 10. The Bet

NLS bets that:

> The bottleneck in AI-assisted development isn't code generation—it's **intent verification**.

Anyone can get an LLM to write code. The hard part is knowing if it wrote *the right* code.

NLS creates a checkpoint where humans can verify intent in their native language before code ever runs.

**AI writes specs. Compilers write code. Humans approve specs.**

That's the separation that makes AI-assisted development auditable.

---

*"Meaning for humans. Certainty for machines."*
