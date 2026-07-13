package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type op struct {
	kind string
	args []int
}

type input struct {
	Ops []op `json:"ops"`
}

func (in *input) UnmarshalJSON(data []byte) error {
	var raw struct {
		Ops [][]json.RawMessage `json:"ops"`
	}
	if err := json.Unmarshal(data, &raw); err != nil {
		return err
	}
	in.Ops = make([]op, len(raw.Ops))
	for i, r := range raw.Ops {
		if len(r) == 0 {
			return fmt.Errorf("empty op at %d", i)
		}
		var kind string
		if err := json.Unmarshal(r[0], &kind); err != nil {
			return err
		}
		args := make([]int, len(r)-1)
		for j := 1; j < len(r); j++ {
			if err := json.Unmarshal(r[j], &args[j-1]); err != nil {
				return err
			}
		}
		in.Ops[i] = op{kind: kind, args: args}
	}
	return nil
}

func solve(ops []op) []int {
	return nil
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	res := solve(in.Ops)
	parts := make([]string, len(res))
	for i, v := range res {
		parts[i] = fmt.Sprint(v)
	}
	fmt.Println(strings.Join(parts, " "))
}
