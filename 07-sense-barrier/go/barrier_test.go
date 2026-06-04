package barrier

import (
	"sync/atomic"
	"testing"
)

func TestNoDoublePass(t *testing.T) {
	const n, rounds = 8, 10_000
	b := New(n)
	var total atomic.Int64
	done := make(chan struct{})
	for range n {
		go func() {
			for range rounds {
				b.Wait()
				total.Add(1)
				b.Wait()
			}
			done <- struct{}{}
		}()
	}
	for range n { <-done }
	if got := total.Load(); got != n*rounds {
		t.Fatalf("got %d want %d", got, n*rounds)
	}
}
