use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub k: usize,
    pub arr: Vec<i32>,
}

/// `#[no_mangle]` keeps this symbol named `solve` in the binary, so that
/// `make vec` can find where each call to it starts and returns.
#[no_mangle]
pub fn solve(k: usize, arr: &[i32]) -> Vec<i32> {
    let _ = k;
    let _ = arr;
    todo!()
}
