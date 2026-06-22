// QUIZ 08 — Close channel receive
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

// Run with: make race QUIZ=08_close_channel.go
