// QUIZ 10 — False sharing: measure it
// This is a benchmark, not a print quiz.
// Run: go test -bench=. -benchmem -cpu=2,4,8
// Predict: which struct layout is faster with multiple goroutines? Why?
// Your answer: ________________________________

package main

import (
	"sync"
	"sync/atomic"
	"testing"
)

// Two counters on the SAME cache line — false sharing
type SharedLine struct {
	a, b atomic.Int64
}

// Two counters on DIFFERENT cache lines — padding eliminates false sharing
type PaddedLine struct {
	a       atomic.Int64
	_padA   [56]byte // 56 + 8 = 64 bytes = one cache line
	b       atomic.Int64
	_padB   [56]byte
}

func BenchmarkFalseSharing(b *testing.B) {
	var s SharedLine
	var wg sync.WaitGroup
	b.ResetTimer()
	for range b.N {
		wg.Add(2)
		go func() { defer wg.Done(); s.a.Add(1) }()
		go func() { defer wg.Done(); s.b.Add(1) }()
		wg.Wait()
	}
}

func BenchmarkPadded(b *testing.B) {
	var s PaddedLine
	var wg sync.WaitGroup
	b.ResetTimer()
	for range b.N {
		wg.Add(2)
		go func() { defer wg.Done(); s.a.Add(1) }()
		go func() { defer wg.Done(); s.b.Add(1) }()
		wg.Wait()
	}
}

func main() {}

// WHY: When goroutines on different cores write to fields sharing a cache line,
// every write invalidates the other core's cache line (MESI protocol).
// PaddedLine puts each counter on its own cache line — no invalidation.
// Expected: Padded is 3-10x faster under contention on multi-core.
// Use `perf c2c` on Linux to directly observe cache-to-cache transfers.
