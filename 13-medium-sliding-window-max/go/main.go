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
	K   int     `json:"k"`
	Arr []int32 `json:"arr"`
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
	out := solve(in.K, in.Arr)
	parts := make([]string, len(out))
	for i, v := range out {
		parts[i] = strconv.Itoa(int(v))
	}
	fmt.Println(strings.Join(parts, " "))
}
