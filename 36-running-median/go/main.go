package main

import (
	"container/heap"
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type input struct {
	Stream []int `json:"stream"`
}

// maxHeap and minHeap over int. lo is a max-heap (lower half), hi a min-heap.
type maxHeap []int

func (h maxHeap) Len() int           { return len(h) }
func (h maxHeap) Less(i, j int) bool { return h[i] > h[j] }
func (h maxHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *maxHeap) Push(x any)        { *h = append(*h, x.(int)) }
func (h *maxHeap) Pop() any          { o := *h; n := len(o); v := o[n-1]; *h = o[:n-1]; return v }

type minHeap []int

func (h minHeap) Len() int           { return len(h) }
func (h minHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h minHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x any)        { *h = append(*h, x.(int)) }
func (h *minHeap) Pop() any          { o := *h; n := len(o); v := o[n-1]; *h = o[:n-1]; return v }

func solve(stream []int) []string {
	lo := &maxHeap{}
	hi := &minHeap{}
	out := make([]string, 0, len(stream))
	for _, x := range stream {
		if lo.Len() > 0 && x > (*lo)[0] {
			heap.Push(hi, x)
		} else {
			heap.Push(lo, x)
		}
		if lo.Len() > hi.Len()+1 {
			heap.Push(hi, heap.Pop(lo))
		} else if hi.Len() > lo.Len() {
			heap.Push(lo, heap.Pop(hi))
		}
		if lo.Len() > hi.Len() {
			out = append(out, strconv.Itoa((*lo)[0]))
		} else {
			med := float64((*lo)[0]+(*hi)[0]) / 2
			out = append(out, strconv.FormatFloat(med, 'f', 1, 64))
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
	fmt.Println(strings.Join(solve(in.Stream), " "))
}
