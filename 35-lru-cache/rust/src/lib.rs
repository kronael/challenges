use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub capacity: usize,
    pub ops: Vec<Vec<serde_json::Value>>,
}

pub fn solve(capacity: usize, ops: &[Vec<serde_json::Value>]) -> Vec<i64> {
    // TODO: implement LRU cache; return results of "get" ops (-1 if miss)
    // each op is ["get", k] or ["put", k, v]
    let _ = (capacity, ops);
    todo!()
}
