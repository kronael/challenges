package main

// solve stays a call of its own so that `make vec` can find where it starts
// and returns; keep the directive.
//
//go:noinline
func solve(k int, arr []int) []int {
	_ = k
	_ = arr
	return nil
}
