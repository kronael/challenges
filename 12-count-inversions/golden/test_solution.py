import json
import pathlib
import subprocess
import sys

import pytest

CASES = sorted(pathlib.Path("../cases").glob("*.in"))


@pytest.mark.parametrize("inp", CASES, ids=lambda p: p.stem)
def test_case(inp):
    obj = json.loads(inp.read_text())
    assert obj["n"] == len(obj["arr"])
    result = subprocess.run(
        [sys.executable, "main.py"],
        input=inp.read_text(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    got = result.stdout.strip()
    want = inp.with_suffix(".out").read_text().strip()
    assert got == want, f"got {got!r}, want {want!r}"
