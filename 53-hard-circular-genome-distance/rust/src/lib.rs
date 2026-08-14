use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub a: Vec<Vec<i64>>,
    pub b: Vec<Vec<i64>>,
}

pub fn solve(a: &[Vec<i64>], b: &[Vec<i64>]) -> i64 {
    let _ = (a, b);
    todo!()
}
