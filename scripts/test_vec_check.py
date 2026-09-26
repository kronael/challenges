from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import vec_check

ROOT = Path(__file__).resolve().parents[1]
N = 4096

# Every C probe links one of these drivers beside a solution.c, so that solve is
# a call the compiler cannot inline or clone from main.
SCALE_MAIN = """
#include <stdlib.h>
void solve(const float *restrict a, const float *restrict b, float *restrict c, long n);
int main(void) {
    float *a = malloc(%(n)d * sizeof *a);
    float *b = malloc(%(n)d * sizeof *b);
    float *c = malloc(%(n)d * sizeof *c);
    for (long i = 0; i < %(n)d; i++) { a[i] = (float)(i %% 7); b[i] = 2.0f; }
    solve(a, b, c, %(n)d);
    return c[%(n)d - 1] == c[%(n)d - 1] ? 0 : 1;
}
""" % {"n": N}

SELECT_MAIN = """
#include <stdlib.h>
long solve(const int *restrict x, int *restrict out, long n, int t);
int main(void) {
    int *x = malloc(%(n)d * sizeof *x), *out = malloc((%(n)d + 8) * sizeof *out);
    unsigned s = 1;
    for (long i = 0; i < %(n)d; i++) {
        s = s * 1103515245u + 12345u;
        x[i] = (int)((s >> 8) %% 1000);
    }
    return solve(x, out, %(n)d, 500) > 0 ? 0 : 1;
}
""" % {"n": N}

# Vectorizes: every lane is independent, so the loop runs in packed lanes.
ELEMENTWISE = """
void solve(const float *restrict a, const float *restrict b, float *restrict c, long n) {
    for (long i = 0; i < n; i++) c[i] = a[i] * b[i];
}
"""

# Stays scalar: float addition is not associative, so every add waits on the
# last. gcc packs the loads and the multiply beside it and still adds each
# product in order, one scalar add per element.
DOT = """
void solve(const float *restrict a, const float *restrict b, float *restrict c, long n) {
    float s = 0;
    for (long i = 0; i < n; i++) s += a[i] * b[i];
    c[0] = s;
}
"""

# The packed loop lives in a helper that gcc clones as scale_by.constprop.0.
HELPER = """
static __attribute__((noinline)) void
scale_by(float *restrict c, const float *restrict a, long n, float k) {
    for (long i = 0; i < n; i++) c[i] = a[i] * k;
}
void solve(const float *restrict a, const float *restrict b, float *restrict c, long n) {
    (void)b;
    scale_by(c, a, n, 2.0f);
}
"""

# A packed loop that loads nothing: gcc counts the indices in a vector register.
INDICES = """
void solve(const float *restrict a, const float *restrict b, float *restrict c, long n) {
    (void)a;
    (void)b;
    for (int i = 0; i < (int)n; i++) c[i] = (float)i;
}
"""

# The same multiply, then the first call the program makes to strlen.
FIRST_CALL = """
#include <string.h>
void solve(const float *restrict a, const float *restrict b, float *restrict c, long n) {
    for (long i = 0; i < n; i++) c[i] = a[i] * b[i];
    c[0] = (float)strlen((const char *)(c + 1));
}
"""

SELECT = """
long solve(const int *restrict x, int *restrict out, long n, int t) {
    long k = 0;
    for (long i = 0; i < n; i++) if (x[i] > t) out[k++] = x[i];
    return k;
}
"""

# A packed pass over the input, then the selection in scalar code.
PRE_PASS = """
#include <stdlib.h>
long solve(const int *restrict x, int *restrict out, long n, int t) {
    int *y = malloc(n * sizeof *y);
    for (long i = 0; i < n; i++) y[i] = x[i] + 1;
    long k = 0;
    for (long i = 0; i < n; i++) if (y[i] > t + 1) out[k++] = y[i] - 1;
    free(y);
    return k;
}
"""

# A packed count of the kept scores, then the same scalar append.
COUNT_THEN_APPEND = """
long solve(const int *restrict x, int *restrict out, long n, int t) {
    long m = 0;
    for (long i = 0; i < n; i++) m += x[i] > t;
    long k = 0;
    for (long i = 0; i < n && k < m; i++) if (x[i] > t) out[k++] = x[i];
    return k;
}
"""

# A packed loop that the input never reaches, beside the scalar selection.
DEAD_BRANCH = """
long solve(const int *restrict x, int *restrict out, long n, int t) {
    if (t < -1000000) {
        for (long i = 0; i < n; i++) out[i] = x[i] * 3 + 1;
        return n;
    }
    long k = 0;
    for (long i = 0; i < n; i++) if (x[i] > t) out[k++] = x[i];
    return k;
}
"""

# The same, with the packed loop in inline assembly.
ASM_DECOY = """
long solve(const int *restrict x, int *restrict out, long n, int t) {
    if (t < -1000000) {
        for (long i = 0; i < n; i++) __asm__ volatile("vpaddd %%ymm0, %%ymm0, %%ymm0" ::: "xmm0");
    }
    long k = 0;
    for (long i = 0; i < n; i++) if (x[i] > t) out[k++] = x[i];
    return k;
}
"""

# A packed pass over the input, then the selection on a thread solve starts.
THREAD = """
#include <pthread.h>
#include <stdlib.h>
struct job { const int *y; int *out; long n; int t; long k; };
static void *select_kept(void *raw) {
    struct job *j = raw;
    for (long i = 0; i < j->n; i++) if (j->y[i] > j->t + 1) j->out[j->k++] = j->y[i] - 1;
    return 0;
}
long solve(const int *restrict x, int *restrict out, long n, int t) {
    int *y = malloc(n * sizeof *y);
    for (long i = 0; i < n; i++) y[i] = x[i] + 1;
    struct job j = {y, out, n, t, 0};
    pthread_t thread;
    if (pthread_create(&thread, 0, select_kept, &j) || pthread_join(thread, 0)) abort();
    free(y);
    return j.k;
}
"""

# A C solver directory that make builds with shared/c/: it reads x and prints
# the sum solve returns.
C_HEADER = """
#include "harness.h"
#include "json.h"
#include <stdio.h>
typedef struct { double *x; size_t n; } Input;
typedef struct { double sum; } Answer;
void input_parse(const JsonValue *root, Input *in);
void input_free(Input *in);
Answer solve(const Input *in);
void answer_print(FILE *out, const Answer *a);
void answer_free(Answer *a);
"""
C_SCAFFOLD = """
#include "solution.h"
#include <stdlib.h>
void input_parse(const JsonValue *root, Input *in) {
    const JsonValue *x = json_get(root, "x");
    in->n = json_len(x);
    in->x = xmalloc(in->n * sizeof *in->x);
    for (size_t i = 0; i < in->n; i++) in->x[i] = json_num(json_at(x, i));
}
void input_free(Input *in) { free(in->x); }
void answer_print(FILE *out, const Answer *a) { fprintf(out, "%.1f\\n", a->sum); }
void answer_free(Answer *a) { (void)a; }
"""

# Stays scalar: each add waits on the last.
C_SUM = """
Answer solve(const Input *in) {
    double s = 0;
    for (size_t i = 0; i < in->n; i++) s += in->x[i];
    return (Answer){s};
}
"""

C_CRASH = """
Answer solve(const Input *in) {
    return (Answer){in->x[0] + *(volatile double *)0};
}
"""

GO_MOD = "module probe\n\ngo 1.27.1\n"
GO_MAIN = (
    """package main

import (
\t"fmt"
\t"runtime"
)

func init() { runtime.LockOSThread() }

func main() {
\tn := %d
\ta := make([]int32, n)
\tb := make([]int32, n)
\tc := make([]int32, n)
\tfor i := range a {
\t\ta[i] = int32(i %% 7)
\t\tb[i] = 3
\t}
\tsolve(a, b, c)
\tfmt.Println(c[n-1])
}
"""
    % N
)

# Vectorizes: the loop body is written in simd/archsimd's eight-lane types.
GO_LANES = """package main

import "simd/archsimd"

//go:noinline
func solve(a, b, c []int32) {
\ti := 0
\tfor ; i+8 <= len(a); i += 8 {
\t\tarchsimd.LoadInt32x8(a[i:]).Mul(archsimd.LoadInt32x8(b[i:])).Store(c[i:])
\t}
\tfor ; i < len(a); i++ {
\t\tc[i] = a[i] * b[i]
\t}
}
"""

# Stays scalar: the Go compiler does not vectorize a loop on its own.
GO_PLAIN = """package main

//go:noinline
func solve(a, b, c []int32) {
\tfor i := range a {
\t\tc[i] = a[i] * b[i]
\t}
}
"""

# The packed loop in a helper that Go's inliner declines, so solve calls it.
GO_HELPER = """package main

import "simd/archsimd"

//go:noinline
func multiply(a, b, c []int32) {
\ti := 0
\tfor ; i+8 <= len(a); i += 8 {
\t\tarchsimd.LoadInt32x8(a[i:]).Mul(archsimd.LoadInt32x8(b[i:])).Store(c[i:])
\t}
\tfor ; i < len(a); i++ {
\t\tc[i] = a[i] * b[i]
\t}
}

//go:noinline
func solve(a, b, c []int32) {
\tmultiply(a, b, c)
}
"""

# The same loop, a vector per call two calls deep. Single-stepping outlasts the
# scheduler's time slice, so the goroutine is preempted at one of the calls.
GO_CALLS = """package main

import "simd/archsimd"

//go:noinline
func multiply(a, b, c []int32, i int) {
\tarchsimd.LoadInt32x8(a[i:]).Mul(archsimd.LoadInt32x8(b[i:])).Store(c[i:])
}

//go:noinline
func step(a, b, c []int32, i int) {
\tmultiply(a, b, c, i)
}

//go:noinline
func solve(a, b, c []int32) {
\ti := 0
\tfor ; i+8 <= len(a); i += 8 {
\t\tstep(a, b, c, i)
\t}
\tfor ; i < len(a); i++ {
\t\tc[i] = a[i] * b[i]
\t}
}
"""

# The same loop into a 4 MiB scratch slice, which grows the heap.
GO_HEAP_GROWTH = """package main

import "simd/archsimd"

//go:noinline
func solve(a, b, c []int32) {
\tscratch := make([]int32, 1<<20)
\ti := 0
\tfor ; i+8 <= len(a); i += 8 {
\t\tarchsimd.LoadInt32x8(a[i:]).Mul(archsimd.LoadInt32x8(b[i:])).Store(scratch[i:])
\t}
\tfor ; i < len(a); i++ {
\t\tscratch[i] = a[i] * b[i]
\t}
\tcopy(c, scratch)
}
"""

# The same loop behind a frame too large for the goroutine's stack, so solve's
# prologue moves the stack and solve returns on a different stack than the one
# it was entered on.
GO_MOVED_STACK = """package main

import "simd/archsimd"

//go:noinline
func solve(a, b, c []int32) {
\tvar pad [1 << 14]int32
\tpad[len(a)%len(pad)] = 1
\ti := 0
\tfor ; i+8 <= len(a); i += 8 {
\t\tarchsimd.LoadInt32x8(a[i:]).Mul(archsimd.LoadInt32x8(b[i:])).Store(c[i:])
\t}
\tfor ; i < len(a); i++ {
\t\tc[i] = a[i] * b[i]
\t}
\tc[0] += pad[len(b)%len(pad)]
}
"""

# The lane multiply, then a scalar pass on a goroutine that solve starts.
GO_GOROUTINE = """package main

import "simd/archsimd"

//go:noinline
func solve(a, b, c []int32) {
\ti := 0
\tfor ; i+8 <= len(a); i += 8 {
\t\tarchsimd.LoadInt32x8(a[i:]).Mul(archsimd.LoadInt32x8(b[i:])).Store(c[i:])
\t}
\tfor ; i < len(a); i++ {
\t\tc[i] = a[i] * b[i]
\t}
\tdone := make(chan bool)
\tgo func() {
\t\tfor i := range c {
\t\t\tc[i] += a[i]
\t\t}
\t\tdone <- true
\t}()
\t<-done
}
"""

# A cfg(target_feature) branch that is wrong only where AVX2 is enabled.
RUST_CFG_SPLIT = """
#[no_mangle]
pub fn solve(x: &[i32]) -> i64 {
    #[cfg(target_feature = "avx2")]
    {
        x.iter().map(|&v| v as i64).sum::<i64>() + 1
    }
    #[cfg(not(target_feature = "avx2"))]
    {
        x.iter().map(|&v| v as i64).sum()
    }
}
"""
# Stays scalar: each add waits on the last, unless the vectorizer is told to
# reorder them.
RUST_SUM = """
#[no_mangle]
pub fn solve(x: &[f64]) -> f64 {
    let mut s = 0.0;
    for &v in x {
        s += v;
    }
    s
}
"""
RUST_SUM_MAIN = (
    """
fn main() {
    println!("{}", probe::solve(&vec![0.0; %d]));
}
"""
    % N
)
RUST_CARGO = '[package]\nname = "probe"\nversion = "0.1.0"\nedition = "2021"\n'
RUST_TEST = """
#[test]
fn sums() {
    assert_eq!(probe::solve(&[1, 2, 3]), 6);
}
"""


# A vec challenge beside links to shared/ and scripts/, with 68's Makefile for
# the language; files maps paths in the challenge to their text, and make vec
# traces cases/01.in, N zeros in x.
def lay_out(root: Path, language: str, files: dict[str, str]) -> Path:
    challenge = root / "99-medium-probe"
    workdir = challenge / language
    workdir.mkdir(parents=True)
    for name in ("shared", "scripts"):
        (root / name).symlink_to(ROOT / name)
    (challenge / "vec.mk").write_text(
        "VEC_INPUT := ../cases/01.in\nVEC_UNITS := x\n", encoding="utf-8"
    )
    files = {"cases/01.in": json.dumps({"x": [0] * N}), **files}
    for name, text in files.items():
        (challenge / name).parent.mkdir(parents=True, exist_ok=True)
        (challenge / name).write_text(text, encoding="utf-8")
    shutil.copy(
        ROOT / f"68-hard-sparse-activation-gate/{language}/Makefile",
        workdir / "Makefile",
    )
    return workdir


def grade(
    workdir: Path, binary: Path, function: str, expect: str
) -> subprocess.CompletedProcess[str]:
    (workdir / "input.json").write_text(json.dumps({"x": [0] * N}), encoding="utf-8")
    return subprocess.run(
        [
            sys.executable,
            vec_check.__file__,
            "--binary",
            str(binary),
            "--function",
            function,
            "--input",
            str(workdir / "input.json"),
            "--units",
            "x",
            "--expect",
            expect,
            "--sources",
            str(workdir),
        ],
        capture_output=True,
        text=True,
    )


class CTests(unittest.TestCase):
    cc = "cc"

    def build(self, workdir: Path, driver: str, source: str) -> Path:
        (workdir / "main.c").write_text(driver, encoding="utf-8")
        (workdir / "solution.c").write_text(source, encoding="utf-8")
        built = subprocess.run(
            [
                self.cc,
                "-std=c11",
                "-O3",
                "-march=x86-64-v3",
                "-o",
                "prog",
                "main.c",
                "solution.c",
            ],
            cwd=workdir,
            capture_output=True,
            text=True,
        )
        self.assertEqual(built.returncode, 0, built.stderr)
        return workdir / "prog"

    def check(
        self, driver: str, source: str, expect: str
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as raw_dir:
            workdir = Path(raw_dir)
            binary = self.build(workdir, driver, source)
            return grade(workdir, binary, "solve", expect)

    def assert_grade(self, driver: str, source: str, expect: str) -> None:
        done = self.check(driver, source, expect)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)

    def test_elementwise_multiply_is_vectorized(self) -> None:
        self.assert_grade(SCALE_MAIN, ELEMENTWISE, "vectorized")

    def test_float_dot_with_packed_multiplies_is_scalar(self) -> None:
        self.assert_grade(SCALE_MAIN, DOT, "scalar")

    def test_packed_loop_in_a_helper_counts_for_solve(self) -> None:
        self.assert_grade(SCALE_MAIN, HELPER, "vectorized")

    def test_scalar_selection_is_scalar(self) -> None:
        self.assert_grade(SELECT_MAIN, SELECT, "scalar")

    def test_packed_pre_pass_does_not_hide_a_scalar_selection(self) -> None:
        self.assert_grade(SELECT_MAIN, PRE_PASS, "scalar")

    def test_packed_count_does_not_hide_a_scalar_append(self) -> None:
        self.assert_grade(SELECT_MAIN, COUNT_THEN_APPEND, "scalar")

    def test_packed_loop_the_input_never_runs_does_not_count(self) -> None:
        self.assert_grade(SELECT_MAIN, DEAD_BRANCH, "scalar")

    def test_elementwise_multiply_rejects_a_scalar_expectation(self) -> None:
        self.assertEqual(self.check(SCALE_MAIN, ELEMENTWISE, "scalar").returncode, 1)

    def test_inline_assembly_is_refused(self) -> None:
        done = self.check(SELECT_MAIN, ASM_DECOY, "vectorized")
        self.assertEqual(done.returncode, 1)
        self.assertIn("inline assembly", done.stdout)

    def test_selection_on_a_thread_solve_starts_is_refused(self) -> None:
        done = self.check(SELECT_MAIN, THREAD, "vectorized")
        self.assertEqual(done.returncode, 1)
        self.assertIn("solve started a thread", done.stderr)

    def test_first_call_into_libc_is_not_charged_for_binding(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            workdir = Path(raw_dir)
            binary = self.build(workdir, SCALE_MAIN, FIRST_CALL).resolve()
            (workdir / "input.json").write_text("{}", encoding="utf-8")
            count = vec_check.run(binary, "solve", workdir / "input.json", float("inf"))
            self.assertLess(count.scalar, 50)

    def test_packed_loop_that_loads_nothing_pays_its_control_per_vector(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            workdir = Path(raw_dir)
            binary = self.build(workdir, SCALE_MAIN, INDICES).resolve()
            (workdir / "input.json").write_text("{}", encoding="utf-8")
            count = vec_check.run(binary, "solve", workdir / "input.json", float("inf"))
            self.assertLess(count.scalar, N / 64)

    def test_trace_stops_at_the_step_limit_whatever_the_clock(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            workdir = Path(raw_dir)
            binary = self.build(workdir, SCALE_MAIN, ELEMENTWISE).resolve()
            (workdir / "input.json").write_text("{}", encoding="utf-8")
            count = vec_check.run(
                binary, "solve", workdir / "input.json", float("inf"), 100
            )
            self.assertFalse(count.returned)
            self.assertEqual(count.steps, 101)

    def test_missing_symbol_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            workdir = Path(raw_dir)
            (workdir / "main.c").write_text(
                "int main(void) { return 0; }\n", encoding="utf-8"
            )
            subprocess.run(
                [self.cc, "-O2", "-o", "prog", "main.c"], cwd=workdir, check=True
            )
            self.assertNotEqual(
                grade(workdir, workdir / "prog", "solve", "scalar").returncode, 0
            )


class CMakeTests(unittest.TestCase):
    def vec(
        self, source: str, makefile: str = "", *args: str
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as raw_dir:
            workdir = lay_out(
                Path(raw_dir),
                "c",
                {
                    "c/solution.h": C_HEADER,
                    "c/solution.c": C_SCAFFOLD + source,
                    "cases/01.out": "0.0\n",
                },
            )
            with (workdir / "Makefile").open("a", encoding="utf-8") as extra:
                extra.write(makefile)
            return subprocess.run(
                ["make", "vec", *args], cwd=workdir, capture_output=True, text=True
            )

    def test_a_scalar_verdict_names_the_lines_that_ran_scalar(self) -> None:
        done = self.vec(C_SUM)
        self.assertEqual(done.returncode, 2, done.stdout + done.stderr)
        self.assertIn("-> scalar  EXPECTED vectorized", done.stdout)
        loop = (
            (C_SCAFFOLD + C_SUM)
            .splitlines()
            .index("    for (size_t i = 0; i < in->n; i++) s += in->x[i];")
        )
        self.assertRegex(done.stdout, rf"\n +[\d,]+  solution\.c:{loop + 1} solve\n")

    def test_flags_a_solver_adds_do_not_reach_the_grade(self) -> None:
        for makefile, args in (
            ("CFLAGS += -ffast-math\n", []),
            ("CC := cc -ffast-math\n", []),
            ("", ["CFLAGS=-std=c11 -O3 -march=x86-64-v3 -g -ffast-math"]),
        ):
            with self.subTest(makefile=makefile, args=args):
                done = self.vec(C_SUM, makefile, *args)
                self.assertEqual(done.returncode, 2, done.stdout + done.stderr)
                self.assertIn("-> scalar  EXPECTED vectorized", done.stdout)

    def test_a_crash_is_reported_as_a_crash(self) -> None:
        done = self.vec(C_CRASH)
        self.assertEqual(done.returncode, 2, done.stdout + done.stderr)
        self.assertIn("./main crashed with SIGSEGV on ../cases/01.in", done.stdout)


@unittest.skipUnless(shutil.which("clang"), "clang is not on PATH")
class ClangTests(CTests):
    cc = "clang"


@unittest.skipUnless(shutil.which("go"), "go is not on PATH")
class GoTests(unittest.TestCase):
    def build(self, workdir: Path, source: str) -> Path:
        (workdir / "go.mod").write_text(GO_MOD, encoding="utf-8")
        (workdir / "main.go").write_text(GO_MAIN, encoding="utf-8")
        (workdir / "solution.go").write_text(source, encoding="utf-8")
        built = subprocess.run(
            ["go", "build", "-o", "prog", "."],
            cwd=workdir,
            capture_output=True,
            text=True,
            env={**os.environ, "GOEXPERIMENT": "simd", "GOAMD64": "v3"},
        )
        self.assertEqual(built.returncode, 0, built.stderr)
        return workdir / "prog"

    def check(self, source: str, expect: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as raw_dir:
            workdir = Path(raw_dir)
            return grade(workdir, self.build(workdir, source), "main.solve", expect)

    def assert_grade(self, source: str, expect: str) -> None:
        done = self.check(source, expect)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)

    def test_lane_multiply_is_vectorized(self) -> None:
        self.assert_grade(GO_LANES, "vectorized")

    def test_plain_multiply_is_scalar(self) -> None:
        self.assert_grade(GO_PLAIN, "scalar")

    def test_lane_multiply_in_a_helper_counts_for_solve(self) -> None:
        self.assert_grade(GO_HELPER, "vectorized")

    def test_scheduler_preempting_solve_does_not_count(self) -> None:
        self.assert_grade(GO_CALLS, "vectorized")

    def test_heap_growth_does_not_count(self) -> None:
        self.assert_grade(GO_HEAP_GROWTH, "vectorized")

    def test_return_is_found_after_solve_moves_its_stack(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            workdir = Path(raw_dir)
            binary = self.build(workdir, GO_MOVED_STACK).resolve()
            (workdir / "input.json").write_text("{}", encoding="utf-8")
            count = vec_check.run(
                binary, "main.solve", workdir / "input.json", float("inf")
            )
            self.assertTrue(count.returned)

    def test_pass_on_a_goroutine_solve_starts_is_refused(self) -> None:
        done = self.check(GO_GOROUTINE, "vectorized")
        self.assertEqual(done.returncode, 1)
        self.assertIn("solve started a thread", done.stderr)

    def test_build_and_grade_stay_in_the_solver_directory(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            workdir = lay_out(
                Path(raw_dir),
                "go",
                {
                    "go/go.mod": GO_MOD,
                    "go/main.go": GO_MAIN,
                    "go/solution.go": GO_LANES,
                    "cases/01.out": "0\n",
                },
            )
            done = subprocess.run(
                ["make", "vec"], cwd=workdir, capture_output=True, text=True
            )
            self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
            self.assertTrue((workdir / "probe").is_file())

    def test_assembly_file_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            workdir = Path(raw_dir)
            (workdir / "go.mod").write_text(GO_MOD, encoding="utf-8")
            (workdir / "solve_amd64.s").write_text("", encoding="utf-8")
            self.assertEqual(
                vec_check.lint(workdir),
                ["solve_amd64.s: compiled outside the graded build"],
            )


@unittest.skipUnless(shutil.which("cargo"), "cargo is not on PATH")
class RustBuildTests(unittest.TestCase):
    def test_tests_run_the_build_the_grade_traces(self) -> None:
        """A branch taken only under AVX2 must fail `make test`, because the
        grade traces a build with AVX2 enabled."""
        with tempfile.TemporaryDirectory() as raw_dir:
            crate = lay_out(
                Path(raw_dir),
                "rust",
                {
                    "rust/Cargo.toml": RUST_CARGO,
                    "rust/src/lib.rs": RUST_CFG_SPLIT,
                    "rust/tests/sums.rs": RUST_TEST,
                },
            )
            done = subprocess.run(
                ["make", "test"], cwd=crate, capture_output=True, text=True
            )
            self.assertNotEqual(done.returncode, 0, done.stdout + done.stderr)
            self.assertIn("left: 7", done.stdout + done.stderr)

    def test_rustflags_a_solver_adds_do_not_reach_the_grade(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            crate = lay_out(
                Path(raw_dir),
                "rust",
                {
                    "rust/Cargo.toml": RUST_CARGO,
                    "rust/src/lib.rs": RUST_SUM,
                    "rust/src/main.rs": RUST_SUM_MAIN,
                    "cases/01.out": "0\n",
                },
            )
            with (crate / "Makefile").open("a", encoding="utf-8") as extra:
                extra.write(
                    "export RUSTFLAGS := -C target-cpu=x86-64-v3"
                    " -C llvm-args=-force-vector-width=4\n"
                )
            done = subprocess.run(
                ["make", "vec"], cwd=crate, capture_output=True, text=True
            )
            self.assertEqual(done.returncode, 2, done.stdout + done.stderr)
            self.assertIn("-> scalar  EXPECTED vectorized", done.stdout)


class HelpTests(unittest.TestCase):
    def targets(self, workdir: Path) -> set[str]:
        done = subprocess.run(
            ["make", "-s", "help"], cwd=workdir, capture_output=True, text=True
        )
        self.assertEqual(done.returncode, 0, done.stderr)
        return {line.split()[0] for line in done.stdout.splitlines()}

    def has_rule(self, workdir: Path, target: str) -> bool:
        done = subprocess.run(["make", "-n", target], cwd=workdir, capture_output=True)
        return done.returncode == 0

    def test_help_lists_the_same_levels_in_every_language(self) -> None:
        for challenge in sorted(path.parent for path in ROOT.glob("[0-9]*/vec.mk")):
            listed = {}
            for language in ("c", "go", "rust"):
                workdir = challenge / language
                listed[language] = self.targets(workdir)
                for target in ("bench", "vec"):
                    with self.subTest(workdir=workdir, target=target):
                        self.assertEqual(
                            target in listed[language], self.has_rule(workdir, target)
                        )
            with self.subTest(challenge=challenge.name):
                self.assertIn("vec", listed["c"])
                self.assertEqual(listed["c"], listed["go"])
                self.assertEqual(listed["c"], listed["rust"])


class LintTests(unittest.TestCase):
    def lint(self, files: dict[str, str]) -> list[str]:
        with tempfile.TemporaryDirectory() as raw_dir:
            workdir = Path(raw_dir)
            for name, text in files.items():
                (workdir / name).parent.mkdir(parents=True, exist_ok=True)
                (workdir / name).write_text(text, encoding="utf-8")
            return vec_check.lint(workdir)

    def test_c_refuses_what_changes_the_target_or_optimizer(self) -> None:
        for source in (
            '#pragma GCC target("avx512f")\n',
            '_Pragma("GCC optimize(\\"O3\\")")\n',
            '__attribute__((target("avx512f"))) void f(void) {}\n',
            '__attribute__((noinline, optimize("unroll-loops"))) void f(void) {}\n',
            '[[gnu::target_clones("avx2", "default")]] void f(void) {}\n',
            'void f(void) { asm("nop"); }\n',
        ):
            with self.subTest(source=source):
                self.assertTrue(self.lint({"solution.c": source}))

    def test_c_allows_intrinsics_and_comments_that_name_the_constructs(self) -> None:
        source = (
            "#include <immintrin.h>\n/* no asm, no #pragma here */\n"
            "__attribute__((noinline)) int f(void) { return _mm_popcnt_u32(3); }\n"
        )
        self.assertEqual(self.lint({"solution.c": source}), [])

    def test_rust_refuses_assembly_target_features_and_build_scripts(self) -> None:
        for files in (
            {"src/lib.rs": 'pub fn f() { unsafe { std::arch::asm!("nop") } }\n'},
            {
                "src/lib.rs": '#[target_feature(enable = "avx512f")]\n'
                "pub unsafe fn f() {}\n"
            },
            {"src/lib.rs": "pub fn f() {}\n", "build.rs": "fn main() {}\n"},
        ):
            with self.subTest(files=files):
                self.assertEqual(len(self.lint({"Cargo.toml": "", **files})), 1)

    def test_rust_allows_cfg_target_feature_and_intrinsics(self) -> None:
        source = (
            "use std::arch::x86_64::_popcnt32;\n"
            '#[cfg(target_feature = "avx2")]\n'
            "pub fn f() -> i32 { unsafe { _popcnt32(3) } }\n"
        )
        self.assertEqual(self.lint({"Cargo.toml": "", "src/lib.rs": source}), [])

    def test_go_refuses_cgo(self) -> None:
        source = 'package main\n\nimport "C"\n\nfunc solve() {}\n'
        self.assertEqual(
            self.lint({"go.mod": GO_MOD, "solution.go": source}), ["solution.go: cgo"]
        )


class UnitTests(unittest.TestCase):
    def count(self, fields: dict[str, object], units: str) -> int:
        with tempfile.TemporaryDirectory() as raw_dir:
            path = Path(raw_dir) / "input.json"
            path.write_text(json.dumps(fields), encoding="utf-8")
            return vec_check.count_units(path, units)

    def test_array_counts_its_elements_and_string_its_bytes(self) -> None:
        self.assertEqual(self.count({"x": [5, 6, 7]}, "x"), 3)
        self.assertEqual(self.count({"s": "ACGT"}, "s"), 4)

    def test_integer_counts_its_value(self) -> None:
        self.assertEqual(self.count({"capacity": 2000}, "capacity"), 2000)

    def test_product_multiplies_every_factor(self) -> None:
        fields = {"items": [{}, {}, {}], "capacity": 2000, "s": "AR", "t": "NDC"}
        self.assertEqual(self.count(fields, "items*capacity"), 6000)
        self.assertEqual(self.count(fields, "s*t"), 6)


class DecodeTests(unittest.TestCase):
    def test_scalar_float_in_objdump_spellings_is_scalar(self) -> None:
        for mnemonic, operands in (
            ("vcvtsi2ssl", "(%rdi),%xmm1,%xmm1"),
            ("vcvtsi2sdq", "%rax,%xmm1,%xmm1"),
            ("vcmpgt_oqss", "%xmm2,%xmm1,%xmm1"),
            ("vcmpneq_oqsd", "(%rdi),%xmm1,%xmm1"),
        ):
            with self.subTest(mnemonic=mnemonic):
                self.assertIs(
                    vec_check.decode(mnemonic, operands, 0xC5).kind,
                    vec_check.Kind.SCALAR,
                )

    def test_zeroing_a_vector_register_is_not_packed_work(self) -> None:
        for mnemonic, operands in (
            ("vpxor", "%xmm0,%xmm0,%xmm0"),
            ("vxorps", "%ymm1,%ymm1,%ymm1"),
            ("xorps", "%xmm15,%xmm15"),
        ):
            with self.subTest(mnemonic=mnemonic):
                insn = vec_check.decode(mnemonic, operands, 0xC5)
                self.assertIs(insn.kind, vec_check.Kind.OTHER)
                self.assertFalse(insn.vector_work)
        self.assertIs(
            vec_check.decode("vpxor", "%xmm1,%xmm0,%xmm0", 0xC5).kind,
            vec_check.Kind.PACKED,
        )

    def test_packed_compare_is_packed(self) -> None:
        self.assertIs(
            vec_check.decode("vcmpgt_oqps", "%ymm2,%ymm1,%ymm1", 0xC5).kind,
            vec_check.Kind.PACKED,
        )


if __name__ == "__main__":
    unittest.main()
