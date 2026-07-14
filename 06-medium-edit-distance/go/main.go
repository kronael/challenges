package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	S string `json:"s"`
	T string `json:"t"`
}

func solve(s, t string) int {
	_ = s
	_ = t
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.S, in.T))
}
