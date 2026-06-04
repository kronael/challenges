use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub rna: String,
    pub min_loop: usize,
    pub allow_wobble: bool,
}

pub fn solve(rna: &str, min_loop: usize, allow_wobble: bool) -> usize {
    // TODO: return the maximum number of non-crossing base pairs
    let _ = (rna, min_loop, allow_wobble);
    todo!()
}
