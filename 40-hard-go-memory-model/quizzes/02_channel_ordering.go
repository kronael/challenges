// QUIZ 02 — Channel ordering
// Predict: is the output always "done: 42"? Can it print "done: 0"?
// Your answer: ________________________________

package main

import "fmt"

func main() {
	c := make(chan struct{})
	x := 0
	go func() {
		x = 42
		c <- struct{}{}
	}()
	<-c
	fmt.Println("done:", x)
}

// Run with: make race QUIZ=02_channel_ordering.go
