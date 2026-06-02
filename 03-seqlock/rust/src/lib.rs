use std::cell::UnsafeCell;
use std::sync::atomic::fence;
use std::sync::atomic::AtomicU64;
use std::sync::atomic::Ordering;

pub struct Seqlock {
    pub seq: AtomicU64,
    pub data: UnsafeCell<[u8; 64]>,
}

// SAFETY: the seqlock protocol ensures readers never observe torn data.
unsafe impl Send for Seqlock {}
unsafe impl Sync for Seqlock {}

impl Seqlock {
    pub fn new() -> Self {
        Seqlock {
            seq: AtomicU64::new(0),
            data: UnsafeCell::new([0u8; 64]),
        }
    }

    pub fn write(&self, buf: &[u8; 64]) {
        let seq = self.seq.load(Ordering::Relaxed);
        self.seq.store(seq + 1, Ordering::Relaxed);
        fence(Ordering::Release);
        // SAFETY: single writer; odd seq tells readers a write is in progress.
        unsafe { (*self.data.get()).copy_from_slice(buf) };
        self.seq.store(seq + 2, Ordering::Release);
    }

    pub fn read(&self, out: &mut [u8; 64]) -> bool {
        let s1 = self.seq.load(Ordering::Acquire);
        if s1 & 1 != 0 {
            return false;
        }
        // SAFETY: read into a local; validity is confirmed by the seq recheck.
        unsafe { *out = *self.data.get() };
        fence(Ordering::Acquire);
        let s2 = self.seq.load(Ordering::Relaxed);
        s1 == s2
    }
}

impl Default for Seqlock {
    fn default() -> Self {
        Self::new()
    }
}
