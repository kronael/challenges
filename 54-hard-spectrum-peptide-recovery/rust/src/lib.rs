use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub masses: Vec<i64>,
    pub spectrum: Vec<i64>,
}

pub fn solve(masses: &[i64], spectrum: &[i64]) -> Option<Vec<i64>> {
    let _ = (masses, spectrum);
    todo!()
}
