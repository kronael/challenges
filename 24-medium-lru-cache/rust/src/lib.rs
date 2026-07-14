use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub capacity: usize,
    pub ops: Vec<Vec<serde_json::Value>>,
}

pub fn solve(capacity: usize, ops: &[Vec<serde_json::Value>]) -> Vec<i64> {
    let _ = (capacity, ops);
    todo!()
}
