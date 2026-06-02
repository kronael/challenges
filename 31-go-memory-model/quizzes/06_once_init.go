// QUIZ 06 — sync.Once visibility
// Predict: can any goroutine ever see val == 0 inside the print loop?
// Your answer: ________________________________

package main

import (
	"fmt"
	"sync"
)

var (
	val  int
	once sync.Once
)

func init_val() {
	val = 99
}

func main() {
	var wg sync.WaitGroup
	for range 10 {
		wg.Add(1)
		go func() {
			defer wg.Done()
			once.Do(init_val)
			fmt.Println(val)
		}()
	}
	wg.Wait()
}

// WHY: sync.Once guarantees that init_val runs exactly once AND that the
// return from once.Do in every goroutine happens-after the init_val call
// completes. So all goroutines see val == 99. This is the canonical
// safe lazy initialisation pattern.
