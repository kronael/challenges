package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type input struct {
	N      int   `json:"n"`
	Prices []int `json:"prices"`
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	out := solve(in.N, in.Prices)
	parts := make([]string, len(out))
	for i, v := range out {
		parts[i] = strconv.Itoa(v)
	}
	fmt.Println(strings.Join(parts, " "))
}
