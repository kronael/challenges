package main

// solve stays a call of its own so that `make vec` can find where it starts
// and returns; keep the directive.
//
//go:noinline
func solve(capacity int, items []item) int64 {
	_ = capacity
	_ = items
	return 0
}
