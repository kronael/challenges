package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type Job struct {
	Start  int `json:"start"`
	End    int `json:"end"`
	Weight int `json:"weight"`
}

type input struct {
	Jobs []Job `json:"jobs"`
}

func solve(jobs []Job) int {
	// TODO: return maximum total weight of non-overlapping jobs
	_ = jobs
	return 0
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Jobs))
}
