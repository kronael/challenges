use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub words: Vec<String>,
    pub queries: Vec<String>,
}

pub fn solve(words: &[String], queries: &[String]) -> String {
    // Join query results with ";", and words inside one result with " ".
    let _ = (words, queries);
    todo!()
}
