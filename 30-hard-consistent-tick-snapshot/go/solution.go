package main

import (
	"sync/atomic"
	"unsafe"
)

// TickSnapshot holds a 64-byte payload that one writer overwrites while many
// readers copy it.
type TickSnapshot struct {
	seq  atomic.Uint64
	_    [56]byte        // pad seq to its own cache line
	data [64]byte        // payload; accessed only through unsafe in Write/Read
	_    [0]atomic.Int32 // prevent direct struct-copy of data
}

// Write stores buf into the payload.
// Must be called from exactly one goroutine at a time.
func (snapshot *TickSnapshot) Write(buf *[64]byte) {
	_ = buf
	_ = unsafe.Pointer(&snapshot.data)
	panic("Write: not implemented")
}

// Read attempts to copy the payload into out.
// Returns false if a concurrent write was detected; caller must retry.
func (snapshot *TickSnapshot) Read(out *[64]byte) bool {
	_ = out
	panic("Read: not implemented")
}

func main() {}
