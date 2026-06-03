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
	return 0
}

func main() {
	var in input
	json.NewDecoder(os.Stdin).Decode(&in)
	fmt.Println(solve(in.Jobs))
}
