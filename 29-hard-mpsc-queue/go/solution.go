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

// Queue is the interface a solver must satisfy.
type Queue interface {
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

// MpscQueue is the multi-producer single-consumer queue stub.
// head is the producer end of the list; tail is the consumer end.
type MpscQueue struct {
	head atomic.Pointer[node]
	_    [56]byte // padding to push tail to a separate cache line
	tail *node
}

// NewMpscQueue allocates an MpscQueue with a sentinel stub node.
func NewMpscQueue() *MpscQueue {
	stub := &node{}
	q := &MpscQueue{tail: stub}
	q.head.Store(stub)
	return q
}

func (q *MpscQueue) Push(value uint64) {
	_ = value
	panic("Push: not implemented")
}

func (q *MpscQueue) TryPop() PopResult {
	panic("TryPop: not implemented")
}

func main() {}
