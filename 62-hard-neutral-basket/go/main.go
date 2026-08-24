package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	N         int     `json:"n"`
	Target    int64   `json:"target"`
	Exposures []int64 `json:"exposures"`
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.N, in.Target, in.Exposures))
}
