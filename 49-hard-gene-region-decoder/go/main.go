package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type input struct {
	Sequence   string    `json:"sequence"`
	Start      []int64   `json:"start"`
	Transition [][]int64 `json:"transition"`
	Emission   [][]int64 `json:"emission"`
}

func solve(sequence string, start []int64, transition, emission [][]int64) []int {
	return nil
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	result := solve(in.Sequence, in.Start, in.Transition, in.Emission)
	parts := make([]string, len(result))
	for index, state := range result {
		parts[index] = fmt.Sprint(state)
	}
	fmt.Println(strings.Join(parts, " "))
}
