use std::cell::UnsafeCell;
use std::sync::atomic::{AtomicU64, Ordering};

// TODO: implement write() and read() using the seqlock protocol.
// The stub compiles but panics at runtime — replace the bodies.
//
// Protocol:
//   write: seq++ (now odd), memcpy data, seq++ (now even), release fences around both.
//   read:  load seq (must be even), memcpy data, load seq again; if either seq was
//          odd or the two loads differ, return false (caller must retry).
//
// Rules:
//   - No Mutex or OS primitive.
//   - read() returning false is correct behaviour — the caller spins.
//   - Use acquire/release fences; do NOT use SeqCst unless you can justify it.

pub struct Seqlock {
    pub seq: AtomicU64,
    pub data: UnsafeCell<[u8; 64]>,
}

// SAFETY: Seqlock is designed for concurrent access; the seqlock protocol
// ensures readers never observe torn data when used correctly.
unsafe impl Send for Seqlock {}
unsafe impl Sync for Seqlock {}

impl Seqlock {
    pub fn new() -> Self {
        Seqlock {
            seq: AtomicU64::new(0),
            data: UnsafeCell::new([0u8; 64]),
        }
    }

    /// Write a 64-byte payload. Must be called from exactly one writer thread.
    pub fn write(&self, buf: &[u8; 64]) {
        // TODO: implement seqlock write
        let _ = buf;
        todo!("implement seqlock write")
    }

    /// Attempt to read the payload into `out`.
    /// Returns false if a concurrent write was detected — the caller must retry.
    pub fn read(&self, out: &mut [u8; 64]) -> bool {
        // TODO: implement seqlock read
        let _ = out;
        todo!("implement seqlock read")
    }
}

impl Default for Seqlock {
    fn default() -> Self {
        Self::new()
    }
}
