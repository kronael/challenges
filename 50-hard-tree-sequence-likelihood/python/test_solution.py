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
    want = inp.with_suffix(".out").read_text().strip()
    got = solve(obj["parent"], obj["sequences"], obj["prior"], obj["transition"])
    assert f"{got:.6f}" == want
