use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub quantities: Vec<i64>,
}

pub fn solve(n: usize, quantities: &[i64]) -> i64 {
    let _ = (n, quantities);
    todo!()
}
