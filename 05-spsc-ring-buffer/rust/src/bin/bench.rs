// Throughput bench: producer pushes, dedicated consumer drains. std only.
use spsc_ring_buffer::SpscQueue;
use std::sync::Arc;
use std::sync::Barrier;
use std::thread;
use std::time::Instant;

const MESSAGES: u64 = 50_000_000;
const CAP: usize = 4096;

fn main() {
    let queue = Arc::new(SpscQueue::<u64, CAP>::new());
    let barrier = Arc::new(Barrier::new(2));

    let consumer = {
        let queue = Arc::clone(&queue);
        let barrier = Arc::clone(&barrier);
        thread::spawn(move || {
            barrier.wait();
            let mut count = 0u64;
            let mut checksum = 0u64;
            while count < MESSAGES {
                if let Some(value) = queue.pop() {
                    checksum = checksum.wrapping_add(value);
                    count += 1;
                } else {
                    std::hint::spin_loop();
                }
            }
            checksum
        })
    };

    barrier.wait();
    let start = Instant::now();
    for value in 0..MESSAGES {
        while !queue.push(value) {
            std::hint::spin_loop();
        }
    }
    let checksum = consumer.join().unwrap();
    let elapsed = start.elapsed();

    let mops = MESSAGES as f64 / elapsed.as_secs_f64() / 1e6;
    println!("spsc: {MESSAGES} msgs (cap {CAP}) in {elapsed:.3?}");
    println!("spsc: {mops:.1} Mops/s push+pop (checksum {checksum})");
}
