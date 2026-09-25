package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	Dosage     []float64 `json:"dosage"`
	Depth      []int32   `json:"depth"`
	Quality    []int32   `json:"quality"`
	MinDepth   int32     `json:"min_depth"`
	MinQuality int32     `json:"min_quality"`
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	alleleCount, calledAlleles := solve(in.Dosage, in.Depth, in.Quality, in.MinDepth, in.MinQuality)
	fmt.Printf("%.12f %d\n", alleleCount, calledAlleles)
}
