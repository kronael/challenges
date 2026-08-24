use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub root: usize,
    pub pnl: Vec<i64>,
    pub left: Vec<i32>,
    pub right: Vec<i32>,
}

pub fn solve(n: usize, root: usize, pnl: &[i64], left: &[i32], right: &[i32]) -> i64 {
    let _ = (n, root, pnl, left, right);
    todo!()
}
