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
    // TODO: merge the K sorted feeds by ts (tie-break feed index, then id);
    // return a flat vec [ts, id, ts, id, ...] in merged order
    let _ = feeds;
    todo!()
}
