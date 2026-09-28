use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub edges: Vec<Vec<i64>>,
}

pub fn solve(n: usize, edges: &[Vec<i64>]) -> i64 {
    let _ = n;
    let _ = edges;
    todo!()
}
