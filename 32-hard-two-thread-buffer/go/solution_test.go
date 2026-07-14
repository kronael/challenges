package main

import (
	"testing"
)

const messageCount = 10_000_000

func TestOrderedDelivery(t *testing.T) {
	if testing.Short() {
		t.Skip("skipping stress test in short mode")
	}

	queue := NewSpscQueue(4096)
	done := make(chan struct{})

	// Consumer goroutine.
	go func() {
		defer close(done)
		for expected := uint64(0); expected < messageCount; expected++ {
			for {
				value, ok := queue.Pop()
				if ok {
					if value != expected {
						panic("out-of-order or missing message")
					}
					break
				}
			}
		}
	}()

	// Producer (main goroutine).
	for value := uint64(0); value < messageCount; value++ {
		for !queue.Push(value) {
			// spin until space available
		}
	}

	<-done
}

func BenchmarkThroughput(b *testing.B) {
	queue := NewSpscQueue(4096)
	done := make(chan struct{})

	go func() {
		defer close(done)
		consumed := 0
		for consumed < b.N {
			if _, ok := queue.Pop(); ok {
				consumed++
			}
		}
	}()

	b.ResetTimer()
	for i := range b.N {
		for !queue.Push(uint64(i)) {
		}
	}
	<-done
}
