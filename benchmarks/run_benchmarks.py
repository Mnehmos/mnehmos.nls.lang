#!/usr/bin/env python3
"""NLS pipeline benchmarks (Issue #151).

Measures each stage of the compiler on synthetic files of increasing size
and on the repository's largest real example, then prints a markdown table
(``--json`` for machine-readable output).  Run from the repository root:

    python benchmarks/run_benchmarks.py
    python benchmarks/run_benchmarks.py --json > results.json

Numbers are wall-clock medians of repeated runs on the current machine;
compare within a machine, not across them.  See docs/performance.md for
documented results, limits, and known bottlenecks.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from nlsc.emitter import emit_python  # noqa: E402
from nlsc.emitter_typescript import emit_typescript  # noqa: E402
from nlsc.ir import module_to_canonical  # noqa: E402
from nlsc.lowering import lower_module  # noqa: E402
from nlsc.parser import parse_nl_file  # noqa: E402
from nlsc.typecheck import check_module  # noqa: E402


def generate_nl_source(num_anlus: int) -> str:
    """A synthetic module with arithmetic, guards, and calls."""
    lines = ["@module benchmark", "@version 1.0.0", "@target python", ""]
    for i in range(num_anlus):
        lines.extend(
            [
                f"[op-{i}]",
                f"PURPOSE: Operation {i}",
                "INPUTS:",
                "  - a: number",
                "  - b: number",
                "GUARDS:",
                '  - a >= 0 -> ValueError("a must be non-negative")',
                "LOGIC:",
                "  1. total = a + b",
                f"  2. IF a > b THEN total * 2 -> scaled ELSE total + 1 -> scaled",
                "RETURNS: scaled",
                "",
            ]
        )
    return "\n".join(lines)


def _median_seconds(fn, repeats: int) -> float:
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        samples.append(time.perf_counter() - start)
    return statistics.median(samples)


def benchmark_source(label: str, source: str, repeats: int, results: list) -> None:
    nl_file = parse_nl_file(source, source_path=f"{label}.nl")
    operation_count = len(nl_file.anlus)

    stages = {
        "parse+lower": lambda: lower_module(
            parse_nl_file(source, source_path=f"{label}.nl")
        ),
        "semantic gate": lambda: check_module(
            parse_nl_file(source, source_path=f"{label}.nl"),
            file_token=f"{label}.nl",
        ),
        "emit python": lambda: emit_python(nl_file),
        "emit typescript": lambda: emit_typescript(nl_file),
        "canonical IR": lambda: module_to_canonical(lower_module(nl_file)),
    }
    for stage, fn in stages.items():
        seconds = _median_seconds(fn, repeats)
        results.append(
            {
                "source": label,
                "anlus": operation_count,
                "stage": stage,
                "median_seconds": round(seconds, 4),
            }
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--repeats", type=int, default=5, help="runs per stage")
    args = parser.parse_args()

    results: list[dict] = []
    sizes = (10, 50, 200)
    for size in sizes:
        benchmark_source(f"synthetic-{size}", generate_nl_source(size), args.repeats, results)

    real_example = ROOT / "examples" / "workflow_engine.nl"
    if real_example.exists():
        benchmark_source(
            "workflow_engine", real_example.read_text(encoding="utf-8"), args.repeats, results
        )

    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    print("| Source | ANLUs | Stage | Median (s) |")
    print("| --- | --- | --- | --- |")
    for row in results:
        print(
            f"| {row['source']} | {row['anlus']} | {row['stage']} | "
            f"{row['median_seconds']:.4f} |"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
