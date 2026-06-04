use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub edges: Vec<Vec<i64>>,
}

pub fn solve(n: usize, edges: &[Vec<i64>]) -> Vec<i64> {
    // TODO: return the shortest distance from node 0 to each node, -1 if unreachable
    let _ = n;
    let _ = edges;
    todo!()
}
