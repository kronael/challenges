package barrier

import (
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

func TestNoEarlyPassNoStall(t *testing.T) {
	const n = 8
	const rounds int64 = 10_000

	barrier := New(n)
	slots := make([]atomic.Int64, n)
	for i := range slots {
		slots[i].Store(-1)
	}
	var early atomic.Int64

	done := make(chan struct{})
	for id := 0; id < n; id++ {
		go func(id int) {
			waiter := barrier.NewWaiter()
			for round := int64(0); round < rounds; round++ {
				waiter.Wait()
				slots[id].Store(round)
				waiter.Wait()
				for i := range slots {
					if slots[i].Load() != round {
						early.Add(1)
					}
				}
			}
			done <- struct{}{}
		}(id)
	}

	for i := 0; i < n; i++ {
		select {
		case <-done:
		case <-time.After(5 * time.Second):
			t.Fatalf("barrier stalled before all goroutines completed")
		}
	}

	if got := early.Load(); got != 0 {
		t.Fatalf("barrier released a goroutine before all %d arrived: %d stale reads", n, got)
	}
}

func BenchmarkReusableBarrier(b *testing.B) {
	const participants = 8

	barrier := New(participants)
	start := make(chan struct{})
	var workers sync.WaitGroup
	workers.Add(participants)

	for range participants {
		go func() {
			defer workers.Done()
			waiter := barrier.NewWaiter()
			<-start
			for range b.N {
				waiter.Wait()
			}
		}()
	}

	b.ResetTimer()
	close(start)
	workers.Wait()
}
