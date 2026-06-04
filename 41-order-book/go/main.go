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

// solve runs the order book and returns
// [numTrades, p1, q1, p2, q2, ..., bestBid, bidQty, bestAsk, askQty].
func solve(orders []order) []int {
	// TODO: implement the matching engine
	_ = orders
	return nil
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
