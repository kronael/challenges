use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub k: usize,
    pub kmers: Vec<String>,
}

pub fn solve(k: usize, kmers: &[String]) -> String {
    let _ = k;
    let _ = kmers;
    todo!()
}
