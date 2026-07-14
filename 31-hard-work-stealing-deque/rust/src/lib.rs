use std::cell::UnsafeCell;
use std::mem::MaybeUninit;
use std::sync::atomic::{AtomicIsize, AtomicPtr, Ordering};

pub enum Steal<T> {
    Empty,
    Success(T),
    Retry,
}

// The stub compiles but panics at runtime — replace the bodies of push/pop/steal.
//
// Reference: "Dynamic Circular Work-Stealing Deque" — Chase & Lev, SPAA 2005.
//
// Rules:
//   - push() and pop() are called only from the owner thread.
//   - steal() may be called from any number of thief threads simultaneously.
//   - The backing buffer is fixed-size, power-of-two storage; tests stay within
//     the default capacity.
//   - No Mutex or OS primitive on the hot path.

const DEFAULT_CAPACITY: usize = 1 << 22;

struct Buffer<T> {
    cap: usize,
    data: Vec<UnsafeCell<MaybeUninit<T>>>,
}

#[allow(dead_code)]
impl<T> Buffer<T> {
    fn new(cap: usize) -> *mut Self {
        assert!(cap.is_power_of_two());
        let data = (0..cap)
            .map(|_| UnsafeCell::new(MaybeUninit::uninit()))
            .collect();
        Box::into_raw(Box::new(Buffer { cap, data }))
    }

    unsafe fn read(&self, index: isize) -> T {
        // SAFETY: caller ensures index is within bounds and no writer races.
        let slot = (index as usize) & (self.cap - 1);
        unsafe { (*self.data[slot].get()).assume_init_read() }
    }

    unsafe fn write(&self, index: isize, value: T) {
        // SAFETY: caller ensures index is within bounds and only owner writes.
        let slot = (index as usize) & (self.cap - 1);
        unsafe { self.data[slot].get().write(MaybeUninit::new(value)) };
    }
}

pub struct Deque<T: Send> {
    bottom: AtomicIsize,
    top: AtomicIsize,
    buffer: AtomicPtr<Buffer<T>>,
}

// SAFETY: Deque is designed for concurrent owner+thief access; the Chase-Lev
// protocol ensures safe sharing when push/pop are restricted to one thread.
unsafe impl<T: Send> Send for Deque<T> {}
unsafe impl<T: Send> Sync for Deque<T> {}

impl<T: Send> Deque<T> {
    pub fn new() -> Self {
        Deque {
            bottom: AtomicIsize::new(0),
            top: AtomicIsize::new(0),
            buffer: AtomicPtr::new(Buffer::new(DEFAULT_CAPACITY)),
        }
    }

    /// Push a value onto the bottom. Owner thread only.
    pub fn push(&self, _value: T) {
        todo!("implement Chase-Lev push")
    }

    /// Pop a value from the bottom. Owner thread only.
    pub fn pop(&self) -> Option<T> {
        todo!("implement Chase-Lev pop")
    }

    /// Steal a value from the top. Any thread.
    pub fn steal(&self) -> Steal<T> {
        todo!("implement Chase-Lev steal")
    }
}

impl<T: Send> Default for Deque<T> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T: Send> Drop for Deque<T> {
    fn drop(&mut self) {
        let ptr = self.buffer.load(Ordering::Relaxed);
        if !ptr.is_null() {
            let top = self.top.load(Ordering::Relaxed);
            let bottom = self.bottom.load(Ordering::Relaxed);

            // SAFETY: &mut self guarantees no concurrent access during drop.
            // Live items occupy the half-open range [top, bottom).
            unsafe {
                let buffer = &mut *ptr;
                for index in top..bottom {
                    let slot = (index as usize) & (buffer.cap - 1);
                    (&mut *buffer.data[slot].get()).assume_init_drop();
                }

                // ptr was allocated via Box::into_raw in Buffer::new.
                drop(Box::from_raw(ptr));
            }
        }
    }
}
