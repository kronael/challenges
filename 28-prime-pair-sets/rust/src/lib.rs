use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    #[serde(default = "default_size")]
    pub size: u64,
}

fn default_size() -> u64 {
    5
}

impl Input {
    pub fn size(&self) -> u64 {
        self.size
    }
}

pub fn solve(_size: u64) -> u64 {
    todo!()
}
