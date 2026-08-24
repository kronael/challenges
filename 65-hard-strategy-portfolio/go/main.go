package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	N        int      `json:"n"`
	Pnl      []int64  `json:"pnl"`
	Requires [][2]int `json:"requires"`
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.N, in.Pnl, in.Requires))
}
