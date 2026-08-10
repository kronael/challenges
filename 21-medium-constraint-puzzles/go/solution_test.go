package main

import (
	"fmt"
	"testing"
)

func validQueens(sol []int, n int) bool {
	if len(sol) != n {
		return false
	}
	seen := make(map[int]bool, n)
	for _, col := range sol {
		if col < 0 || col >= n || seen[col] {
			return false
		}
		seen[col] = true
	}
	for r1 := 0; r1 < n; r1++ {
		for r2 := r1 + 1; r2 < n; r2++ {
			d := sol[r1] - sol[r2]
			if d < 0 {
				d = -d
			}
			if d == r2-r1 {
				return false
			}
		}
	}
	return true
}

func distinct(sols [][]int) int {
	seen := make(map[string]bool, len(sols))
	for _, sol := range sols {
		seen[fmt.Sprint(sol)] = true
	}
	return len(seen)
}

func TestNQueensZeroHasEmptyBoardSolution(t *testing.T) {
	sols := SolveNQueens(0)
	if len(sols) != 1 || len(sols[0]) != 0 {
		t.Fatalf("got %v, want one empty placement", sols)
	}
}

func TestNQueensFourHasTwoSolutions(t *testing.T) {
	sols := SolveNQueens(4)
	if len(sols) != 2 {
		t.Fatalf("got %d solutions, want 2", len(sols))
	}
	for _, sol := range sols {
		if !validQueens(sol, 4) {
			t.Errorf("invalid placement %v", sol)
		}
	}
	if distinct(sols) != 2 {
		t.Errorf("solutions are not distinct: %v", sols)
	}
}

func TestNQueensEightHas92Solutions(t *testing.T) {
	sols := SolveNQueens(8)
	if len(sols) != 92 {
		t.Fatalf("got %d solutions, want 92", len(sols))
	}
	for _, sol := range sols {
		if !validQueens(sol, 8) {
			t.Errorf("invalid placement %v", sol)
		}
	}
	if distinct(sols) != 92 {
		t.Errorf("solutions are not distinct")
	}
}

func distinctColorings(sols []map[int]int, n int) int {
	seen := make(map[string]bool, len(sols))
	for _, c := range sols {
		key := ""
		for node := 0; node < n; node++ {
			key += fmt.Sprintf("%d,", c[node])
		}
		seen[key] = true
	}
	return len(seen)
}

func checkColorings(t *testing.T, sols []map[int]int, n, k int, edges [][2]int) {
	t.Helper()
	for _, coloring := range sols {
		if len(coloring) != n {
			t.Errorf("coloring %v does not assign all %d nodes", coloring, n)
			continue
		}
		for node := 0; node < n; node++ {
			color, ok := coloring[node]
			if !ok {
				t.Errorf("coloring %v is missing node %d", coloring, node)
			} else if color < 0 || color >= k {
				t.Errorf("node %d got color %d, want 0..%d", node, color, k-1)
			}
		}
		for _, e := range edges {
			if coloring[e[0]] == coloring[e[1]] {
				t.Errorf("edge %v has matching colors in %v", e, coloring)
			}
		}
	}
}

func TestTriangleThreeColoringHasSix(t *testing.T) {
	edges := [][2]int{{0, 1}, {1, 2}, {0, 2}}
	sols := SolveGraphColoring(3, edges, 3)
	if len(sols) != 6 {
		t.Fatalf("got %d colorings, want 6", len(sols))
	}
	checkColorings(t, sols, 3, 3, edges)
	if distinctColorings(sols, 3) != 6 {
		t.Errorf("colorings are not distinct: %v", sols)
	}
}

func TestIsolatedNodesAreStillColored(t *testing.T) {
	sols := SolveGraphColoring(3, nil, 2)
	if len(sols) != 8 {
		t.Fatalf("got %d colorings, want 8", len(sols))
	}
	checkColorings(t, sols, 3, 2, nil)
	if distinctColorings(sols, 3) != 8 {
		t.Errorf("colorings are not distinct: %v", sols)
	}
}

func TestK4ThreeColoringImpossible(t *testing.T) {
	edges := [][2]int{{0, 1}, {0, 2}, {0, 3}, {1, 2}, {1, 3}, {2, 3}}
	if sols := SolveGraphColoring(4, edges, 3); len(sols) != 0 {
		t.Fatalf("got %d colorings, want none", len(sols))
	}
}

func TestSendMoreMoneyUnique(t *testing.T) {
	sols := SolveSendMoreMoney()
	if len(sols) != 1 {
		t.Fatalf("got %d assignments, want 1", len(sols))
	}
	want := map[string]int{"S": 9, "E": 5, "N": 6, "D": 7, "M": 1, "O": 0, "R": 8, "Y": 2}
	if len(sols[0]) != len(want) {
		t.Fatalf("got %v, want %v", sols[0], want)
	}
	for letter, digit := range want {
		if sols[0][letter] != digit {
			t.Fatalf("got %v, want %v", sols[0], want)
		}
	}
}

func sameInts(got, want []int) bool {
	if len(got) != len(want) {
		return false
	}
	for i := range want {
		if got[i] != want[i] {
			return false
		}
	}
	return true
}

func TestEnumerateSplits(t *testing.T) {
	got := EnumerateSplits([]int{1, 2, 3})
	want := []Split{
		{Prefix: []int{}, Suffix: []int{1, 2, 3}},
		{Prefix: []int{1}, Suffix: []int{2, 3}},
		{Prefix: []int{1, 2}, Suffix: []int{3}},
		{Prefix: []int{1, 2, 3}, Suffix: []int{}},
	}
	if len(got) != len(want) {
		t.Fatalf("got %d splits, want %d", len(got), len(want))
	}
	for i := range want {
		if !sameInts(got[i].Prefix, want[i].Prefix) || !sameInts(got[i].Suffix, want[i].Suffix) {
			t.Errorf("split %d: got %v, want %v", i, got[i], want[i])
		}
	}

	empty := EnumerateSplits(nil)
	if len(empty) != 1 || len(empty[0].Prefix) != 0 || len(empty[0].Suffix) != 0 {
		t.Errorf("got %v, want a single empty split", empty)
	}
}
