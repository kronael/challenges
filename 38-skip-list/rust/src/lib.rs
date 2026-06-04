use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub ops: Vec<Vec<serde_json::Value>>,
}

pub fn solve(ops: &[Vec<serde_json::Value>]) -> Vec<i64> {
    // TODO: skip list supporting insert/delete/search/range_count
    // Return results of "search" (1/0) and "range_count" ops in order
    let _ = ops;
    todo!()
}
