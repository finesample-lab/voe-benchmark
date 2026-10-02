from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import (
    DIMENSIONS,
    ValidationError,
    export_workset,
    load_cases,
    load_predictions,
    reference_predictions,
    score,
    template_predictions,
    write_jsonl,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="emb", description="Evidence Memory Benchmark")
    parser.add_argument("--corpus", type=Path, help="alternate domains directory")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate", help="validate all public cases")

    template = sub.add_parser("template", help="write an empty prediction file")
    template.add_argument("--output", type=Path)

    export = sub.add_parser("export", help="write cases without expected labels")
    export.add_argument("--output", type=Path)

    reference = sub.add_parser("reference", help="write scorer-verification predictions")
    reference.add_argument("--output", type=Path)

    scoring = sub.add_parser("score", help="score a prediction JSONL file")
    scoring.add_argument("predictions", type=Path)
    scoring.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        cases = load_cases(args.corpus)
        if args.command == "validate":
            domains = sorted({case["domain"] for case in cases})
            print(f"valid: {len(cases)} cases across {len(domains)} domains ({', '.join(domains)})")
            return 0
        if args.command == "template":
            write_jsonl(template_predictions(cases), args.output)
            return 0
        if args.command == "export":
            write_jsonl(export_workset(cases), args.output)
            return 0
        if args.command == "reference":
            write_jsonl(reference_predictions(cases), args.output)
            return 0
        if args.command == "score":
            report = score(cases, load_predictions(args.predictions))
            if args.as_json:
                print(json.dumps(report, indent=2, sort_keys=True))
            else:
                print(f"Evidence Memory Benchmark: {report['overall'] * 100:.1f}/100")
                for dimension in DIMENSIONS:
                    value = report["dimensions"][dimension]
                    floor = report["floors"][dimension]
                    mark = "PASS" if report["floors_met"][dimension] else "FAIL"
                    print(f"  {dimension:10s} {value:0.3f}  floor {floor:0.2f}  {mark}")
                if report["critical_failures"]:
                    print("Critical failures:")
                    for failure in report["critical_failures"]:
                        print(f"  - {failure}")
                print("release gate: " + ("PASS" if report["passed"] else "FAIL"))
            return 0 if report["passed"] else 1
    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 2
