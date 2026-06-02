package main

import (
	"sync"
	"testing"
)

const producers = 8
const msgsPerProducer = 100_000

func TestStressMpsc(t *testing.T) {
	queue := NewVyukovQueue()

	var wg sync.WaitGroup
	barrier := make(chan struct{})

	for range producers {
		wg.Add(1)
		go func() {
			defer wg.Done()
			<-barrier
			for i := uint64(1); i <= msgsPerProducer; i++ {
				queue.Push(i)
			}
		}()
	}

	close(barrier)

	expected := uint64(producers) * (msgsPerProducer * (msgsPerProducer + 1) / 2)
	var sum uint64
	remaining := producers * msgsPerProducer

	for remaining > 0 {
		result := queue.TryPop()
		switch result.State {
		case 0: // Item
			sum += result.Value
			remaining--
		default:
			// Empty or Retry — spin
		}
	}

	wg.Wait()

	if sum != expected {
		t.Fatalf("sum mismatch: got %d want %d — messages lost or duplicated", sum, expected)
	}
}

func BenchmarkPushPop(b *testing.B) {
	queue := NewVyukovQueue()
	done := make(chan struct{})

	go func() {
		defer close(done)
		consumed := 0
		for consumed < b.N {
			result := queue.TryPop()
			if result.State == 0 {
				consumed++
			}
		}
	}()

	b.ResetTimer()
	for i := range b.N {
		queue.Push(uint64(i))
	}
	<-done
}
