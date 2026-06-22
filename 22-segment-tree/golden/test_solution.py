import json
import pathlib
import subprocess
import sys

import pytest

CASES = sorted(pathlib.Path("../cases").glob("*.in"))


def test_cases_exist():
    assert CASES, "no cases found in ../cases"


@pytest.mark.parametrize("inp", CASES, ids=lambda p: p.stem)
def test_case(inp):
    result = subprocess.run(
        [sys.executable, "main.py"],
        input=inp.read_text(),
        capture_output=True,
        text=True,
    )
    got = result.stdout.strip()
    want = inp.with_suffix(".out").read_text().strip()
    assert got == want, f"got {got!r}, want {want!r}"
