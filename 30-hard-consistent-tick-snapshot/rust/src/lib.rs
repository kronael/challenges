use std::cell::UnsafeCell;
use std::sync::atomic::{AtomicU64, Ordering};

// The stub compiles but panics at runtime — replace the bodies.
//
// Rules:
//   - No Mutex or OS primitive.
//   - read() returning false is correct behaviour — the caller spins.

pub struct TickSnapshot {
    pub seq: AtomicU64,
    pub data: UnsafeCell<[u8; 64]>,
}

// SAFETY: TickSnapshot is designed for concurrent access; a correct write/read
// implementation ensures readers never observe torn data.
unsafe impl Send for TickSnapshot {}
unsafe impl Sync for TickSnapshot {}

impl TickSnapshot {
    pub fn new() -> Self {
        TickSnapshot {
            seq: AtomicU64::new(0),
            data: UnsafeCell::new([0u8; 64]),
        }
    }

    /// Write a 64-byte payload. Must be called from exactly one writer thread.
    pub fn write(&self, buf: &[u8; 64]) {
        let _ = buf;
        todo!("implement write")
    }

    /// Attempt to read the payload into `out`.
    /// Returns false if a concurrent write was detected — the caller must retry.
    pub fn read(&self, out: &mut [u8; 64]) -> bool {
        let _ = out;
        todo!("implement read")
    }
}

impl Default for TickSnapshot {
    fn default() -> Self {
        Self::new()
    }
}
