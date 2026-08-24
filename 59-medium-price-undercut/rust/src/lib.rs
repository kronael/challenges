use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub prices: Vec<i32>,
}

pub fn solve(n: usize, prices: &[i32]) -> Vec<i32> {
    let _ = (n, prices);
    todo!()
}
