use serde::Deserialize;

#[derive(Deserialize)]
pub struct Item {
    pub weight: i64,
    pub value: i64,
}

#[derive(Deserialize)]
pub struct Input {
    pub capacity: i64,
    pub items: Vec<Item>,
}

pub fn solve(capacity: i64, items: &[Item]) -> i64 {
    // TODO: return the maximum achievable total value
    let _ = capacity;
    let _ = items;
    todo!()
}
