package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type event struct {
	Ts int64 `json:"ts"`
	ID int64 `json:"id"`
}

type input struct {
	Feeds [][]event `json:"feeds"`
}

func solve(feeds [][]event) []int64 {
	_ = feeds
	return nil
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	out := solve(in.Feeds)
	parts := make([]string, len(out))
	for i, v := range out {
		parts[i] = strconv.FormatInt(v, 10)
	}
	fmt.Println(strings.Join(parts, " "))
}
