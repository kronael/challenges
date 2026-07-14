package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	N     int     `json:"n"`
	Edges [][]int `json:"edges"`
}

func solve(n int, edges [][]int) int64 {
	_ = n
	_ = edges
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.N, in.Edges))
}
