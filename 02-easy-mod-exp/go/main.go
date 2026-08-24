package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	Base int64 `json:"base"`
	Exp  int64 `json:"exp"`
	Mod  int64 `json:"mod"`
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Base, in.Exp, in.Mod))
}
