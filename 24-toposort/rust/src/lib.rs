use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub edges: Vec<[usize; 2]>,
}

pub fn solve(n: usize, edges: &[[usize; 2]]) -> Option<Vec<usize>> {
    let _ = (n, edges);
    todo!()
}
