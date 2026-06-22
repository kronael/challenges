package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type input struct {
	K   int   `json:"k"`
	Arr []int `json:"arr"`
}

func solve(k int, arr []int) []int {
	_ = k
	_ = arr
	return nil
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	out := solve(in.K, in.Arr)
	parts := make([]string, len(out))
	for i, v := range out {
		parts[i] = strconv.Itoa(v)
	}
	fmt.Println(strings.Join(parts, " "))
}
