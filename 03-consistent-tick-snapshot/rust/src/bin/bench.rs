// Throughput bench: one writer stamps the payload while readers spin. std only.
use seqlock::Seqlock;
use std::sync::atomic::AtomicBool;
use std::sync::atomic::Ordering;
use std::sync::Arc;
use std::thread;
use std::time::Instant;

const READERS: usize = 4;
const READS_PER_THREAD: u64 = 5_000_000;

fn main() {
    let lock = Arc::new(Seqlock::new());
    let stop = Arc::new(AtomicBool::new(false));

    let writer = {
        let lock = Arc::clone(&lock);
        let stop = Arc::clone(&stop);
        thread::spawn(move || {
            let mut counter = 1u64;
            let mut buf = [0u8; 64];
            while !stop.load(Ordering::Relaxed) {
                buf[0..8].copy_from_slice(&counter.to_ne_bytes());
                lock.write(&buf);
                counter = counter.wrapping_add(1);
            }
        })
    };

    let start = Instant::now();
    let readers: Vec<_> = (0..READERS)
        .map(|_| {
            let lock = Arc::clone(&lock);
            thread::spawn(move || {
                let mut buf = [0u8; 64];
                let mut accepted = 0u64;
                for _ in 0..READS_PER_THREAD {
                    while !lock.read(&mut buf) {
                        std::hint::spin_loop();
                    }
                    accepted += 1;
                }
                accepted
            })
        })
        .collect();

    let mut total = 0u64;
    for reader in readers {
        total += reader.join().unwrap();
    }
    let elapsed = start.elapsed();
    stop.store(true, Ordering::Relaxed);
    writer.join().unwrap();

    let mops = total as f64 / elapsed.as_secs_f64() / 1e6;
    println!("seqlock: {READERS} readers, {total} accepted reads in {elapsed:.3?}");
    println!("seqlock: {mops:.1} Mreads/s under one concurrent writer");
}
