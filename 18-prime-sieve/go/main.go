package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	N int `json:"n"`
}

func solve(n int) int {
	// TODO: return the number of primes p with p < n
	_ = n
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.N))
}
