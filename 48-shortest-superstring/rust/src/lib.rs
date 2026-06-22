use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub reads: Vec<String>,
}

pub fn solve(reads: &[String]) -> String {
    let _ = reads;
    todo!()
}
