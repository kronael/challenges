use serde::Deserialize;

#[derive(Deserialize)]
pub struct Event {
    pub id: i64,
    pub process: usize,
    pub clock: Vec<usize>,
}

#[derive(Deserialize)]
pub struct Input {
    pub processes: usize,
    pub events: Vec<Event>,
}

pub fn solve(processes: usize, events: &[Event]) -> Vec<i64> {
    let _ = (processes, events);
    todo!()
}
