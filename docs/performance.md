# Performance

What to expect from the compiler, how to measure it yourself, and the
known limits and bottlenecks. Everything here is measured, not estimated.

## Methodology

```bash
python benchmarks/run_benchmarks.py            # markdown table
python benchmarks/run_benchmarks.py --json     # machine-readable
```

Each stage runs repeatedly and the reported number is the **median**
wall-clock time in-process, with the module parsed fresh per run. The
table below was measured on a Windows machine (Python 3.12, tree-sitter
parser) — compare numbers within a machine, never across them. CI runs
the same script and uploads the JSON results as an artifact so trends are
visible over time, and `tests/test_performance_budgets.py` fails the
build on order-of-magnitude regressions.

## Measured throughput

Synthetic modules of arithmetic operations with guards and branch steps:

| ANLUs | parse + lower | semantic gate | emit Python | emit TypeScript | canonical IR |
| --- | --- | --- | --- | --- | --- |
| 10 | 5.6 ms | 5.5 ms | 3.7 ms | 2.5 ms | 2.2 ms |
| 50 | 23 ms | 27 ms | 20 ms | 15 ms | 12 ms |
| 200 | 99 ms | 136 ms | 87 ms | 66 ms | 55 ms |
| 2000 | ~1.0 s | ~1.3 s | ~0.9 s | ~0.7 s | ~0.6 s |

Scaling is linear in file size. The repository's largest real example
(`examples/workflow_engine.nl`, 67 ANLUs, heavy prose and foreign
expressions) lowers in **36 ms** and passes the full semantic gate in
**39 ms**.

User-visible CLI wall times (include interpreter startup):

| Command | File | Wall time |
| --- | --- | --- |
| `nlsc verify` | workflow_engine.nl (67 ANLUs) | ~0.39 s |
| `nlsc compile` | workflow_engine.nl | ~0.48 s |
| `nlsc compile` | synthetic 2000 ANLUs | ~4 s |

Rough rule of thumb: **compile time ≈ 1 ms per ANLU plus ~0.25 s of
interpreter startup**, so even very large generated modules (thousands of
ANLUs) compile in seconds.

## Limits and what happens at them

| Limit | Behavior when exceeded |
| --- | --- |
| File size / ANLU count | No hard limit; linear scaling. A 2000-ANLU module compiles in ~4 s. |
| Recursion depth | Python's default (~1000 frames) applies to generated code. `nlsc run` reports a source-mapped `RecursionError` and exits 1 — a diagnostic, not a crash. |
| `@use` / `@imports` count | No hard limit; resolution is linear over search roots. |
| Duplicate LOGIC step numbers | Rejected at parse time with both source lines (`EPARSE001`) — never silently merged. |
| Duplicate or colliding identifiers | Rejected (`ESEM007`) before emission. |
| Untrusted input resources | Analysis is CPU/memory-bound but never executes file content; use `nlsc run --sandbox` with `--timeout` (see [security model](security.md)). |

## Known bottlenecks (and their fixes)

- **Quadratic dependency resolution** — *fixed*. The topological sort
  rescanned every ANLU per node with dataclass equality in list
  membership; a 2000-ANLU compile took **470 s**. It now builds reverse
  edges once: the same compile takes **4 s**, and 1000 ANLUs run in
  2.5 s (linear).
- **Per-ANLU module re-lowering in lockfile hashing** — *fixed*. Semantic
  hashes lowered the whole module once per ANLU (O(n²)); `hash_anlus()`
  lowers once per file and all lock/diff/verify/rebuild consumers use it.
- **Per-ANLU function extraction from emitted code** — *fixed*. Lockfile
  generation ran a DOTALL regex over the entire output per ANLU;
  `extract_all_function_code()` scans once.

Remaining costs to know about:

- **The module is lowered twice per compile** (once for the semantic
  gate, once for lockfile hashes). Both are linear; caching a single
  lowering would roughly halve the non-startup cost of `compile`.
- **`nlsc ci --compile` with the tsc fallback** (Node without native type
  stripping) shells out to `tsc` once per run — allow a few seconds.
  CI uses Node 22 native stripping.
- **TypeScript emission of large `foreign` expressions** relies on the
  legacy translator; deep nesting there is regex-bound rather than IR-bound.

## Improving performance

The dominant startup cost in every CLI invocation is Python interpreter
startup (~250 ms); for repeated CI checks, prefer running several files
per process (`nlsc ci` per file is cheap relative to startup). If you hit
a genuine slowdown, reproduce it with `benchmarks/run_benchmarks.py`
before and after and include both tables in the issue.
