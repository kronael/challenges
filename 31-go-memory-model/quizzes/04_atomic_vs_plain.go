// QUIZ 04 — Atomic vs plain read
// Predict: which of these two goroutines can loop forever? Which is guaranteed to terminate?
// Your answer: ________________________________

package main

import (
	"sync/atomic"
)

func main() {
	// Version A: plain variable
	stopA := false
	go func() { stopA = true }()
	for !stopA {
	}

	// Version B: atomic
	var stopB atomic.Bool
	go func() { stopB.Store(true) }()
	for !stopB.Load() {
	}
}

// Compile with: make compile QUIZ=04_atomic_vs_plain.go
// Run only with your own timeout.
