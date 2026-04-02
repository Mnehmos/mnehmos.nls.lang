"""Run Python -> NLS -> Python roundtrip analysis on a repository."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from nlsc.roundtrip import roundtrip_python_repository


def _serialize_report(report) -> dict:
    return {
        "repo_root": report.repo_root,
        "output_root": report.output_root,
        "total_files": report.total_files,
        "succeeded_files": report.succeeded_files,
        "failed_files": report.failed_files,
        "file_results": [
            {
                "source_name": result.source_name,
                "success": result.success,
                "all_match": result.all_match,
                "stage": result.stage,
                "errors": result.errors,
            }
            for result in report.file_results
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Atomize a Python repository, regenerate Python, and record failures."
    )
    parser.add_argument("repo_root", help="Path to the source Python repository")
    parser.add_argument(
        "output_root", help="Path to write mirrored .nl and roundtrip .py artifacts"
    )
    parser.add_argument(
        "--max-files",
        type=int,
        help="Optional cap on the number of Python files to analyze",
    )
    parser.add_argument(
        "--report",
        default="roundtrip-report.json",
        help="Filename for the JSON summary written under output_root",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    report = roundtrip_python_repository(
        repo_root,
        output_root,
        max_files=args.max_files,
    )

    report_path = output_root / args.report
    report_path.write_text(
        json.dumps(_serialize_report(report), indent=2),
        encoding="utf-8",
    )

    print(f"Analyzed {report.total_files} file(s)")
    print(f"  Successful roundtrips: {report.succeeded_files}")
    print(f"  Failed roundtrips: {report.failed_files}")
    print(f"  Report: {report_path}")
    return 0 if report.failed_files == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
