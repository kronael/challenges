use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub initial: Vec<i64>,
    pub queries: Vec<Vec<serde_json::Value>>,
}

pub fn solve(n: usize, initial: &[i64], queries: &[Vec<serde_json::Value>]) -> Vec<i64> {
    // TODO: Fenwick tree — handle ["sum", i] and ["update", i, delta] queries
    // Return results of "sum" queries (1-indexed) in order
    let _ = (n, initial, queries);
    todo!()
}
