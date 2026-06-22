use serde::Deserialize;

#[derive(Deserialize)]
pub struct Op(pub String, pub i64, pub i64);

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub values: Vec<i64>,
    pub ops: Vec<Op>,
}

pub fn solve(n: usize, values: &[i64], ops: &[Op]) -> Vec<i64> {
    let _ = (n, values, ops);
    todo!()
}
