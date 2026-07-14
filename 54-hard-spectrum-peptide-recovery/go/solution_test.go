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
			want, _ := os.ReadFile(strings.TrimSuffix(path, ".in") + ".out")
			result, ok := solve(in.Masses, in.Spectrum)
			if got := format(result, ok); got != strings.TrimSpace(string(want)) {
				t.Fatalf("got %q want %q", got, strings.TrimSpace(string(want)))
			}
		})
	}
}
