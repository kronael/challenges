import json
import pathlib
import pytest
from main import solve

# golden/ tests ALL cases including large — it must always pass
CASES = sorted(pathlib.Path("../cases").glob("*.in"))


@pytest.mark.parametrize("inp", CASES, ids=lambda p: p.stem)
def test_case(inp):
    obj = json.loads(inp.read_text())
    want = list(map(int, (inp.parent / (inp.stem + ".out")).read_text().split()))
    assert solve(obj["n"], [tuple(e) for e in obj["edges"]], obj["loads"]) == want
