package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"reflect"
	"sort"
	"strconv"
	"strings"
	"testing"
)

func TestCases(t *testing.T) {
	all, _ := filepath.Glob("../cases/*.in")
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
			err = json.NewDecoder(f).Decode(&in)
			f.Close()
			if err != nil {
				t.Fatalf("decode %s: %v", inp, err)
			}

			raw, err := os.ReadFile(strings.TrimSuffix(inp, ".in") + ".out")
			if err != nil {
				t.Fatalf("read .out for %s: %v", inp, err)
			}
			want := []int64{}
			for _, tok := range strings.Fields(string(raw)) {
				n, err := strconv.ParseInt(tok, 10, 64)
				if err != nil {
					t.Fatalf("parse .out for %s: %v", inp, err)
				}
				want = append(want, n)
			}

			got := solve(in.Feeds)
			if got == nil {
				got = []int64{}
			}
			if !reflect.DeepEqual(got, want) {
				t.Errorf("got %v want %v", got, want)
			}
		})
	}
}
