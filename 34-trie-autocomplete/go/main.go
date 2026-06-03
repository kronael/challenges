package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type input struct {
	Words   []string `json:"words"`
	Queries []string `json:"queries"`
}

func solve(words, queries []string) string {
	// TODO: build a trie; for each query return up to 3 lex-smallest completions
	// join query results with ";", completions within a result with " "
	return strings.Join(make([]string, len(queries)), ";")
}

func main() {
	var in input
	json.NewDecoder(os.Stdin).Decode(&in)
	fmt.Println(solve(in.Words, in.Queries))
}
