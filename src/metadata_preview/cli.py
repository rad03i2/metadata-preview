from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .core import inspect_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="metadata-preview",
        description="Inspect local file metadata without modifying the source file.",
    )
    parser.add_argument("paths", nargs="*", type=Path, help="Files to inspect")
    parser.add_argument("--hash", action="store_true", help="Include a streaming SHA-256 digest")
    parser.add_argument("--output", type=Path, help="Write the JSON report to this file")
    parser.add_argument("--version", action="version", version=f"metadata-preview {__version__} — Radwan Abdulhadi Ahmed / @rad03i2")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.paths:
        print("error: provide at least one file path", file=sys.stderr)
        return 2

    reports = []
    failed = False
    for path in args.paths:
        try:
            reports.append(inspect_file(path, include_hash=args.hash))
        except (OSError, ValueError) as exc:
            failed = True
            reports.append({"path": str(path), "error": str(exc)})

    payload = {"schema_version": 1, "files": reports}
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered + "\n", encoding="utf-8")
        except OSError as exc:
            print(f"error: cannot write report: {exc}", file=sys.stderr)
            return 2
    else:
        print(rendered)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
