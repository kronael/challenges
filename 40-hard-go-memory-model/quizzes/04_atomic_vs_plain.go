// QUIZ 04 — Atomic vs plain read
// Predict: which version is race-free? If the store executes, what visibility
// does each version guarantee? Do not assume scheduler fairness or termination.
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
