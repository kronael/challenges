package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	Costs [][]int64 `json:"costs"`
}

func solve(costs [][]int64) int64 {
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Costs))
}
