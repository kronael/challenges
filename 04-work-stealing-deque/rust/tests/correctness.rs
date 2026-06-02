use std::sync::atomic::AtomicBool;
use std::sync::atomic::Ordering;
use std::sync::Arc;
use std::sync::Barrier;
use std::sync::Mutex;
use std::thread;
use work_stealing_deque::Deque;
use work_stealing_deque::Steal;

const TASKS: u64 = 500_000;
const THIEVES: usize = 7;

#[test]
fn stress_work_stealing() {
    let deque = Arc::new(Deque::<u64>::new());
    let stop = Arc::new(AtomicBool::new(false));
    let barrier = Arc::new(Barrier::new(THIEVES + 1));
    // Each thief records the exact values it stole so the final multiset check
    // can detect duplication (two consumers claiming the same single element).
    let stolen: Arc<Mutex<Vec<u64>>> = Arc::new(Mutex::new(Vec::new()));

    let thieves: Vec<_> = (0..THIEVES)
        .map(|_| {
            let deque = Arc::clone(&deque);
            let stop = Arc::clone(&stop);
            let stolen = Arc::clone(&stolen);
            let barrier = Arc::clone(&barrier);
            thread::spawn(move || {
                let mut local = Vec::new();
                barrier.wait();
                loop {
                    match deque.steal() {
                        Steal::Success(value) => local.push(value),
                        Steal::Retry => std::hint::spin_loop(),
                        Steal::Empty => {
                            if stop.load(Ordering::Acquire) {
                                break;
                            }
                            std::hint::spin_loop();
                        }
                    }
                }
                stolen.lock().unwrap().extend(local);
            })
        })
        .collect();

    // Owner: interleave pushes with its own pops so the bottom hovers near the
    // top, maximising the single-element pop-vs-steal race the CAS must resolve.
    let mut owner_popped = Vec::new();
    barrier.wait();
    for task in 1..=TASKS {
        deque.push(task);
        if task % 3 == 0 {
            if let Some(value) = deque.pop() {
                owner_popped.push(value);
            }
        }
    }
    while let Some(value) = deque.pop() {
        owner_popped.push(value);
    }

    stop.store(true, Ordering::Release);
    for thief in thieves {
        thief.join().unwrap();
    }

    // Merge everything the owner and thieves consumed; it must equal 1..=TASKS
    // exactly once each. A repeat means two threads claimed the same element
    // (last-element race lost); a gap means an element was dropped.
    let mut all = owner_popped;
    all.extend(stolen.lock().unwrap().iter().copied());

    assert_eq!(
        all.len(),
        TASKS as usize,
        "consumed {} items, expected {TASKS} — duplication or loss",
        all.len()
    );

    let mut seen = vec![false; TASKS as usize + 1];
    for value in all {
        assert!(value >= 1 && value <= TASKS, "value {value} out of range — corrupt read");
        assert!(!seen[value as usize], "value {value} consumed twice — last-element race lost");
        seen[value as usize] = true;
    }
    // len == TASKS and all distinct in 1..=TASKS implies full coverage; assert
    // the first/last to make a gap failure legible if the invariants ever drift.
    assert!(seen[1] && seen[TASKS as usize], "boundary task missing — loss");
}
