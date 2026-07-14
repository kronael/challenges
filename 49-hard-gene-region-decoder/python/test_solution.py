import json
import pathlib

import pytest

from main import solve

CASES = sorted(
    p for p in pathlib.Path("../cases").glob("*.in") if "_large_" not in p.name
)

assert CASES, "no small cases found in ../cases"


@pytest.mark.parametrize("inp", CASES, ids=lambda path: path.stem)
def test_case(inp):
    obj = json.loads(inp.read_text())
    want = [int(value) for value in inp.with_suffix(".out").read_text().split()]
    got = solve(obj["sequence"], obj["start"], obj["transition"], obj["emission"])
    assert list(got) == want
