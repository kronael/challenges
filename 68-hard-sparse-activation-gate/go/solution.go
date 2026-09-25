package main

// solve stays a call of its own so that `make vec` can find where it starts
// and returns; keep the directive.
//
//go:noinline
func solve(scores []int32, threshold int32) []int32 {
	_ = scores
	_ = threshold
	return nil
}
