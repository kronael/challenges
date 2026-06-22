package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	K     int     `json:"k"`
	Pages []int64 `json:"pages"`
}

func solve(k int, pages []int64) int64 {
	_ = k
	_ = pages
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.K, in.Pages))
}
