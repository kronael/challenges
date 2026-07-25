package main

import (
	"iter"
	"testing"
	"time"
)

// take pulls at most n values, so it terminates on an endless sequence.
func take[T any](seq iter.Seq[T], n int) []T {
	out := make([]T, 0, n)
	if n == 0 {
		return out
	}
	for v := range seq {
		out = append(out, v)
		if len(out) == n {
			break
		}
	}
	return out
}

func collect[T any](seq iter.Seq[T]) []T {
	var out []T
	for v := range seq {
		out = append(out, v)
	}
	return out
}

func equalInts(t *testing.T, got, want []int) {
	t.Helper()
	if len(got) != len(want) {
		t.Fatalf("got %v, want %v", got, want)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Fatalf("got %v, want %v", got, want)
		}
	}
}

func equalFloats(t *testing.T, got, want []float64) {
	t.Helper()
	if len(got) != len(want) {
		t.Fatalf("got %v, want %v", got, want)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Fatalf("got %v, want %v", got, want)
		}
	}
}

func TestNaturals(t *testing.T) {
	equalInts(t, take(Naturals(0), 5), []int{0, 1, 2, 3, 4})
	equalInts(t, take(Naturals(1), 5), []int{1, 2, 3, 4, 5})
}

func TestPrimes(t *testing.T) {
	equalInts(t, take(Primes(), 10), []int{2, 3, 5, 7, 11, 13, 17, 19, 23, 29})
}

func TestSieveDirectly(t *testing.T) {
	equalInts(t, take(Sieve(Naturals(2)), 6), []int{2, 3, 5, 7, 11, 13})
}

func TestFibonacci(t *testing.T) {
	equalInts(t, take(Fibonacci(), 10), []int{0, 1, 1, 2, 3, 5, 8, 13, 21, 34})
}

func TestRunningAverage(t *testing.T) {
	finite := func(yield func(float64) bool) {
		for _, v := range []float64{1, 3, 5, 7} {
			if !yield(v) {
				return
			}
		}
	}
	equalFloats(t, collect(RunningAverage(finite)), []float64{1, 2, 3, 4})
}

func TestRunningAverageFromInfiniteStream(t *testing.T) {
	naturals := func(yield func(float64) bool) {
		for v := 1.0; ; v++ {
			if !yield(v) {
				return
			}
		}
	}
	equalFloats(t, take(RunningAverage(naturals), 4), []float64{1, 1.5, 2, 2.5})
}

func TestCollatz(t *testing.T) {
	equalInts(t, take(Collatz(6), 8), []int{6, 3, 10, 5, 16, 8, 4, 2})
	equalInts(t, take(Collatz(1), 6), []int{1, 4, 2, 1, 4, 2})
}

func TestZipWith(t *testing.T) {
	sums := ZipWith(func(a, b int) int { return a + b }, Naturals(1), Naturals(1))
	equalInts(t, take(sums, 5), []int{2, 4, 6, 8, 10})
}

func TestUnfold(t *testing.T) {
	doubling := Unfold(func(n int) (int, int, bool) { return n, n * 2, n < 100 }, 1)
	equalInts(t, collect(doubling), []int{1, 2, 4, 8, 16, 32, 64})
}

func TestUnfoldCanBeInfinite(t *testing.T) {
	counting := Unfold(func(n int) (int, int, bool) { return n, n + 1, true }, 3)
	equalInts(t, take(counting, 5), []int{3, 4, 5, 6, 7})
}

// Primes must produce values on demand rather than precomputing a bounded list:
// the first value has to arrive without the sequence choosing an upper limit.
func TestPrimesIsLazy(t *testing.T) {
	next, stop := iter.Pull(Primes())
	defer stop()

	start := time.Now()
	first, ok := next()
	if !ok || first != 2 {
		t.Fatalf("first value %d (ok=%v), want 2", first, ok)
	}
	if elapsed := time.Since(start); elapsed > 100*time.Millisecond {
		t.Fatalf("first prime took %v — the sequence is not lazy", elapsed)
	}

	second, _ := next()
	if second != 3 {
		t.Fatalf("second value %d, want 3", second)
	}
	for _, want := range []int{5, 7, 11} {
		got, _ := next()
		if got != want {
			t.Fatalf("got %d, want %d", got, want)
		}
	}
}
