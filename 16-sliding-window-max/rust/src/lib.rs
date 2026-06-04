use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub k: usize,
    pub arr: Vec<i32>,
}

pub fn solve(k: usize, arr: &[i32]) -> Vec<i32> {
    // TODO: return the maximum of each window of k readings, left to right
    let _ = k;
    let _ = arr;
    todo!()
}
