package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type op struct {
	Kind string
	A    int
	B    int
}

func (o *op) UnmarshalJSON(data []byte) error {
	var raw []json.RawMessage
	if err := json.Unmarshal(data, &raw); err != nil {
		return err
	}
	if len(raw) != 3 {
		return fmt.Errorf("op needs 3 fields, got %d", len(raw))
	}
	if err := json.Unmarshal(raw[0], &o.Kind); err != nil {
		return err
	}
	if err := json.Unmarshal(raw[1], &o.A); err != nil {
		return err
	}
	return json.Unmarshal(raw[2], &o.B)
}

type input struct {
	N      int     `json:"n"`
	Values []int64 `json:"values"`
	Ops    []op    `json:"ops"`
}

func solve(n int, values []int64, ops []op) []int64 {
	_, _, _ = n, values, ops
	return nil
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	out := solve(in.N, in.Values, in.Ops)
	parts := make([]string, len(out))
	for i, v := range out {
		parts[i] = fmt.Sprintf("%d", v)
	}
	fmt.Println(strings.Join(parts, " "))
}
