use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub text: String,
    pub pattern: String,
}

pub fn solve(text: &str, pattern: &str) -> Vec<usize> {
    // TODO: return the 1-indexed start positions where pattern occurs in text
    let _ = text;
    let _ = pattern;
    todo!()
}
