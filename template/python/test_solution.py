import json, pathlib, pytest
from solution import solve

CASES = sorted(pathlib.Path("../cases").glob("*.in"))

def _parse(text):
    obj = json.loads(text)
    return obj["n"], obj["data"]

@pytest.mark.parametrize("inp", CASES, ids=lambda p: p.stem)
def test_case(inp):
    n, data = _parse(inp.read_text())
    want = list(map(int, (inp.parent / (inp.stem + ".out")).read_text().split()))
    assert list(solve(n, data)) == want
