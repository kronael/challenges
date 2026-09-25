use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub pnl: Vec<i64>,
    pub requires: Vec<[usize; 2]>,
}

pub fn solve(n: usize, pnl: &[i64], requires: &[[usize; 2]]) -> i64 {
    let _ = (n, pnl, requires);
    todo!()
}
