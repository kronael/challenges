// QUIZ 07 — Mutex ordering
// Predict: what values can this program print for 'a' and 'b'?
// List all possible outputs.
// Your answer: ________________________________

package main

import (
	"fmt"
	"sync"
)

func main() {
	var mu sync.Mutex
	a, b := 0, 0

	go func() {
		mu.Lock()
		a = 1
		mu.Unlock()

		mu.Lock()
		b = 2
		mu.Unlock()
	}()

	go func() {
		mu.Lock()
		fmt.Println(a, b)
		mu.Unlock()
	}()

	var wg sync.WaitGroup
	wg.Add(0) // not actually waiting — intentionally racy for analysis
	_ = wg
	select {} // block forever so goroutines run
}

// WHY: The second goroutine can acquire the mutex at any of 3 points:
// before a=1, between a=1 and b=2, or after b=2.
// Possible outputs: "0 0", "1 0", "1 2"
// "0 2" is NOT possible: b=2 only runs after a=1 (sequenced in the goroutine).
// This is a classic exam question: the mutex synchronises, but the ORDER
// of acquisition is non-deterministic.
