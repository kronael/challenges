use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub arr: Vec<i32>,
}

pub fn solve(arr: &[i32]) -> i64 {
    // TODO: return the number of inversions (pairs i < j with arr[i] > arr[j])
    let _ = arr;
    todo!()
}
