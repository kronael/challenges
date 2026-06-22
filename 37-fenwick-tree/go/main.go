package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type query struct {
	op    string
	i     int
	delta int64
}

type input struct {
	N       int
	Initial []int64
	Queries []query
}

func (in *input) UnmarshalJSON(b []byte) error {
	var raw struct {
		N       int                 `json:"n"`
		Initial []int64             `json:"initial"`
		Queries [][]json.RawMessage `json:"queries"`
	}
	if err := json.Unmarshal(b, &raw); err != nil {
		return err
	}
	in.N = raw.N
	in.Initial = raw.Initial
	in.Queries = make([]query, len(raw.Queries))
	for k, q := range raw.Queries {
		if err := json.Unmarshal(q[0], &in.Queries[k].op); err != nil {
			return err
		}
		if err := json.Unmarshal(q[1], &in.Queries[k].i); err != nil {
			return err
		}
		if len(q) > 2 {
			if err := json.Unmarshal(q[2], &in.Queries[k].delta); err != nil {
				return err
			}
		}
	}
	return nil
}

func solve(n int, initial []int64, queries []query) []int64 {
	_ = n
	_ = initial
	_ = queries
	return nil
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	res := solve(in.N, in.Initial, in.Queries)
	parts := make([]string, len(res))
	for i, v := range res {
		parts[i] = strconv.FormatInt(v, 10)
	}
	fmt.Println(strings.Join(parts, " "))
}
