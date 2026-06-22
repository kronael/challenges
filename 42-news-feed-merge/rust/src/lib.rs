use serde::Deserialize;

#[derive(Deserialize)]
pub struct Event {
    pub ts: i64,
    pub id: i64,
}

#[derive(Deserialize)]
pub struct Input {
    pub feeds: Vec<Vec<Event>>,
}

pub fn solve(feeds: &[Vec<Event>]) -> Vec<i64> {
    let _ = feeds;
    todo!()
}
