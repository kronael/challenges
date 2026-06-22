package main

import (
	"sync/atomic"
	"unsafe"
)

// PopResult mirrors the Rust enum: Item, Empty, or Retry.
type PopResult struct {
	Value uint64
	State int // 0=Item, 1=Empty, 2=Retry
}

// MpscQueue is the interface a solver must satisfy.
type MpscQueue interface {
	Push(value uint64)
	TryPop() PopResult
}

// node is a singly-linked intrusive list node.
// unsafe.Pointer is used for the next field so we can store it atomically
// without a separate AtomicPointer wrapper.
type node struct {
	next  unsafe.Pointer // *node, written/read via atomic ops
	value uint64
}

// VyukovQueue is the Vyukov non-intrusive MPSC queue stub.
// head is the tail of the list (producers swap it); tail is the consumer end.
type VyukovQueue struct {
	head atomic.Pointer[node]
	_    [56]byte // padding to push tail to a separate cache line
	tail *node
}

// NewVyukovQueue allocates a VyukovQueue with a sentinel stub node.
func NewVyukovQueue() *VyukovQueue {
	stub := &node{}
	q := &VyukovQueue{tail: stub}
	q.head.Store(stub)
	return q
}

func (q *VyukovQueue) Push(value uint64) {
	_ = value
	panic("Push: not implemented")
}

func (q *VyukovQueue) TryPop() PopResult {
	panic("TryPop: not implemented")
}

func main() {}
