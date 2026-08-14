use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub data: Vec<i64>,
}

pub fn solve(n: usize, data: &[i64]) -> Vec<i64> {
    let _ = (n, data);
    todo!()
}
