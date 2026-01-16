# NLS Project Knowledge

## What is NLS?

Natural Language Source (NLS) is a programming language where source code is written in plain English. The `nlsc` compiler translates `.nl` files to executable Python.

## Core Concepts

- **ANLU (Atomic Natural Language Unit)** — A single function spec with PURPOSE, INPUTS, LOGIC, RETURNS
- **Lockfile** — Captures generated code hashes for reproducible builds
- **Mock Emitter** — Handles simple expressions; LLM emitter planned for complex logic

## Architecture

```
.nl file → Parser → Resolver → Emitter → .py file
                                  ↓
                             .nl.lock
```

## Key Files

| File               | Purpose                   |
| ------------------ | ------------------------- |
| `nlsc/parser.py`   | Regex-based .nl parser    |
| `nlsc/emitter.py`  | ANLU → Python translation |
| `nlsc/lockfile.py` | Determinism guarantees    |
| `nl-schema.yaml`   | Formal ANLU grammar       |

## Status

Phase 1 MVP complete. Next: LLM emitter with lockfile caching.
