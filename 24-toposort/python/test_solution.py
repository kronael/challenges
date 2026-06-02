import json
import pathlib
import pytest
from solution import solve

CASES = sorted(pathlib.Path("../cases").glob("*.in"))


@pytest.mark.parametrize("inp", CASES, ids=lambda p: p.stem)
def test_case(inp):
    obj = json.loads(inp.read_text())
    want = (inp.parent / (inp.stem + ".out")).read_text().split()
    res = solve(obj["n"], obj["edges"])
    got = ["CYCLE"] if res == "CYCLE" else [str(x) for x in res]
    assert got == want
