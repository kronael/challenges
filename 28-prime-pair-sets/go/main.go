package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	Size *int `json:"size"`
}

func solve(size int) int {
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	size := 5
	if in.Size != nil {
		size = *in.Size
	}
	fmt.Println(solve(size))
}
