use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub seq: Vec<i32>,
}

pub fn solve(seq: &[i32]) -> usize {
    // TODO: return the length of the longest strictly increasing subsequence
    let _ = seq;
    todo!()
}
