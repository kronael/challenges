package main

import (
	"sync/atomic"
)

// SpscQueue is a single-producer single-consumer ring buffer of capacity N.
// N must be a power of two.
type SpscQueue struct {
	head atomic.Uint64
	tail atomic.Uint64
	buf  []uint64
	mask uint64
}

// NewSpscQueue allocates a queue with the given capacity (must be power of two).
func NewSpscQueue(capacity uint64) *SpscQueue {
	if capacity == 0 || capacity&(capacity-1) != 0 {
		panic("capacity must be a power of two")
	}
	return &SpscQueue{
		buf:  make([]uint64, capacity),
		mask: capacity - 1,
	}
}

// Push writes value into the queue. Returns false if full. Producer only.
func (queue *SpscQueue) Push(value uint64) bool {
	_ = value
	panic("Push: not implemented")
}

// Pop reads the next value from the queue. Returns (0, false) if empty. Consumer only.
func (queue *SpscQueue) Pop() (uint64, bool) {
	panic("Pop: not implemented")
}

func main() {}
