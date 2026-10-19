#!/usr/bin/env python3
"""envdiff: compare .env files and report key mismatches."""
import argparse
import sys
from pathlib import Path

from core import parse_env, discover, compare


def print_report(report, all_keys):
    files = report["files"]
    print(f"Comparing {len(files)} env files:")
    for f in files:
        print(f"  - {f}")
    print(f"Total unique keys: {len(all_keys)}\n")
    if report["missing"]:
        print("Missing keys (present in another file but not here):")
        for f, keys in report["missing"].items():
            print(f"  {f}:")
            for k in keys:
                print(f"    - {k}")
        print()
    if report["only"]:
        print("Keys present in only one file:")
        for f, keys in report["only"].items():
            print(f"  {f}: {', '.join(keys)}")
        print()
    if report["empty"]:
        print("Empty values:")
        for f, keys in report["empty"].items():
            print(f"  {f}: {', '.join(keys)}")
        print()
    if report["dups"]:
        print("Duplicate keys:")
        for f, keys in report["dups"].items():
            print(f"  {f}: {', '.join(keys)}")
        print()
    if not any(report[k] for k in ("missing", "only", "empty", "dups")):
        print("All env files are in parity. No issues found.")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compare .env files for key parity.")
    ap.add_argument("files", nargs="*", help=".env files to compare")
    ap.add_argument("--dir", default=".", help="directory to scan for .env files")
    args = ap.parse_args(argv)
    if args.files:
        files = [Path(f) for f in args.files]
    else:
        files = discover(args.dir)
    if len(files) < 2:
        print("Need at least two .env files to compare.", file=sys.stderr)
        return 1
    for f in files:
        if not f.exists():
            print(f"File not found: {f}", file=sys.stderr)
            return 1
    parsed = [parse_env(f) for f in files]
    report, all_keys = compare(parsed)
    print_report(report, all_keys)
    has_issues = any(report[k] for k in ("missing", "only", "empty", "dups"))
    return 1 if has_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
