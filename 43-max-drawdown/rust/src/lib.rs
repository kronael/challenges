use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub prices: Vec<i32>,
}

pub fn solve(prices: &[i32]) -> i64 {
    // TODO: return the maximum drawdown, max over i<j of (prices[i] - prices[j])
    let _ = prices;
    todo!()
}
