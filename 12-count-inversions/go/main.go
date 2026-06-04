package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	N   int   `json:"n"`
	Arr []int `json:"arr"`
}

func solve(arr []int) int64 {
	// TODO: return the number of inversions (pairs i < j with arr[i] > arr[j])
	_ = arr
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Arr))
}
