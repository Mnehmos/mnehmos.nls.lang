# Natural Language Source (NLS)
## Product Requirements Document v0.1

**Author:** Vario (Mnehmos)  
**Date:** January 15, 2026  
**Status:** Vision / Pre-Development

---

## Executive Summary

Natural Language Source (NLS) inverts the programming paradigm: instead of humans writing code that machines execute, humans write atomic natural language specifications that compile to code. The natural language IS the source code. Traditional programming languages become compilation targets.

**The Thesis:** We've spent 60 years teaching humans to speak machine. It's time to make machines speak human—and make that the canonical representation.

---

## Problem Statement

### Current State
1. **Cognitive overhead**: Developers context-switch between thinking in intent and expressing in syntax
2. **Language lock-in**: Business logic is imprisoned in implementation details
3. **AI assistance is additive**: Copilot/Claude generate code, but humans still read/maintain code
4. **Knowledge silos**: Non-programmers can't participate in codebases despite understanding the domain

### The Gap
AI can now:
- Generate code from natural language (proven)
- Explain code in natural language (proven)
- Maintain semantic consistency across regeneration (emerging)

But we still treat code as the source of truth. **What if we didn't?**

---

## Vision

### The Inversion

```
TODAY:
Human Intent → Code (source) → Execution
                 ↑
           [AI assists here]

NLS:
Human Intent → .nl file (source) → Code (artifact) → Execution
                 ↑                        ↑
           [Human works here]      [AI compiles here]
```

### What Developers Experience

**Opening a project:**
```
project/
├── src/
│   ├── auth.nl          ← Human reads/writes this
│   ├── auth.py          ← Generated, gitignored
│   └── auth.nl.lock     ← Determinism guarantee
├── tests/
│   └── auth.test.nl     ← Tests in NL too
└── nl.config.yaml       ← Compiler settings
```

**The editor view:**
```
┌─────────────────────────────────────────────────────────────┐
│ auth.nl                                              [NL View] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  @module authentication                                     │
│  @target python >= 3.11                                     │
│  @imports jwt, datetime                                     │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ [validate-token]                                     │   │
│  │                                                       │   │
│  │ PURPOSE: Verify JWT and extract user identity        │   │
│  │                                                       │   │
│  │ INPUTS:                                               │   │
│  │   • token: string, required                          │   │
│  │   • secret: string, from environment JWT_SECRET      │   │
│  │                                                       │   │
│  │ GUARDS:                                               │   │
│  │   • token must not be empty → AuthError("Missing")   │   │
│  │   • signature must be valid → AuthError("Invalid")   │   │
│  │   • expiry must be future → AuthError("Expired")     │   │
│  │                                                       │   │
│  │ RETURNS: User object with id, email, roles           │   │
│  │                                                       │   │
│  │ [▾ Show generated Python]                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Concepts

### 1. Atomic Natural Language Units (ANLUs)

The fundamental building block. Each ANLU is:
- **Self-contained**: Describes one logical operation
- **Composable**: Can reference other ANLUs
- **Deterministic**: Same ANLU + same compiler = same output
- **Bidirectional**: Can be derived from code OR written directly

```
[calculate-tax]                          ← Identifier
PURPOSE: Compute tax liability           ← Intent
INPUTS:                                  ← Contract
  • income: number, non-negative
  • brackets: list of TaxBracket
LOGIC:                                   ← Specification
  • Find applicable bracket for income
  • Apply marginal rates progressively
  • Sum contributions from each bracket
RETURNS: TaxResult with amount, effective_rate
EDGE CASES:                              ← Robustness
  • Zero income → zero tax
  • Income exceeds all brackets → use highest rate
```

### 2. The NL Schema

Formal grammar for ANLUs. Enables:
- Syntax highlighting and validation
- Schema-aware autocomplete
- Cross-reference checking
- Deterministic compilation

```yaml
# nl-schema.yaml
anlu:
  required:
    - identifier: kebab-case, unique within module
    - purpose: single sentence, imperative mood
    - returns: type specification
  optional:
    - inputs: list of typed parameters
    - guards: preconditions with error mappings
    - logic: ordered list of steps
    - edge_cases: explicit handling
    - depends: list of ANLU references
    - literal: escape hatch for exact code
```

### 3. The Compilation Model

```
┌──────────┐     ┌───────────┐     ┌──────────┐     ┌──────────┐
│  .nl     │────▶│  Parser   │────▶│   AST    │────▶│ Compiler │
│  files   │     │           │     │ (ANLU    │     │ (LLM +   │
│          │     │           │     │  graph)  │     │  rules)  │
└──────────┘     └───────────┘     └──────────┘     └──────────┘
                                                          │
                      ┌───────────────────────────────────┘
                      ▼
              ┌──────────────┐
              │   Targets    │
              ├──────────────┤
              │ • Python     │
              │ • TypeScript │
              │ • Rust       │
              │ • Go         │
              └──────────────┘
```

**Determinism guarantee:**
- Lock file stores: ANLU hash + compiler version + output hash
- Same inputs = same outputs, always
- Lock file enables reproducible builds without LLM calls

### 4. Bidirectional Sync

**Atomize (code → NL):**
```bash
$ nls atomize src/legacy.py
✓ Extracted 12 ANLUs
✓ Wrote src/legacy.nl
✓ Verified round-trip equivalence
```

**Compile (NL → code):**
```bash
$ nls compile src/auth.nl --target python
✓ Parsed 5 ANLUs
✓ Resolved dependencies
✓ Generated src/auth.py (127 lines)
✓ Updated src/auth.nl.lock
```

---

## Product Components

### Component 1: NLS Language Specification

**Deliverable:** Formal grammar + reference documentation

**Features:**
- Module declarations (`@module`, `@target`, `@imports`)
- ANLU syntax (identifier, purpose, inputs, guards, logic, returns)
- Type system (primitives, composites, generics, constraints)
- Composition operators (depends, extends, implements)
- Escape hatches (`@literal` blocks for exact code)
- Test specifications (`@test`, `@property`, `@invariant`)

**Success Criteria:**
- Grammar is parseable by tree-sitter
- Any valid ANLU compiles to working code
- Any working code atomizes to valid ANLUs

---

### Component 2: NLS Compiler (`nlsc`)

**Deliverable:** CLI tool for compilation and atomization

**Commands:**
```bash
nlsc init                    # Initialize NLS project
nlsc compile <file.nl>       # NL → code
nlsc atomize <file.py>       # Code → NL
nlsc verify <file.nl>        # Check without generating
nlsc diff <file.nl>          # Show changes since last compile
nlsc watch                   # Continuous compilation
nlsc test                    # Run NL test specifications
```

**Architecture:**
```
┌─────────────────────────────────────────────────────────┐
│                      nlsc                                │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ Parser  │  │Resolver │  │Compiler │  │ Emitter │   │
│  │         │  │         │  │         │  │         │   │
│  │ .nl →   │  │ Link    │  │ ANLU →  │  │ AST →   │   │
│  │ tokens  │  │ ANLUs   │  │ target  │  │ files   │   │
│  │ → AST   │  │         │  │ AST     │  │         │   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
│                     │                                    │
│              ┌──────┴──────┐                            │
│              │ LLM Backend │                            │
│              │ (pluggable) │                            │
│              └─────────────┘                            │
└─────────────────────────────────────────────────────────┘
```

**LLM Backend Options:**
- Local: Ollama, llama.cpp
- Cloud: Claude API, OpenAI API
- Hybrid: Local for simple ANLUs, cloud for complex

**Success Criteria:**
- Compile 1000 ANLUs in < 60 seconds (cached)
- Round-trip stability: atomize(compile(x)) ≈ x
- Lock file enables zero-LLM rebuilds

---

### Component 3: VS Code Extension

**Deliverable:** Full IDE experience for NLS development

**Features:**

| Feature | Description |
|---------|-------------|
| Syntax highlighting | Full grammar support for .nl files |
| Inline compilation | See generated code without leaving NL view |
| Error diagnostics | Schema violations, unresolved references |
| Autocomplete | ANLU templates, type suggestions, imports |
| Go to definition | Navigate ANLU dependencies |
| Hover documentation | Show ANLU details, generated signature |
| Code lens | "Compile" / "Test" / "Show Python" actions |
| Side-by-side view | NL left, generated code right |
| Diff view | Changes to NL → changes to generated code |
| Refactoring | Rename ANLU, extract ANLU, inline ANLU |

**Views:**

1. **NL View (default):** Shows .nl file with collapsible ANLUs
2. **Code View:** Shows generated code (read-only unless escaped)
3. **Split View:** NL on left, synced code on right
4. **Graph View:** Visualize ANLU dependency graph

**Workflow:**
```
Edit .nl → Auto-compile → Hot reload → See results
              ↓
        Error? Show diagnostic in NL view
              ↓
        Success? Update lock file
```

**Success Criteria:**
- < 500ms from edit to compiled output
- Zero context-switching required
- Non-programmers can read and modify ANLUs

---

### Component 4: Trace Integration (trace-mcp bridge)

**Deliverable:** Schema validation between NL specs and runtime

**Concept:**
```
.nl file (producer schema)
        ↓
   [nlsc compile]
        ↓
generated code (implementation)
        ↓
   [trace-mcp]
        ↓
consumer code (runtime usage)
```

**Features:**
- Validate that consumers use generated code correctly
- Detect schema drift between .nl spec and actual usage
- Generate consumer stubs from .nl specs
- Bi-directional contract comments

**Integration:**
```bash
# Validate entire pipeline
nlsc trace --producer src/api.nl --consumer client/
✓ 12 ANLUs validated
✓ 47 consumer call sites checked
⚠ 2 unused ANLUs detected
✗ 1 contract violation: client expects `userId`, spec provides `user_id`
```

---

## Technical Architecture

### File Format: `.nl`

```nl
# auth.nl - Authentication module

@module authentication
@version 1.0.0
@target python >= 3.11
@imports jwt, datetime, typing

@types {
  User: {
    id: string
    email: string  
    roles: list of string
  }
  
  AuthError: Error {
    code: "MISSING" | "INVALID" | "EXPIRED"
    message: string
  }
}

[validate-token]
PURPOSE: Verify JWT and extract user identity
INPUTS:
  • token: string, required, "The JWT to validate"
  • secret: string, from env JWT_SECRET
GUARDS:
  • token must not be empty → AuthError(MISSING, "Token required")
  • signature must match secret → AuthError(INVALID, "Bad signature")  
  • exp claim must be in future → AuthError(EXPIRED, "Token expired")
RETURNS: User
LOGIC:
  1. Decode token without verification to read header
  2. Verify signature using secret and algorithm from header
  3. Extract payload claims
  4. Construct User from sub, email, roles claims

[require-role]
PURPOSE: Middleware to enforce role-based access
INPUTS:
  • required_role: string
  • user: User, from request context
GUARDS:
  • user must exist → AuthError(MISSING, "Not authenticated")
  • required_role must be in user.roles → AuthError(INVALID, "Insufficient permissions")
RETURNS: void (passes through if valid)
DEPENDS: [validate-token]

@literal python {
  # Escape hatch for performance-critical or unusual code
  def _constant_time_compare(a: bytes, b: bytes) -> bool:
      return hmac.compare_digest(a, b)
}
```

### Lock File: `.nl.lock`

```yaml
# auth.nl.lock - DO NOT EDIT
# Generated by nlsc 0.1.0

schema_version: 1
generated_at: 2026-01-15T14:30:00Z
compiler_version: 0.1.0
llm_backend: claude-sonnet-4-20250514

modules:
  authentication:
    source_hash: sha256:a1b2c3...
    anlus:
      validate-token:
        source_hash: sha256:d4e5f6...
        output_hash: sha256:789abc...
        output_lines: 23
      require-role:
        source_hash: sha256:def012...
        output_hash: sha256:345678...
        output_lines: 12

targets:
  python:
    file: auth.py
    hash: sha256:fedcba...
    lines: 47
```

### Configuration: `nl.config.yaml`

```yaml
# nl.config.yaml

project:
  name: my-service
  version: 0.1.0

compiler:
  default_target: python
  llm_backend: claude  # or openai, ollama, local
  cache_strategy: aggressive  # none, normal, aggressive
  
targets:
  python:
    version: ">=3.11"
    style: black
    type_hints: strict
  typescript:
    version: ">=5.0"
    strict: true
    
atomizer:
  granularity: function  # function, class, module
  preserve_comments: true
  infer_types: true

validation:
  require_purpose: true
  require_guards: false
  max_anlu_complexity: 10  # lines of logic
```

---

## Development Roadmap

### Phase 1: Foundation (Weeks 1-4)

**Goal:** Prove the concept works

| Task | Deliverable |
|------|-------------|
| Define NL schema v0.1 | `nl-schema.yaml` |
| Build parser | Tree-sitter grammar |
| Build basic compiler | Python target only |
| Build basic atomizer | Python source only |
| Prove round-trip | 10 test cases pass |

**Exit Criteria:**
- Can write a .nl file, compile to Python, run it
- Can atomize Python file, get equivalent .nl
- Round-trip produces equivalent behavior

### Phase 2: VS Code Extension (Weeks 5-8)

**Goal:** Usable developer experience

| Task | Deliverable |
|------|-------------|
| Syntax highlighting | TextMate grammar |
| Basic diagnostics | Schema validation |
| Compile on save | Background nlsc |
| Inline code view | Code lens actions |
| Error navigation | Click-to-source |

**Exit Criteria:**
- Developer can write NL, see Python, run tests
- Errors in NL view, not in generated code
- < 1s compile latency

### Phase 3: Production Hardening (Weeks 9-12)

**Goal:** Reliable for real projects

| Task | Deliverable |
|------|-------------|
| Lock file implementation | Deterministic builds |
| TypeScript target | Second language |
| Test specifications | `@test` ANLUs |
| trace-mcp integration | Contract validation |
| CI/CD integration | GitHub Action |

**Exit Criteria:**
- Zero-LLM builds from lock file
- Multi-language project works
- Tests written in NL, executed in target

### Phase 4: Ecosystem (Weeks 13-16)

**Goal:** Community adoption

| Task | Deliverable |
|------|-------------|
| Rust target | Third language |
| LSP server | Editor-agnostic |
| Package registry | Share ANLUs |
| Documentation site | Tutorials, reference |
| Atomize popular libs | Bootstrap content |

**Exit Criteria:**
- Community contributions
- 3+ target languages
- 100+ public ANLUs in registry

---

## Success Metrics

### Adoption
- 1,000 .nl files created in first 6 months
- 100 GitHub repos using NLS
- 10 community-contributed target backends

### Developer Experience
- 80% of users prefer NL view to code view
- < 2 second average compile time
- < 5% round-trip semantic drift

### Quality
- 95% of compiled code passes original tests
- < 1% of ANLUs require `@literal` escape
- 90% of atomized code produces readable ANLUs

---

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| LLM inconsistency | Breaks determinism | Medium | Lock files, test suites, version pinning |
| Complex code can't atomize | Adoption blocked | Medium | `@literal` escape, granularity options |
| Performance overhead | DX suffers | Low | Aggressive caching, local LLMs |
| Schema too restrictive | Expressiveness limited | Medium | Iterative schema evolution, escape hatches |
| Existing tooling incompatible | Integration pain | Medium | Generate standard code, source maps |

---

## Open Questions

1. **Granularity:** Should ANLUs map to functions, classes, or logical operations?
2. **Types:** How much type inference vs explicit annotation?
3. **Side effects:** How to specify I/O, state mutation, async?
4. **Versioning:** How to handle ANLU API changes?
5. **Collaboration:** How do multiple developers edit the same .nl file?
6. **Debugging:** How to set breakpoints in NL view?
7. **Performance:** How to express optimization hints?

---

## Appendix A: Comparison to Existing Tools

| Tool | Approach | NLS Difference |
|------|----------|----------------|
| GitHub Copilot | AI suggests code inline | NLS: NL is the source, code is artifact |
| Cursor | AI-assisted code editing | NLS: Never edit code directly |
| GPT Engineer | NL → full project generation | NLS: Granular ANLUs, bidirectional |
| Devin | Autonomous coding agent | NLS: Human controls spec, AI compiles |
| Langchain/DSPy | Prompt programming | NLS: General purpose, not just LLM chains |

---

## Appendix B: Example Session

```bash
$ mkdir my-api && cd my-api
$ nlsc init
✓ Created nl.config.yaml
✓ Created src/
✓ Created tests/

$ cat > src/math.nl << 'EOF'
@module math
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  • a: number
  • b: number
RETURNS: a + b

[multiply]  
PURPOSE: Multiply two numbers
INPUTS:
  • a: number
  • b: number
RETURNS: a × b

@test [add] {
  add(2, 3) == 5
  add(-1, 1) == 0
  add(0, 0) == 0
}
EOF

$ nlsc compile src/math.nl
✓ Parsed 2 ANLUs, 1 test suite
✓ Generated src/math.py (18 lines)
✓ Generated tests/test_math.py (12 lines)
✓ Updated src/math.nl.lock

$ python -c "from src.math import add; print(add(2, 3))"
5

$ pytest tests/
===== 3 passed in 0.02s =====
```

---

## Appendix C: The Philosophy

> "The database is the intelligence. The agent is just hands."

NLS extends this: **The specification is the intelligence. The code is just hands.**

We've accepted that:
- SQL is better than hand-rolling B-trees
- React is better than hand-rolling DOM manipulation  
- Kubernetes is better than hand-rolling container orchestration

NLS proposes:
- Natural language is better than hand-rolling implementations

The abstraction ladder keeps climbing. We're just taking the next step.

---

*"I don't write code anymore. I write wishes. The computer grants them."*

---

**Document Version:** 0.1  
**Last Updated:** January 15, 2026  
**Next Review:** After Phase 1 completion
