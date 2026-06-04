use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub reads: Vec<String>,
}

pub fn solve(reads: &[String]) -> String {
    // TODO: return the shortest superstring containing every read (the reassembled chromosome)
    let _ = reads;
    todo!()
}
