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
	all, err := filepath.Glob("../cases/*.in")
	if err != nil {
		t.Fatal(err)
	}
	sort.Strings(all)
	inputs := make([]string, 0, len(all))
	for _, path := range all {
		if !strings.Contains(filepath.Base(path), "_large_") {
			inputs = append(inputs, path)
		}
	}
	if len(inputs) == 0 {
		t.Fatal("no small cases found in ../cases")
	}
	for _, path := range inputs {
		path := path
		t.Run(filepath.Base(path), func(t *testing.T) {
			raw, err := os.ReadFile(path)
			if err != nil {
				t.Fatal(err)
			}
			var in input
			if err := json.Unmarshal(raw, &in); err != nil {
				t.Fatal(err)
			}
			want, err := os.ReadFile(strings.TrimSuffix(path, ".in") + ".out")
			if err != nil {
				t.Fatal(err)
			}
			result, ok := solve(in.Masses, in.Spectrum)
			if got := format(result, ok); got != strings.TrimSpace(string(want)) {
				t.Fatalf("got %q want %q", got, strings.TrimSpace(string(want)))
			}
		})
	}
}
