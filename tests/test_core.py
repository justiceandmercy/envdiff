"""Tests for envdiff core."""
import tempfile
from pathlib import Path

from core import parse_env, discover, compare


def write(p, text):
    p.write_text(text)


def test_parse_env_basic():
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / ".env"
        write(f, "A=1\nB=\n# c\nC='x'\nD=\"y\"\nA=2\n")
        r = parse_env(f)
        assert r["keys"] == ["A", "B", "C", "D", "A"]
        assert r["values"]["A"] == "2"
        assert r["values"]["C"] == "x"
        assert r["values"]["D"] == "y"
        assert r["duplicates"] == ["A"]
        assert r["empties"] == ["B"]


def test_discover():
    with tempfile.TemporaryDirectory() as d:
        dp = Path(d)
        write(dp / ".env", "A=1\n")
        write(dp / ".env.local", "A=1\n")
        write(dp / "README.md", "x")
        files = discover(dp)
        assert [p.name for p in files] == [".env", ".env.local"]


def test_compare_missing():
    with tempfile.TemporaryDirectory() as d:
        dp = Path(d)
        a = dp / ".env"
        b = dp / ".env.example"
        write(a, "A=1\nB=2\n")
        write(b, "A=1\n")
        parsed = [parse_env(a), parse_env(b)]
        report, keys = compare(parsed)
        assert keys == ["A", "B"]
        assert report["missing"][str(b)] == ["B"]
        assert report["only"][str(a)] == ["B"]
