package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	Amount int   `json:"amount"`
	Coins  []int `json:"coins"`
}

func solve(amount int, coins []int) int {
	// TODO: return the minimum number of coins summing to amount, or -1 if impossible
	_ = amount
	_ = coins
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Amount, in.Coins))
}
