package main

import (
	"encoding/json"
	"fmt"
	"os"
	"runtime"
)

type input struct {
	S string `json:"s"`
	T string `json:"t"`
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
	fmt.Println(solve(in.S, in.T))
}
