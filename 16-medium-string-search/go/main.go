package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type input struct {
	Text    string `json:"text"`
	Pattern string `json:"pattern"`
}

func solve(text, pattern string) []int {
	_ = text
	_ = pattern
	return nil
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	pos := solve(in.Text, in.Pattern)
	parts := make([]string, len(pos))
	for i, p := range pos {
		parts[i] = strconv.Itoa(p)
	}
	fmt.Println(strings.Join(parts, " "))
}
