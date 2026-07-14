package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type operation struct {
	Type string `json:"type"`
	U    int    `json:"u"`
	V    int    `json:"v"`
}

type input struct {
	N          int         `json:"n"`
	Operations []operation `json:"operations"`
}

func solve(n int, operations []operation) []int {
	return nil
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	result := solve(in.N, in.Operations)
	parts := make([]string, len(result))
	for i, value := range result {
		parts[i] = strconv.Itoa(value)
	}
	fmt.Println(strings.Join(parts, " "))
}
