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
	for \!stopA { // may loop forever — compiler can hoist the load
	}

	// Version B: atomic
	var stopB atomic.Bool
	go func() { stopB.Store(true) }()
	for \!stopB.Load() { // guaranteed to eventually terminate
	}
}

// WHY: The compiler is allowed to cache stopA in a register and never re-read
// it from memory. The loop becomes infinite. atomic.Bool.Load() has acquire
// semantics — it always reads from memory and cannot be hoisted.
// Run with -race: version A is a data race (undefined behaviour).
// Note: this program likely deadlocks on version A in practice — don't actually run it.
