package main

import (
	"encoding/json"
	"fmt"
	"os"
	"runtime"
)

type input struct {
	D      int      `json:"d"`
	Len    int      `json:"len"`
	Genome string   `json:"genome"`
	Guides []string `json:"guides"`
}

// init keeps the main goroutine, and so solve, on the thread the program
// started on: `make vec` single-steps that one thread.
func init() {
	runtime.LockOSThread()
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	counts := solve(in.D, in.Len, in.Genome, in.Guides)
	for i, x := range counts {
		if i > 0 {
			fmt.Print(" ")
		}
		fmt.Print(x)
	}
	fmt.Println()
}
