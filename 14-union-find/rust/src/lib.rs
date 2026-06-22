use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub unions: Vec<[usize; 2]>,
    pub queries: Vec<[usize; 2]>,
}

pub fn solve(n: usize, unions: &[[usize; 2]], queries: &[[usize; 2]]) -> Vec<u8> {
    let _ = (n, unions, queries);
    todo!()
}
