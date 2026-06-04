package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type op struct {
	kind string
	key  int
	val  int
}

type input struct {
	Capacity int  `json:"capacity"`
	Ops      []op `json:"ops"`
}

// ops arrive as heterogeneous JSON arrays: ["get",k] or ["put",k,v].
func (o *op) UnmarshalJSON(data []byte) error {
	var raw []json.RawMessage
	if err := json.Unmarshal(data, &raw); err != nil {
		return err
	}
	if err := json.Unmarshal(raw[0], &o.kind); err != nil {
		return err
	}
	if err := json.Unmarshal(raw[1], &o.key); err != nil {
		return err
	}
	if len(raw) > 2 {
		if err := json.Unmarshal(raw[2], &o.val); err != nil {
			return err
		}
	}
	return nil
}

func solve(capacity int, ops []op) []int {
	// TODO: implement LRU cache; return results of "get" ops (-1 if miss)
	// each op is {kind: "get"|"put", key, val}
	_ = capacity
	_ = ops
	return nil
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	res := solve(in.Capacity, in.Ops)
	parts := make([]string, len(res))
	for i, v := range res {
		parts[i] = fmt.Sprint(v)
	}
	fmt.Println(strings.Join(parts, " "))
}
