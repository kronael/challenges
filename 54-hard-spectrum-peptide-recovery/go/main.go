package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type input struct {
	Masses   []int64 `json:"masses"`
	Spectrum []int64 `json:"spectrum"`
}

func format(result []int64, ok bool) string {
	if !ok {
		return "NONE"
	}
	parts := make([]string, len(result))
	for i, value := range result {
		parts[i] = strconv.FormatInt(value, 10)
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
