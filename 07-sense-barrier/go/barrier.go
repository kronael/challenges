package barrier

import "sync/atomic"

type Barrier struct {
	n     uint64
	count atomic.Uint64
	sense atomic.Bool
}

type Waiter struct {
	barrier    *Barrier
	localSense bool
}

func New(n int) *Barrier {
	if n <= 0 {
		panic("barrier size must be positive")
	}
	b := &Barrier{n: uint64(n)}
	b.count.Store(uint64(n))
	return b
}

// NewWaiter creates the per-participant state used by one goroutine.
// Do not share a Waiter between goroutines.
func (b *Barrier) NewWaiter() *Waiter {
	return &Waiter{barrier: b}
}

// Wait blocks until all n waiters have arrived, then releases them all.
// Spin-only: no channel, no mutex, no OS sleep.
func (w *Waiter) Wait() {
	panic("not implemented")
}
