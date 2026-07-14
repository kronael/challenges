package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type item struct {
	Weight int `json:"weight"`
	Value  int `json:"value"`
}

type input struct {
	Capacity int    `json:"capacity"`
	Items    []item `json:"items"`
}

func solve(capacity int, items []item) int {
	_ = capacity
	_ = items
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Capacity, in.Items))
}
