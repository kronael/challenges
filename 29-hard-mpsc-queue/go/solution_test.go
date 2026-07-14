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

	counts := make([]int, msgsPerProducer+1)
	remaining := producers * msgsPerProducer

	for remaining > 0 {
		result := queue.TryPop()
		switch result.State {
		case 0: // Item
			if result.Value == 0 || result.Value > msgsPerProducer {
				t.Fatalf("unexpected value popped: %d", result.Value)
			}
			counts[result.Value]++
			remaining--
		default:
			// Empty or Retry — spin
		}
	}

	wg.Wait()

	switch result := queue.TryPop(); result.State {
	case 1: // Empty
	case 0:
		t.Fatalf("extra item after draining all messages: %d", result.Value)
	case 2:
		t.Fatal("Retry after all producers joined")
	default:
		t.Fatalf("unknown pop state after drain: %d", result.State)
	}

	for value := uint64(1); value <= msgsPerProducer; value++ {
		if counts[value] != producers {
			t.Fatalf(
				"value %d popped %d times, expected %d — messages lost or duplicated",
				value,
				counts[value],
				producers,
			)
		}
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
