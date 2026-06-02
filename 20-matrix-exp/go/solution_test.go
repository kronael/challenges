package main

import (
	"path/filepath"
	"sort"
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
		inp := inp
		t.Run(filepath.Base(inp), func(t *testing.T) {
			_ = inp // TODO
		})
	}
}
