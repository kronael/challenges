import json
import pathlib

import pytest

from main import solve

CASES = sorted(
    p for p in pathlib.Path("../cases").glob("*.in") if "_large_" not in p.name
)


@pytest.mark.parametrize("inp", CASES, ids=lambda path: path.stem)
def test_case(inp):
    obj = json.loads(inp.read_text())
    text = inp.with_suffix(".out").read_text().strip()
    want = None if text == "NONE" else list(map(int, text.split()))
    assert solve(obj["masses"], obj["spectrum"]) == want
