use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub text: String,
    pub pattern: String,
}

pub fn solve(text: &str, pattern: &str) -> Vec<usize> {
    let _ = text;
    let _ = pattern;
    todo!()
}
