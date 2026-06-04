use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub k: usize,
    pub kmers: Vec<String>,
}

pub fn solve(k: usize, kmers: &[String]) -> String {
    // TODO: reconstruct and return the original DNA string from the k-mers
    let _ = k;
    let _ = kmers;
    todo!()
}
