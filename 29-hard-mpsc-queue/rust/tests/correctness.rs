use mpsc_queue::MpscQueue;
use mpsc_queue::PopResult;
use mpsc_queue::VyukovQueue;
use std::sync::Arc;
use std::sync::Barrier;
use std::thread;

const PRODUCERS: usize = 8;
const MSGS: u64 = 100_000;

// Each producer pushes the values 1..=MSGS. Across all producers, every value v
// must therefore be popped exactly PRODUCERS times — no more (duplication), no
// fewer (loss). Verifying the full multiset, not just the sum, catches a
// lost+duplicated pair that would leave the sum unchanged.
#[test]
fn stress_mpsc() {
    let queue = Arc::new(VyukovQueue::<u64>::new());
    let barrier = Arc::new(Barrier::new(PRODUCERS + 1));

    let handles: Vec<_> = (0..PRODUCERS)
        .map(|_| {
            let queue = Arc::clone(&queue);
            let barrier = Arc::clone(&barrier);
            thread::spawn(move || {
                barrier.wait();
                for value in 1..=MSGS {
                    queue.push(value);
                }
            })
        })
        .collect();

    barrier.wait();

    let total = PRODUCERS * MSGS as usize;
    let mut counts = vec![0u32; MSGS as usize + 1];
    let mut popped = 0usize;

    // Spin until exactly `total` items are popped. A correct queue can always
    // make progress, so this terminates. A queue that loses an item (bad
    // head/tail handoff) never reaches `total` and the test hangs to timeout
    // rather than passing falsely. Empty and Retry both just back off.
    while popped < total {
        match queue.try_pop() {
            PopResult::Item(value) => {
                counts[value as usize] += 1;
                popped += 1;
            }
            PopResult::Empty | PopResult::Retry => std::hint::spin_loop(),
        }
    }

    for handle in handles {
        handle.join().unwrap();
    }

    // After draining `total` items the queue must be cleanly empty: no extra
    // Item (duplication) and, with all producers joined, no lingering Retry
    // (a stuck broken link that was never completed).
    match queue.try_pop() {
        PopResult::Empty => {}
        PopResult::Item(_) => panic!("extra item after draining all messages — duplication"),
        PopResult::Retry => panic!("Retry after all producers joined — stuck broken link"),
    }

    assert_eq!(counts[0], 0, "value 0 was never pushed yet appeared");
    for value in 1..=MSGS as usize {
        assert_eq!(
            counts[value], PRODUCERS as u32,
            "value {value} popped {} times, expected {PRODUCERS} — lost or duplicated",
            counts[value]
        );
    }
}
