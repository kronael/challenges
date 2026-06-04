package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct{}

func solve() int {
	// TODO: return the smallest sum of a pairwise-compatible set of five primes
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	_ = in
	fmt.Println(solve())
}
