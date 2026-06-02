package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"testing"
)

func TestCases(t *testing.T) {
	all, _ := filepath.Glob("../cases/*.in")
	sort.Strings(all)
	var ins []string
	for _, f := range all {
		if \!strings.Contains(filepath.Base(f), "_large_") {
			ins = append(ins, f)
		}
	}
	for _, inp := range ins {
		t.Run(filepath.Base(inp), func(t *testing.T) {
			f, _ := os.Open(inp)
			var in input
			json.NewDecoder(f).Decode(&in)
			f.Close()
			got := solve(in.Stream)
			raw, _ := os.ReadFile(strings.TrimSuffix(inp, ".in") + ".out")
			want := strings.Fields(string(raw))
			if len(got) != len(want) {
				t.Fatalf("len got=%d want=%d", len(got), len(want))
			}
			for i := range got {
				if got[i] != want[i] {
					t.Errorf("[%d] got %s want %s", i, got[i], want[i])
				}
			}
		})
	}
}
