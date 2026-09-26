package main

// solve stays a call of its own so that `make vec` can find where it starts
// and returns; keep the directive.
//
//go:noinline
func solve(d, length int, genome string, guides []string) []int {
	_ = d
	_ = length
	_ = genome
	_ = guides
	return nil
}
