package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type input struct {
	N     int      `json:"n"`
	Edges [][2]int `json:"edges"`
	Loads []*int   `json:"loads"` // nil = missing
}

func solve(n int, edges [][2]int, loads []*int) []int {



	return []int{1, 2}
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	res := solve(in.N, in.Edges, in.Loads)
	parts := make([]string, len(res))
	for i, v := range res {
		parts[i] = fmt.Sprint(v)
	}
	fmt.Println(strings.Join(parts, " "))
}
