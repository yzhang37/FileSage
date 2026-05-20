from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from . import __version__
from .core import PlanItem, build_plan


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "plan":
        return run_plan(args)

    parser.print_help()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="filesage",
        description="Generate evidence-driven, risk-aware file organization plans.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command")
    plan = subparsers.add_parser("plan", help="Preview how files would be organized.")
    plan.add_argument("folder", type=Path, help="Folder to scan.")
    plan.add_argument("-r", "--recursive", action="store_true", help="Scan subfolders.")
    plan.add_argument("--include-hidden", action="store_true", help="Include hidden files.")
    plan.add_argument("--json", action="store_true", help="Print JSON output.")

    return parser


def run_plan(args: argparse.Namespace) -> int:
    try:
        plan = build_plan(
            args.folder,
            recursive=args.recursive,
            include_hidden=args.include_hidden,
        )
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([item.as_dict() for item in plan], indent=2, ensure_ascii=False))
    else:
        print_plan(plan)

    return 0


def print_plan(plan: list[PlanItem]) -> None:
    if not plan:
        print("No files need organizing.")
        return

    for item in plan:
        print(f"{item.source} -> {item.destination}")
        print(f"  reason: {item.reason}")

