package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	Width      int    `json:"width"`
	Separators []int  `json:"separators"`
	Stream     string `json:"stream"`
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	clean, stray := solve(in.Width, in.Separators, []byte(in.Stream))
	fmt.Println(clean, stray)
}
