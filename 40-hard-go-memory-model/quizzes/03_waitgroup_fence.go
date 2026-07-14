// QUIZ 03 — WaitGroup as memory barrier
// Predict: what does this print? Can results ever contain zeros?
// Your answer: ________________________________

package main

import (
	"fmt"
	"sync"
)

func main() {
	const N = 5
	results := make([]int, N)
	var wg sync.WaitGroup
	for i := range N {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			results[i] = i * i
		}(i)
	}
	wg.Wait()
	fmt.Println(results)
}

// Run with: make race QUIZ=03_waitgroup_fence.go
