use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub parts: Vec<String>,
    pub queries: Vec<[i64; 2]>,
}

pub fn solve(parts: &[String], queries: &[[i64; 2]]) -> String {
    let _ = (parts, queries);
    todo!()
}
