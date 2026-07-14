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
	all, _ := filepath.Glob("../cases/*.in")
	sort.Strings(all)
	for _, path := range all {
		if strings.Contains(filepath.Base(path), "_large_") {
			continue
		}
		t.Run(filepath.Base(path), func(t *testing.T) {
			raw, _ := os.ReadFile(path)
			var in input
			if err := json.Unmarshal(raw, &in); err != nil {
				t.Fatal(err)
			}
			out, _ := os.ReadFile(strings.TrimSuffix(path, ".in") + ".out")
			want, _ := strconv.Atoi(strings.TrimSpace(string(out)))
			if got := solve(in.A, in.B); got != want {
				t.Fatalf("got %d want %d", got, want)
			}
		})
	}
}
