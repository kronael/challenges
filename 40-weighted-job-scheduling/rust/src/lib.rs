use serde::Deserialize;

#[derive(Deserialize)]
pub struct Job {
    pub start: i64,
    pub end: i64,
    pub weight: i64,
}

#[derive(Deserialize)]
pub struct Input {
    pub jobs: Vec<Job>,
}

pub fn solve(jobs: &[Job]) -> i64 {
    // TODO: return maximum total weight of non-overlapping jobs
    let _ = jobs;
    todo!()
}
