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

// Run with: go run -race 01_unsynchronised_write.go
// The race detector will flag this even if the output looks correct.
// WHY: time.Sleep is NOT a synchronisation event. The Go memory model
// gives no guarantee that the write to x is visible in main.
// On current amd64 hardware it usually prints 42 — but it's undefined behaviour.
