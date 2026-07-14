use std::cell::UnsafeCell;
use std::sync::atomic::AtomicUsize;

// stub compiles but panics at runtime; replace the bodies. Rules: push() is
// called only from the producer thread, pop() only from the consumer thread, no
// Mutex or OS primitive is allowed, and N must be a power of two.

pub struct SpscQueue<T, const N: usize> {
    #[allow(dead_code)]
    head: AtomicUsize,
    #[allow(dead_code)]
    tail: AtomicUsize,
    #[allow(dead_code)]
    buf: [UnsafeCell<std::mem::MaybeUninit<T>>; N],
}

// SAFETY: SpscQueue is designed for one producer + one consumer. push() and
// pop() access disjoint slots; the protocol ensures no data races.
unsafe impl<T: Send, const N: usize> Send for SpscQueue<T, N> {}
unsafe impl<T: Send, const N: usize> Sync for SpscQueue<T, N> {}

impl<T: Copy, const N: usize> SpscQueue<T, N> {
    pub fn new() -> Self {
        assert!(N.is_power_of_two(), "N must be a power of two");
        // SAFETY: MaybeUninit array is valid in zeroed state.
        unsafe {
            SpscQueue {
                head: AtomicUsize::new(0),
                tail: AtomicUsize::new(0),
                buf: std::mem::zeroed(),
            }
        }
    }

    /// Push a value. Returns false if the buffer is full. Producer thread only.
    pub fn push(&self, _value: T) -> bool {
        todo!("implement SPSC push")
    }

    /// Pop a value. Returns None if the buffer is empty. Consumer thread only.
    pub fn pop(&self) -> Option<T> {
        todo!("implement SPSC pop")
    }
}

impl<T: Copy, const N: usize> Default for SpscQueue<T, N> {
    fn default() -> Self {
        Self::new()
    }
}
