use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub scores: Vec<i32>,
    pub threshold: i32,
}

/// Returns the scores strictly above `threshold`, in batch order.
///
/// `#[no_mangle]` keeps this symbol named `solve` in the object file, so that
/// `make vec` can find its loops in the emitted assembly.
#[no_mangle]
pub fn solve(scores: &[i32], threshold: i32) -> Vec<i32> {
    let _ = (scores, threshold);
    todo!()
}
