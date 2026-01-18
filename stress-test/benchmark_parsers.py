#!/usr/bin/env python3
"""
Parser Performance Benchmark

Compares regex and tree-sitter parser performance on various input sizes.
Run with: python stress-test/benchmark_parsers.py
"""

import time
import statistics
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from nlsc.parser import parse_nl_file


def generate_nl_source(num_anlus: int) -> str:
    """Generate a .nl file with specified number of ANLUs."""
    lines = [
        "@module benchmark",
        "@version 1.0.0",
        "@target python",
        "",
    ]

    for i in range(num_anlus):
        lines.extend([
            f"[function-{i}]",
            f"PURPOSE: Benchmark function number {i}",
            "INPUTS:",
            f"  - a{i}: number",
            f"  - b{i}: number",
            "GUARDS:",
            f"  - a{i} >= 0 -> ValueError(\"a must be non-negative\")",
            "LOGIC:",
            f"  1. Calculate sum -> result",
            f"  2. Apply multiplier -> final",
            f"RETURNS: a{i} + b{i}",
            "",
        ])

    return "\n".join(lines)


def benchmark_parser(parser_name: str, source: str, iterations: int = 5) -> dict:
    """Benchmark a parser on given source."""
    times = []

    for _ in range(iterations):
        start = time.perf_counter()
        try:
            nl_file = parse_nl_file(source, source_path="benchmark.nl")
            anlu_count = len(nl_file.anlus)
        except Exception as e:
            return {"error": str(e)}
        end = time.perf_counter()
        times.append(end - start)

    return {
        "parser": parser_name,
        "anlu_count": anlu_count,
        "iterations": iterations,
        "mean_ms": statistics.mean(times) * 1000,
        "min_ms": min(times) * 1000,
        "max_ms": max(times) * 1000,
        "stdev_ms": statistics.stdev(times) * 1000 if len(times) > 1 else 0,
    }


def try_treesitter_parser(source: str, iterations: int = 5) -> dict:
    """Try to benchmark tree-sitter parser."""
    try:
        from nlsc.parser_treesitter import parse_nl_file_treesitter, is_available

        if not is_available():
            return {"error": "tree-sitter not available"}

        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            nl_file = parse_nl_file_treesitter(source, source_path="benchmark.nl")
            anlu_count = len(nl_file.anlus)
            end = time.perf_counter()
            times.append(end - start)

        return {
            "parser": "treesitter",
            "anlu_count": anlu_count,
            "iterations": iterations,
            "mean_ms": statistics.mean(times) * 1000,
            "min_ms": min(times) * 1000,
            "max_ms": max(times) * 1000,
            "stdev_ms": statistics.stdev(times) * 1000 if len(times) > 1 else 0,
        }
    except ImportError as e:
        return {"error": f"tree-sitter import failed: {e}"}


def format_result(result: dict) -> str:
    """Format benchmark result for display."""
    if "error" in result:
        return f"  {result.get('parser', 'unknown')}: ERROR - {result['error']}"

    return (
        f"  {result['parser']:12s}: "
        f"mean={result['mean_ms']:7.2f}ms, "
        f"min={result['min_ms']:7.2f}ms, "
        f"max={result['max_ms']:7.2f}ms, "
        f"stdev={result['stdev_ms']:6.2f}ms"
    )


def main():
    print("=" * 60)
    print("NLS Parser Performance Benchmark")
    print("=" * 60)
    print()

    # Test with different sizes
    sizes = [10, 50, 100, 200]

    results = []

    for num_anlus in sizes:
        print(f"Benchmarking with {num_anlus} ANLUs...")
        source = generate_nl_source(num_anlus)
        source_size_kb = len(source.encode()) / 1024

        print(f"  Source size: {source_size_kb:.1f} KB")

        # Benchmark regex parser
        regex_result = benchmark_parser("regex", source)
        print(format_result(regex_result))

        # Benchmark tree-sitter parser
        ts_result = try_treesitter_parser(source)
        print(format_result(ts_result))

        # Calculate speedup if both worked
        if "error" not in regex_result and "error" not in ts_result:
            speedup = regex_result["mean_ms"] / ts_result["mean_ms"]
            print(f"  Speedup (ts vs regex): {speedup:.2f}x")

        results.append({
            "num_anlus": num_anlus,
            "source_kb": source_size_kb,
            "regex": regex_result,
            "treesitter": ts_result,
        })
        print()

    # Summary table
    print("=" * 60)
    print("Summary (mean parse time in ms)")
    print("=" * 60)
    print(f"{'ANLUs':>6s} {'Size(KB)':>8s} {'Regex':>10s} {'TreeSitter':>12s} {'Speedup':>8s}")
    print("-" * 50)

    for r in results:
        regex_ms = r["regex"].get("mean_ms", "N/A")
        ts_ms = r["treesitter"].get("mean_ms", "N/A")

        regex_str = f"{regex_ms:.2f}" if isinstance(regex_ms, float) else "ERROR"
        ts_str = f"{ts_ms:.2f}" if isinstance(ts_ms, float) else "ERROR"

        if isinstance(regex_ms, float) and isinstance(ts_ms, float):
            speedup = f"{regex_ms / ts_ms:.2f}x"
        else:
            speedup = "N/A"

        print(f"{r['num_anlus']:>6d} {r['source_kb']:>8.1f} {regex_str:>10s} {ts_str:>12s} {speedup:>8s}")

    print()
    print("Benchmark complete.")


if __name__ == "__main__":
    main()
