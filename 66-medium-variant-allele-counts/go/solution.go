package main

// solve stays a call of its own so that `make vec` can find where it starts
// and returns; keep the directive.
//
//go:noinline
func solve(dosage []float64, depth, quality []int32, minDepth, minQuality int32) (float64, int64) {
	return 0, 0
}
