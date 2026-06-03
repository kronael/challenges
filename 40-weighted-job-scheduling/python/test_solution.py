import json, pathlib, pytest
from main import solve

CASES = sorted(p for p in pathlib.Path("../cases").glob("*.in") if "_large_" not in p.name)

@pytest.mark.parametrize("inp", CASES, ids=lambda p: p.stem)
def test_case(inp):
    obj = json.loads(inp.read_text())
    jobs = [(j["start"], j["end"], j["weight"]) for j in obj["jobs"]]
    want = int(inp.with_suffix(".out").read_text().strip())
    assert solve(jobs) == want
