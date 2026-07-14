package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	Parent     []int       `json:"parent"`
	Sequences  []*string   `json:"sequences"`
	Prior      []float64   `json:"prior"`
	Transition [][]float64 `json:"transition"`
}

func solve(parent []int, sequences []*string, prior []float64, transition [][]float64) float64 {
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Printf("%.6f\n", solve(in.Parent, in.Sequences, in.Prior, in.Transition))
}
