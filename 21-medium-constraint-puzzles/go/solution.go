package main

// Split is one way to cut a slice into a prefix and a suffix that concatenate
// back to the original.
type Split struct {
	Prefix []int
	Suffix []int
}

// SolveNQueens returns EVERY placement of n queens on an n×n board where no two
// share a row, column, or diagonal. Index = row, value = column. n=0 yields one
// empty placement, n=4 yields 2, n=8 yields 92.
func SolveNQueens(n int) [][]int {
	_ = n
	panic("SolveNQueens: not implemented")
}

// SolveGraphColoring returns EVERY assignment of colors 0..k-1 to nodes 0..n-1
// where the endpoints of each edge differ. An impossible instance returns an
// empty slice.
func SolveGraphColoring(n int, edges [][2]int, k int) []map[int]int {
	_, _, _ = n, edges, k
	panic("SolveGraphColoring: not implemented")
}

// SolveSendMoreMoney returns EVERY assignment of distinct digits 0-9 to the
// letters S E N D M O R Y with SEND + MORE = MONEY and no leading zero on S or
// M. There is exactly one.
func SolveSendMoreMoney() []map[string]int {
	panic("SolveSendMoreMoney: not implemented")
}

// EnumerateSplits returns EVERY (prefix, suffix) pair that concatenates back to
// lst, shortest prefix first. For an empty input that is the single pair of two
// empty slices.
func EnumerateSplits(lst []int) []Split {
	_ = lst
	panic("EnumerateSplits: not implemented")
}

func main() {}
