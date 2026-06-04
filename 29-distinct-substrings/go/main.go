package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	S string `json:"s"`
}

func solve(s string) int {
	// TODO: count the number of distinct non-empty substrings of s
	_ = s
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.S))
}
