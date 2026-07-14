use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub dims: Vec<i64>,
}

pub fn solve(dims: &[i64]) -> i64 {
    let _ = dims;
    todo!()
}
