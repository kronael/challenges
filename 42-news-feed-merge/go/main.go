package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type event struct {
	Ts int `json:"ts"`
	ID int `json:"id"`
}

type input struct {
	Feeds [][]event `json:"feeds"`
}

func solve(feeds [][]event) []int {
	// TODO: merge the K sorted feeds by ts (tie-break feed index, then id);
	// return a flat slice [ts, id, ts, id, ...] in merged order
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
		parts[i] = strconv.Itoa(v)
	}
	fmt.Println(strings.Join(parts, " "))
}
