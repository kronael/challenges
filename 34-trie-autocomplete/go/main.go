package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	Words   []string `json:"words"`
	Queries []string `json:"queries"`
}

func solve(words, queries []string) string {
	// Join query results with ";", and words inside one result with " ".
	_ = words
	_ = queries
	return ""
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Words, in.Queries))
}
