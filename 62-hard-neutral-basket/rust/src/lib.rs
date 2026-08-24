use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub target: i64,
    pub exposures: Vec<i64>,
}

pub fn solve(n: usize, target: i64, exposures: &[i64]) -> i64 {
    let _ = (n, target, exposures);
    todo!()
}
