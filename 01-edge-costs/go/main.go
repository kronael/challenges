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

	vis := []int{}
	for i, v := range loads {
		if v != nil {
			vis = append(vis, i)
		}
	}

	for _, v := range slices.Clone(edges) {
		edges = append(edges, [2]int{v[1], v[0]})
	}

	for {
		slices.Sort(vis)
		if len(vis) == 0 {
			break
		}
		vertex := vis[len(vis)-1]
		vis = vis[:len(vis)-1]
		fmt.Println(*loads[vertex])
		for _, edge := range edges {
			max_load := 1
			if vertex == edge[0] && loads[edge[1]] == nil {
				for _, other := range edges {
					if edge[1] == other[0] {
						v := loads[other[1]]
						if v != nil && *v > max_load {
							max_load = *v
						}
					}
				}
				v := max_load - 1
				loads[edge[1]] = &v
				vis = append(vis, edge[1])
			}
		}
	}

	ans := []int{}
	for _, v := range loads {
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
