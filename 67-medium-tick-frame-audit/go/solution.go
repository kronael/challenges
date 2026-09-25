package main

// solve stays a call of its own so that `make vec` can find where it starts
// and returns; keep the directive.
//
//go:noinline
func solve(width int, separators []int, stream []byte) (int64, int64) {
	_ = width
	_ = separators
	_ = stream
	return 0, 0
}
