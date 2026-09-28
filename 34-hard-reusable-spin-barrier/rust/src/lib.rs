use std::sync::atomic::{AtomicBool, AtomicUsize};

pub struct Barrier {
    n: usize,
    count: AtomicUsize,
    phase: AtomicBool,
}

pub struct Waiter<'a> {
    barrier: &'a Barrier,
    local_phase: bool,
}

impl Barrier {
    pub fn new(n: usize) -> Self {
        assert!(n > 0, "barrier size must be positive");
        Barrier {
            n,
            count: AtomicUsize::new(n),
            phase: AtomicBool::new(false),
        }
    }

    pub fn waiter(&self) -> Waiter<'_> {
        Waiter {
            barrier: self,
            local_phase: false,
        }
    }
}

impl Waiter<'_> {
    pub fn wait(&mut self) {
        let _ = (
            self.barrier.n,
            &self.barrier.count,
            &self.barrier.phase,
            self.local_phase,
        );
        todo!()
    }
}
