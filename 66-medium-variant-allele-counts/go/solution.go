package main

// solve stays a call of its own so that `make vec` can find where it starts
// and returns; keep the directive.
//
//go:noinline
func solve(dosage []float64, depth []int32, quality []int32, minDepth int32, minQuality int32) (float64, int64) {
	_ = dosage
	_ = depth
	_ = quality
	_ = minDepth
	_ = minQuality
	return 0, 0
}
