use std::cell::UnsafeCell;
use std::sync::atomic::{AtomicUsize, Ordering};

// TODO: implement push() and pop() using the SPSC ring-buffer protocol.
// The stub compiles but panics at runtime — replace the bodies.
//
// Layout requirements:
//   - head (producer index) and tail (consumer index) must be on separate
//     cache lines to avoid false sharing. Use #[repr(C, align(64))].
//   - N must be a power of two; use (index & (N-1)) for cheap modulo.
//
// Rules:
//   - push() is called only from the producer thread.
//   - pop() is called only from the consumer thread.
//   - No Mutex or OS primitive.
//   - push() returns false when the buffer is full; pop() returns None when empty.

#[repr(C, align(64))]
pub struct SpscQueue<T, const N: usize> {
    head: AtomicUsize,
    _pad_head: [u8; 64 - std::mem::size_of::<AtomicUsize>()],
    tail: AtomicUsize,
    _pad_tail: [u8; 64 - std::mem::size_of::<AtomicUsize>()],
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
                _pad_head: [0; 64 - std::mem::size_of::<AtomicUsize>()],
                tail: AtomicUsize::new(0),
                _pad_tail: [0; 64 - std::mem::size_of::<AtomicUsize>()],
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
