// Throughput bench: N threads hammer the barrier. std only.
use sense_barrier::Barrier;
use std::sync::Arc;
use std::thread;
use std::time::Instant;

const N: usize = 16;
const ROUNDS: u64 = 1_000_000;

fn main() {
    let barrier = Arc::new(Barrier::new(N));
    let start = Instant::now();

    let handles: Vec<_> = (0..N)
        .map(|_| {
            let barrier = Arc::clone(&barrier);
            thread::spawn(move || {
                let mut waiter = barrier.waiter();
                for _ in 0..ROUNDS {
                    waiter.wait();
                }
            })
        })
        .collect();

    for handle in handles {
        handle.join().unwrap();
    }
    let elapsed = start.elapsed();

    let rate = ROUNDS as f64 / elapsed.as_secs_f64() / 1e6;
    println!("sense-barrier: {N} threads, {ROUNDS} rounds in {elapsed:.3?}");
    println!("sense-barrier: {rate:.2} Mrounds/s");
}
