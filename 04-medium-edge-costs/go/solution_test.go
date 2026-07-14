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
		t.Fatalf("glob: %v", err)
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
		inp := inp
		t.Run(filepath.Base(inp), func(t *testing.T) {
			f, err := os.Open(inp)
			if err != nil {
				t.Fatalf("open %s: %v", inp, err)
			}
			var in input
			if err := json.NewDecoder(f).Decode(&in); err != nil {
				f.Close()
				t.Fatalf("decode %s: %v", inp, err)
			}
			f.Close()

			got := solve(in.N, in.Edges, in.Loads)

			expRaw, err := os.ReadFile(strings.TrimSuffix(inp, ".in") + ".out")
			if err != nil {
				t.Fatalf("read .out for %s: %v", inp, err)
			}
			var want []int
			for _, s := range strings.Fields(string(expRaw)) {
				v, err := strconv.Atoi(s)
				if err != nil {
					t.Fatalf("parse .out for %s: %v", inp, err)
				}
				want = append(want, v)
			}

			if len(got) != len(want) {
				t.Fatalf("len: got %d want %d", len(got), len(want))
			}
			for i := range got {
				if got[i] != want[i] {
					t.Errorf("[%d] got %d want %d", i, got[i], want[i])
				}
			}
		})
	}
}
