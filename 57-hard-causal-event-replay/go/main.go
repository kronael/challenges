package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type event struct {
	ID      int64 `json:"id"`
	Process int   `json:"process"`
	Clock   []int `json:"clock"`
}

type input struct {
	Processes int     `json:"processes"`
	Events    []event `json:"events"`
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	result := solve(in.Processes, in.Events)
	parts := make([]string, len(result))
	for i, value := range result {
		parts[i] = strconv.FormatInt(value, 10)
	}
	fmt.Println(strings.Join(parts, " "))
}
