use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub sequence: String,
    pub start: Vec<i64>,
    pub transition: Vec<Vec<i64>>,
    pub emission: Vec<Vec<i64>>,
}

pub fn solve(
    sequence: &str,
    start: &[i64],
    transition: &[Vec<i64>],
    emission: &[Vec<i64>],
) -> Vec<usize> {
    let _ = (sequence, start, transition, emission);
    todo!()
}
