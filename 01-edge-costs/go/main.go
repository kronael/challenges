package main

import (
	"encoding/json"
	"fmt"
	"os"
	"slices"
	"strings"
)

type input struct {
	N     int      `json:"n"`
	Edges [][2]int `json:"edges"`
	Loads []*int   `json:"loads"` // nil = missing
}

func solve(n int, edges [][2]int, loads []*int) []int {

	vis := [][2]int{}
	for i, v := range loads {
		if v != nil {
			vis = append(vis, [2]int{i, *v})
		}
	}

	adj := make([][]int, n)
	for _, edge := range edges {
		adj[edge[0]] = append(adj[edge[0]], edge[1])
		adj[edge[1]] = append(adj[edge[1]], edge[0])
	}

	for {
		slices.SortFunc(vis, func(a, b [2]int) int {
			return a[1] - b[1]
		})
		if len(vis) == 0 {
			break
		}
		vx := vis[len(vis)-1]
		vertex := vx[0]
		vis = vis[:len(vis)-1]
		for _, edge := range adj[vertex] {
			if loads[edge] == nil {
				max_load := 1
				for _, other := range adj[edge] {
					v := loads[other]
					if v != nil && *v > max_load {
						max_load = *v
					}
				}
				v := max_load - 1
				loads[edge] = &v
				vis = append(vis, [2]int{edge, v})
			}
		}
	}

	ans := []int{}
	for _, v := range loads {
		if v == nil {
			x := 0
			v = &x
		}
		ans = append(ans, *v)
	}

	return ans
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	res := solve(in.N, in.Edges, in.Loads)
	parts := make([]string, len(res))
	for i, v := range res {
		parts[i] = fmt.Sprint(v)
	}
	fmt.Println(strings.Join(parts, " "))
}
