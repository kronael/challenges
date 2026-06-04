package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	Dims []int `json:"dims"`
}

func solve(dims []int) int {
	// TODO: return the minimum number of scalar multiplications
	_ = dims
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Dims))
}
