use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub d: usize,
    pub len: usize,
    pub genome: String,
    pub guides: Vec<String>,
}

pub fn solve(d: usize, len: usize, genome: &str, guides: &[String]) -> Vec<u64> {
    let _ = (d, len, genome, guides);
    todo!()
}
