"""Core parsing and comparison logic for envdiff."""
from __future__ import annotations
from pathlib import Path
from typing import Dict, List


def parse_env(path):
    """Parse a .env file into a dict of metadata.

    Returns a dict with keys: path, keys (list in file order), values (dict),
    duplicates (list), empties (list).
    """
    keys = []
    values = {}
    duplicates = []
    empties = []
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip()
            if (len(val) >= 2 and val[0] == val[-1]
                    and val[0] in ('"', "'")):
                val = val[1:-1]
            if key in values:
                duplicates.append(key)
            values[key] = val
            keys.append(key)
            if val == "":
                empties.append(key)
    return {
        "path": str(path),
        "keys": keys,
        "values": values,
        "duplicates": duplicates,
        "empties": empties,
    }


def discover(directory):
    """Return sorted list of .env* files in a directory."""
    d = Path(directory)
    return sorted(p for p in d.iterdir()
                  if p.is_file() and p.name.startswith(".env"))


def compare(parsed):
    """Compare a list of parsed env files and return a report dict."""
    all_keys = sorted(set().union(*(set(p["keys"]) for p in parsed)))
    report = {
        "files": [p["path"] for p in parsed],
        "missing": {},
        "only": {},
        "empty": {},
        "dups": {},
    }
    for i, p in enumerate(parsed):
        others = set()
        for j, q in enumerate(parsed):
            if i != j:
                others |= set(q["keys"])
        missing = sorted(others - set(p["keys"]))
        if missing:
            report["missing"][p["path"]] = missing
        if p["duplicates"]:
            report["dups"][p["path"]] = list(p["duplicates"])
        if p["empties"]:
            report["empty"][p["path"]] = list(p["empties"])
    for key in all_keys:
        present = [p["path"] for p in parsed if key in p["values"]]
        if len(present) == 1 and len(parsed) > 1:
            report["only"].setdefault(present[0], []).append(key)
    for f in report["only"]:
        report["only"][f].sort()
    return report, all_keys
