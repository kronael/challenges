package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	D      int      `json:"d"`
	Len    int      `json:"len"`
	Genome string   `json:"genome"`
	Guides []string `json:"guides"`
}

func solve(d, length int, genome string, guides []string) []int {
	// TODO: for each guide, count the length-`length` windows of `genome` within
	// Hamming distance `d` of it. Return one count per guide, in input order.
	_ = d
	_ = length
	_ = genome
	_ = guides
	return nil
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	counts := solve(in.D, in.Len, in.Genome, in.Guides)
	for i, x := range counts {
		if i > 0 {
			fmt.Print(" ")
		}
		fmt.Print(x)
	}
	fmt.Println()
}
