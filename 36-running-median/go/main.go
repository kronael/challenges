package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type input struct {
	Stream []float64 `json:"stream"`
}

func solve(stream []float64) []string {
	// TODO: return median after each insertion
	// Format: integer if count is odd, one-decimal float if even
	return make([]string, len(stream))
}

func main() {
	var in input
	json.NewDecoder(os.Stdin).Decode(&in)
	fmt.Println(strings.Join(solve(in.Stream), " "))
}
