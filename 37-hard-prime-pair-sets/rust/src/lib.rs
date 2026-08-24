use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    #[serde(default = "default_size")]
    pub size: u64,
    #[serde(default = "default_limit")]
    pub limit: u64,
}

fn default_size() -> u64 {
    5
}

fn default_limit() -> u64 {
    10_000
}

pub fn solve(_size: u64, _limit: u64) -> i64 {
    todo!()
}
