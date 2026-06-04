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

func solve(n int, edges [][]int) []int64 {
	// TODO: return the shortest distance from node 0 to each node, -1 if unreachable
	_ = n
	_ = edges
	return nil
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	d := solve(in.N, in.Edges)
	for i, x := range d {
		if i > 0 {
			fmt.Print(" ")
		}
		fmt.Print(x)
	}
	fmt.Println()
}
