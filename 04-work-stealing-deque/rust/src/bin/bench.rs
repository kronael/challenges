// Throughput bench: owner pushes, thieves steal. std only.
use std::sync::atomic::AtomicBool;
use std::sync::atomic::AtomicU64;
use std::sync::atomic::Ordering;
use std::sync::Arc;
use std::sync::Barrier;
use std::thread;
use std::time::Instant;
use work_stealing_deque::Deque;
use work_stealing_deque::Steal;

const TASKS: u64 = 4_000_000;
const THIEVES: usize = 7;

fn main() {
    let deque = Arc::new(Deque::<u64>::new());
    let stop = Arc::new(AtomicBool::new(false));
    let stolen = Arc::new(AtomicU64::new(0));
    let barrier = Arc::new(Barrier::new(THIEVES + 1));

    let thieves: Vec<_> = (0..THIEVES)
        .map(|_| {
            let deque = Arc::clone(&deque);
            let stop = Arc::clone(&stop);
            let stolen = Arc::clone(&stolen);
            let barrier = Arc::clone(&barrier);
            thread::spawn(move || {
                let mut count = 0u64;
                barrier.wait();
                loop {
                    match deque.steal() {
                        Steal::Success(_) => count += 1,
                        Steal::Retry => std::hint::spin_loop(),
                        Steal::Empty => {
                            if stop.load(Ordering::Acquire) {
                                break;
                            }
                            std::hint::spin_loop();
                        }
                    }
                }
                stolen.fetch_add(count, Ordering::Relaxed);
            })
        })
        .collect();

    barrier.wait();
    let start = Instant::now();
    let mut owner = 0u64;
    for task in 1..=TASKS {
        deque.push(task);
        if task % 3 == 0 && deque.pop().is_some() {
            owner += 1;
        }
    }
    while deque.pop().is_some() {
        owner += 1;
    }
    let elapsed = start.elapsed();

    stop.store(true, Ordering::Release);
    for thief in thieves {
        thief.join().unwrap();
    }

    let total = owner + stolen.load(Ordering::Relaxed);
    let mops = total as f64 / elapsed.as_secs_f64() / 1e6;
    println!("deque: {THIEVES} thieves, {total} tasks ({owner} by owner) in {elapsed:.3?}");
    println!("deque: {mops:.1} Mtasks/s");
}
