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
	_ = amount
	_ = coins
	panic("TODO")
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Amount, in.Coins))
}
