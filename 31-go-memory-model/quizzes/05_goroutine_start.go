// QUIZ 05 — Goroutine start ordering
// Predict: is "hello" always printed before "world"?
// Your answer: ________________________________

package main

import (
	"fmt"
	"sync"
)

func main() {
	var wg sync.WaitGroup
	wg.Add(2)

	go func() {
		defer wg.Done()
		fmt.Println("hello")
	}()

	go func() {
		defer wg.Done()
		fmt.Println("world")
	}()

	wg.Wait()
}

// WHY: The two goroutines run concurrently. There is no happens-before between
// the two fmt.Println calls. The order is non-deterministic — run it 10 times
// and you may see both orderings. "go" starts a goroutine but does NOT
// synchronise its execution relative to other goroutines.
