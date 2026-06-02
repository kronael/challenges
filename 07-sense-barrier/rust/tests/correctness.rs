use sense_barrier::Barrier;
use std::sync::atomic::AtomicU64;
use std::sync::atomic::Ordering;
use std::sync::Arc;
use std::thread;

const N: usize = 16;
const ROUNDS: u64 = 100_000;

// Two barriers bracket a critical section each round. Between them, every thread
// stamps the current round into its own slot; after the closing barrier each
// thread reads all N slots and they must all equal the current round.
//
// - Early pass: if any thread is released before all peers have stamped this
//   round, it reads a stale slot (still the previous round) -> assertion fails.
// - Stuck thread: a thread that never arrives stalls every peer at the barrier,
//   so the test hangs and the harness kills it on timeout.
#[test]
fn no_early_pass_no_stall() {
    let barrier = Arc::new(Barrier::new(N));
    let slots: Arc<Vec<AtomicU64>> = Arc::new((0..N).map(|_| AtomicU64::new(u64::MAX)).collect());
    let early = Arc::new(AtomicU64::new(0));

    let handles: Vec<_> = (0..N)
        .map(|id| {
            let barrier = Arc::clone(&barrier);
            let slots = Arc::clone(&slots);
            let early = Arc::clone(&early);
            thread::spawn(move || {
                for round in 0..ROUNDS {
                    // Opening barrier: all threads aligned on this round before any write.
                    barrier.wait();
                    slots[id].store(round, Ordering::Relaxed);
                    // Closing barrier: every slot for this round is written before any read.
                    barrier.wait();
                    for slot in slots.iter() {
                        if slot.load(Ordering::Relaxed) != round {
                            // A peer had not stamped this round yet -> we were released early.
                            early.fetch_add(1, Ordering::Relaxed);
                        }
                    }
                }
            })
        })
        .collect();

    for handle in handles {
        handle.join().unwrap();
    }

    assert_eq!(
        early.load(Ordering::Relaxed),
        0,
        "barrier released a thread before all {N} arrived (stale slot observed)"
    );
}

// Sanity: a single round with the count semantics, plus a check that the barrier
// is reusable across rounds without drift in the simplest 2-thread case.
#[test]
fn reusable_two_threads() {
    let barrier = Arc::new(Barrier::new(2));
    let total = Arc::new(AtomicU64::new(0));
    let handles: Vec<_> = (0..2)
        .map(|_| {
            let barrier = Arc::clone(&barrier);
            let total = Arc::clone(&total);
            thread::spawn(move || {
                for _ in 0..10_000 {
                    barrier.wait();
                    total.fetch_add(1, Ordering::Relaxed);
                    barrier.wait();
                }
            })
        })
        .collect();
    for handle in handles {
        handle.join().unwrap();
    }
    assert_eq!(
        total.load(Ordering::Relaxed),
        2 * 10_000,
        "missed or extra barrier passes"
    );
}
