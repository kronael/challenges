use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub intervals: Vec<[i32; 2]>,
}

pub fn solve(intervals: &[[i32; 2]]) -> usize {
    // TODO: return the maximum number of non-overlapping intervals
    let _ = intervals;
    todo!()
}
