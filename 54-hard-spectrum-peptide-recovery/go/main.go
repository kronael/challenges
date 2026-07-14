package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type input struct {
	Masses   []int `json:"masses"`
	Spectrum []int `json:"spectrum"`
}

func solve(masses, spectrum []int) ([]int, bool) {
	return nil, false
}

func format(result []int, ok bool) string {
	if !ok {
		return "NONE"
	}
	parts := make([]string, len(result))
	for i, value := range result {
		parts[i] = strconv.Itoa(value)
	}
	return strings.Join(parts, " ")
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	result, ok := solve(in.Masses, in.Spectrum)
	fmt.Println(format(result, ok))
}
