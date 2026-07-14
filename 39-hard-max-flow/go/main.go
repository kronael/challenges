package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	N     int       `json:"n"`
	Edges [][]int64 `json:"edges"`
}

func solve(n int, edges [][]int64) int64 {
	_ = n
	_ = edges
	panic("TODO")
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.N, in.Edges))
}
