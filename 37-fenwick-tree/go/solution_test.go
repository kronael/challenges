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
	ins, _ := filepath.Glob("../cases/*.in")
	sort.Strings(ins)
	for _, inp := range ins {
		t.Run(filepath.Base(inp), func(t *testing.T) {
			f, _ := os.Open(inp)
			var in input
			json.NewDecoder(f).Decode(&in)
			f.Close()
			got := solve(in.N, in.Initial, in.Queries)
			raw, _ := os.ReadFile(strings.TrimSuffix(inp, ".in") + ".out")
			var want []int64
			for _, s := range strings.Fields(string(raw)) {
				v, _ := strconv.ParseInt(s, 10, 64)
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
