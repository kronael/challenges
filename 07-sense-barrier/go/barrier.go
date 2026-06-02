package barrier

import "sync/atomic"

type Barrier struct {
	n     uint64
	count atomic.Uint64
	sense atomic.Bool
}

func New(n int) *Barrier {
	b := &Barrier{n: uint64(n)}
	b.count.Store(uint64(n))
	return b
}

// Wait blocks until all n goroutines have called Wait, then releases all.
// Spin-only: no channel, no mutex, no OS sleep.
func (b *Barrier) Wait() {
	// TODO: sense-reversing — local sense per goroutine via argument or closure
	panic("not implemented")
}
