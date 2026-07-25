package main

import "iter"

// Naturals yields start, start+1, start+2, … forever.
func Naturals(start int) iter.Seq[int] {
	_ = start
	panic("Naturals: not implemented")
}

// Sieve takes an ascending stream of integers ≥ 2 and yields the primes among
// them, in order.
func Sieve(nums iter.Seq[int]) iter.Seq[int] {
	_ = nums
	panic("Sieve: not implemented")
}

// Primes yields 2, 3, 5, 7, 11, … forever.
func Primes() iter.Seq[int] {
	panic("Primes: not implemented")
}

// Fibonacci yields 0, 1, 1, 2, 3, 5, 8, … forever.
func Fibonacci() iter.Seq[int] {
	panic("Fibonacci: not implemented")
}

// RunningAverage yields the average of every prefix of nums — x₀, (x₀+x₁)/2,
// (x₀+x₁+x₂)/3, … — one output per input.
func RunningAverage(nums iter.Seq[float64]) iter.Seq[float64] {
	_ = nums
	panic("RunningAverage: not implemented")
}

// Collatz yields n, then repeatedly n/2 when even and 3n+1 when odd, continuing
// past 1 into the 1, 4, 2, 1, … cycle.
func Collatz(n int) iter.Seq[int] {
	_ = n
	panic("Collatz: not implemented")
}

// ZipWith applies f element-wise to two possibly infinite sequences, yielding
// f(x₀,y₀), f(x₁,y₁), … and stopping when either side runs out.
func ZipWith[A, B, C any](f func(A, B) C, xs iter.Seq[A], ys iter.Seq[B]) iter.Seq[C] {
	_, _, _ = f, xs, ys
	panic("ZipWith: not implemented")
}

// Unfold repeatedly applies f to the current state: f(state) returns a value,
// the next state, and true to continue, or false to stop.
func Unfold[S, V any](f func(S) (V, S, bool), seed S) iter.Seq[V] {
	_, _ = f, seed
	panic("Unfold: not implemented")
}

func main() {}
