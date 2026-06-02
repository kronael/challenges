package main

import (
	"sync/atomic"
	"testing"
)

const readerCount = 15
const readerIters = 5_000_000

func pack(counter uint64) [64]byte {
	var buf [64]byte
	for slot := range 8 {
		buf[slot*8] = byte(counter)
		buf[slot*8+1] = byte(counter >> 8)
		buf[slot*8+2] = byte(counter >> 16)
		buf[slot*8+3] = byte(counter >> 24)
		buf[slot*8+4] = byte(counter >> 32)
		buf[slot*8+5] = byte(counter >> 40)
		buf[slot*8+6] = byte(counter >> 48)
		buf[slot*8+7] = byte(counter >> 56)
	}
	return buf
}

func checkConsistent(buf *[64]byte) bool {
	first := uint64(buf[0]) | uint64(buf[1])<<8 | uint64(buf[2])<<16 | uint64(buf[3])<<24 |
		uint64(buf[4])<<32 | uint64(buf[5])<<40 | uint64(buf[6])<<48 | uint64(buf[7])<<56
	for slot := 1; slot < 8; slot++ {
		base := slot * 8
		value := uint64(buf[base]) | uint64(buf[base+1])<<8 | uint64(buf[base+2])<<16 |
			uint64(buf[base+3])<<24 | uint64(buf[base+4])<<32 | uint64(buf[base+5])<<40 |
			uint64(buf[base+6])<<48 | uint64(buf[base+7])<<56
		if value != first {
			return false
		}
	}
	return true
}

func TestNoTornReads(t *testing.T) {
	if testing.Short() {
		t.Skip("skipping stress test in short mode")
	}

	lock := &Seqlock{}
	var tornCount atomic.Int64
	done := make(chan struct{})

	// Writer goroutine.
	go func() {
		for counter := uint64(0); ; counter++ {
			payload := pack(counter)
			lock.Write(&payload)
			select {
			case <-done:
				return
			default:
			}
		}
	}()

	// Reader goroutines.
	readersDone := make(chan struct{}, readerCount)
	for range readerCount {
		go func() {
			var buf [64]byte
			for range readerIters {
				for !lock.Read(&buf) {
					// retry
				}
				if !checkConsistent(&buf) {
					tornCount.Add(1)
				}
			}
			readersDone <- struct{}{}
		}()
	}

	for range readerCount {
		<-readersDone
	}
	close(done)

	if count := tornCount.Load(); count != 0 {
		t.Fatalf("torn reads detected: %d", count)
	}
}

func BenchmarkRead(b *testing.B) {
	lock := &Seqlock{}
	counter := uint64(0)
	done := make(chan struct{})
	go func() {
		for {
			select {
			case <-done:
				return
			default:
				payload := pack(counter)
				lock.Write(&payload)
				counter++
			}
		}
	}()

	b.ResetTimer()
	var buf [64]byte
	for range b.N {
		for !lock.Read(&buf) {
		}
	}
	close(done)
}
