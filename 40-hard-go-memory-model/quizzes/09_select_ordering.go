// QUIZ 09 — select is non-deterministic
// Predict: what does this print? Is it deterministic?
// Your answer: ________________________________

package main

import "fmt"

func main() {
	c1 := make(chan int, 1)
	c2 := make(chan int, 1)
	c1 <- 1
	c2 <- 2

	select {
	case v := <-c1:
		fmt.Println("c1:", v)
	case v := <-c2:
		fmt.Println("c2:", v)
	}
}

// Run with: make race QUIZ=09_select_ordering.go
