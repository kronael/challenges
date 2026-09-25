package main

import (
	"encoding/json"
	"fmt"
	"os"
	"runtime"
)

type input struct {
	Width      int    `json:"width"`
	Separators []int  `json:"separators"`
	Stream     string `json:"stream"`
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
	clean, stray := solve(in.Width, in.Separators, []byte(in.Stream))
	fmt.Println(clean, stray)
}
