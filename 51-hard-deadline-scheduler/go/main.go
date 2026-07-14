package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type command struct {
	Operation string
	ID        int
	Value     int64
}

func (cmd *command) UnmarshalJSON(data []byte) error {
	var fields []json.RawMessage
	if err := json.Unmarshal(data, &fields); err != nil {
		return err
	}
	if err := json.Unmarshal(fields[0], &cmd.Operation); err != nil {
		return err
	}
	if cmd.Operation == "advance" {
		return json.Unmarshal(fields[1], &cmd.Value)
	}
	if err := json.Unmarshal(fields[1], &cmd.ID); err != nil {
		return err
	}
	if cmd.Operation == "schedule" {
		return json.Unmarshal(fields[2], &cmd.Value)
	}
	return nil
}

type input struct {
	Commands []command `json:"commands"`
}

func solve(commands []command) []int {
	return nil
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	result := solve(in.Commands)
	parts := make([]string, len(result))
	for index, timerID := range result {
		parts[index] = fmt.Sprint(timerID)
	}
	fmt.Println(strings.Join(parts, " "))
}
