// QUIZ 08 — Close happens-before receive
// Predict: can any goroutine print a non-zero value? Can any print zero?
// Your answer: ________________________________

package main

import (
	"fmt"
	"sync"
)

func main() {
	c := make(chan struct{})
	x := 0

	go func() {
		x = 100
		close(c)
	}()

	var wg sync.WaitGroup
	for range 5 {
		wg.Add(1)
		go func() {
			defer wg.Done()
			<-c            // receives zero value after close
			fmt.Println(x) // what can this be?
		}()
	}
	wg.Wait()
}

// WHY: Closing a channel happens-before a receive of the zero value from that
// channel (go.dev/ref/mem). So x=100 happens-before close(c) happens-before
// each <-c. All goroutines see x==100. Output: five lines of "100".
// Contrast: if you used a buffered channel and sent values instead of closing,
// only the goroutines that received an actual value would have the guarantee.
