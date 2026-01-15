# Natural Language Source (NLS)
## Product Requirements Document v0.1

**Author:** Vario (Mnehmos)  
**Date:** January 15, 2026  
**Status:** Vision / Pre-Development

---

## Executive Summary

Natural Language Source (NLS) creates an auditable intermediate layer between human intent and executable code. Humans converse naturally with AI (exactly as they already do). The AI generates `.nl` specification files as a canonical audit trail—readable by anyone who understands English. These specs then compile to executable code.

**The Thesis:** The conversation IS the programming. The `.nl` file is the receipt. The code is the artifact.

**Key Insight:** Humans don't learn new syntax. They keep talking. The AI handles the translation to auditable specs. Non-programmers can now review, approve, and understand codebases.

---

## Problem Statement

### Current State
1. **No audit trail**: AI-assisted coding leaves no canonical record of intent
2. **Code is opaque**: Non-programmers can't review what systems actually do
3. **Compliance gap**: Regulators can't audit AI-generated code decisions
4. **Knowledge loss**: Intent lives in Slack threads, chat logs, and disappears
5. **Handoff friction**: New developers reverse-engineer intent from implementation

### The Gap
AI can now:
- Generate code from conversation (proven—we do this daily)
- Explain code in natural language (proven)
- Maintain semantic consistency (emerging)

But there's no **canonical intermediate artifact**. The conversation disappears. The code is opaque. Intent is lost.

**What if every AI coding session produced a human-readable specification as a side effect?**

---

## Vision

### The Flow

```
TODAY:
Human ←→ AI Chat → Code → Execution
              ↓
         [Conversation vanishes]

NLS:
Human ←→ AI Chat → .nl spec (audit trail) → Code → Execution
              ↓              ↓
         [Same UX]    [Permanent record]
```

### What Each Stakeholder Experiences

**Developer (same as today):**
```
You: "Add rate limiting to the API. 100 requests per minute per user,
     with a 429 response when exceeded."

AI: "I'll add rate limiting middleware. Here's what I'm implementing..."
    [Generates code AND writes to api.nl]
```

**Manager/Auditor (new capability):**
```
Opens: src/api.nl

Sees:
┌─────────────────────────────────────────────────────────────┐
│ [rate-limit-middleware]                                      │
│                                                              │
│ PURPOSE: Prevent API abuse by limiting request frequency     │
│                                                              │
│ POLICY:                                                      │
│   • Maximum 100 requests per minute per authenticated user   │
│   • Identified by user ID from JWT token                     │
│   • Sliding window algorithm                                 │
│                                                              │
│ BEHAVIOR:                                                    │
│   • Under limit → pass request through                       │
│   • At limit → return 429 Too Many Requests                  │
│   • Include Retry-After header with seconds until reset      │
│                                                              │
│ CREATED: 2026-01-15 via conversation                        │
│ APPROVED: [pending]                                          │
└─────────────────────────────────────────────────────────────┘

Thinks: "I understand exactly what this does. Approved."
```

**New Developer (onboarding):**
```
$ ls src/*.nl
api.nl          # API endpoints and middleware
auth.nl         # Authentication logic  
billing.nl      # Payment processing
notifications.nl # Email/SMS sending

$ cat src/auth.nl
# Reads plain English, understands system in 10 minutes
```

### The Project Structure

```
project/
├── src/
│   ├── auth.nl          ← AI-generated audit trail (human-readable)
│   ├── auth.py          ← AI-generated code (machine-executable)
│   └── auth.nl.lock     ← Determinism guarantee
├── conversations/
│   └── 2026-01-15.json  ← Optional: raw chat logs
├── tests/
│   └── auth.test.nl     ← Test specs in NL
└── nl.config.yaml       ← Compiler settings
```

---

## Key Distinction: Conversation vs Specification

**This is critical:** Humans never write `.nl` files directly.

| What Users Do | What They DON'T Do |
|---------------|---------------------|
| Chat naturally: "Add auth middleware" | Learn ANLU syntax |
| Review generated specs | Write formal specifications |
| Approve changes in plain English | Edit structured formats |
| Ask questions: "Why does this work?" | Debug compilation errors |

**The `.nl` file serves three audiences:**

1. **Auditors/Compliance**: Can read and verify what code does
2. **Managers**: Can review and approve without programming knowledge  
3. **Future Developers**: Can understand intent without reverse-engineering

**The conversation is the interface. The `.nl` is the receipt.**

---

## Core Concepts

### 1. Atomic Natural Language Units (ANLUs)

The fundamental building block—**generated by AI from conversation**, not written by humans.

Each ANLU is:
- **Self-contained**: Describes one logical operation
- **Composable**: Can reference other ANLUs
- **Deterministic**: Same ANLU + same compiler = same output
- **Auditable**: Any English speaker can understand what it does
- **Bidirectional**: Can be derived from existing code OR conversation

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

**Deliverable:** Conversational IDE + audit viewer for NLS development

**Primary Interface: Chat Panel**

The conversation IS the IDE. The extension provides:

| Feature | Description |
|---------|-------------|
| Integrated chat | Converse with AI directly in VS Code |
| Context awareness | AI sees open files, project structure |
| Live .nl generation | Watch specs appear as you talk |
| Approval workflow | "Accept" / "Reject" / "Modify" generated specs |
| History panel | Scroll through conversation → spec evolution |

**Secondary Interface: Spec Viewer**

| Feature | Description |
|---------|-------------|
| Syntax highlighting | Read .nl files with clear formatting |
| Split view | Spec left, generated code right |
| Diff view | See what changed between versions |
| Dependency graph | Visualize ANLU relationships |
| Code lens | "Show Python" / "Run Tests" quick actions |

**Views:**

1. **Chat View (primary):** Conversation interface—where work happens
2. **Spec View:** Read-only .nl viewer for audit/review
3. **Code View:** Generated code (read-only)
4. **History View:** Timeline of conversation → spec → code

**Workflow:**
```
Converse → AI generates .nl → Review spec → Approve → Code updates
              ↓                    ↓
         [Live preview]      [Reject? Continue talking]
```

**Success Criteria:**
- Conversation feels native, not bolted on
- Non-programmers can read and approve specs
- Zero .nl editing required (chat only)

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
- 1,000 conversational sessions generating .nl files in first 6 months
- 100 GitHub repos with .nl audit trails
- 10 organizations using .nl for compliance/audit

### Developer Experience
- Zero syntax learning required (conversation only)
- < 2 second spec generation from conversation
- 95% of generated specs accepted without modification

### Audit Value
- Non-programmers can accurately describe system behavior from .nl files
- Compliance reviews 5x faster with .nl vs code review
- New developer onboarding time reduced 50%

### Quality
- 95% of compiled code passes original tests
- < 1% of ANLUs require `@literal` escape
- Round-trip (code → .nl → code) preserves behavior

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
