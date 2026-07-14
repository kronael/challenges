// QUIZ 01 — Unsynchronised write
// Predict: what does this print? Is the output deterministic?
// Your answer: ________________________________

package main

import (
	"fmt"
	"time"
)

var x int

func main() {
	go func() { x = 42 }()
	time.Sleep(time.Millisecond)
	fmt.Println(x)
}

// Run with: make race QUIZ=01_unsynchronised_write.go
