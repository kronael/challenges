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

// Run with: make race QUIZ=05_goroutine_start.go
