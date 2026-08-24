package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	Horizontal [][3]int64 `json:"horizontal"`
	Vertical   [][3]int64 `json:"vertical"`
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Horizontal, in.Vertical))
}
