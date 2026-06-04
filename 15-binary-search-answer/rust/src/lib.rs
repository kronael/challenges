use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub k: usize,
    pub pages: Vec<i64>,
}

pub fn solve(k: usize, pages: &[i64]) -> i64 {
    // TODO: return the minimum possible value of the largest contiguous block sum
    let _ = k;
    let _ = pages;
    todo!()
}
