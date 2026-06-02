package main

import (
	"sync/atomic"
	"unsafe"
)

// Seqlock protects a 64-byte payload with a sequence counter.
// Even seq = no write in progress; odd seq = write in progress.
type Seqlock struct {
	seq  atomic.Uint64
	_    [56]byte        // pad seq to its own cache line
	data [64]byte        // payload; accessed only through unsafe in Write/Read
	_    [0]atomic.Int32 // prevent direct struct-copy of data
}

// Write stores buf into the payload using the seqlock protocol.
// Must be called from exactly one goroutine at a time.
func (seqlock *Seqlock) Write(buf *[64]byte) {
	// TODO: implement seqlock write
	// 1. seq++ (make odd — write in progress)
	// 2. atomic.StorePointer / copy data
	// 3. seq++ (make even — write done)
	_ = buf
	_ = unsafe.Pointer(&seqlock.data)
	panic("Write: not implemented")
}

// Read attempts to copy the payload into out.
// Returns false if a concurrent write was detected; caller must retry.
func (seqlock *Seqlock) Read(out *[64]byte) bool {
	// TODO: implement seqlock read
	// 1. load seq; if odd, return false
	// 2. copy data
	// 3. load seq again; if changed, return false
	_ = out
	panic("Read: not implemented")
}

func main() {}
