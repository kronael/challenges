use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub amount: u32,
    pub coins: Vec<u32>,
}

pub fn solve(amount: u32, coins: &[u32]) -> i64 {
    // TODO: return the minimum number of coins summing to amount, or -1 if impossible
    let _ = amount;
    let _ = coins;
    todo!()
}
