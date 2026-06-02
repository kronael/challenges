use spsc_ring_buffer::SpscQueue;
use std::sync::Arc;
use std::sync::Barrier;
use std::thread;

const MESSAGES: u64 = 10_000_000;
const CAP: usize = 4096;

#[test]
fn ordered_delivery() {
    let queue = Arc::new(SpscQueue::<u64, CAP>::new());
    let barrier = Arc::new(Barrier::new(2));

    let producer = {
        let queue = Arc::clone(&queue);
        let barrier = Arc::clone(&barrier);
        thread::spawn(move || {
            barrier.wait();
            for value in 0..MESSAGES {
                while !queue.push(value) {
                    std::hint::spin_loop();
                }
            }
        })
    };

    let consumer = {
        let queue = Arc::clone(&queue);
        let barrier = Arc::clone(&barrier);
        thread::spawn(move || {
            barrier.wait();
            // Every pop must return the next expected value. Equality at each
            // position rules out skips, duplicates, and reordering in one check;
            // the loop count rules out loss.
            for expected in 0..MESSAGES {
                let value = loop {
                    match queue.pop() {
                        Some(value) => break value,
                        None => std::hint::spin_loop(),
                    }
                };
                assert_eq!(value, expected, "out-of-order or missing message at position {expected}");
            }
            expected_received(&queue);
        })
    };

    producer.join().unwrap();
    consumer.join().unwrap();
}

/// After receiving all MESSAGES, the queue must be empty: a stray Some here
/// would mean a duplicate slipped through that the position check could not see.
fn expected_received<const N: usize>(queue: &SpscQueue<u64, N>) {
    assert!(queue.pop().is_none(), "queue not empty after draining all messages — duplicate produced");
}

#[test]
fn full_buffer_backpressure() {
    // Fill to capacity with no consumer, then confirm push fails (full) and the
    // full state is distinct from empty. CAP-1 usable slots is also acceptable
    // depending on the chosen full-detection scheme, so accept either boundary.
    let queue = SpscQueue::<u64, 8>::new();
    let mut pushed = 0u64;
    while queue.push(pushed) {
        pushed += 1;
        assert!(pushed <= 8, "pushed more than capacity — full not detected");
    }
    assert!(pushed == 8 || pushed == 7, "expected to fill 7 or 8 slots, filled {pushed}");

    // Drain in order.
    for expected in 0..pushed {
        assert_eq!(queue.pop(), Some(expected), "out-of-order drain after full");
    }
    assert!(queue.pop().is_none(), "queue should be empty after full drain");
}
