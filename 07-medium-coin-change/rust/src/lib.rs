use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub amount: u32,
    pub coins: Vec<u32>,
}

pub fn solve(amount: u32, coins: &[u32]) -> i64 {
    let _ = amount;
    let _ = coins;
    todo!()
}
