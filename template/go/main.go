package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type input struct {
	N    int   `json:"n"`
	Data []int `json:"data"`
}

func solve(n int, data []int) []int {
	// TODO
	return nil
}

func main() {
	var in input
	json.NewDecoder(os.Stdin).Decode(&in)
	res := solve(in.N, in.Data)
	parts := make([]string, len(res))
	for i, v := range res {
		parts[i] = fmt.Sprint(v)
	}
	fmt.Println(strings.Join(parts, " "))
}
