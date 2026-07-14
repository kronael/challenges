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

	done := make(chan struct{})
	go func() {
		defer close(done)
		mu.Lock()
		fmt.Println(a, b)
		mu.Unlock()
	}()

	<-done
}

// Run with: make race QUIZ=07_mutex_interleave.go
