"""Performance regression budgets (Issue #151).

Generous ceilings that catch order-of-magnitude regressions (the class of
bug that made a 2000-ANLU compile take 470 seconds) without flaking on
slow CI runners.  Current timings are roughly 10-100x under each budget;
see docs/performance.md for measured numbers and methodology.
"""

from __future__ import annotations

import time

from nlsc.lowering import lower_module
from nlsc.parser import parse_nl_file
from nlsc.resolver import resolve_dependencies
from nlsc.typecheck import check_module


def _generate(num_anlus: int) -> str:
    lines = ["@module bench", "@target python", ""]
    for i in range(num_anlus):
        lines.extend(
            [
                f"[op-{i}]",
                f"PURPOSE: Operation {i}",
                "INPUTS:",
                "  - a: number",
                "  - b: number",
                "LOGIC:",
                "  1. total = a + b",
                "RETURNS: total",
                "",
            ]
        )
    return "\n".join(lines)


def _seconds(fn) -> float:
    start = time.perf_counter()
    fn()
    return time.perf_counter() - start


def test_resolver_scales_past_500_anlus():
    # The regression guard for the quadratic topological sort: 500 ANLUs
    # at one point took minutes; anything superlinear trips this budget.
    nl_file = parse_nl_file(_generate(500), source_path="bench.nl")
    elapsed = _seconds(lambda: resolve_dependencies(nl_file))
    assert elapsed < 5.0, f"resolver took {elapsed:.1f}s for 500 ANLUs"


def test_lowering_200_anlus_within_budget():
    source = _generate(200)
    nl_file = parse_nl_file(source, source_path="bench.nl")
    elapsed = _seconds(lambda: lower_module(nl_file))
    assert elapsed < 10.0, f"lowering took {elapsed:.1f}s for 200 ANLUs"


def test_semantic_gate_200_anlus_within_budget():
    nl_file = parse_nl_file(_generate(200), source_path="bench.nl")
    elapsed = _seconds(lambda: check_module(nl_file, file_token="bench.nl"))
    assert elapsed < 15.0, f"checker took {elapsed:.1f}s for 200 ANLUs"


def test_cli_compile_200_anlus_within_budget(tmp_path):
    from nlsc.cli import main

    path = tmp_path / "bench.nl"
    path.write_text(_generate(200), encoding="utf-8")
    elapsed = _seconds(lambda: main(["compile", str(path)]))
    assert elapsed < 30.0, f"compile took {elapsed:.1f}s for 200 ANLUs"
