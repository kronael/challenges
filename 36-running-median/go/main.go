package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type input struct {
	Stream []int64 `json:"stream"`
}

func solve(stream []int64) []string {
	// TODO: return the median after each insertion
	// Format: integer if count is odd, one-decimal float if even (e.g. "5" or "4.5")
	_ = stream
	return nil
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(strings.Join(solve(in.Stream), " "))
}
