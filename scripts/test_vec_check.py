from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import vec_check

# Vectorizes: every lane is independent, so the whole loop body is packed.
ELEMENTWISE = """
void scale(const float *restrict a, const float *restrict b, float *restrict c, long n) {
    for (long i = 0; i < n; i++) c[i] = a[i] * b[i];
}
"""

# Stays scalar: float addition is not associative, so the sum keeps its serial
# dependency even though the compiler packs the multiply beside it.
DOT = """
float dot(const float *restrict a, const float *restrict b, long n) {
    float s = 0;
    for (long i = 0; i < n; i++) s += a[i] * b[i];
    return s;
}
"""

GO_MOD = "module probe\n\ngo 1.27.1\n"

# Vectorizes: the loop body is written in simd/archsimd's eight-lane types.
GO_LANES = """package main

import "simd/archsimd"

func scale(a, b, c []int32) {
	for i := 0; i+8 <= len(a); i += 8 {
		archsimd.LoadInt32x8(a[i:]).Mul(archsimd.LoadInt32x8(b[i:])).Store(c[i:])
	}
}

func main() { scale(nil, nil, nil) }
"""

# Stays scalar: the Go compiler does not vectorize a loop on its own.
GO_PLAIN = """package main

func scale(a, b, c []int32) {
	for i := range a {
		c[i] = a[i] * b[i]
	}
}

func main() { scale(nil, nil, nil) }
"""


class VerdictTests(unittest.TestCase):
    def check(self, source: str, function: str, expect: str) -> int:
        with tempfile.TemporaryDirectory() as raw_dir:
            workdir = Path(raw_dir)
            (workdir / "solution.c").write_text(source, encoding="utf-8")
            done = subprocess.run(
                [sys.executable, vec_check.__file__, "--workdir", str(workdir),
                 "--lang", "c", "--function", function, "--expect", expect],
                capture_output=True, text=True,
            )
            return done.returncode

    def test_elementwise_multiply_is_vectorized(self) -> None:
        self.assertEqual(self.check(ELEMENTWISE, "scale", "vectorized"), 0)

    def test_naive_float_dot_is_scalar(self) -> None:
        self.assertEqual(self.check(DOT, "dot", "scalar"), 0)

    def test_elementwise_multiply_rejects_a_scalar_expectation(self) -> None:
        self.assertEqual(self.check(ELEMENTWISE, "scale", "scalar"), 1)

    def test_naive_float_dot_rejects_a_vectorized_expectation(self) -> None:
        self.assertEqual(self.check(DOT, "dot", "vectorized"), 1)

    def test_missing_symbol_fails(self) -> None:
        self.assertEqual(self.check(DOT, "absent", "scalar"), 1)


class GoVerdictTests(unittest.TestCase):
    def check(self, source: str, function: str, expect: str) -> int:
        with tempfile.TemporaryDirectory() as raw_dir:
            workdir = Path(raw_dir)
            (workdir / "go.mod").write_text(GO_MOD, encoding="utf-8")
            (workdir / "main.go").write_text(source, encoding="utf-8")
            done = subprocess.run(
                [sys.executable, vec_check.__file__, "--workdir", str(workdir),
                 "--lang", "go", "--function", function, "--expect", expect],
                capture_output=True, text=True,
            )
            return done.returncode

    def test_lane_multiply_is_vectorized(self) -> None:
        self.assertEqual(self.check(GO_LANES, "scale", "vectorized"), 0)

    def test_plain_multiply_is_scalar(self) -> None:
        self.assertEqual(self.check(GO_PLAIN, "scale", "scalar"), 0)

    def test_lane_multiply_rejects_a_scalar_expectation(self) -> None:
        self.assertEqual(self.check(GO_LANES, "scale", "scalar"), 1)

    def test_plain_multiply_rejects_a_vectorized_expectation(self) -> None:
        self.assertEqual(self.check(GO_PLAIN, "scale", "vectorized"), 1)

    def test_missing_symbol_fails(self) -> None:
        self.assertEqual(self.check(GO_PLAIN, "absent", "scalar"), 1)


if __name__ == "__main__":
    unittest.main()
