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

// WHY: When multiple cases are ready, select chooses one uniformly at random
// (per the spec). Both c1 and c2 are buffered and immediately ready.
// Output is either "c1: 1" or "c2: 2" — non-deterministic.
// Run 20 times to observe both outputs.
// This trips people up when they assume select is FIFO or ordered by case position.
