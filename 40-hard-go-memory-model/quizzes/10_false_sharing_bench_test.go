// QUIZ 10 — False sharing: measure it
// This is a benchmark, not a print quiz.
// Run: make bench
// Predict: which struct layout is faster with multiple goroutines? Why?
// Your answer: ________________________________

package main

import (
	"sync"
	"sync/atomic"
	"testing"
)

type SharedLine struct {
	a, b atomic.Int64
}

type PaddedLine struct {
	a     atomic.Int64
	_padA [56]byte
	b     atomic.Int64
	_padB [56]byte
}

func BenchmarkFalseSharing(b *testing.B) {
	var s SharedLine
	runCounterPair(b, s.a.Add, s.b.Add)
}

func BenchmarkPadded(b *testing.B) {
	var s PaddedLine
	runCounterPair(b, s.a.Add, s.b.Add)
}

func runCounterPair(b *testing.B, incA, incB func(int64) int64) {
	b.Helper()

	var wg sync.WaitGroup
	start := make(chan struct{})
	worker := func(inc func(int64) int64) {
		defer wg.Done()
		<-start
		for range b.N {
			inc(1)
		}
	}

	wg.Add(2)
	go worker(incA)
	go worker(incB)

	b.ResetTimer()
	close(start)
	wg.Wait()
}
