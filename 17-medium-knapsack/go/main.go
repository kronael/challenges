package main

import (
	"encoding/json"
	"fmt"
	"os"
	"runtime"
)

type item struct {
	Weight int   `json:"weight"`
	Value  int64 `json:"value"`
}

type input struct {
	Capacity int    `json:"capacity"`
	Items    []item `json:"items"`
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
	fmt.Println(solve(in.Capacity, in.Items))
}
