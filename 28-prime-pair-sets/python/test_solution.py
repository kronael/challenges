import pathlib, pytest
from solution import solve

CASES = sorted(pathlib.Path("../cases").glob("*.in"))

@pytest.mark.parametrize("inp", CASES, ids=lambda p: p.stem)
def test_case(inp):
    pass  # TODO
