use hazard_stack::Stack;
use std::sync::atomic::AtomicI64;
use std::sync::atomic::AtomicU64;
use std::sync::atomic::Ordering;
use std::sync::Arc;
use std::sync::Barrier;
use std::thread;

// Net live payloads: +1 on construct, -1 on drop. A leak leaves this > 0; a
// double-free (use-after-free in node reclamation) drives it < 0.
static LIVE: AtomicI64 = AtomicI64::new(0);
// Total drops ever, to cross-check against total constructs.
static DROPS: AtomicU64 = AtomicU64::new(0);
static CONSTRUCTS: AtomicU64 = AtomicU64::new(0);

struct Tracked(u64);

impl Tracked {
    fn new(value: u64) -> Self {
        LIVE.fetch_add(1, Ordering::Relaxed);
        CONSTRUCTS.fetch_add(1, Ordering::Relaxed);
        Tracked(value)
    }
}

impl Drop for Tracked {
    fn drop(&mut self) {
        LIVE.fetch_sub(1, Ordering::Relaxed);
        DROPS.fetch_add(1, Ordering::Relaxed);
    }
}

const THREADS: usize = 16;
const OPS: u64 = 10_000;

#[test]
fn no_use_after_free_no_leak() {
    let stack = Arc::new(Stack::<Tracked>::new());
    let barrier = Arc::new(Barrier::new(THREADS));
    let popped = Arc::new(AtomicU64::new(0));

    let handles: Vec<_> = (0..THREADS)
        .map(|thread_id| {
            let stack = Arc::clone(&stack);
            let barrier = Arc::clone(&barrier);
            let popped = Arc::clone(&popped);
            thread::spawn(move || {
                barrier.wait();
                let mut local_popped = 0u64;
                for i in 0..OPS {
                    stack.push(Tracked::new(thread_id as u64 * OPS + i));
                    // Pop and immediately drop — exercises reclamation while
                    // other threads may hold a hazard pointer into this node.
                    if let Some(value) = stack.pop() {
                        std::hint::black_box(value.0);
                        local_popped += 1;
                    }
                }
                popped.fetch_add(local_popped, Ordering::Relaxed);
            })
        })
        .collect();

    for handle in handles {
        handle.join().unwrap();
    }

    // Drain whatever remains; must not segfault or double-free.
    let mut drained = 0u64;
    while let Some(value) = stack.pop() {
        std::hint::black_box(value.0);
        drained += 1;
    }

    let total_pushed = THREADS as u64 * OPS;
    let total_popped = popped.load(Ordering::Relaxed) + drained;
    assert_eq!(total_popped, total_pushed, "popped {total_popped} of {total_pushed} — lost or duplicated nodes");

    // Drop the stack to flush any retired-but-not-yet-freed nodes.
    drop(Arc::try_unwrap(stack).ok().expect("stack still shared"));

    let constructs = CONSTRUCTS.load(Ordering::Relaxed);
    let drops = DROPS.load(Ordering::Relaxed);
    let live = LIVE.load(Ordering::Relaxed);

    assert_eq!(constructs, total_pushed, "construct count drifted — test harness bug");
    assert_eq!(
        drops, constructs,
        "dropped {drops} payloads but constructed {constructs} — leak (too few) or double-free (too many)"
    );
    assert_eq!(live, 0, "{live} payloads still live — leak (>0) or double-free/use-after-free (<0)");
}
