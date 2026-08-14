use serde::Deserialize;

#[derive(Deserialize)]
pub struct Operation {
    #[serde(rename = "type")]
    pub kind: String,
    pub u: usize,
    pub v: usize,
}

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub operations: Vec<Operation>,
}

pub fn solve(n: usize, operations: &[Operation]) -> Vec<i64> {
    let _ = (n, operations);
    todo!()
}
