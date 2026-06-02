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

// WHY: wg.Done() (internally a decrement + release store) happens-before
// wg.Wait() returns (internally a load that observes count==0).
// So all writes to results[] happen-before the fmt.Println.
// Output: [0 1 4 9 16] — always correct, always in order (indices are disjoint).
