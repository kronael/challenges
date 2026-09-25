package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
	"testing"
)

func TestCases(t *testing.T) {
	inputs, err := filepath.Glob("../cases/*.in")
	if err != nil {
		t.Fatal(err)
	}
	sort.Strings(inputs)
	if len(inputs) == 0 {
		t.Fatal("no cases found in ../cases")
	}
	for _, path := range inputs {
		t.Run(filepath.Base(path), func(t *testing.T) {
			raw, err := os.ReadFile(path)
			if err != nil {
				t.Fatal(err)
			}
			var in input
			if err := json.Unmarshal(raw, &in); err != nil {
				t.Fatal(err)
			}
			out, err := os.ReadFile(strings.TrimSuffix(path, ".in") + ".out")
			if err != nil {
				t.Fatal(err)
			}
			want := strings.TrimRight(string(out), "\n")
			kept := solve(in.Scores, in.Threshold)
			parts := make([]string, len(kept))
			for i, score := range kept {
				parts[i] = strconv.FormatInt(int64(score), 10)
			}
			if got := strings.Join(parts, " "); got != want {
				t.Fatalf("got %q want %q", got, want)
			}
		})
	}
}
