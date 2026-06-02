package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type op struct {
	kind string
	key  int
	val  int
}

type input struct {
	Capacity int  `json:"capacity"`
	Ops      []op `json:"ops"`
}

// ops arrive as heterogeneous JSON arrays: ["get",k] or ["put",k,v].
func (o *op) UnmarshalJSON(data []byte) error {
	var raw []json.RawMessage
	if err := json.Unmarshal(data, &raw); err != nil {
		return err
	}
	if err := json.Unmarshal(raw[0], &o.kind); err != nil {
		return err
	}
	if err := json.Unmarshal(raw[1], &o.key); err != nil {
		return err
	}
	if len(raw) > 2 {
		if err := json.Unmarshal(raw[2], &o.val); err != nil {
			return err
		}
	}
	return nil
}

type node struct {
	key, val   int
	prev, next *node
}

func solve(capacity int, ops []op) []int {
	table := make(map[int]*node)
	head := &node{} // sentinel; head.next is MRU
	tail := &node{} // sentinel; tail.prev is LRU
	head.next = tail
	tail.prev = head

	remove := func(n *node) {
		n.prev.next = n.next
		n.next.prev = n.prev
	}
	pushFront := func(n *node) {
		n.prev = head
		n.next = head.next
		head.next.prev = n
		head.next = n
	}

	out := []int{}
	for _, o := range ops {
		if o.kind == "get" {
			n, ok := table[o.key]
			if !ok {
				out = append(out, -1)
				continue
			}
			remove(n)
			pushFront(n)
			out = append(out, n.val)
		} else {
			if n, ok := table[o.key]; ok {
				n.val = o.val
				remove(n)
				pushFront(n)
				continue
			}
			n := &node{key: o.key, val: o.val}
			table[o.key] = n
			pushFront(n)
			if len(table) > capacity {
				lru := tail.prev
				remove(lru)
				delete(table, lru.key)
			}
		}
	}
	return out
}

func main() {
	var in input
	if err := json.NewDecoder(os.Stdin).Decode(&in); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	res := solve(in.Capacity, in.Ops)
	parts := make([]string, len(res))
	for i, v := range res {
		parts[i] = fmt.Sprint(v)
	}
	fmt.Println(strings.Join(parts, " "))
}
