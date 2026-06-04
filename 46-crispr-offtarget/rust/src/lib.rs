use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub d: usize,
    pub len: usize,
    pub genome: String,
    pub guides: Vec<String>,
}

pub fn solve(d: usize, len: usize, genome: &str, guides: &[String]) -> Vec<u64> {
    // TODO: for each guide, count the length-`len` windows of `genome` within
    // Hamming distance `d` of it. Return one count per guide, in input order.
    let _ = (d, len, genome, guides);
    todo!()
}
