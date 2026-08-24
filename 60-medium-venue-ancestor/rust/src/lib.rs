use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub parent: Vec<i32>,
    pub queries: Vec<[usize; 2]>,
}

pub fn solve(n: usize, parent: &[i32], queries: &[[usize; 2]]) -> Vec<usize> {
    let _ = (n, parent, queries);
    todo!()
}
