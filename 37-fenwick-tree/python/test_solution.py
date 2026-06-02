import json
import pathlib

import pytest
from solution import solve

CASES = sorted(p for p in pathlib.Path("../cases").glob("*.in") if "_large_" not in p.name)


@pytest.mark.parametrize("inp", CASES, ids=lambda p: p.stem)
def test_case(inp):
    obj = json.loads(inp.read_text())
    want = list(map(int, (inp.parent / (inp.stem + ".out")).read_text().split()))
    assert solve(obj["n"], obj["initial"], obj["queries"]) == want
