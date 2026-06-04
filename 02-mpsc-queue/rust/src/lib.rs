use std::ptr;
use std::sync::atomic::{AtomicPtr, Ordering};

pub enum PopResult<T> {
    Item(T),
    Empty,
    Retry,
}

pub trait MpscQueue<T: Send>: Send + Sync {
    fn push(&self, value: T);
    fn try_pop(&self) -> PopResult<T>;
}

// TODO: implement VyukovQueue using an intrusive linked list.
// The stub compiles but panics at runtime — replace the bodies of push/try_pop.
//
// Reference:
//   https://www.1024cores.net/home/lock-free-algorithms/queues/non-intrusive-mpsc-node-based-queue
//
// Rules:
//   - No Mutex, Condvar, or OS blocking on the hot path.
//   - push() may be called from any thread simultaneously.
//   - try_pop() is called from exactly one thread.
//   - Return PopResult::Retry when a producer is mid-enqueue (stub node visible
//     but next pointer not yet written).

struct Node<T> {
    next: AtomicPtr<Node<T>>,
    val: Option<T>,
}

pub struct VyukovQueue<T> {
    head: AtomicPtr<Node<T>>,
    tail: AtomicPtr<Node<T>>,
}

impl<T: Send> VyukovQueue<T> {
    pub fn new() -> Self {
        // Allocate a sentinel/stub node.
        let stub = Box::into_raw(Box::new(Node::<T> {
            next: AtomicPtr::new(ptr::null_mut()),
            val: None,
        }));
        VyukovQueue {
            head: AtomicPtr::new(stub),
            tail: AtomicPtr::new(stub),
        }
    }
}

impl<T: Send> Default for VyukovQueue<T> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T: Send> MpscQueue<T> for VyukovQueue<T> {
    fn push(&self, value: T) {
        // TODO: implement Vyukov MPSC push (wait-free: one exchange + one store)
        let _ = value;
        let _ = ptr::null_mut::<Node<T>>();
        todo!("implement Vyukov MPSC push")
    }

    fn try_pop(&self) -> PopResult<T> {
        // TODO: implement Vyukov MPSC try_pop; return Retry when mid-enqueue
        todo!("implement Vyukov MPSC try_pop")
    }
}

impl<T> Drop for VyukovQueue<T> {
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
