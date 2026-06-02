use seqlock::Seqlock;
use std::sync::atomic::AtomicBool;
use std::sync::atomic::AtomicU64;
use std::sync::atomic::Ordering;
use std::sync::Arc;
use std::sync::Barrier;
use std::thread;

const READERS: usize = 15;
const READER_ITERS: u64 = 2_000_000;

/// Pack a counter value into all eight u64 slots of a 64-byte payload.
fn pack(counter: u64) -> [u8; 64] {
    let mut buf = [0u8; 64];
    for slot in 0..8 {
        buf[slot * 8..(slot + 1) * 8].copy_from_slice(&counter.to_ne_bytes());
    }
    buf
}

/// Return the common slot value if all eight u64 slots are identical, else None.
fn check_consistent(buf: &[u8; 64]) -> Option<u64> {
    let first = u64::from_ne_bytes(buf[0..8].try_into().unwrap());
    for slot in 1..8 {
        let value = u64::from_ne_bytes(buf[slot * 8..(slot + 1) * 8].try_into().unwrap());
        if value != first {
            return None;
        }
    }
    Some(first)
}

#[test]
fn no_torn_reads() {
    let lock = Arc::new(Seqlock::new());
    let torn = Arc::new(AtomicU64::new(0));
    // Highest fully-consistent value any reader observed; used to prove the
    // writer actually made progress, so a no-op writer cannot pass the test.
    let max_seen = Arc::new(AtomicU64::new(0));
    let stop = Arc::new(AtomicBool::new(false));
    let barrier = Arc::new(Barrier::new(READERS + 1));

    let writer = {
        let lock = Arc::clone(&lock);
        let stop = Arc::clone(&stop);
        let barrier = Arc::clone(&barrier);
        thread::spawn(move || {
            barrier.wait();
            let mut counter = 1u64;
            while !stop.load(Ordering::Relaxed) {
                lock.write(&pack(counter));
                counter = counter.wrapping_add(1);
            }
            counter
        })
    };

    let readers: Vec<_> = (0..READERS)
        .map(|_| {
            let lock = Arc::clone(&lock);
            let torn = Arc::clone(&torn);
            let max_seen = Arc::clone(&max_seen);
            let barrier = Arc::clone(&barrier);
            thread::spawn(move || {
                let mut buf = [0u8; 64];
                let mut local_max = 0u64;
                barrier.wait();
                for _ in 0..READER_ITERS {
                    while !lock.read(&mut buf) {
                        std::hint::spin_loop();
                    }
                    match check_consistent(&buf) {
                        Some(value) => local_max = local_max.max(value),
                        None => {
                            torn.fetch_add(1, Ordering::Relaxed);
                        }
                    }
                }
                max_seen.fetch_max(local_max, Ordering::Relaxed);
            })
        })
        .collect();

    for reader in readers {
        reader.join().unwrap();
    }
    stop.store(true, Ordering::Relaxed);
    let written = writer.join().unwrap();

    assert_eq!(torn.load(Ordering::Relaxed), 0, "torn reads detected — payload tore between epochs");
    // Sanity: the writer cycled and readers observed real, advancing values.
    // Guards against a degenerate impl that always reports the same payload.
    assert!(written > 1, "writer never advanced the sequence");
    assert!(max_seen.load(Ordering::Relaxed) > 0, "readers never observed a written value");
}
