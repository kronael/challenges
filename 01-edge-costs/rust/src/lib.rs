use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub edges: Vec<[usize; 2]>,
    pub loads: Vec<Option<i64>>,
}

pub fn solve(n: usize, edges: &[[usize; 2]], loads: &[Option<i64>]) -> Vec<i64> {
    let _ = (n, edges, loads);
    todo!()
}
