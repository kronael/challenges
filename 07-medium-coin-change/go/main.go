package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	Amount int     `json:"amount"`
	Coins  []int64 `json:"coins"`
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Amount, in.Coins))
}
