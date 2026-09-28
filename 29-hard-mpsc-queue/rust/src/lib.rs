use std::ptr;
use std::sync::atomic::{AtomicPtr, Ordering};

pub enum PopResult<T> {
    Item(T),
    Empty,
    Retry,
}

pub trait Queue<T: Send>: Send + Sync {
    fn push(&self, value: T);
    fn try_pop(&self) -> PopResult<T>;
}

// The stub compiles but panics at runtime — replace the bodies of push/try_pop.
//
// Rules:
//   - No Mutex, Condvar, or OS blocking on the hot path.
//   - push() may be called from any thread simultaneously.
//   - try_pop() is called from exactly one thread.
//   - Return PopResult::Retry when a producer is mid-enqueue.

struct Node<T> {
    next: AtomicPtr<Node<T>>,
    val: Option<T>,
}

pub struct MpscQueue<T> {
    head: AtomicPtr<Node<T>>,
    tail: AtomicPtr<Node<T>>,
}

impl<T: Send> MpscQueue<T> {
    pub fn new() -> Self {
        // Allocate a sentinel/stub node.
        let stub = Box::into_raw(Box::new(Node::<T> {
            next: AtomicPtr::new(ptr::null_mut()),
            val: None,
        }));
        MpscQueue {
            head: AtomicPtr::new(stub),
            tail: AtomicPtr::new(stub),
        }
    }
}

impl<T: Send> Default for MpscQueue<T> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T: Send> Queue<T> for MpscQueue<T> {
    fn push(&self, value: T) {
        let _ = value;
        let _ = ptr::null_mut::<Node<T>>();
        todo!("implement MPSC push")
    }

    fn try_pop(&self) -> PopResult<T> {
        todo!("implement MPSC try_pop")
    }
}

impl<T> Drop for MpscQueue<T> {
    fn drop(&mut self) {
        // Drain remaining nodes to avoid leaks.
        let mut cur = *self.head.get_mut();
        while !cur.is_null() {
            // SAFETY: all nodes were allocated via Box::into_raw in push() or new().
            // head is the only live pointer after the queue is dropped.
            let node = unsafe { Box::from_raw(cur) };
            cur = node.next.load(Ordering::Relaxed);
        }
    }
}
