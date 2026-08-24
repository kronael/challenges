use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub links: Vec<[usize; 2]>,
}

pub fn solve(n: usize, links: &[[usize; 2]]) -> Vec<usize> {
    let _ = (n, links);
    todo!()
}
