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
	all, err := filepath.Glob("../cases/*.in")
	if err != nil {
		t.Fatal(err)
	}
	sort.Strings(all)
	var ins []string
	for _, f := range all {
		if !strings.Contains(filepath.Base(f), "_large_") {
			ins = append(ins, f)
		}
	}
	if len(ins) == 0 {
		t.Fatal("no small cases found in ../cases")
	}
	for _, inp := range ins {
		t.Run(filepath.Base(inp), func(t *testing.T) {
			f, err := os.Open(inp)
			if err != nil {
				t.Fatal(err)
			}
			var in input
			if err := json.NewDecoder(f).Decode(&in); err != nil {
				f.Close()
				t.Fatal(err)
			}
			if err := f.Close(); err != nil {
				t.Fatal(err)
			}
			got := solve(in.Capacity, in.Ops)
			raw, err := os.ReadFile(strings.TrimSuffix(inp, ".in") + ".out")
			if err != nil {
				t.Fatal(err)
			}
			var want []int
			for _, s := range strings.Fields(string(raw)) {
				v, err := strconv.Atoi(s)
				if err != nil {
					t.Fatal(err)
				}
				want = append(want, v)
			}
			if len(got) != len(want) {
				t.Fatalf("len got=%d want=%d", len(got), len(want))
			}
			for i := range got {
				if got[i] != want[i] {
					t.Errorf("[%d] got %d want %d", i, got[i], want[i])
				}
			}
		})
	}
}
