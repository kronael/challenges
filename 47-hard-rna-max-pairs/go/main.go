package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type input struct {
	Rna         string `json:"rna"`
	MinLoop     int    `json:"min_loop"`
	AllowWobble bool   `json:"allow_wobble"`
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Rna, in.MinLoop, in.AllowWobble))
}
