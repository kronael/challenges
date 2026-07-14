package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	A [][]int `json:"a"`
	B [][]int `json:"b"`
}

func solve(a, b [][]int) int {
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.A, in.B))
}
