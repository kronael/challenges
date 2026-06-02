package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type input struct {
	Words   []string `json:"words"`
	Queries []string `json:"queries"`
}

type node struct {
	kids [26]*node
	end  bool
}

func solve(words, queries []string) string {
	root := &node{}
	for _, w := range words {
		cur := root
		for i := 0; i < len(w); i++ {
			c := w[i] - 'a'
			if cur.kids[c] == nil {
				cur.kids[c] = &node{}
			}
			cur = cur.kids[c]
		}
		cur.end = true
	}

	results := make([]string, len(queries))
	for qi, q := range queries {
		cur := root
		ok := true
		for i := 0; i < len(q); i++ {
			next := cur.kids[q[i]-'a']
			if next == nil {
				ok = false
				break
			}
			cur = next
		}
		if !ok {
			results[qi] = ""
			continue
		}
		var found []string
		collect(cur, q, &found)
		results[qi] = strings.Join(found, " ")
	}
	return strings.Join(results, ";")
}

func collect(cur *node, prefix string, found *[]string) {
	if len(*found) == 3 {
		return
	}
	if cur.end {
		*found = append(*found, prefix)
		if len(*found) == 3 {
			return
		}
	}
	for c := 0; c < 26; c++ {
		if cur.kids[c] != nil {
			collect(cur.kids[c], prefix+string(rune('a'+c)), found)
			if len(*found) == 3 {
				return
			}
		}
	}
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(solve(in.Words, in.Queries))
}
