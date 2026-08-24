use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub slippage: Vec<i32>,
    pub ks: Vec<usize>,
}

pub fn solve(n: usize, slippage: &[i32], ks: &[usize]) -> Vec<i32> {
    let _ = (n, slippage, ks);
    todo!()
}
