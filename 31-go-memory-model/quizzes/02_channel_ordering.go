// QUIZ 02 — Channel as happens-before
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

// WHY: The send on c (in the goroutine) happens-before the receive completes
// (in main). Therefore x=42 is visible after <-c. Output is always "done: 42".
// Remove the channel and it becomes quiz 01.
