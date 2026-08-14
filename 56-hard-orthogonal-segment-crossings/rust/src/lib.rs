use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub horizontal: Vec<[i64; 3]>,
    pub vertical: Vec<[i64; 3]>,
}

pub fn solve(horizontal: &[[i64; 3]], vertical: &[[i64; 3]]) -> i64 {
    let _ = (horizontal, vertical);
    todo!()
}
