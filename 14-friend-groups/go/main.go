package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type input struct {
	N       int     `json:"n"`
	Unions  [][]int `json:"unions"`
	Queries [][]int `json:"queries"`
}

func solve(n int, unions, queries [][]int) []int {
	_, _, _ = n, unions, queries
	return nil
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	out := solve(in.N, in.Unions, in.Queries)
	parts := make([]string, len(out))
	for i, v := range out {
		parts[i] = strconv.Itoa(v)
	}
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()
	fmt.Fprintln(w, strings.Join(parts, " "))
}
