package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	Arr []int64 `json:"arr"`
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Arr))
}
