use std::sync::atomic::{AtomicPtr, AtomicUsize, Ordering::*};

pub struct Stack<T: Send> {
    head: AtomicPtr<Node<T>>,
    // TODO: hazard pointer slots, retired lists
}

struct Node<T> {
    val: T,
    next: *mut Node<T>,
}

impl<T: Send> Stack<T> {
    pub fn new() -> Self {
        Stack {
            head: AtomicPtr::new(std::ptr::null_mut()),
        }
    }

    pub fn push(&self, val: T) {
        // TODO
        todo!()
    }

    pub fn pop(&self) -> Option<T> {
        // TODO: guess-publish-verify loop, then safe reclamation
        // 1. load head (guess)
        // 2. publish to hazard slot
        // 3. fence(SeqCst), re-load head (verify still same)
        // 4. CAS; on success, retire the old node through hazard reclamation
        todo!()
    }
}

impl<T: Send> Default for Stack<T> {
    fn default() -> Self {
        Self::new()
    }
}
