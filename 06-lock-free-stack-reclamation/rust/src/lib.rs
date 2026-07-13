use std::sync::atomic::AtomicPtr;

pub struct Stack<T: Send> {
    #[allow(dead_code)]
    head: AtomicPtr<Node<T>>,
}

#[allow(dead_code)]
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

    pub fn push(&self, _val: T) {
        todo!()
    }

    pub fn pop(&self) -> Option<T> {
        todo!()
    }
}

impl<T: Send> Default for Stack<T> {
    fn default() -> Self {
        Self::new()
    }
}
