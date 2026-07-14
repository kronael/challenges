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
			fields := strings.Fields(string(out))
			want := make([]int, len(fields))
			for i, field := range fields {
				want[i], _ = strconv.Atoi(field)
			}
			got := solve(in.Processes, in.Events)
			if len(got) != len(want) {
				t.Fatalf("got %v want %v", got, want)
			}
			for i := range got {
				if got[i] != want[i] {
					t.Fatalf("got %v want %v", got, want)
				}
			}
		})
	}
}
