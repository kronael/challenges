// Throughput bench: N producers push, one consumer drains. std only.
use mpsc_queue::MpscQueue;
use mpsc_queue::PopResult;
use mpsc_queue::VyukovQueue;
use std::sync::Arc;
use std::sync::Barrier;
use std::thread;
use std::time::Instant;

const PRODUCERS: usize = 4;
const PER_PRODUCER: u64 = 2_000_000;

fn main() {
    let total = PRODUCERS as u64 * PER_PRODUCER;
    let queue = Arc::new(VyukovQueue::<u64>::new());
    let barrier = Arc::new(Barrier::new(PRODUCERS + 1));

    let producers: Vec<_> = (0..PRODUCERS)
        .map(|_| {
            let queue = Arc::clone(&queue);
            let barrier = Arc::clone(&barrier);
            thread::spawn(move || {
                barrier.wait();
                for value in 0..PER_PRODUCER {
                    queue.push(value);
                }
            })
        })
        .collect();

    barrier.wait();
    let start = Instant::now();

    let mut popped = 0u64;
    let mut checksum = 0u64;
    while popped < total {
        match queue.try_pop() {
            PopResult::Item(value) => {
                checksum = checksum.wrapping_add(value);
                popped += 1;
            }
            PopResult::Empty | PopResult::Retry => std::hint::spin_loop(),
        }
    }

    let elapsed = start.elapsed();
    for producer in producers {
        producer.join().unwrap();
    }

    let mops = total as f64 / elapsed.as_secs_f64() / 1e6;
    println!("mpsc: {PRODUCERS} producers, {total} msgs in {elapsed:.3?}");
    println!("mpsc: {mops:.1} Mops/s consumed (checksum {checksum})");
}
