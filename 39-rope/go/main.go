package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	Parts   []string `json:"parts"`
	Queries [][]int  `json:"queries"`
}

func solve(parts []string, queries [][]int) string {
	// TODO: build a rope from parts, answer [lo, hi) substring queries
	// Return extracted substrings joined by "|"
	return ""
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Parts, in.Queries))
}
