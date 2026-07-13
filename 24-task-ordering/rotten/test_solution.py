import pathlib
import subprocess
import sys

import pytest

# Small cases only: rotten is correct, so it PASSES these. It is excluded from the
# large cases on purpose — those are where it TIMEOUTs (see `make bench`).
CASES = sorted(p for p in pathlib.Path("../cases").glob("*.in") if "_large_" not in p.name)
assert CASES, "no small cases found in ../cases"


@pytest.mark.parametrize("inp", CASES, ids=lambda p: p.stem)
def test_case(inp):
    result = subprocess.run(
        [sys.executable, "main.py"],
        input=inp.read_text(),
        capture_output=True,
        text=True,
    )
    got = result.stdout.strip()
    want = inp.with_suffix(".out").read_text().strip()
    assert got == want, f"got {got!r}, want {want!r}"
