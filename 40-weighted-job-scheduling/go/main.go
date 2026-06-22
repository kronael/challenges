package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type Job struct {
	Start  int64 `json:"start"`
	End    int64 `json:"end"`
	Weight int64 `json:"weight"`
}

type input struct {
	Jobs []Job `json:"jobs"`
}

func solve(jobs []Job) int64 {
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
