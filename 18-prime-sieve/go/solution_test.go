package main

import (
	"path/filepath"
	"sort"
	"testing"
)

func TestCases(t *testing.T) {
	ins, _ := filepath.Glob("../cases/*.in")
	sort.Strings(ins)
	for _, inp := range ins {
		inp := inp
		t.Run(filepath.Base(inp), func(t *testing.T) {
			_ = inp // TODO
		})
	}
}
