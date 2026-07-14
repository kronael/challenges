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

// Run with: make race QUIZ=06_once_init.go
