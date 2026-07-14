use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub base: u64,
    pub exp: u64,
    #[serde(rename = "mod")]
    pub modulus: u64,
}

pub fn solve(base: u64, exp: u64, m: u64) -> u64 {
    let _ = (base, exp, m);
    todo!()
}
