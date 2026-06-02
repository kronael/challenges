use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering::*};

pub struct Barrier {
    n: usize,
    count: AtomicUsize,
    sense: AtomicBool,
}

impl Barrier {
    pub fn new(n: usize) -> Self {
        Barrier {
            n,
            count: AtomicUsize::new(n),
            sense: AtomicBool::new(false),
        }
    }

    pub fn wait(&self) {
        // TODO: sense-reversing barrier — no Mutex, no Condvar, no OS sleep
        // Each caller has its own local sense (pass it in or use thread_local!).
        // Last thread to arrive: reset count to n, flip shared sense.
        // Others: spin on shared sense != local sense.
        // Ordering: the count reset must be visible before the sense flip.
        todo!()
    }
}
