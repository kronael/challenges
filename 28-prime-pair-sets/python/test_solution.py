import pathlib
import pytest
from solution import solve

CASES = sorted(pathlib.Path("../cases").glob("*.in"))


@pytest.mark.parametrize("inp", CASES, ids=lambda p: p.stem)
def test_case(inp):
    want = list(map(int, (inp.parent / (inp.stem + ".out")).read_text().split()))
    assert [solve()] == want
