package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	Reads []string `json:"reads"`
}

func solve(reads []string) string {
	// TODO: return the shortest superstring containing every read (the reassembled chromosome)
	return ""
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Reads))
}
