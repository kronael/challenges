use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub prices: Vec<i32>,
}

pub fn solve(prices: &[i32]) -> i64 {
    let _ = prices;
    todo!()
}
