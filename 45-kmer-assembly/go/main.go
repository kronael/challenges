package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	K     int      `json:"k"`
	Kmers []string `json:"kmers"`
}

func solve(k int, kmers []string) string {
	// TODO: reconstruct and return the original DNA string from the k-mers
	_ = k
	_ = kmers
	return ""
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.K, in.Kmers))
}
