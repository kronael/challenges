package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	N     int     `json:"n"`
	Root  int     `json:"root"`
	Pnl   []int64 `json:"pnl"`
	Left  []int   `json:"left"`
	Right []int   `json:"right"`
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.N, in.Root, in.Pnl, in.Left, in.Right))
}
