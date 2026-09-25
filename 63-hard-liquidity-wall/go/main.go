package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	N          int     `json:"n"`
	Quantities []int64 `json:"quantities"`
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.N, in.Quantities))
}
