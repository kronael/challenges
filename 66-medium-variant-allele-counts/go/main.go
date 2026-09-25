package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type sample struct {
	Genotype int32 `json:"genotype"`
	Depth    int32 `json:"depth"`
	Quality  int32 `json:"quality"`
}

type input struct {
	Samples    []*sample `json:"samples"`
	MinDepth   int32     `json:"min_depth"`
	MinQuality int32     `json:"min_quality"`
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	alleleCount, calledAlleles := solve(in.Samples, in.MinDepth, in.MinQuality)
	fmt.Println(alleleCount, calledAlleles)
}
