use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub parent: Vec<isize>,
    pub sequences: Vec<Option<String>>,
    pub prior: Vec<f64>,
    pub transition: Vec<Vec<f64>>,
}

pub fn solve(
    parent: &[isize],
    sequences: &[Option<String>],
    prior: &[f64],
    transition: &[Vec<f64>],
) -> f64 {
    let _ = (parent, sequences, prior, transition);
    todo!()
}
