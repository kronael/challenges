package main

import (
	"encoding/json"
	"fmt"
	"os"
	"runtime"
	"strconv"
	"strings"
)

type input struct {
	Scores    []int32 `json:"scores"`
	Threshold int32   `json:"threshold"`
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
	kept := solve(in.Scores, in.Threshold)
	parts := make([]string, len(kept))
	for i, score := range kept {
		parts[i] = strconv.FormatInt(int64(score), 10)
	}
	fmt.Println(strings.Join(parts, " "))
}
