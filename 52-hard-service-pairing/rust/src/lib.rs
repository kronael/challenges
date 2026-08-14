use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub costs: Vec<Vec<i64>>,
}

pub fn solve(costs: &[Vec<i64>]) -> i64 {
    let _ = costs;
    todo!()
}
