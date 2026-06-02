// Throughput bench: 16 threads each push+pop. std only.
use hazard_stack::Stack;
use std::sync::atomic::AtomicU64;
use std::sync::atomic::Ordering;
use std::sync::Arc;
use std::sync::Barrier;
use std::thread;
use std::time::Instant;

const THREADS: usize = 16;
const OPS: u64 = 1_000_000;

fn main() {
    let stack = Arc::new(Stack::<u64>::new());
    let barrier = Arc::new(Barrier::new(THREADS));
    let popped = Arc::new(AtomicU64::new(0));

    let start = Instant::now();
    let handles: Vec<_> = (0..THREADS)
        .map(|thread_id| {
            let stack = Arc::clone(&stack);
            let barrier = Arc::clone(&barrier);
            let popped = Arc::clone(&popped);
            thread::spawn(move || {
                barrier.wait();
                let mut count = 0u64;
                for i in 0..OPS {
                    stack.push(thread_id as u64 * OPS + i);
                    if stack.pop().is_some() {
                        count += 1;
                    }
                }
                popped.fetch_add(count, Ordering::Relaxed);
            })
        })
        .collect();

    for handle in handles {
        handle.join().unwrap();
    }
    let elapsed = start.elapsed();

    let ops = THREADS as u64 * OPS * 2; // push + pop
    let mops = ops as f64 / elapsed.as_secs_f64() / 1e6;
    println!("hazard-stack: {THREADS} threads, {ops} ops in {elapsed:.3?}");
    println!(
        "hazard-stack: {mops:.1} Mops/s (popped {})",
        popped.load(Ordering::Relaxed)
    );
}
