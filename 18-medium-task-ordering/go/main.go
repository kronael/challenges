package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type input struct {
	N     int     `json:"n"`
	Edges [][]int `json:"edges"`
}

func solve(n int, edges [][]int) []int {
	_ = n
	_ = edges
	return nil
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	order := solve(in.N, in.Edges)
	if order == nil {
		fmt.Println("CYCLE")
		return
	}
	parts := make([]string, len(order))
	for i, v := range order {
		parts[i] = strconv.Itoa(v)
	}
	fmt.Println(strings.Join(parts, " "))
}
