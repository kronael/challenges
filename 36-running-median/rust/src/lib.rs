use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub stream: Vec<i64>,
}

pub fn solve(stream: &[i64]) -> Vec<String> {
    // TODO: return the median after each insertion
    // Format: integer if count is odd, one-decimal float if even (e.g. "5" or "4.5")
    let _ = stream;
    todo!()
}
