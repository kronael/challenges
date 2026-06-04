package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	N int64 `json:"n"`
}

func solve(n int64) int64 {
	// TODO: return F(n) mod 1_000_000_007
	_ = n
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.N))
}
