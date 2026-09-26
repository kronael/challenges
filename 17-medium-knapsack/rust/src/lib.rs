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

/// `#[no_mangle]` keeps this symbol named `solve` in the binary, so that
/// `make vec` can find where each call to it starts and returns.
#[no_mangle]
pub fn solve(capacity: i64, items: &[Item]) -> i64 {
    let _ = capacity;
    let _ = items;
    todo!()
}
