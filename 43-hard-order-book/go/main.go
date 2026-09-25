package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type order struct {
	Side  string `json:"side"`
	Price int    `json:"price"`
	Qty   int    `json:"qty"`
	Type  string `json:"type"`
}

type input struct {
	Orders []order `json:"orders"`
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	out := solve(in.Orders)
	parts := make([]string, len(out))
	for i, v := range out {
		parts[i] = fmt.Sprint(v)
	}
	fmt.Println(strings.Join(parts, " "))
}
