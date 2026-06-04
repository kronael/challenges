package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	N      int   `json:"n"`
	Prices []int `json:"prices"`
}

func solve(prices []int) int {
	// TODO: return the maximum drawdown, max over i<j of (prices[i] - prices[j])
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Prices))
}
