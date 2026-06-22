use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub arr: Vec<i32>,
}

pub fn solve(arr: &[i32]) -> i64 {
    let _ = arr;
    todo!()
}
