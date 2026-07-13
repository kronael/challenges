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

func checkConsistent(buf *[64]byte) (uint64, bool) {
	first := uint64(buf[0]) | uint64(buf[1])<<8 | uint64(buf[2])<<16 | uint64(buf[3])<<24 |
		uint64(buf[4])<<32 | uint64(buf[5])<<40 | uint64(buf[6])<<48 | uint64(buf[7])<<56
	for slot := 1; slot < 8; slot++ {
		base := slot * 8
		value := uint64(buf[base]) | uint64(buf[base+1])<<8 | uint64(buf[base+2])<<16 |
			uint64(buf[base+3])<<24 | uint64(buf[base+4])<<32 | uint64(buf[base+5])<<40 |
			uint64(buf[base+6])<<48 | uint64(buf[base+7])<<56
		if value != first {
			return 0, false
		}
	}
	return first, true
}

func raiseMax(dst *atomic.Uint64, value uint64) {
	for {
		cur := dst.Load()
		if value <= cur || dst.CompareAndSwap(cur, value) {
			return
		}
	}
}

func TestNoTornReads(t *testing.T) {
	if testing.Short() {
		t.Skip("skipping stress test in short mode")
	}

	lock := &Seqlock{}
	var tornCount atomic.Int64
	var maxSeen atomic.Uint64
	done := make(chan struct{})
	writerDone := make(chan struct{})

	// Writer goroutine.
	go func() {
		defer close(writerDone)
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
			var localMax uint64
			for range readerIters {
				for !lock.Read(&buf) {
					// retry
				}
				if value, ok := checkConsistent(&buf); ok {
					if value > localMax {
						localMax = value
					}
				} else {
					tornCount.Add(1)
				}
			}
			raiseMax(&maxSeen, localMax)
			readersDone <- struct{}{}
		}()
	}

	for range readerCount {
		<-readersDone
	}
	close(done)
	<-writerDone

	if count := tornCount.Load(); count != 0 {
		t.Fatalf("torn reads detected: %d", count)
	}
	if seen := maxSeen.Load(); seen == 0 {
		t.Fatalf("readers never observed a written value")
	}
}

func BenchmarkRead(b *testing.B) {
	lock := &Seqlock{}
	counter := uint64(0)
	done := make(chan struct{})
	writerDone := make(chan struct{})
	go func() {
		defer close(writerDone)
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
	<-writerDone
}
